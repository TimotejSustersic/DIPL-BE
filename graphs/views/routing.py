from graphs.models.user import Route
from graphs.utils.routing import RoutingFactory
from graphs.views.utils import *

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "vehicle_id": openapi.Schema(type=openapi.TYPE_STRING),
            "start_city": openapi.Schema(type=openapi.TYPE_STRING),
            "end_city": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "vehicle_id",
            "start_city",
            "end_city",
        ],
    ),
)
@api_view(["POST"])
def routing_new(request):
    if not isPOST(request):
        return getNotallowedResponse()

    try:
        # Query all Test objects
        route = RoutingFactory(request.data)
        result = route.startRoute()
        return Response(result)
    except Exception as e:
        return getNotFoundResponse(e)


########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
)
@api_view(["POST"])
def routing_query(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    name = request.data.get("name")

    try:
        routes = Route.objects.all()[::-1]
        
        result = [
            {
                "vehicle_name": r.vehicle.name,
                "current_battery": r.vehicle.current_battery,
                "start_city": r.start_city,
                "end_city": r.end_city,
                "distance": r.distance,
                "waypoints": r.waypoints,
            }
            for r in routes
        ]
        return Response(result)
    except Exception as e:
        return getNotFoundResponse(e)
