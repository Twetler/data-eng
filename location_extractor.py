import os
import numpy as np
from dotenv import load_dotenv
from src.utils import load_config_yaml, unpack_results, load_tmp_data, get_places_etl
from src.spatial import RectanglePolygonIterator
from src.api import fetch_places_api
from src.gcp import upload_blob
from pandas_gbq import to_gbq
from pandas import DataFrame


import logging
logging.basicConfig(level=logging.INFO)

# Get environment variables
load_dotenv()   
FOURSQUARE_KEY: str = os.getenv("FOURSQUARE_API_KEY")
CONFIG: dict = load_config_yaml("config.yaml")

# Produces the json files
def mine_fsq_places():
    first_city: dict = CONFIG['cities'][0]
    city_name: str = first_city['name'].lower()
    samples: list = list()
    batches_len: list[int] = list()
    for city in CONFIG['cities']:
        city_name: str = city['name'].lower()
        logging.info(f"Starting city: {city_name}")
        poly_idx: int = 0
        for poly in RectanglePolygonIterator(rect_points=city['rectangle_coords'], n_polygons=64):
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

# This sends data do Google Cloud
def run_tables(debug_mode: bool = True):
    logging.info("Starting location extractor...")
    if debug_mode: 
        logging.info("Debug Mode is ON, using /tmp existing files")
    else:
        mine_fsq_places()
    df: DataFrame  = load_tmp_data("tmp/")
    df = get_places_etl(df)
    to_gbq(df, CONFIG['raw_table_destination'], if_exists = 'append')

# Sends raw data to GCP Bucket which will be pulled by Databricks
def upload_raw():
    destination_bucket: str = os.getenv("GOOGLE_CLOUD_BUCKET")
    tmp_path: str = "tmp/"

    for _,_, files in os.walk(tmp_path):
        for file in files:
            if not os.path.isdir(file):
                logging.info(f"Sending {file} to bucket...")
                fullpath: str = os.path.join(tmp_path, file)
                city_name : str = fullpath.split("/")[-1].split("-")[0]
                bucket_destination: str = os.path.join(city_name, file)
                upload_blob(
                    bucket_name = destination_bucket,
                    source_file_name = fullpath,
                    destination_blob_name = bucket_destination
                )
    return True


#mine_fsq_places()

run_tables()

upload_raw()


    