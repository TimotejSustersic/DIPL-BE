from itertools import combinations
from graphs.models.test import TestRoute, TestRouteSerializer
from graphs.tests.TestingFactory import TestingFactory
from graphs.views.utils import *

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "search": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(["POST"])
def test_items_query(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        search = request.data.get("search", "").strip().lower()

        # Filter and select only start_city, end_city directly in the database
        if search:
            routes = TestRoute.objects.filter(
                start_city__icontains=search
            ) | TestRoute.objects.filter(
                end_city__icontains=search
            )
            routes = routes.values("start_city", "end_city").distinct()
        else:
            routes = TestRoute.objects.values("start_city", "end_city").distinct()

        output = []
        if routes:
            output = list(routes)
        # Return queryset directly as JSON
        return Response(output)
    except Exception as e:
        return getNotFoundResponse(e)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "start_city": openapi.Schema(type=openapi.TYPE_STRING),
            "end_city": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "start_city",
            "end_city",
        ],
    ),
)
@api_view(["POST"])
def test_query(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        start_city = request.data.get("start_city")
        end_city = request.data.get("end_city")
        
        route = TestRoute.objects.get(start_city=start_city, end_city=end_city)
        serializer = TestRouteSerializer(route)
        return Response(serializer.data)
    except Exception as e:
        try:
            route = TestRoute.objects.get(start_city=end_city, end_city=start_city)            
            serializer = TestRouteSerializer(route)
            return Response(serializer.data)
        except Exception as e:
            return getNotFoundResponse(e)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "cities": openapi.Schema(type=openapi.TYPE_STRING),
            "battery_capacity": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "cities",
        ],
    ),
)
@api_view(["POST"])
def test_new(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        # Query all Test objects
        testing_factory = TestingFactory(request.data)
        result = testing_factory.run_tests()

        return Response(result)
    except Exception as e:
        return getNotFoundResponse(e)
