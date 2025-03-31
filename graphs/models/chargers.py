from django.contrib.gis.db import models


class ChargingStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField(srid=4326)  # lon, lat
    charging_speed = models.FloatField()  # kW
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
