from datetime import datetime
import requests

from graphs.utils.util import Coordinate

API_URL = "https://api.open-meteo.com/v1/forecast"


def Request_weather(coord) -> float:

    parsed_coord = Coordinate(coord)

    params = {
        "latitude": parsed_coord.latitude,
        "longitude": parsed_coord.longitude,
        "hourly": "temperature_2m",  # Join variables with commas
        "timezone": "Europe/Ljubljana",  # Slovenia timezone
        "forecast_days": 1,
    }
    response = requests.get(API_URL, params).json()

    hourly = response.get("hourly", {})
    temperature_2m = hourly.get("temperature_2m", [])

    now_hour = datetime.now().hour

    return temperature_2m[now_hour]

