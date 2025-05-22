from django.urls import path

###################
# endpoints
from graphs.views.routing import *
from graphs.views.vehicles import *
from graphs.views.testing import *

# add all endpoint urls

# if there are no custom endpoints that except extra params,
# just build a loop and insert them automatically

urlpatterns = [
    path("vehicles/new", new_vehicle, name="new_vehicle"),
    path("vehicles/query", vehicle_query, name="vehicle_query"),
    path("vehicles/discard", vehicle_discard, name="vehicle_discard"),
    
    path("routing/new", routing_new, name="routing_new"),
    path("routing/query", routing_query, name="routing_query"),

    path("testing/items/query", test_items_query, name="testing_itemsQuery"),
    path("testing/query", test_query, name="testing_query"),
    path("testing/new", test_new, name="testing_new"),
]

###################
# websockets

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from .utils.channels import TradingConsumer

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter([
#             path('ws/<channel_name>/', TradingConsumer.as_asgi()),
#         ])
#     ),
# })
