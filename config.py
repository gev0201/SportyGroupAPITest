import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = "https://api.aviationstack.com/v1"
    API_KEY = os.getenv("AVIATIONSTACK_API_KEY", "")
    DEFAULT_LIMIT = 100
    DEFAULT_OFFSET = 0
    
    ENDPOINTS = {
        "flights": "/flights",
        "airports": "/airports",
        "airlines": "/airlines",
        "airplanes": "/airplanes",
        "aircraft_types": "/aircraft_types",
        "countries": "/countries",
    }
