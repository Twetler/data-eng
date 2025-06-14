import os

from dotenv import load_dotenv
from src.utils import load_config_yaml


# Get environment variables
load_dotenv()
FOURSQUARE_KEY = os.getenv("FOURSQUARE_API_KEY")

# Get config
config = load_config_yaml("config.yaml")




