from typing import Any, Dict, List
from graphs.models import Vehicle
from graphs.utils.weather import Request_weather
from graphs.utils.elevation import Request_elevation


class BatteryConsumptionFactory:
    def __init__(self, vehicle: Vehicle, osrm_response: Dict[str, Any], battery_capacity: float):
        self.vehicle = vehicle
        self.osrm_response = osrm_response
        self.battery_capacity = battery_capacity  # kWh
        self.current_battery = vehicle.current_battery / 100 * self.battery_capacity  # kWh
        self.consumption_rate = vehicle.consumption_rate  # kWh/km
        self.battery_state_log = []  # Track battery state along the route
        self.charging_stops = []

    def calculate_speed_effect(self) -> float:
        # Calculate battery consumption effect based on speed limits from OSRM annotations
        total_speed_factor = 0.0
        legs = self.osrm_response.get("routes", [])[0].get("legs", [])
        for leg in legs:
            for step in leg.get("steps", []):
                speed = step.get("speed", None)
                distance = step.get("distance", 0) / 1000  # meters to km
                if speed is not None:
                    # Example: higher speed increases consumption by a factor
                    speed_factor = 1 + max(0, (speed - 50) / 100)  # simplistic model
                    total_speed_factor += speed_factor * distance
                else:
                    total_speed_factor += self.consumption_rate * distance
        return total_speed_factor

    def calculate_temperature_effect(self) -> float:
        # Calculate battery consumption effect based on temperature averaged over route
        coords = self._extract_route_coords()
        temps = []
        for coord in coords:
            weather = Request_weather(coord["lat"], coord["lon"])
            if weather and "temperature" in weather:
                temps.append(weather["temperature"])
        if not temps:
            avg_temp = 20  # default average temp
        else:
            avg_temp = sum(temps) / len(temps)
        # Example: battery consumption increases if temp < 10 or temp > 30
        if avg_temp < 10:
            temp_factor = 1.2
        elif avg_temp > 30:
            temp_factor = 1.15
        else:
            temp_factor = 1.0
        return temp_factor

    def calculate_elevation_effect(self) -> float:
        # Calculate battery consumption effect based on elevation gain/loss
        coords = self._extract_route_coords()
        elevations = Request_elevation([(c["lon"], c["lat"]) for c in coords])
        if not elevations or len(elevations) < 2:
            return 1.0  # no effect if no elevation data

        total_gain = 0.0
        total_loss = 0.0
        for i in range(1, len(elevations)):
            diff = elevations[i]["elevation"] - elevations[i - 1]["elevation"]
            if diff > 0:
                total_gain += diff
            else:
                total_loss += abs(diff)

        # Example: energy spent going up is proportional to gain, energy recovered going down is proportional to loss
        gain_factor = 1 + (total_gain / 1000)  # simplistic model
        loss_factor = 1 - (total_loss / 2000)  # regenerative braking reduces consumption
        elevation_factor = max(0.7, gain_factor * loss_factor)  # limit min factor
        return elevation_factor

    def _extract_route_coords(self) -> List[Dict[str, float]]:
        # Extract coordinates from OSRM response geometry
        coords = []
        route = self.osrm_response.get("routes", [])[0]
        geometry = route.get("geometry", {})
        if "coordinates" in geometry:
            for lon, lat in geometry["coordinates"]:
                coords.append({"lon": lon, "lat": lat})
        else:
            # fallback: extract from legs and steps
            legs = route.get("legs", [])
            for leg in legs:
                for step in leg.get("steps", []):
                    maneuver = step.get("maneuver", {})
                    location = maneuver.get("location", None)
                    if location:
                        coords.append({"lon": location[0], "lat": location[1]})
        return coords

    def calculate_total_consumption(self) -> float:
        # Aggregate all effects to calculate total battery consumption in kWh
        speed_effect = self.calculate_speed_effect()
        temp_effect = self.calculate_temperature_effect()
        elevation_effect = self.calculate_elevation_effect()

        # Base consumption is consumption_rate * total distance
        route = self.osrm_response.get("routes", [])[0]
        distance_km = route.get("distance", 0) / 1000

        base_consumption = self.consumption_rate * distance_km

        # Adjust base consumption by effects
        adjusted_consumption = base_consumption * temp_effect * elevation_effect

        # For speed effect, we use it as a multiplier on consumption rate per km
        # Here speed_effect is sum of speed_factor * distance, so normalize it
        if distance_km > 0:
            speed_multiplier = speed_effect / distance_km
        else:
            speed_multiplier = 1.0

        total_consumption = adjusted_consumption * speed_multiplier

        return total_consumption

    def simulate_battery_along_route(self) -> List[float]:
        # Simulate battery state along the route segments
        battery_state = self.current_battery
        battery_states = []
        route = self.osrm_response.get("routes", [])[0]
        legs = route.get("legs", [])
        for leg in legs:
            for step in leg.get("steps", []):
                distance_km = step.get("distance", 0) / 1000
                
                consumption = self.consumption_rate * distance_km

                # Adjust consumption by effects (simplified here)
                consumption *= self.calculate_temperature_effect()
                consumption *= self.calculate_elevation_effect()

                # Speed effect per step
                speed = step.get("speed", None)
                if speed is not None:
                    speed_factor = 1 + max(0, (speed - 50) / 100)
                    consumption *= speed_factor

                battery_state -= consumption
                battery_states.append(battery_state)
                if battery_state <= 0:
                    self.charging_stops.append(step.get("maneuver", {}).get("location", None))
                    battery_state = self.battery_capacity  # simulate charging

        self.battery_state_log = battery_states
        return battery_states
