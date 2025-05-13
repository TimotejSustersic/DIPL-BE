from django.contrib.gis.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    year_of_manufacture = models.IntegerField()
    battery_capacity = models.FloatField()  # kWh
    consumption_rate = models.FloatField()  # kWh/km

    def __str__(self):
        return self.name


class Route(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_city = models.CharField(max_length=100)
    end_city = models.CharField(max_length=100)
    total_distance = models.IntegerField(null=True)  # m
    total_travel_time = models.IntegerField(null=True)  # s
    total_consumption = models.IntegerField(null=True)  # kw

    def __str__(self):
        return f"{self.vehicle} Route"
