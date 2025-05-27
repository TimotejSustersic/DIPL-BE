from itertools import combinations
from graphs.models.test import Test, TestRoute, TestRouteSerializer
from graphs.tests.TestingFactory import TestingFactory
from graphs.views.utils import *

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "get_empty": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(["POST"])
def tests_query(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        output = list(Test.objects.values("name", "id", "cities", "battery_capacity"))

        if bool(request.data.get("get_empty")):
            from django.db.models import Q
            for i in range(len(output)):
                test_cities = output[i]["cities"]
                # Generate all possible city pairs (combinations)
                city_pairs = list(combinations(test_cities, 2))

                # Build Q objects for filtering TestRoute by city pairs in both directions
                query = Q()
                for start_city, end_city in city_pairs:
                    query |= Q(start_city=start_city, end_city=end_city) | Q(start_city=end_city, end_city=start_city)

                # Query TestRoute for these city pairs
                routes = TestRoute.objects.filter(query)

                # Collect and flatten all my_accumulated_empty_battery arrays from these routes
                empty_battery_locations = []
                for route in routes:
                    empty_battery_locations.extend(route.my_accumulated_empty_battery)

                # Add the combined array to the test output
                output[i]["my_accumulated_empty_battery"] = empty_battery_locations

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
            "search": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(["POST"])
def test_items_query(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        test_id = request.data.get("test_id")
        search = request.data.get("search", "").strip().lower()

        # Retrieve the Test instance
        test_instance = Test.objects.get(id=test_id)
        cities = test_instance.cities

        # Generate all possible city pairs (combinations)
        city_pairs = list(combinations(cities, 2))

        # Build Q objects for filtering TestRoute by city pairs in both directions
        from django.db.models import Q

        query = Q()
        for start_city, end_city in city_pairs:
            query |= Q(start_city=start_city, end_city=end_city) | Q(start_city=end_city, end_city=start_city)

        routes = TestRoute.objects.filter(query)

        # If search string is given, filter routes by partial match on start_city or end_city
        if search:
            routes = routes.filter(Q(start_city__icontains=search) | Q(end_city__icontains=search))

        serializer = TestRouteSerializer(routes, many=True)
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
