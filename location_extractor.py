import os
import folium
from dotenv import load_dotenv
from src.utils import load_config_yaml

import logging
logging.basicConfig(level=logging.INFO)

# Get environment variables
load_dotenv()
FOURSQUARE_KEY: str = os.getenv("FOURSQUARE_API_KEY")
CONFIG: dict = load_config_yaml("config.yaml")

def mine_fsq_places():
    assert len(CONFIG['cities'] > 0), logging.warning("Check for missing cities polygons")
    first_city: dict = CONFIG['cities'][0]
    
    





    return True

mine_fsq_places()


