# Miscellaneous operating system interfaces
import os

# JSON encoder and decoder
import json

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

    data = {
        'iserror': False, 'errmsg': '',
    }

    if not request:
        return data

    # dataframe
    df = pd.DataFrame(columns=['A', 'B'], index=np.arange(1))

    try:

        df = pd.read_csv(os.path.join(
            appdir.datasets, '서울시_시군구_별__공원수_인구수_2017_2019.csv'))

        data.update({'html': df})

    except Exception as e:
        data.update({'iserror': True, 'errmsg': e})

    return data
