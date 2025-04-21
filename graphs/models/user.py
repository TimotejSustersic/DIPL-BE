from django.contrib.gis.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    battery_capacity = models.FloatField()  # kWh
    consumption_rate = models.FloatField()  # kWh/km
    current_battery = models.FloatField(default=100)  # % charge
    year_of_manufacture = models.IntegerField()

    def __str__(self):
        return self.name


class Route(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start = models.PointField(srid=4326)
    end = models.PointField(srid=4326)    
    start_city = models.CharField(max_length=100)
    end_city = models.CharField(max_length=100)
    distance = models.FloatField(null=True)  # km
    waypoints = models.JSONField(null=True)  # Store charging stops as JSON

    def __str__(self):
        return f"{self.vehicle} Route"
