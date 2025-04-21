import datetime
from typing import Any, Dict, List
from graphs.models import Vehicle
from graphs.utils.weather import Request_weather
from graphs.utils.elevation import Request_elevation

min_milage = 15

class BatteryConsumptionFactory:
    def __init__(self, vehicle: Vehicle, osrm_response: Dict[str, Any], battery_capacity: float):
        self.vehicle = vehicle
        self.osrm_response = osrm_response
        self.battery_capacity = battery_capacity  # kWh

        # Incorporate battery aging: adjust battery capacity based on vehicle age and degradation
        self.adjusted_battery_capacity = self._adjust_battery_capacity_for_age()

        self.min_battery_capacity = self.get_min_battery_capacity(min_milage)

        # Current battery state in kWh, adjusted for aging
        self.battery_capacity = vehicle.current_battery / 100 * self.adjusted_battery_capacity  # kWh

        self.consumption_rate = vehicle.consumption_rate  # kWh/km

        self.charging_stops = []

    def get_min_battery_capacity(self, min_milage: float = 15, avg_speed: float = 80) -> float:
        return min_milage * self.consumption_rate * ((avg_speed / 50) ** 2)

    def _adjust_battery_capacity_for_age(self) -> float:
        vehicle_age_years = self._get_vehicle_age_years()
        degradation_rate_per_year = 0.025
        degradation = max(0, vehicle_age_years * degradation_rate_per_year)
        adjusted_capacity = self.battery_capacity * (1 - degradation)
        return max(adjusted_capacity, self.battery_capacity * 0.7)

    def _get_vehicle_age_years(self) -> float:
        current_year = datetime.now().year
        return current_year - self.vehicle.year_of_manufacture

    def selfcalculate_temperature_effect(self, start_coord: Dict[str, float], end_coord: Dict[str, float]) -> float:

        temps = []
        for coord in [start_coord, end_coord]:
            weather = Request_weather(coord["lat"], coord["lon"])
            if weather and "temperature" in weather:
                temps.append(weather["temperature"])
        if not temps:
            avg_temp = 20  # default average temp
        else:
            avg_temp = sum(temps) / len(temps)
        if avg_temp < 15:
            temp_factor = 1 + (15 - avg_temp) * 0.03
        elif avg_temp > 25:
            temp_factor = 1 + (avg_temp - 25) * 0.02
        else:
            temp_factor = 1.0
        temp_factor = max(0.9, min(temp_factor, 1.3))
        return temp_factor

    def calculate_elevation_effect(self, start_coord: Dict[str, float], end_coord: Dict[str, float]) -> float:
        """
        Calculate elevation effect for a segment between start and end coordinates.
        """
        elevations = Request_elevation([(start_coord["lon"], start_coord["lat"]), (end_coord["lon"], end_coord["lat"])])
        if not elevations or len(elevations) < 2:
            return 1.0
        diff = elevations[1]["elevation"] - elevations[0]["elevation"]
        if diff > 0:
            gain_factor = 1 + (diff / 800) ** 1.2
            loss_factor = 1.0
        else:
            gain_factor = 1.0
            loss_factor = 1 - min(0.5, (abs(diff) / 1500) ** 1.1)
        elevation_factor = max(0.7, gain_factor * loss_factor)
        return elevation_factor

    def calculate_speed_effect(self, step) -> float:

        duration = step.get("duration", None)
        distance = step.get("distance", None)

        # Calculate speed effect per step using quadratic model
        speed_factor = 1.0

        if duration is not None and distance is not None:
            speed = (distance / duration) * 3.6  # v = t*s
            speed_factor = (speed / 50) ** 2
        return speed_factor

    def simulate_battery_along_route(self, interval_km: float = 100.0) -> List[float]:

        battery_state = self.battery_capacity
        battery_states = []
        route = self.osrm_response.get("routes", [])[0]
        legs = route.get("legs", [])

        total_distance = 0.0
        total_consumption = 0.0

        interval_distance = 0.0
        interval_consumption = 0.0
        interval_start_coord = None

        steps = [step for leg in legs for step in leg.get("steps", [])]
        for step in steps:
            distance = step.get("distance", 0) / 1000  # km
            location = step.get("maneuver", {}).get("location", None)
            step_coord = {"lon": location[0], "lat": location[1]} if location else None

            # Case 3: too big
            if interval_distance + distance > interval_km * 1.1:
                # TODO
                pass
            # Case 2: just right
            elif interval_distance + distance > interval_km * 0.9 and interval_distance + distance < interval_km * 1.1:  # margin

                if interval_start_coord and step_coord:
                    temp_effect = self.selfcalculate_temperature_effect(interval_start_coord, step_coord)
                    elev_effect = self.calculate_elevation_effect(interval_start_coord, step_coord)
                else:
                    temp_effect = 1.0
                    elev_effect = 1.0

                interval_consumption *= temp_effect * elev_effect

                total_distance += interval_distance
                total_consumption += interval_consumption

                # reset interval
                interval_distance = 0.0
                interval_consumption = 0.0
                interval_start_coord = None

            # Case 1: just another step
            else:

                # Calculate consumption for this step with speed effect
                speed_factor = self.calculate_speed_effect(step)
                step_consumption = self.consumption_rate * distance * speed_factor

                interval_distance += distance
                interval_consumption += step_consumption

            # check if any battery left at all times
            if self.battery_capacity - interval_consumption - self.min_battery_capacity <= 0:
                chargings_station_coord = self.find_next_charging_station(step_coord, self.vehicle)

                # TODO create a route to the charging station and track steps to get the distance and consumption

                return {"consumption": total_consumption, "end_location": chargings_station_coord}

            if interval_start_coord is None and step_coord is not None:
                interval_start_coord = step_coord

        return {"consumption": total_consumption, "end_location": None}

    def find_next_charging_station(self, start_location, vehicle):
        """
        Find the nearest reachable charging station from start_location within battery range.
        """
        from graphs.utils.open_charge_map import find_nearest_charging_stations

        max_distance_km = vehicle.current_battery / 100 * vehicle.battery_capacity / vehicle.consumption_rate
        charging_stations = find_nearest_charging_stations(
            start_location.latitude, start_location.longitude, max_distance_km=max_distance_km
        )

        if not charging_stations:
            raise Exception("No reachable charging stations found within battery range")

        charging_station = charging_stations[0]
        charging_location = Point(charging_station["AddressInfo"]["Longitude"], charging_station["AddressInfo"]["Latitude"])
        return charging_location
