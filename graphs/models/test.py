from django.contrib.gis.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()  # Geospatial field for testing PostGIS

    def __str__(self):
        return self.name
