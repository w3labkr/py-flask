# Miscellaneous operating system interfaces
import os

# A light weight extension of the default python dict object. This allows for the use of key names as object attributes.
from dotted_dict import DottedDict

# The Python micro framework for building web applications.
from flask import Blueprint, session, redirect, url_for, escape, flash
from flask import request, Response, make_response, render_template, send_from_directory

# Import the application's modules and packages.
from modules.os import get_app_dir
from modules.flask import get_render_template_path, get_metadata
from modules.importlib import import_model
from modules.session import make_session, is_session
from packages.openweathermap import openweathermap

# Set the absolute directory path.
appdir = get_app_dir()


def constructor(settings):
    filename = os.path.splitext(os.path.basename(__file__))[0]
    router = Blueprint(filename, __name__)

    # Such a function is executed before the first request to the application.
    @router.before_app_first_request
    def before_app_first_request_func():
      pass

    # Such a function is executed before each request, even if outside of a blueprint.
    @router.before_app_request
    def before_app_request_func():
      pass
    
    # This function is only executed before each request that is handled by a function of that blueprint.
    @router.before_request
    def before_request_func():
        # Create a new session or clear the session on timeout.
        make_session(username='anonymous')

        # Force a redirect after the session is cleared.
        if not is_session():
            return redirect(request.url)

    # This function is only executed after each request that is handled by a function of that blueprint.
    @router.after_request
    def after_request_func(response):
        return response

    # This function is only executed when tearing down requests handled by a function of that blueprint. Teardown request functions are executed when the request context is popped, even when no actual request was performed.
    @router.teardown_request
    def teardown_request_func(exception):
        pass

    @router.route('/<username>/<uuid>/<filename>', methods=['GET'])
    def anonymous(username, uuid, filename):
        basepath = os.path.join(appdir.storage, username, uuid)
        return send_from_directory(basepath, filename)

    @router.route('/<username>/<filename>', methods=['GET'])
    def username(username, filename):
        basepath = os.path.join(appdir.storage, username)
        return send_from_directory(basepath, filename)

    return router
