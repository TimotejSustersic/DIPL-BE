from typing import Any, Dict
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework.decorators import api_view
from graphs.models import Vehicle, Route
from graphs.shemas.routingDTO import RouteDB, RouteDTO
from graphs.utils.geopy import Request_geopy
from graphs.utils.osrm import Request_osrm  # Adjust import path if needed


class RoutingFactory:

    from_history = False

    def __init__(self, params):

        self.data = params
        
        self.start_city = self.data.get("start_city")
        self.end_city = self.data.get("end_city")
        self.vehicle_id = float(self.data.get("vehicle_id"))
        self.battery_capacity = self.data.get("battery_capacity")
        
        # Get coordinates from city names
        geolocator = Request_geopy()
        self.start_location = geolocator.geocode(self.start_city)
        self.end_location = geolocator.geocode(self.end_city)

        if not self.start_location or not self.end_location:
            raise ValueError("Invalid city name")


    def startRoute(self):
        
        vehicle = Vehicle.objects.get(id=self.vehicle_id)
        if self.battery_capacity:
            vehicle.battery_capacity = float(self.battery_capacity)
            vehicle.save()
        else:
            self.battery_capacity = vehicle.battery_capacity
            self.from_history = True            
                
        ## 
        start_lon = self.start_location.longitude
        start_lat = self.start_location.latitude
        end_lon = self.end_location.longitude
        end_lat = self.end_location.latitude

        osrm_params = f"/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?steps=true"
        osrm_response = Request_osrm(osrm_params)

        # print(osrm_response)
        
        route = RouteDB(osrm_response, vehicle, self.start_city, self.end_city, self.start_location, self.end_location)
        
        if not self.from_history:
            route.save_to_db()

            # delete old to never exceed 10 routes
            if Route.objects.count() > 10:
                Route.objects.order_by('id').first().delete()  # Lowest ID = oldest
                
        frontend_dto = RouteDTO(osrm_response, vehicle, self.start_city, self.end_city, self.start_location, self.end_location)
        frontend_dto.to_dict()
        
        return frontend_dto.to_dict()
