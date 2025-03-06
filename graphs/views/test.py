# utils
# import pandas as pd
# libraries
import asyncio

# functions
from graphs.models.test import Test
from graphs.views.utils import *

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
        required=["user_name",],
    ),
)
@api_view(["POST"])
def test(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    user_name = request.data.get("user_name")
    
    if user_name is None:
        return getErrorResponse(ERR_MESS_PARAMS)
    try:
        # Query all Test objects
        tests = Test.objects.all()
        # Serialize manually (or use DRF serializers below)
        data = [
            {
                "id": test.id,
                "name": test.name,
                "location": test.location.geojson  # Returns GeoJSON string
            }
            for test in tests
        ]
        return Response(data, status=200)
    except Exception as e:
        return getNotFoundResponse(e)

    return getPOSTResponse("Succ")
