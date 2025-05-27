from itertools import combinations
from graphs.models.infrastructure import TestInstance, TestInstanceRoute, TestInstanceRouteSerializer
from graphs.models.test import Test, TestRoute, TestRouteSerializer
from graphs.tests.TestingFactory import TestingFactory
from graphs.utils.InfrastructureFactory import InfrastructureFactory
from graphs.views.utils import *

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "test_id": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["test_id"],
    ),
)
@api_view(["POST"])
def infrastructure_query(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        test_id = request.data.get("test_id")
        output = list(TestInstance.objects.filter(id=test_id).values("test", "name", "charging_stops"))

        return Response(output)
    except Exception as e:
        return getNotFoundResponse(e)


########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "test_id": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(["POST"])
def infrastructure_items_query(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        test_id = request.data.get("test_id")

        # Retrieve the Test instance
        test_instance = TestInstance.objects.get(id=test_id)

        routes = TestInstanceRoute.objects.filter(test=test_instance)

        serializer = TestInstanceRouteSerializer(routes, many=True)
        return Response(serializer.data)
    except Test.DoesNotExist:
        return getNotFoundResponse("Test with given id does not exist.")
    except Exception as e:
        return getNotFoundResponse(e)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "test_id": openapi.Schema(type=openapi.TYPE_STRING),
            "additional_charging_stations": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "test_id",
            "additional_charging_stations",
        ],
    ),
)
@api_view(["POST"])
def infrastructure_new(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        # Query all Test objects
        testing_factory = InfrastructureFactory(request.data)
        result = testing_factory.run_test()

        return Response(result.data)
    except Exception as e:
        return getNotFoundResponse(e)
