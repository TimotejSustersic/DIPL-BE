from typing import Dict
from graphs.models import Vehicle
from graphs.utils.weather import Request_weather
from graphs.utils.elevation import Request_elevation

avg_speed = 50 #km/h


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

        speed_factor = 1.0  # Default factor if data is missing

        if duration is not None and distance is not None and duration > 0:
            speed = (distance / duration) * 3.6  # Convert m/s to km/h
            # Quadratic model: consumption increases with square of speed ratio
            speed_factor += (speed / avg_speed) ** 2

            # Clamp speed_factor to a reasonable range to avoid extreme values
            speed_factor = max(0.8, min(speed_factor, 2.0))

        return speed_factor


# def calculate_speed_effect(
#     velocity: float,               # Current speed (km/h)
#     reference_velocity: float,     # Baseline speed for known consumption (km/h)
#     drag_coefficient: float,       # Vehicle's Cd (0.2-0.4)
#     frontal_area: float,           # Vehicle's A (m²)
#     rolling_resistance_coeff: float,  # Cr (0.008-0.015)
#     vehicle_mass: float,           # kg
#     air_density: float = 1.225,    # kg/m³ (default sea level)
#     gravity: float = 9.81          # m/s²
# ) -> float:
#     """
#     Calculates the speed adjustment factor for EV energy consumption.
#     Returns: Multiplier for base consumption rate at reference speed.
#     """
#     # Aerodynamic drag component (v³ term)
#     drag_force = 0.5 * air_density * drag_coefficient * frontal_area * velocity**3
    
#     # Rolling resistance component (v² and v terms)
#     rolling_resistance = vehicle_mass * gravity * rolling_resistance_coeff * (
#         0.01 * velocity**2 + 0.0002 * velocity  # Empirical coefficients
#     )
    
#     # Reference speed components
#     ref_drag = 0.5 * air_density * drag_coefficient * frontal_area * reference_velocity**3
#     ref_rolling = vehicle_mass * gravity * rolling_resistance_coeff * (
#         0.01 * reference_velocity**2 + 0.0002 * reference_velocity
#     )

#     return (drag_force + rolling_resistance) / (ref_drag + ref_rolling)

# # Example: Tesla Model 3 at 90 km/h vs 60 km/h baseline
# speed_factor = calculate_speed_effect(
#     velocity=90,
#     reference_velocity=60,
#     drag_coefficient=0.23,
#     frontal_area=2.22,  # m²
#     rolling_resistance_coeff=0.01,
#     vehicle_mass=1800  # kg
# )

# base_consumption = 0.15  # kWh/km at 60 km/h
# adjusted_consumption = base_consumption * speed_factor  # Now 0.15 × 1.85 ≈ 0.278 kWh/km
