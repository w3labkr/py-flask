# Miscellaneous operating system interfaces
import os

# The implementation of import
import importlib

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()


def import_module(filepath='', filename='', prefix='', suffix=''):
    abspath = os.path.join(filepath, prefix + filename + suffix)
    relpath = abspath.replace(appdir.root, '').strip('/')
    mdlpath = relpath.replace('/', '.')
    if os.path.isfile(abspath + '.py'):
        return importlib.import_module(mdlpath)
    return None


def import_model(filename='', prefix='', suffix=''):
    return import_module(filepath=appdir.models, filename=filename, prefix=prefix, suffix=suffix)
