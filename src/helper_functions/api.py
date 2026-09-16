import requests
from config import (
    API
)

def get_api(path, params=None):
    response = requests.get(
        f"{API}/{path}",
        params=params
    )
    response.raise_for_status()
    return response.json()