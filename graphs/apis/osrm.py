from typing import Any
import requests

API_URL = "http://router.project-osrm.org"


def Request_osrm(params) -> Any:
    url = f"{API_URL}{params}"
    return requests.get(url).json()
