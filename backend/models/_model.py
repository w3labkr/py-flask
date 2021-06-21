# Miscellaneous operating system interfaces
import os

# Basic date and time types
from datetime import date, datetime, timedelta

# The fundamental package for scientific computing with Python.
import numpy as np

# Flexible and powerful data analysis / manipulation library for Python, providing labeled data structures similar to R data.frame objects, statistical functions, and much more
import pandas as pd

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()


def constructor(request):

    obj = {'iserror': False, 'errmsg': '', 'dataset': {}}

    if (not request.form):
        return obj

    # dataframe
    df = pd.DataFrame(columns=['A', 'B'], index=np.arange(1))

    try:
        pass
    except Exception as e:
        obj.update({'iserror': True, 'errmsg': e})

    return obj
