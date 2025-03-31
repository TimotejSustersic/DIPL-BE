from typing import Any
from geopy.geocoders import Nominatim


def Request_geopy() -> Nominatim:
    return Nominatim(user_agent="EVRoutingThesis")
