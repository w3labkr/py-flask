# Miscellaneous operating system interfaces
import os

# Basic date and time types
from datetime import date, datetime, timedelta

# Higher-order functions and operations on callable objects
from functools import wraps, update_wrapper

# The Python micro framework for building web applications.
from flask import make_response, request, abort

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()

# Remove Cache
# https://frhyme.github.io/python-lib/flask_matplotlib/
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


# Require Api Key
# https://stackoverflow.com/questions/14367991/flask-before-request-add-exception-for-specific-route
def require_api_key(api_method):
    @wraps(api_method)

    def check_api_key(*args, **kwargs):
        apikey = request.headers.get('ApiKey')
        if apikey and apikey == SECRET_KEY:
            return api_method(*args, **kwargs)
        else:
            abort(401)

    return check_api_key