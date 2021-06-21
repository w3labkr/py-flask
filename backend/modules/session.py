# Miscellaneous operating system interfaces
import os

# High-level file operations
import shutil

# Basic date and time types
from datetime import date, datetime, timedelta

# The Python micro framework for building web applications.
from flask import request, session

# Import the application's modules and packages.
from modules.os import get_app_dir
from modules.request import get_ip, get_user_agent

# Set the absolute directory path.
appdir = get_app_dir()


def is_session(name='username'):
    return True if name in session else False


def make_session(username='anonymous', anonymous_seconds=1800, username_seconds=-1):
    if not is_session():
        create_session(username=username)
    else:
        remove_session(anonymous_seconds=anonymous_seconds,
                       username_seconds=username_seconds)


def create_session(username='anonymous'):
    # UUID objects according to RFC 4122
    from uuid import uuid4

    # flask sessions expire once you close the browser unless you have a permanent session.
    session.permanent = True

    session['lifetime'] = datetime.now()
    session['username'] = username
    session['uuid'] = str(uuid4())
    session['ip'] = get_ip()
    session['user_agent'] = get_user_agent()

    if session.get('username') == 'anonymous':
        create_anonymous_session()
    else:
        create_storage_session()


def create_storage_session():
    basedir = os.path.join(appdir.storage, session.get('username'))
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    create_temporary_session(basedir)


def create_anonymous_session():
    basedir = os.path.join(appdir.anonymous, session.get('uuid'))
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    create_temporary_session(basedir)


def create_temporary_session(basedir):
    for dirname in ['uploads']:
        basepath = os.path.join(basedir, dirname)
        if not os.path.exists(basepath):
            os.makedirs(basepath)


# Session has expired after 30 minutes, you have been logged out.
# https://stackoverflow.com/questions/36707367/call-a-function-when-flask-session-expires
def remove_session(anonymous_seconds=1800, username_seconds=-1):
    if session.get('username') == 'anonymous':
        remove_anonymous_session(seconds=anonymous_seconds)
    else:
        remove_storage_session(seconds=username_seconds)


def remove_storage_session(seconds=-1):
    basedir = os.path.join(appdir.storage, session.get('username'))
    holdingtime = datetime.now() - session.get('lifetime')
    if seconds != -1:
        if holdingtime.seconds < seconds:
            return
        if os.path.exists(basedir):
            if os.path.basename(basedir) == 'anonymous':
                return
            shutil.rmtree(basedir)
        session.clear()


def remove_anonymous_session(seconds=1800):
    basedir = os.path.join(appdir.anonymous, session.get('uuid'))
    holdingtime = datetime.now() - session.get('lifetime')
    if seconds != -1:
        if holdingtime.seconds < seconds:
            return
        if os.path.exists(basedir):
            shutil.rmtree(basedir)
        session.clear()


# Scheduler
# func must be a callable or a textual reference to one.
def destroy_session():
    destroy_storage_session(seconds=-1)
    destroy_anonymous_session(seconds=1800)


def destroy_session_immediately():
    destroy_storage_session(seconds=1)
    destroy_anonymous_session(seconds=1)


def destroy_storage_session(seconds=-1):
    basedir = appdir.storage
    holdingtime = datetime.now() - timedelta(seconds=seconds)
    if seconds != -1:
        for basename in os.listdir(basedir):
            basepath = os.path.join(basedir, basename)
            if not os.path.isdir(basepath):
                continue
            if basename == 'anonymous':
                continue
            ctime = datetime.fromtimestamp(os.path.getctime(basepath))
            if ctime < holdingtime:
                shutil.rmtree(basepath)


def destroy_anonymous_session(seconds=1800):
    basedir = appdir.anonymous
    holdingtime = datetime.now() - timedelta(seconds=seconds)
    if seconds != -1:
        for basename in os.listdir(basedir):
            basepath = os.path.join(basedir, basename)
            if not os.path.isdir(basepath):
                continue
            ctime = datetime.fromtimestamp(os.path.getctime(basepath))
            if ctime < holdingtime:
                shutil.rmtree(basepath)
