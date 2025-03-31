from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework.decorators import api_view
from graphs.models import Vehicle, Route
from graphs.utils.geopy import Request_geopy
from graphs.utils.osrm import Request_osrm  # Adjust import path if needed


class RoutingFactory:

    def __init__(self, params):

        self.data = params
        
        self.start_city = self.data.get("start_city")
        self.end_city = self.data.get("end_city")
        self.vehicle_id = float(self.data.get("vehicle_id"))
        self.battery_capacity = float(self.data.get("battery_capacity"))
        
        # Get coordinates from city names
        geolocator = Request_geopy()
        start_location = geolocator.geocode(self.start_city)
        end_location = geolocator.geocode(self.end_city)

        if not start_location or not end_location:
            raise ValueError("Invalid city name")
        
        self.start_lon = start_location.longitude
        self.start_lat = start_location.latitude
        self.end_lon = end_location.longitude
        self.end_lat = end_location.latitude


    def startRoute(self):
        
        vehicle = Vehicle.objects.get(id=self.vehicle_id)
        vehicle.battery_capacity = self.battery_capacity
        vehicle.save()

        start = Point(self.start_lon, self.start_lat)
        end = Point(self.end_lon, self.end_lat)

        osrm_params = f"/route/v1/driving/{self.start_lon},{self.start_lat};{self.end_lon},{self.end_lat}?steps=true"

        route = Request_osrm(osrm_params)
        routes = route.get("routes")[0]
        
        distance = routes.get("distance") / 1000  # km
        geometry = routes.get("geometry")  # Polyline for frontend

        # Save route without waypoints (no charging needed)
        Route.objects.create(
            vehicle=vehicle,
            start=start,
            end=end,
            start_city=self.start_city,
            end_city=self.end_city,
            distance=distance,
            waypoints=[]  # Empty for now
        )

        return {
            "distance": distance,
            "start": [self.start_lon, self.start_lat],
            "end": [self.end_lon, self.end_lat],
            "geometry": geometry
        }
