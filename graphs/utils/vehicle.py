from datetime import datetime
from graphs.models.user import Vehicle


degradation_rate_per_year = 0.025
full_percentage_best_practise = 0.8 # %
empty_percentage_best_practise = 0.15 # %


class ClassVehicle:

    def __init__(self, vehicle: Vehicle, current_battery_percentage=None):
        self.vehicle = vehicle

        self.adjusted_battery_capacity = self.adjust_battery_capacity_for_age()

        full_battery = self.adjusted_battery_capacity * full_percentage_best_practise

        if current_battery_percentage:
            self.current_battery = full_battery * (current_battery_percentage / 100)
        else:
            self.current_battery = full_battery

    # it's possible initial battery capacity is not full
    def recharge_battery(self):
        self.current_battery = self.adjusted_battery_capacity * full_percentage_best_practise

    # def get_min_battery_capacity(self, min_milage: float = 30) -> float:
    #     return min_milage * self.vehicle.consumption_rate
    def get_min_battery_capacity(self) -> float:
        return self.adjusted_battery_capacity * empty_percentage_best_practise

    def adjust_battery_capacity_for_age(self) -> float:

        vehicle_age_years = self.get_vehicle_age_years()
        degradation = (1 - degradation_rate_per_year) ** vehicle_age_years

        adjusted_capacity = self.vehicle.battery_capacity * degradation
        return adjusted_capacity

    def get_vehicle_age_years(self) -> float:
        current_year = datetime.now().year
        return current_year - self.vehicle.year_of_manufacture
