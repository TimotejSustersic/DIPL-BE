from typing import Any
import requests

API_KEY = "b6bbeeea-493a-4e01-a12b-4bfdf86a2fca"

API_URL = f"https://api.openchargemap.io/v3/poi/?key={API_KEY}"


def Request_open_charge_map() -> Any:
    url = f"{API_URL}&countrycode=SI&maxresults=15"
    return requests.get(url).json()
