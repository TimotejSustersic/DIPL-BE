import requests
from typing import List

from graphs.utils.util import Coordinate

API_URL = "https://api.open-elevation.com/api/v1/lookup"


# coords = osrm_response.json()["routes"][0]["geometry"]["coordinates"][::5]
def Request_elevation(coords) -> List[dict]:

    parsed_coordinates = (Coordinate(coord).to_tuple() for coord in coords)
    loc_str = "|".join(f"{lat},{lng}" for lat, lng in parsed_coordinates)
    
    try:
        response = requests.get(f"{API_URL}?locations={loc_str}", timeout=5)
        response.raise_for_status()
        x = response.json()["results"]
        return [res.get("elevation") for res in response.json()["results"]]
    except requests.RequestException as e:
        print(f"Elevation API error: {e}")
        return []