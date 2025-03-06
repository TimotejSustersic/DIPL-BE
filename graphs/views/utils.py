from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Response messages


def getErrorResponse(message: str, e: Exception = None) -> Response:
    if e:
        error_message = f"{message}: {str(e)}"
    else:
        error_message = message
    return Response(
        {"message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def getNotFoundResponse(e: Exception = None) -> Response:
    return Response({"message": e}, status=status.HTTP_404_NOT_FOUND)


def getNotallowedResponse(e: Exception = None) -> Response:
    return Response({"message": e}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


ERR_MESS_PARAMS = "Error: Wrong parameters!"
ERR_MESS_QUERY = "Error: Database Query error!"
ERR_MESS_KEY = "Error: No Key Found!"
ERR_MESS = "Error: "


def getPOSTResponse(message: str = None) -> Response:
    return Response({"message": message}, status=status.HTTP_201_CREATED)


def getResponse(message: str, statusCode: status) -> Response:
    return Response({"message": message}, status=statusCode)


def getDELETEResponse(message: str) -> Response:
    return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)


SUCC_MESS_CREATED = "Success: Instance successfully created."
SUCC_MESS_DELETED = "Success: Instance successfully deleted."


def isPOST(request: Request) -> bool:
    return request.method == "POST"
