from django.urls import path

###################
# endpoints
from graphs.views.routing import *
from graphs.views.vehicles import *
from graphs.views.testing import *
from graphs.views.infrastructure import *
from graphs.views.admin import *

# add all endpoint urls

# if there are no custom endpoints that except extra params,
# just build a loop and insert them automatically

urlpatterns = [
    path("vehicles/new", new_vehicle, name="new_vehicle"),
    path("vehicles/query", vehicle_query, name="vehicle_query"),
    path("vehicles/discard", vehicle_discard, name="vehicle_discard"),
    
    path("routing/new", routing_new, name="routing_new"),
    path("routing/query", routing_query, name="routing_query"),

    path("tests/query", tests_query, name="tests_query"),
    path("testing/items/query", test_items_query, name="test_items_query"),
    path("testing/new", test_new, name="testing_new"),

    path("infrastructure/query", infrastructure_query, name="infrastructure_query"),
    path("infrastructure/items/query", infrastructure_items_query, name="infrastructure_items_query"),
    path("infrastructure/new", infrastructure_new, name="infrastructure_new"),

    path("admin/clear/TestInstance", clear_TestInstance, name="clear_TestInstance"),
    path("admin/clear/TestInstanceRoute", clear_TestInstanceRoute, name="clear_TestInstanceRoute"),
    path("admin/clear/Test", clear_Test, name="clear_Test"),
    path("admin/clear/TestRoute", clear_TestRoute, name="clear_TestRoute"),
    path("admin/clear/Route", clear_Route, name="clear_Route"),
    path("admin/clear/Vehicle", clear_Vehicle, name="clear_Vehicle"),
]
