from typing import Any, Dict
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework.decorators import api_view
from graphs.models import Vehicle, Route
from graphs.shemas.routingDTO import RouteDB, RouteDTO
from graphs.utils.geopy import Request_geopy
from graphs.utils.osrm import Request_osrm  # Adjust import path if needed
from graphs.utils.battery_consumption import BatteryConsumptionFactory


class RoutingFactory:

    from_history = False

    def __init__(self, params):

        self.data = params

        self.start_city = self.data.get("start_city")
        self.end_city = self.data.get("end_city")

        self.vehicle_id = float(self.data.get("vehicle_id"))
        self.vehicle = Vehicle.objects.get(id=self.vehicle_id)

        self.battery_capacity = self.data.get("battery_capacity")
        if self.battery_capacity:
            self.vehicle.battery_capacity = float(self.battery_capacity)
            self.vehicle.save()
        else:
            self.battery_capacity = self.vehicle.battery_capacity
            self.from_history = True

        # Get coordinates from city names
        geolocator = Request_geopy()
        self.start_location = geolocator.geocode(self.start_city)
        self.end_location = geolocator.geocode(self.end_city)

        if not self.start_location or not self.end_location:
            raise ValueError("Invalid city name")

    def start_route(self, start_location=None, end_location=None, accumulated_charging_stops=None):

        if start_location is None:
            start_location = self.start_location
        if end_location is None:
            end_location = self.end_location
        if accumulated_charging_stops is None:
            accumulated_charging_stops = []

        start_lon = start_location.longitude
        start_lat = start_location.latitude
        end_lon = end_location.longitude
        end_lat = end_location.latitude

        # get route geometry
        osrm_params = f"/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?steps=true&annotations=speed"
        osrm_response = Request_osrm(osrm_params)

        route = RouteDB(osrm_response, self.vehicle, self.start_city, self.end_city, start_location, end_location)

        if not self.from_history:
            route.save_to_db()

            # delete old to never exceed 10 routes
            if Route.objects.count() > 10:
                Route.objects.order_by("id").first().delete()  # Lowest ID = oldest

        # # Calculate estimated consumption and time
        # battery_factory = BatteryConsumptionFactory(self.vehicle, osrm_response, self.battery_capacity)
        # total_consumption = battery_factory.calculate_total_consumption()
        # estimated_time = route.time  # seconds from RouteDB

        frontend_dto = RouteDTO(
            osrm_response,
            self.vehicle,
            self.start_city,
            self.end_city,
            start_location,
            end_location,
            # estimated_consumption_kwh=total_consumption,
            # estimated_time_seconds=estimated_time,
        )
        result = frontend_dto.to_dict()

        return result

