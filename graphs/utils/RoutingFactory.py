from typing import Any, Dict, List
from graphs.models import Vehicle, Route
from graphs.shemas.routingDTO import RouteDB, RouteDTO
from graphs.apis.geopy import Request_geopy
from graphs.apis.osrm import Request_osrm  # Adjust import path if needed
from graphs.utils.battery_consumption import BatteryConsumptionFactory
from graphs.utils.util import Coordinate
from graphs.utils.vehicle import ClassVehicle
from graphs.apis.open_charge_map import find_charging_stations

INTERVAL_SIZE_KM = 100


class RoutingFactory:

    from_history = False

    def __init__(self, params):

        self.start_city = params.get("start_city")
        self.end_city = params.get("end_city")

        vehicle_id = int(params.get("vehicle_id"))
        self.vehicle = Vehicle.objects.get(id=vehicle_id)

        current_battery = params.get("battery_capacity", None)
        if not current_battery:
            self.from_history = True
        else:
            current_battery = float(current_battery)

        self.vehicle_class = ClassVehicle(self.vehicle, current_battery)
        self.min_battery_capacity = self.vehicle_class.get_min_battery_capacity()

        # Get coordinates from city names
        geolocator = Request_geopy()
        self.start_location = geolocator.geocode(self.start_city)
        self.end_location = geolocator.geocode(self.end_city)

        if not self.start_location or not self.end_location:
            raise ValueError("Invalid city name")
        
        # Expansion
        self.additional_charging_stations = params.get("additional_charging_stations", [])

    def start_route(self):

        self.accumulated_routes: List[RouteDTO] = []
        self.accumulated_charging_stops = []
        self.accumulated_empty_battery = []

        self.new_route(self.start_location, self.end_location)

        total_distance = int(sum([route.estimated_distance for route in self.accumulated_routes]))
        total_time = int(sum([route.estimated_time for route in self.accumulated_routes]))
        total_consumption = int(sum([route.estimated_consumption for route in self.accumulated_routes]))

        # history
        route = RouteDB(
            self.vehicle,
            self.start_city,
            self.end_city,
            total_distance,
            total_consumption,
            total_time,
        )

        # save to database
        if not self.from_history:
            route.save_to_db()

            # delete old to never exceed 10 routes
            if Route.objects.count() > 10:
                Route.objects.order_by("id").first().delete()  # Lowest ID = oldest

        response = {
            "accumulated_routes": [route.to_dict() for route in self.accumulated_routes],
            "accumulated_charging_stops": self.accumulated_charging_stops,
            "accumulated_empty_battery": self.accumulated_empty_battery,
            "total_distance": total_distance,
            "total_time": total_time,
            "total_consumption": total_consumption,
        }

        return response

    def new_route(self, start_location=None, end_location=None):

        osrm_response = get_OSRM(start_location, end_location, include_steps=True)

        # parse steps
        route = osrm_response.get("routes", [])[0]
        legs = route.get("legs", [])
        steps = [step for leg in legs for step in leg.get("steps", [])]

        # get battery factory
        battery_factory = BatteryConsumptionFactory(self.vehicle)

        ############################
        ############################
        ############################
        # Simulation

        total_consumption = 0.0

        def calculate_consumption(step_distance, speed_factor):
            return self.vehicle.consumption_rate * step_distance * speed_factor

        def process_step(step):
            nonlocal interval_distance, interval_consumption
            # Calculate consumption for this step with speed effect
            speed_factor = battery_factory.calculate_speed_effect(step)
            step_consumption = calculate_consumption(step_distance, speed_factor)

            interval_distance += step_distance
            interval_consumption += step_consumption

        def remaining_battery() -> float:
            nonlocal interval_consumption, total_consumption
            return self.vehicle_class.current_battery - self.min_battery_capacity - (total_consumption + interval_consumption)

        def account_interval_consumption(start_coord, end_coord) -> None:
            nonlocal interval_consumption, total_consumption, interval_distance, interval_start_coord

            if interval_consumption == 0:
                return

            temp_effect = battery_factory.calculate_temperature_effect(start_coord, end_coord)
            elev_effect = battery_factory.calculate_elevation_effect(start_coord, end_coord)

            interval_consumption *= temp_effect * elev_effect
            total_consumption += interval_consumption

            # reset interval
            interval_distance = 0.0
            interval_consumption = 0.0
            interval_start_coord = end_coord

        interval_distance = 0.0
        interval_consumption = 0.0
        interval_start_coord = start_location

        for index, step in enumerate(steps):

            step_distance = step.get("distance", 0) / 1000  # km

            if step_distance == 0:
                continue

            step_start_coord = get_coord(step)
            step_end_coord = get_coord(steps[index + 1])

            # consumption was fine till this step so we put start as charging station
            charging_coord = step_start_coord

            estimated_distance = interval_distance + step_distance

            # Case 2: just right
            if (
                estimated_distance > INTERVAL_SIZE_KM * 0.9
                and estimated_distance < INTERVAL_SIZE_KM * 1.1
            ):  # margin
                process_step(step)
                account_interval_consumption(interval_start_coord, step_end_coord)
            # Case 3: too big
            elif estimated_distance > INTERVAL_SIZE_KM:

                # estemate the batery drain
                speed_factor = battery_factory.calculate_speed_effect(step)

                # condition is redundant yet appropriate
                while step_distance > 0:

                    charge_the_batery = False

                    # Calculate how much distance we can add to reach interval_km
                    available_distance = INTERVAL_SIZE_KM - interval_distance

                    if step_distance > available_distance:

                        # get total
                        step_consumption = calculate_consumption(step_distance, speed_factor)
                        split_percentage = available_distance / INTERVAL_SIZE_KM
                        proposed_consumption = step_consumption * split_percentage

                        # Calculate battery left to decide if we need to split early
                        if remaining_battery() < proposed_consumption:
                            split_percentage = remaining_battery() / proposed_consumption
                            charge_the_batery = True

                        # Interpolate coordinate between step_start_coord and next_step_start_coord
                        split_coord = {
                            "longitude": step_start_coord["longitude"]
                            + (step_end_coord["longitude"] - step_start_coord["longitude"]) * split_percentage,
                            "latitude": step_start_coord["latitude"]
                            + (step_end_coord["latitude"] - step_start_coord["latitude"]) * split_percentage,
                        }

                        # calc actual taken values
                        parsed_distance = split_percentage * step_distance
                        parsed_consumption = split_percentage * step_consumption

                        interval_distance += parsed_distance
                        interval_consumption += parsed_consumption

                        step_distance -= parsed_distance

                        account_interval_consumption(interval_start_coord, split_coord)

                        if charge_the_batery:
                            # battery was depleted arround this point and we have some minimum spare to get there
                            charging_coord = split_coord
                            break
                    # the remainig part of step. Last iteration
                    else:
                        step_consumption = calculate_consumption(step_distance, speed_factor)

                        interval_distance += step_distance
                        interval_consumption += step_consumption

                        break
            # Case 1: just another step
            else:
                process_step(step)

            # check if any battery left
            if remaining_battery() <= 0:
                self.accumulated_empty_battery.append(Coordinate(charging_coord).to_string())
                
                chargings_stations = self.find_nearest_charging_stations(Coordinate(charging_coord))
                # here we add additioanl charging stations we might get trough infrastructure testing
                if self.additional_charging_stations:
                    chargings_stations.extend(self.additional_charging_stations)
                # start_location is a must since its the last point on the map from which we started
                charging_station, charging_station_response, charging_station_location = self.find_next_charging_station(
                    start_location, chargings_stations
                )
                
                account_interval_consumption(interval_start_coord, charging_station_location)
                
                self.accumulated_charging_stops.append(charging_station)

                routedto = RouteDTO(
                    charging_station_response,
                    self.vehicle,
                    start_location,
                    charging_station_location,
                    total_consumption,
                )

                self.accumulated_routes.append(routedto)

                # charge the battery (it's possible initial battery capacity is not full)
                self.vehicle_class.recharge_battery()

                # recursion
                self.new_route(charging_station_location, self.end_location)

                # since route finished early we end the cycle
                return

        ###############################
        ###############################
        ###############################

        account_interval_consumption(interval_start_coord, step_end_coord)

        routedto = RouteDTO(
            osrm_response,
            self.vehicle,
            start_location,
            end_location,
            total_consumption,
        )
        self.accumulated_routes.append(routedto)

    def find_nearest_charging_stations(self, location: Coordinate):

        result = []
        multiplier = 1

        while len(result) == 0:

            result = find_charging_stations(
                lat=location.latitude, lon=location.longitude, max_distance_km=10 * multiplier
            )
            multiplier * 2

        return result

    def find_next_charging_station(self, start_loc, chargings_stations):

        def distance(coord1, coord2):
            from math import radians, cos, sin, asin, sqrt

            lon1, lat1 = coord1.longitude, coord1.latitude
            lon2, lat2 = coord2.longitude, coord2.latitude

            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers
            return c * r

        # Filter charging stations to nearest 5 based on geographic distance to start_loc
        start_coord = Coordinate(start_loc)
        stations_with_distance = []

        for station in chargings_stations:
            location = getattr(station, "AddressInfo", None)
            if not location:
                location = station
            station_coord = Coordinate(location)
            dist = distance(start_coord, station_coord)
            stations_with_distance.append((dist, station))

        stations_with_distance.sort(key=lambda x: x[0])
        filtered_stations = [station for _, station in stations_with_distance[:5]]

        nearest_station = filtered_stations[0]
        nearest_station_location = nearest_station
        try:
            nearest_station_location = nearest_station.get("AddressInfo", None)
        except:
            nearest_station_location = nearest_station
        if not nearest_station_location:
            nearest_station_location = nearest_station
        best_response = get_OSRM(start_loc, nearest_station_location)
        best_time = best_response.get("routes")[0].get("duration")

        for station in filtered_stations:

            location = station
            try:
                location = station.get("AddressInfo", None)
            except:
                location = station
               
            response = get_OSRM(start_loc, location)
            time = response.get("routes")[0].get("duration")

            if time < best_time:
                nearest_station = station
                nearest_station_location = location
                best_response = response
                best_time = time

        return nearest_station, best_response, Coordinate(nearest_station_location)


def get_coord(step):
    location = step.get("maneuver", {}).get("location", None)
    return {"longitude": location[0], "latitude": location[1]} if location else None


def get_OSRM(start_location, end_location, include_steps=False, include_detail=True):

    parsed_start = Coordinate(start_location)
    parsed_end = Coordinate(end_location)

    start_lon = parsed_start.longitude
    start_lat = parsed_start.latitude
    end_lon = parsed_end.longitude
    end_lat = parsed_end.latitude

    # get route geometry
    osrm_params = f"/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
    query_params = []

    if include_steps:
        query_params.append("steps=true")
    if include_detail:
        query_params.append("overview=full")

    if query_params:
        osrm_params += "?" + "&".join(query_params)

    return Request_osrm(osrm_params)
