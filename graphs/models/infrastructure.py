from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from rest_framework import serializers

from graphs.models.test import Test, TestRoute, TestRouteSerializer


class TestInstance(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    charging_stops = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
    )
    avg_distance_diff = models.FloatField()
    avg_time_diff = models.FloatField()

    def __str__(self):
        return "TestInstance"


class TestInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestInstance
        fields = ["id", "name", "charging_stops", "avg_distance_diff", "avg_time_diff"]


class TestInstanceRoute(models.Model):
    test_instance = models.ForeignKey(TestInstance, on_delete=models.CASCADE)
    test_route = models.ForeignKey(TestRoute, on_delete=models.CASCADE)
    new_accumulated_routes = ArrayField(
        models.TextField(),
        default=list,
        blank=False,
    )
    new_accumulated_charging_stops = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
    )
    new_total_distance = models.FloatField()
    new_total_time = models.FloatField()

    def __str__(self):
        return f"{self.start_city} to {self.end_city} Route"


class TestInstanceRouteSerializer(serializers.ModelSerializer):
    test_instance = TestInstanceSerializer()
    test_route = TestRouteSerializer()

    class Meta:
        model = TestInstanceRoute
        fields = [
            "id",
            "test_instance",
            "test_route",
            "new_accumulated_routes",
            "new_accumulated_charging_stops",
            "new_total_distance",
            "new_total_time",
        ]
