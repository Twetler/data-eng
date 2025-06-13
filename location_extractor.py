import os
import requests
from dotenv import load_dotenv


# Get environment variables
load_dotenv()
FOURSQUARE_KEY = os.getenv("FOURSQUARE_API_KEY")
