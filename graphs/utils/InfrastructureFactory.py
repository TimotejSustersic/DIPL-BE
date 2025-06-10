from itertools import combinations
import json
from graphs.models.infrastructure import TestInstance, TestInstanceRoute, TestInstanceSerializer
from graphs.models.test import Test, TestRoute
from graphs.models.user import Vehicle
from graphs.utils.RoutingFactory import RoutingFactory
from graphs.utils.util import Coordinate
from django.db.models import Q


class InfrastructureFactory:

    def __init__(self, params):

        test_id = params.get("test_id")
        self.test = Test.objects.get(id=test_id)
        self.name = params.get("name")

        self.infrastructure = [Coordinate(coord) for coord in params.get("additional_charging_stations", [])]

    def get_problematic_routes(self, distance_threshold_km=4) -> list[TestRoute]:
        city_pairs = list(combinations(self.test.cities, 2))
        query = Q()
        for start_city, end_city in city_pairs:
            query |= Q(start_city=start_city, end_city=end_city) | Q(start_city=end_city, end_city=start_city)

        test_routes = TestRoute.objects.filter(query)

        problematic_routes = [
            route for route in test_routes if ((route.my_total_distance - route.osrm_total_distance) / 1000) > distance_threshold_km
        ]

        return problematic_routes

    def run_route(self, route: TestRoute):

        first_vehicle = Vehicle.objects.first()

        params = {
            "start_city": route.start_city,
            "end_city": route.end_city,
            "vehicle_id": first_vehicle.id,
            "battery_capacity": self.test.battery_capacity if hasattr(self.test, "battery_capacity") else 100,
            "additional_charging_stations": self.infrastructure,
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

        return response

    def run_test(self):

        problematic_routes = self.get_problematic_routes()

        if not problematic_routes:
            return

        distance_diff_sum = 0
        time_diff_sum = 0
        counter = 0

        # Store run_route results to avoid redundant calls
        route_responses = {}

        # run algoritem and get data
        for problematic_route in problematic_routes:
            new_route_response = self.run_route(problematic_route)
            route_responses[problematic_route.id] = new_route_response

            # Evaluate the new route compared to the old route
            old_distance = problematic_route.my_total_distance
            new_distance = new_route_response.get("total_distance")
            distance_diff = new_distance - old_distance

            old_time = problematic_route.my_total_time
            new_time = new_route_response.get("total_time")
            time_diff = new_time - old_time

            distance_diff_sum += distance_diff
            time_diff_sum += time_diff
            counter += 1

        # Store testing instance result summary
        avg_distance_diff = distance_diff_sum / counter
        avg_time_diff = time_diff_sum / counter

        new_test_instance = TestInstance.objects.create(
            test=self.test,
            name=self.name,
            charging_stops=[coord.to_string() for coord in self.infrastructure],
            avg_distance_diff=avg_distance_diff,
            avg_time_diff=avg_time_diff,
        )
        new_test_instance.save()

        # store data
        for problematic_route in problematic_routes:
            new_route_response = route_responses.get(problematic_route.id)

            # Evaluate the new route compared to the old route
            old_distance = problematic_route.my_total_distance
            new_distance = new_route_response.get("total_distance")
            distance_diff = new_distance - old_distance

            old_time = problematic_route.my_total_time
            new_time = new_route_response.get("total_time")
            time_diff = new_time - old_time
        
            accumulated_routes = [route.get("geometry", "") for route in new_route_response.get("accumulated_routes")]
            accumulated_charging_stops = [Coordinate(coord).to_string() for coord in new_route_response.get("accumulated_charging_stops")]

            new_instance_route = TestInstanceRoute.objects.create(
                test_instance=new_test_instance,
                test_route=problematic_route,
                new_accumulated_routes= accumulated_routes,
                new_accumulated_charging_stops=accumulated_charging_stops,
                new_total_distance=distance_diff,
                new_total_time=time_diff,
            )
            new_instance_route.save()

        # Return serializable summary object
        return TestInstanceSerializer(new_test_instance)
