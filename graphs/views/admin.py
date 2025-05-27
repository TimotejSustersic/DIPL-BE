# utils
# import pandas as pd
# libraries
import asyncio

# functions
from graphs.models.infrastructure import TestInstance, TestInstanceRoute
from graphs.models.test import Test, TestRoute
from graphs.models.user import Route, Vehicle
from graphs.views.utils import *

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
    ),
)
@api_view(["POST"])
def clear_TestInstance(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    TestInstance.objects.all().delete()

    return getPOSTResponse("Succ")


########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
)
@api_view(["POST"])
def clear_TestInstanceRoute(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    TestInstanceRoute.objects.all().delete()

    return getPOSTResponse("Succ")


########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
)
@api_view(["POST"])
def clear_Test(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    Test.objects.all().delete()

    return getPOSTResponse("Succ")


########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
)
@api_view(["POST"])
def clear_TestRoute(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    TestRoute.objects.all().delete()

    return getPOSTResponse("Succ")


########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
)
@api_view(["POST"])
def clear_Route(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    Route.objects.all().delete()

    return getPOSTResponse("Succ")


########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
)
@api_view(["POST"])
def clear_Vehicle(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    Vehicle.objects.all().delete()

    return getPOSTResponse("Succ")


########################################
########################################
