# Miscellaneous operating system interfaces
import os

# The fundamental package for scientific computing with Python.
import numpy as np

# Flexible and powerful data analysis / manipulation library for Python, providing labeled data structures similar to R data.frame objects, statistical functions, and much more
import pandas as pd

# A simple, yet elegant HTTP library.
import requests

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()

# Get API Key
API_PATH = os.path.join(appdir.configs, 'openweathermapapikey.txt')
with open(API_PATH, 'r') as f:
    API_KEY = f.read().strip()

def forecast(**kwargs):
    endpoint = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': 37.5683,
        'lon': 126.9778,
        'units': 'metric',
        'lang': 'kr',
        'appid': API_KEY
    }
    for k, v in kwargs.items():
        params.update({k: v})

    return requests.get(endpoint, params=params).json()
