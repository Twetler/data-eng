import requests
import numpy as np

import logging
logging.basicConfig(level=logging.INFO)

def fetch_places_api(
        save_path: str,
        api_key: str,
        polygon: list[tuple[float]],
        categories: list[str] = []
    ):
    """
        Fetch places from Foursquare Places API by lat, long, and categories.

        See: https://docs.foursquare.com/developer/reference/place-search
    """
    base_url = "https://api.foursquare.com/v3/places/search"
    header = {
        "accept" : "application/json",
        "Authorization" : api_key
    }
    # Params init
    params = {
        "polygon" : format_fsq_polygon(polygon),
        "categories" : categories
    }
    response = requests.get(base_url, headers = header, params = params)

    # Status check
    if response.status_code == 200:
        with open(save_path, "w") as f:
            f.write(response.text)
    else:
        response.raise_for_status()

def format_fsq_polygon(coords_list: list[list[np.float64]]):
    polygon_parts = [f"{point[0]},{point[1]}" for point in coords_list]
    
    if polygon_parts[0] != polygon_parts[-1]:
        polygon_parts.append(polygon_parts[0])  # Close
    
    return "~".join(polygon_parts)