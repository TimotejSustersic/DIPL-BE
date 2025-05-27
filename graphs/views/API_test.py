# utils
# import pandas as pd
# libraries
import asyncio

# functions
from graphs.models.test import Test
from graphs.apis.open_charge_map import Request_open_charge_map
from graphs.apis.osrm import Request_osrm
from graphs.views.utils import *

from geopy.geocoders import Nominatim
import requests

############
# API
############

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "user_name": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "user_name",
        ],
    ),
)
@api_view(["POST"])
def testOSRM(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    user_name = request.data.get("user_name")

    if user_name is None:
        return getErrorResponse(ERR_MESS_PARAMS)
    try:
        response = Request_osrm("/route/v1/driving/14.5058,46.0569;15.6466,46.5570")
        print(response["routes"][0]["distance"])
        return Response(response, status=200)
    except Exception as e:
        return getNotFoundResponse(e)

    return getPOSTResponse("Succ")

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "user_name": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "user_name",
        ],
    ),
)
@api_view(["POST"])
def testGEOPY(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    user_name = request.data.get("user_name")

    if user_name is None:
        return getErrorResponse(ERR_MESS_PARAMS)
    try:
        geolocator = Nominatim(user_agent="EVRoutingThesis")
        location = geolocator.geocode("Ljubljana")
        if location:
            data = {
                "city": "Ljubljana",
                "lon": location.longitude,
                "lat": location.latitude
            }
            return Response(data, status=200)
    except Exception as e:
        return getNotFoundResponse(e)

    return getPOSTResponse("Succ")

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "user_name": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "user_name",
        ],
    ),
)
@api_view(["POST"])
def testRequests(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    user_name = request.data.get("user_name")

    if user_name is None:
        return getErrorResponse(ERR_MESS_PARAMS)
    try:
        stations = Request_open_charge_map()
        return Response(stations, status=200)
    except Exception as e:
        return getNotFoundResponse(e)

    return getPOSTResponse("Succ")
