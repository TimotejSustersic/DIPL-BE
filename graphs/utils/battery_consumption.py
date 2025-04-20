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

    def calculate_temperature_effect_segment(self, start_coord: Dict[str, float], end_coord: Dict[str, float]) -> float:
        # Calculate temperature effect for a segment between start and end coordinates
        # For simplicity, average temperature at start and end points
        temps = []
        for coord in [start_coord, end_coord]:
            weather = Request_weather(coord["lat"], coord["lon"])
            if weather and "temperature" in weather:
                temps.append(weather["temperature"])
        if not temps:
            avg_temp = 20  # default average temp
        else:
            avg_temp = sum(temps) / len(temps)
        if avg_temp < 10:
            temp_factor = 1.2
        elif avg_temp > 30:
            temp_factor = 1.15
        else:
            temp_factor = 1.0
        return temp_factor

    def calculate_elevation_effect_segment(self, start_coord: Dict[str, float], end_coord: Dict[str, float]) -> float:
        # Calculate elevation effect for a segment between start and end coordinates
        elevations = Request_elevation([(start_coord["lon"], start_coord["lat"]), (end_coord["lon"], end_coord["lat"])])
        if not elevations or len(elevations) < 2:
            return 1.0
        diff = elevations[1]["elevation"] - elevations[0]["elevation"]
        if diff > 0:
            gain_factor = 1 + (diff / 1000)
            loss_factor = 1.0
        else:
            gain_factor = 1.0
            loss_factor = 1 - (abs(diff) / 2000)
        elevation_factor = max(0.7, gain_factor * loss_factor)
        return elevation_factor

    def simulate_battery_along_route(self, interval_km: float = 100.0) -> List[float]:
        # Simulate battery state along the route every interval_km kilometers
        battery_state = self.current_battery
        battery_states = []
        route = self.osrm_response.get("routes", [])[0]
        legs = route.get("legs", [])

        accumulated_distance = 0.0
        accumulated_consumption = 0.0
        last_location = None
        interval_start_coord = None

        def apply_consumption(consumption, location):
            nonlocal battery_state
            battery_state -= consumption
            battery_states.append(battery_state)
            if battery_state <= 0:
                self.charging_stops.append(location)
                battery_state = self.battery_capacity  # simulate charging

        for leg in legs:
            for step in leg.get("steps", []):
                step_distance = step.get("distance", 0) / 1000  # km
                step_speed = step.get("speed", None)
                step_location = step.get("maneuver", {}).get("location", None)
                step_coord = {"lon": step_location[0], "lat": step_location[1]} if step_location else None

                # Calculate speed effect per step
                speed_factor = 1.0
                if step_speed is not None:
                    speed_factor = 1 + max(0, (step_speed - 50) / 100)

                # Calculate consumption for this step with speed effect
                step_consumption = self.consumption_rate * step_distance * speed_factor

                if interval_start_coord is None and step_coord is not None:
                    interval_start_coord = step_coord

                # Accumulate distance and consumption
                while step_distance > 0:
                    remaining_to_interval = interval_km - accumulated_distance
                    if step_distance >= remaining_to_interval:
                        # Calculate fraction of step to complete interval
                        fraction = remaining_to_interval / step_distance
                        consumption_chunk = step_consumption * fraction
                        accumulated_consumption += consumption_chunk
                        accumulated_distance += remaining_to_interval

                        # Calculate temperature and elevation effects for interval segment
                        if interval_start_coord and step_coord:
                            temp_effect = self.calculate_temperature_effect_segment(interval_start_coord, step_coord)
                            elev_effect = self.calculate_elevation_effect_segment(interval_start_coord, step_coord)
                        else:
                            temp_effect = 1.0
                            elev_effect = 1.0

                        # Apply effects to accumulated consumption
                        adjusted_consumption = accumulated_consumption * temp_effect * elev_effect

                        apply_consumption(adjusted_consumption, step_location)

                        # Reset accumulators and start coord
                        accumulated_distance = 0.0
                        accumulated_consumption = 0.0
                        interval_start_coord = None

                        # Reduce step distance and consumption for remaining part
                        step_distance -= remaining_to_interval
                        step_consumption -= consumption_chunk
                    else:
                        # Accumulate remaining step distance and consumption
                        accumulated_distance += step_distance
                        accumulated_consumption += step_consumption
                        step_distance = 0

        # Apply any remaining consumption after loop
        if accumulated_distance > 0:
            # Use last known coordinates for effects if available
            if interval_start_coord and step_coord:
                temp_effect = self.calculate_temperature_effect_segment(interval_start_coord, step_coord)
                elev_effect = self.calculate_elevation_effect_segment(interval_start_coord, step_coord)
            else:
                temp_effect = 1.0
                elev_effect = 1.0
            adjusted_consumption = accumulated_consumption * temp_effect * elev_effect
            apply_consumption(adjusted_consumption, step_location)

        self.battery_state_log = battery_states
        return battery_states
