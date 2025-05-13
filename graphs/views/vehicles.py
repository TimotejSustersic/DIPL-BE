from graphs.models.user import Vehicle
from graphs.utils.vehicle import ClassVehicle
from graphs.views.utils import *

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "battery_capacity": openapi.Schema(type=openapi.TYPE_STRING),
            "consumption_rate": openapi.Schema(type=openapi.TYPE_STRING),
            "year_of_manufacture": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "name",
            "battery_capacity",
            "consumption_rate",
            "year_of_manufacture",
        ],
    ),
)
@api_view(["POST"])
def new_vehicle(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    name = request.data.get("name")
    year_of_manufacture = request.data.get("year_of_manufacture")
    battery_capacity = request.data.get("battery_capacity")
    consumption_rate = request.data.get("consumption_rate")

    if name is None or battery_capacity is None or consumption_rate is None or year_of_manufacture is None:
        return getErrorResponse(ERR_MESS_PARAMS)
    try:
        # Query all Test objects
        vehicle = Vehicle(
            name=name,
            year_of_manufacture=int(year_of_manufacture),
            battery_capacity=float(battery_capacity),
            consumption_rate=float(consumption_rate) , # kWh/km
        )
        vehicle.save()

        return getPOSTResponse({"id": vehicle.id, "name": vehicle.name})
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
def vehicle_query(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    name = request.data.get("name")

    try:

        vehicles = Vehicle.objects.all()
        
        result = [
            {
                "id": v.id,
                "name": v.name,
                "year_of_manufacture": v.year_of_manufacture,
                "battery_capacity": v.battery_capacity,
                "consumption_rate": v.consumption_rate,
            }
            for v in vehicles
        ]
        return Response(result)
    except Exception as e:
        return getNotFoundResponse(e)

########################################
########################################


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "vehicle_id": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=[
            "vehicle_id",
        ],
    ),
)
@api_view(["POST"])
def vehicle_discard(request: Request) -> Response:
    if not isPOST(request):
        return getNotallowedResponse()

    vehicle_id = request.data.get("vehicle_id")

    if vehicle_id is None:
        return getErrorResponse(ERR_MESS_PARAMS)
    try:
        vehicle = Vehicle.objects.get(id=int(vehicle_id))

        vehicle.delete()

        return getPOSTResponse({"message": f"Vehicle {vehicle_id} discarded successfully"})
    except Exception as e:
        return getNotFoundResponse(e)
