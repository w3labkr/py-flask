# Miscellaneous operating system interfaces
import os

# Basic date and time types
from datetime import date, datetime, timedelta

# A light weight extension of the default python dict object. This allows for the use of key names as object attributes.
from dotted_dict import DottedDict

# The Python micro framework for building web applications.
# A common use for g is to manage resources during a request.
# https://flask.palletsprojects.com/en/1.1.x/appcontext/
from flask import Flask, session

# Simple integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.
from flask_wtf.csrf import CSRFProtect, CSRFError

# Adds APScheduler support to Flask
from flask_apscheduler import APScheduler

# Cross Origin Resource Sharing ( CORS ) support for Flask
from flask_cors import CORS

# Import the application's modules and packages.
from modules.os import get_app_dir
from modules.flask import auto_register_blueprint
from modules.session import destroy_session, destroy_session_immediately

# create and configure the app
app = Flask(__name__)
app.secret_key = 'secret'
app.permanent_session_lifetime = timedelta(days=31)

# The maximum upload file size limit is 10MB.
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Set up the jinja environment.
app.jinja_env.globals.update(
    zip=zip,
    enumerate=enumerate,
)

# To enable CSRF protection globally for a Flask app, register the CSRFProtect extension.
# https://flask-wtf.readthedocs.io/en/stable/csrf.html
csrf = CSRFProtect()
csrf.init_app(app)

# Resource specific CORS
#cors = CORS(app, resources={r"*": {"origins": "*"}})

# initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

# Set the absolute directory path.
appdir = get_app_dir()

# Setting global variables for use in blueprints.
settings = {
    'theme': 'none',
    'layout': 'content',
    'metadata': {'slug': '', 'current': '', 'parent': '', 'ancestor': ''},
    'navigation': {
        'primary': {'filename': 'navigation', 'title': ''},
        'secondary': {'filename': 'navigation', 'title': ''},
    },
    'sidebar': {
        'primary': {'filename': 'sidebar'},
        'secondary': {'filename': 'sidebar'},
    },
}
settings = DottedDict(settings)


# A list of functions that will be called at the beginning of the first request to this instance.
@app.before_first_request
def before_first_request_func():
    pass


# Registers a function to run before each request.
@app.before_request
def before_request_func():
    pass


# Register a function to be run after each request.
@app.after_request
def after_request_func(response):
    return response


# Register a function to be run at the end of each request, regardless of whether there was an exception or not. These functions are executed when the request context is popped, even if not an actual request was performed.
@app.teardown_request
def teardown_request_func(exception):
    pass


# Registers a function to be called when the application context ends. These functions are typically also called when the request context is popped.
@app.teardown_appcontext
def teardown_appcontext_func(exception):
    pass


# Automatically register the router.
# File names in the path directory are converted to URL slugs.
# Double underscores are used as URL slug separators, and single underscores are converted to hyphens
# and if the filename starts with an underscore, it is not rendered.
auto_register_blueprint(app, settings=settings, excludes=[])


# Register a function to handle errors by code or exception class.
@app.errorhandler(404)
def page_not_found(e):
    return e


# Register the scheduler job.
#scheduler.add_job(func=job1, trigger="interval", id='do_job1', seconds=3)
#scheduler.add_job(func=job2, trigger="cron", id='do_job2', hour='5', minute='0')
#scheduler.add_job(func=destroy_session, trigger="cron", id='do_destroy_session', hour='5', minute='0')
#scheduler.add_job(func=destroy_session_immediately, trigger="interval", id='do_destroy_session_immediately', seconds=3)


if __name__ == '__main__':
    app.run(debug=True)
