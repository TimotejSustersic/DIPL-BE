from datetime import datetime
from graphs.models.user import Vehicle


degradation_rate_per_year = 0.025
full_percentage_best_practise = 0.8 # %


class ClassVehicle:

    min_milage = 30

    def __init__(self, vehicle: Vehicle, current_battery_percentage=None):
        self.vehicle = vehicle

        self.adjusted_battery_capacity = self.adjust_battery_capacity_for_age()

        full_battery = self.adjusted_battery_capacity * full_percentage_best_practise

        if current_battery_percentage:
            self.current_battery = current_battery_percentage
        else:
            self.current_battery = full_battery

    # it's possible initial battery capacity is not full
    def recharge_battery(self):
        self.current_battery = self.adjusted_battery_capacity * full_percentage_best_practise

    def get_min_battery_capacity(self, avg_speed: float = 80, min_milage: float = 15) -> float:
        return self.min_milage * self.vehicle.consumption_rate * ((avg_speed / 50) ** 2)

    def adjust_battery_capacity_for_age(self) -> float:

        vehicle_age_years = self.get_vehicle_age_years()
        degradation = vehicle_age_years * degradation_rate_per_year

        adjusted_capacity = self.vehicle.battery_capacity * (1 - degradation)
        return adjusted_capacity

    def get_vehicle_age_years(self) -> float:
        current_year = datetime.now().year
        return current_year - self.vehicle.year_of_manufacture
