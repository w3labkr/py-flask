# Miscellaneous operating system interfaces
import os

# JSON encoder and decoder
import json

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()

# you cannot use json.loads on file object
with open(os.path.join(appdir.configs, 'db.json'), 'r') as f:
    config = json.load(f)
    
config