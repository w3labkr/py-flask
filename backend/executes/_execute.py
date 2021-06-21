#!/usr/bin/python

# System-specific parameters and functions
import sys

# JSON encoder and decoder
import json

# A compendium of commonly-used regular expressions.
import re

# A light weight extension of the default python dict object. This allows for the use of key names as object attributes.
from dotted_dict import DottedDict

# Convert the argument to an object.
def get_arguments():
    obj = {}
    for arg in sys.argv:
        if not arg.startswith('--'):
            continue
        arr = arg.split('=')
        k = re.sub('^--', '', arr[0])
        v = re.sub('^\"|\"$', '', arr[1])
        if v.startswith('{'):
            v = re.sub("\'", '\"', v)
            v = json.loads(v)
        obj.update({k: v})
    obj = dotted_dict(obj)
    return obj
args = get_arguments()


def main():
    print('main')


main()
