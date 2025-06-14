import requests
import json


def fetch_places_api(
        lat: float,
        long: float, 
        categories: list[str] = [],

    ):
    """
        Fetch places from Foursquare Places API by lat, long, and categories.

        See: https://docs.foursquare.com/developer/reference/place-search
    """
    
    base_url = "https://api.foursquare.com/v3/places/search"
    response = requests.get(base_url)
    # Status check
    if response.status_code == 200:
        return json.loads(response)
    else:
        response.raise_for_status()