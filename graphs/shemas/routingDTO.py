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
            osrm_response: Dict[str, Any], 
            vehicle: Vehicle, 
            start_city: str, 
            end_city: str,
            start,
            end
        ):
        
        if not osrm_response or osrm_response.get("code") != "Ok":
            raise ValueError("Invalid OSRM response")

        # Vehicle
        try:
            self.vehicle = vehicle  # Store name for simplicity
        except Vehicle.DoesNotExist:
            raise ValueError("Vehicle not found")

        # Cities
        self.start_city = str(start_city) if start_city else ""
        self.end_city = str(end_city) if end_city else ""

        # Start/End
        try:
            self.start = Point(start.longitude, start.latitude, srid=4326)
            self.end = Point(end.longitude, end.latitude, srid=4326)
        except:
            raise TypeError("Route parse error: Invalid Points")

        # Distance and Time from OSRM
        try:
            routes = osrm_response["routes"]
            # print(osrm_response.keys())
            
            route = routes[0]
            # print(route.keys())
            self.distance = float(route.get("distance")) / 1000  # meters to km
            self.time = float(route.get("duration"))  # seconds
        except:
            raise TypeError("Route parse error: Invalid distance or time")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vehicle": self.vehicle.name,
            "start": [self.start.x, self.start.y],
            "end": [self.end.x, self.end.y],
            "start_city": self.start_city,
            "end_city": self.end_city,
            "distance": self.distance,
            # "time": self.time,
        }

    def save_to_db(self) -> Route:
        return Route.objects.create(
            vehicle=self.vehicle,
            start=self.start,
            end=self.end,
            start_city=self.start_city,
            end_city=self.end_city,
            distance=self.distance,
            # time=self.time,
            waypoints=[],  # Empty for basic route
        )


class RouteDTO(RouteDB):
    geometry: str  # OSRM polyline
    waypoints: list[dict]  # List of {name, lon, lat}

    def __init__(
            self, 
            osrm_response: Dict[str, Any], 
            vehicle_id: int, 
            start_city: str, 
            end_city: str,
            start,
            end
        ):
        super().__init__(osrm_response, vehicle_id, start_city, end_city, start, end)

        # Geometry
        try:
            routes = osrm_response["routes"]
            # print(osrm_response.keys())
            
            route = routes[0]
            # print(route.keys())
            self.geometry = route.get("geometry")
        except:
            self.geometry = ""  # Default if missing

        # Waypoints (basic route has none, but extensible)
        self.waypoints = []  # Add logic here if waypoints come from OSRM or elsewhere

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "geometry": self.geometry,
                "waypoints": self.waypoints,
            }
        )
        return base_dict
