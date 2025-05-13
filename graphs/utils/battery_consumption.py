from typing import Dict
from graphs.models import Vehicle
from graphs.utils.weather import Request_weather
from graphs.utils.elevation import Request_elevation

avg_speed = 50


class BatteryConsumptionFactory:
    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def calculate_temperature_effect(self, start_coord: Dict[str, float], end_coord: Dict[str, float]) -> float:

        start_temp = Request_weather(start_coord)
        end_temp = Request_weather(end_coord)

        avg_temp = (start_temp + end_temp) / 2

        if avg_temp < 15:
            temp_factor = 1 + (15 - avg_temp) * 0.03
        elif avg_temp > 25:
            temp_factor = 1 + (avg_temp - 25) * 0.02
        else:
            temp_factor = 1.0
        temp_factor = max(0.9, min(temp_factor, 1.3))
        return temp_factor

    def calculate_elevation_effect(self, start_coord: Dict[str, float], end_coord: Dict[str, float]) -> float:

        elevations = Request_elevation([start_coord, end_coord])
        if not elevations or len(elevations) < 2:
            return 1.0
        diff = elevations[1] - elevations[0]
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
            speed_factor = (speed / avg_speed) ** 2
        return speed_factor
