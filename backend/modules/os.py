# Miscellaneous operating system interfaces
import os

# A light weight extension of the default python dict object. This allows for the use of key names as object attributes.
from dotted_dict import DottedDict


def get_absolute_directories(file=None, includes=()):
    if file is None:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    else:
        path = os.path.dirname(os.path.abspath(file))

    names = []
    for name in os.listdir(path):
        if not os.path.isdir(os.path.join(path, name)):
            continue
        if not name.startswith('_'):
            names.append(name)

    obj = {'root': path}
    for name in names:
        obj.update({name: os.path.join(path, name)})

    for arr in includes:
        arr = [path] + arr
        obj.update({arr[-1]: os.path.join(*arr)})

    return DottedDict(obj)


def get_absolute_directory(file=None):
    return os.path.dirname(os.path.abspath(__file__)) if file is None else os.path.dirname(os.path.abspath(file))


def get_app_dir():
    return get_absolute_directories(includes=(
        ['storage', 'anonymous'],
    ))


def get_latest_file(path, key=os.path.getctime):
    files = []
    for basename in os.listdir(path):
        basepath = os.path.join(path, basename)
        if not os.path.isfile(basepath):
            continue
        files.append(basepath)
    return max(files, key=key)


# https://stackoverflow.com/questions/44348067/modifying-os-stat-object
def get_stat(filepath):
    s = os.stat(filepath)
    d = dict(zip('mode ino dev nlink uid gid size atime mtime ctime'.split(), s))
    return d


def is_file(file):
    return True if file else False


def is_extensions(file, extensions=[]):
    filename, extension = os.path.splitext(file.filename)
    # setting the maxsplit parameter to 1, will return a list with 2 elements!
    extension = extension.rsplit('.', 1)[1].lower()
    return True if extension in extensions else False
