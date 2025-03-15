from django.urls import path

###################
# endpoints
from graphs.views.test import *
from graphs.views.API_test import *

# add all endpoint urls

# if there are no custom endpoints that except extra params,
# just build a loop and insert them automatically

urlpatterns = [
    path("test/", test, name="test"),
    path("testOSRM/", testOSRM, name="testOSRM"),
    path("testGEOPY/", testGEOPY, name="testGEOPY"),
    path("testRequests/", testRequests, name="testRequests"),
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
