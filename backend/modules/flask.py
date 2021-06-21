# Miscellaneous operating system interfaces
import os

# A light weight extension of the default python dict object. This allows for the use of key names as object attributes.
from dotted_dict import DottedDict

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()


def get_render_template_path(slug='', theme='none', rel=''):
    slug = 'index' if (slug == '') or (slug == '/') else slug
    basedir = os.path.join(theme.strip('/'), rel.strip('/'), slug.strip('/'))
    basepath = os.path.join(appdir.templates, basedir)
    for ext in ['.html', '.jinja', '.jinja2']:
        if os.path.isfile(basepath + ext):
            return basedir + ext
    return ''


def get_metadata(slug=''):
    names = ['current', 'parent', 'ancestor']
    values = slug.strip('/').split('/')
    obj = dict(zip(names, reversed(values)))
    obj.update({'slug': slug})
    return DottedDict(obj)


def auto_register_blueprint(router, settings={}, excludes=[]):
    import importlib
    basedir = appdir.routes
    for basename in os.listdir(basedir):
        try:
            basepath = os.path.join(basedir, basename)
            if (not os.path.isfile(basepath)):
                continue

            filename, extension = os.path.splitext(basename)

            if (filename.startswith('_')) \
                    or (extension != '.py') \
                    or (filename in excludes):
                continue

            # Import a module. Because this function is meant for use by the Python interpreter and not for general use it is better to use importlib.import_module() to programmatically import a module.
            # route = __import__('routes.{}'.format(filename))
            route = importlib.import_module('routes.{}'.format(filename))

            # Register Blueprints
            url_prefix = '/' if filename == 'index' else '/{}/'.format(
                filename.replace('__', '/'))
            url_prefix = url_prefix.replace('_', '-')

            router.register_blueprint(
                route.constructor(settings), url_prefix=url_prefix)
        except Exception as e:
            pass


def subprocess_exec(filename):
    import subprocess
    basedir = appdir.executes
    basepath = os.path.join(basedir, filename)
    basename = os.path.basename(basepath)
    if not os.path.isfile(basepath):
        return
    if basename.startswith('_'):
        return
    try:
        filename = os.path.splitext(basename)[0]
        subprocess.Popen(['python', basepath,
                          '--basepath="{}"'.format(basepath),
                          '--filename="{}"'.format(filename),
                          '--appdir="{}"'.format(appdir)
                          ])
    except Exception as e:
        pass


def subprocess_execs(excludes=[]):
    import subprocess
    basedir = appdir.executes
    for basename in os.listdir(basedir):
        try:
            basepath = os.path.join(basedir, basename)
            if (not os.path.isfile(basepath)):
                continue
            if (basename.startswith('_')) or (basename in excludes):
                continue
            filename = os.path.splitext(basename)[0]
            subprocess.Popen(['python', basepath,
                              '--basepath="{}"'.format(basepath),
                              '--filename="{}"'.format(filename),
                              '--appdir="{}"'.format(appdir)
                              ])
        except Exception as e:
            pass
