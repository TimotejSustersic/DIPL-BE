import requests
from typing import List, Tuple

API_URL = "https://api.open-elevation.com/api/v1/lookup"

# coords = osrm_response.json()["routes"][0]["geometry"]["coordinates"][::5]
def Request_elevation(coords) -> List[dict]:

    payload = {"locations": [{"latitude": lat, "longitude": lon} for lon, lat in coords]}

    elev_response = requests.post(API_URL, json=payload)

    if elev_response.status_code != 200:
        return []

    elevations = [r["elevation"] for r in elev_response.json()["results"]]

    # Combine
    return [{"lon": lon, "lat": lat, "elevation": elev} for (lon, lat), elev in zip(coords, elevations)]
