from typing import Any, Dict
from django.contrib.gis.geos import Point
from graphs.models import Vehicle, Route


class RouteDB:
    vehicle: Vehicle
    start: Point  # GIS Point
    end: Point  # GIS Point
    start_city: str
    end_city: str
    distance: float  # km
    time: float  # seconds

    def __init__(
        self,
        vehicle: Vehicle,
        start_city: str,
        end_city: str,
        total_distance: int,
        total_consumption: int,
        total_travel_time: int,
    ):

        # Vehicle
        try:
            self.vehicle = vehicle  # Store name for simplicity
        except Vehicle.DoesNotExist:
            raise ValueError("Vehicle not found")

        # Cities
        self.start_city = str(start_city) if start_city else ""
        self.end_city = str(end_city) if end_city else ""

        # Distance and Time from OSRM
        try:
            self.total_distance = total_distance
            self.total_consumption = total_consumption
            self.total_travel_time = total_travel_time
        except:
            raise TypeError("Route parse error: Invalid distance or time")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vehicle": self.vehicle.name,
            "start_city": self.start_city,
            "end_city": self.end_city,
            "total_distance": self.total_distance,
            "total_consumption": self.total_consumption,
            "total_travel_time": self.total_travel_time,
        }

    def save_to_db(self) -> Route:
        return Route.objects.create(
            vehicle=self.vehicle,
            start_city=self.start_city,
            end_city=self.end_city,
            total_distance=self.total_distance,
            total_consumption=self.total_consumption,
            total_travel_time=self.total_travel_time,
        )


class RouteDTO:

    geometry: str  # OSRM
    estimated_consumption: float
    estimated_time: float
    estimated_distance: float
    start_coord: float
    end_coord: float

    def __init__(
        self,
        osrm_response: Dict[str, Any],
        vehicle: Vehicle,
        start_coord,
        end_coord,
        total_consumption,
    ):

        # Geometry
        try:
            routes = osrm_response["routes"]
            self.route = routes[0]
            self.geometry = self.route.get("geometry")
        except:
            raise ValueError("Geometry is missing")

        # Vehicle
        try:
            self.vehicle = vehicle  # Store name for simplicity
        except Vehicle.DoesNotExist:
            raise ValueError("Vehicle not found")

        # Start/End
        self.start_coord = start_coord
        self.end_coord = end_coord

        self.estimated_consumption = total_consumption
        self.estimated_time = self.route.get("duration")
        self.estimated_distance = self.route.get("distance")

    def to_dict(self) -> Dict[str, Any]:
        return {
            # "route": self.route,
            "geometry": self.geometry,
            "start_coord": [self.start_coord.latitude, self.start_coord.longitude],
            "end_coord": [self.end_coord.latitude, self.end_coord.longitude],
            "estimated_consumption": self.estimated_consumption,
            "estimated_time": self.estimated_time,
            "estimated_distance": self.estimated_distance,
        }
