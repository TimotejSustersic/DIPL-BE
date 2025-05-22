from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from rest_framework import serializers


class TestRoute(models.Model):
    start_city = models.CharField(max_length=200)
    end_city = models.CharField(max_length=200)
    start_coord = models.CharField(max_length=100)
    end_coord = models.CharField(max_length=100)
    osrm_accumulated_routes = models.TextField()
    osrm_total_time = models.IntegerField()
    osrm_total_distance = models.IntegerField()
    my_accumulated_routes = ArrayField(
        models.TextField(),
        default=list,
        blank=False,
    )
    my_accumulated_charging_stops = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
    )
    my_total_distance = models.IntegerField()
    my_total_time = models.IntegerField()

    class Meta:
        #     unique_together = ("start_city", "end_city")  # Composite unique constraint
        indexes = [
            models.Index(fields=["start_city", "end_city"]),  # Improve query performance
        ]

    def __str__(self):
        return f"{self.start_city} to {self.end_city} Route"


class TestRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRoute
        fields = [
            "id",  # Include if you want the primary key
            "start_city",
            "end_city",
            "start_coord",
            "end_coord",
            "osrm_accumulated_routes",
            "osrm_total_time",
            "osrm_total_distance",
            "my_accumulated_routes",
            "my_accumulated_charging_stops",
            "my_total_distance",
            "my_total_time",
        ]
