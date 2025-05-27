import json
from graphs.models.test import Test, TestRoute
from graphs.models.user import Vehicle
from graphs.apis.geopy import Request_geopy
from graphs.utils.RoutingFactory import RoutingFactory, get_OSRM
from graphs.utils.util import Coordinate, Parse_str_to_list


class TestingFactory:

    def __init__(self, params):

        self.name = params.get("name")
        self.cities = Parse_str_to_list(params.get("cities", []))
        self.battery_capacity = int(params.get("battery_capacity", 100))

        test = Test.objects.create(
            name= self.name,
            battery_capacity=self.battery_capacity,
            cities=self.cities,
        )
        test.save()

    def run_tests(self):

        for i in range(len(self.cities)):
            for j in range(i + 1, len(self.cities)):
                start_city = self.cities[i]
                end_city = self.cities[j]

                # Get coordinates from city names
                geolocator = Request_geopy()
                start_location = geolocator.geocode(start_city)
                end_location = geolocator.geocode(end_city)

                # Check if already computed
                routing_response = self.get_route(start_city, end_city)
                # If not start new
                if not routing_response:
                    routing_response, start_location, end_location = self.start_test_route(start_city, end_city)

                    # Run OSRM for comparison
                    osrm_response = get_OSRM(start_location, end_location)

                    osrm_route = osrm_response.get("routes", [])[0] if osrm_response.get("routes") else {}

                    self.store_route_result(start_city, end_city, routing_response, osrm_route, start_location, end_location)

    def start_test_route(self, start_city, end_city):

        first_vehicle = Vehicle.objects.first()

        params = {
            "start_city": start_city,
            "end_city": end_city,
            "vehicle_id": first_vehicle.id,
            "battery_capacity": self.battery_capacity,  # Assume full battery for testing
        }

        routing_factory = RoutingFactory(params)

        routing_factory.accumulated_routes = []
        routing_factory.accumulated_charging_stops = []
        routing_factory.accumulated_empty_battery = []

        routing_factory.new_route(routing_factory.start_location, routing_factory.end_location)

        total_distance = int(sum([route.estimated_distance for route in routing_factory.accumulated_routes]))
        total_time = int(sum([route.estimated_time for route in routing_factory.accumulated_routes]))
        total_consumption = int(sum([route.estimated_consumption for route in routing_factory.accumulated_routes]))

        response = {
            "accumulated_routes": [route.to_dict() for route in routing_factory.accumulated_routes],
            "accumulated_charging_stops": routing_factory.accumulated_charging_stops,
            "accumulated_empty_battery": routing_factory.accumulated_empty_battery,
            "total_distance": total_distance,
            "total_time": total_time,
            "total_consumption": total_consumption,
        }

        return response, routing_factory.start_location, routing_factory.end_location

    def get_route(self, start_city: str, end_city: str) -> TestRoute:
        return (
            TestRoute.objects.filter(start_city=start_city, end_city=end_city).first()
            or TestRoute.objects.filter(start_city=end_city, end_city=start_city).first()
        )

    def store_route_result(self, start_city: str, end_city: str, routing_response: dict, osrm_route: dict, start_location: str, end_location: str): 

        my_accumulated_routes = [route.get("geometry", "") for route in routing_response.get("accumulated_routes")]
        my_accumulated_charging_stops = [Coordinate(coord.get("AddressInfo")).to_string() for coord in routing_response.get("accumulated_charging_stops")]
        my_accumulated_empty_battery = routing_response.get("accumulated_empty_battery")

        test_route = TestRoute.objects.create(
            start_city=str(start_city),
            end_city=str(end_city),
            start_coord=Coordinate(start_location).to_string(),
            end_coord=Coordinate(end_location).to_string(),
            osrm_accumulated_routes=str(osrm_route.get("geometry", "")),
            osrm_total_time=int(osrm_route.get("duration", 0)),
            osrm_total_distance=int(osrm_route.get("distance", 0)),
            my_accumulated_routes=my_accumulated_routes,
            my_accumulated_charging_stops=my_accumulated_charging_stops,
            my_accumulated_empty_battery=my_accumulated_empty_battery,
            my_total_time=int(routing_response.get("total_time", 0)),
            my_total_distance=int(routing_response.get("total_distance", 0)),
        )
        test_route.save()
