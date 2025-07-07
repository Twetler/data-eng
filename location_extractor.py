import os
import numpy as np
from dotenv import load_dotenv
from src.utils import load_config_yaml, unpack_results
from src.spatial import RectanglePolygonIterator
from src.api import fetch_places_api

import logging
logging.basicConfig(level=logging.INFO)

# Get environment variables
load_dotenv()   
FOURSQUARE_KEY: str = os.getenv("FOURSQUARE_API_KEY")
CONFIG: dict = load_config_yaml("config.yaml")

def mine_fsq_places():
    first_city: dict = CONFIG['cities'][0]
    city_name: str = first_city['name'].lower()
    poly_idx: int = 0
    samples: list = list()
    batches_len: list[int] = list()
    for poly in RectanglePolygonIterator(rect_points=first_city['rectangle_coords'], n_polygons=64):
        logging.info(f"Fetching Polygon : {poly_idx}")
        file_path: str = f"tmp/{city_name}-poly-{poly_idx}.json"
        fetch_places_api(file_path, FOURSQUARE_KEY, polygon = poly,
            fields = [
                "description", "website", "social_media", "hours", "hours_popular", "rating"
                , "price", "date_closed", "features", "venue_reality_bucket",
                "geocodes", "fsq_id", "name", "categories","location"
            ])
        results = unpack_results(file_path)

        len_batch = len(results)
        logging.info(f"Batch len: {len_batch}")

        batches_len.append(len_batch)
        if len(batches_len) > 2:
            mean = round(np.mean(batches_len), 3)
            logging.info(f"Length average: {mean}")

        samples.append(results)

        #upload_blob(BUCKET_NAME, file_path, destination_path)
        poly_idx += 1
    return True

mine_fsq_places()


