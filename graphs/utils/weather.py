import requests
from typing import List, Tuple

API_URL = "https://api.open-meteo.com/v1/forecast?"


def Request_weather(lat, lon) -> List[dict]:

    url = f"{API_URL}latitude={lat}&longitude={lon}&current=temperature_2m"
    response = requests.get(url)
    if response.status_code == 200:
        temp = response.json()["current"]["temperature_2m"]
        return {"lat": lat, "lon": lon, "temperature": temp}

    return
