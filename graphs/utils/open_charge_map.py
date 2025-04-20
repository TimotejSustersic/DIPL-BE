from typing import Any, Dict, List
import requests

API_KEY = "b6bbeeea-493a-4e01-a12b-4bfdf86a2fca"
API_URL = f"https://api.openchargemap.io/v3/poi/?key={API_KEY}"

def find_nearest_charging_stations(lat: float, lon: float, max_distance_km: float = 50, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Query the Open Charge Map API to find nearest charging stations within max_distance_km from the given lat, lon.
    Returns a list of charging stations with their details.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "distance": max_distance_km,
        "distanceunit": "KM",
        "maxresults": max_results,
        "compact": True,
        "verbose": False,
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []
