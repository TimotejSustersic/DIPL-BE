import json
from typing import Tuple


class Coordinate:

    def __init__(self, coord):
        try:
            self.latitude = coord.latitude
            self.longitude = coord.longitude
        except:
            self.latitude = coord.get("latitude", 0.0)
            self.longitude = coord.get("longitude", 0.0)

            if self.latitude == 0:
                self.latitude = coord.get("Latitude", 0.0)
                self.longitude = coord.get("Longitude", 0.0)

    def to_tuple(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)
    
    def to_string(self) -> str:
        # Serialize to JSON string
        return json.dumps({"latitude": self.latitude, "longitude": self.longitude})

def Parse_str_to_list(input_string: str) -> list[str]:
    if isinstance(input_string, str):
        return [item.strip() for item in input_string.split(",") if item.strip()]
    return input_string
