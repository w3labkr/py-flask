# Miscellaneous operating system interfaces
import os

# Mathematical functions
import math

# The fundamental package for scientific computing with Python.
import numpy as np

# Flexible and powerful data analysis / manipulation library for Python, providing labeled data structures similar to R data.frame objects, statistical functions, and much more
import pandas as pd

# Basic date and time types
from datetime import datetime

# A simple, yet elegant HTTP library.
import requests

# Python HTTP library with thread-safe connection pooling, file post support, user friendly, and more.
from urllib import parse

# Beautiful Soup is a Python library for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()

# Get API Key
API_PATH = os.path.join(appdir.configs, 'openapirestapikey.txt')
with open(API_PATH, 'r') as f:
    API_KEY = f.read().strip()

# Set the absolute directory path.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_PATH = os.path.join(BASE_DIR, 'tmp')


def main(request):

    basename = os.path.basename(request.get('endpoint'))
    endpoint = request.get('endpoint') + '?ServiceKey=' + API_KEY

    params = {
        'pageNo': 1,
        'numOfRows': 10,
        'startCreateDt': '20200410',
        'endCreateDt': '20200410',
    }

    for k, v in request.items():
        if k == 'endpoint':
            continue
        params.update({k: v})

    response = requests.get(endpoint, params=params)
    soup = BeautifulSoup(response.text, 'xml')
    data = []

    # paging
    paging = {
        'num_of_rows': int(soup.select_one('numOfRows').get_text(strip=True)),
        'total_count': int(soup.select_one('totalCount').get_text(strip=True)),
    }
    paging.update({ 'total_page': math.ceil(paging.get('total_count') / paging.get('num_of_rows')) })

    # period
    start_strptime = datetime.strptime(params.get('startCreateDt'), '%Y%m%d')
    end_strptime = datetime.strptime(params.get('endCreateDt'), '%Y%m%d')
    periods_strptime = pd.date_range(start_strptime, end_strptime, freq='M').notna().sum() + 1
    periods = pd.date_range(start_strptime, periods=periods_strptime, freq='M')

    for period in periods:
        try:
            monthly = []

            start_strftime = datetime.strptime(params.get('startCreateDt'), '%Y%m%d').strftime('%Y%m')
            end_strftime = datetime.strptime(params.get('endCreateDt'), '%Y%m%d').strftime('%Y%m')
            period_strftime = period.strftime('%Y%m')

            if start_strftime == period_strftime:
                start_date = params.get('startCreateDt')
            else:
                start_date = period_strftime + '01'

            if end_strftime == period_strftime:
                end_date = params.get('endCreateDt')
            else:
                end_date = period.strftime('%Y%m%d')

            params.update({'startCreateDt': start_date})
            params.update({'endCreateDt': end_date})

            for page_no in np.arange(1, paging.get('total_page')+1):
                try:
                    params.update({'pageNo': page_no})

                    r = requests.get(endpoint, params=params)

                    # parsing
                    soup = BeautifulSoup(r.text, 'xml')
                    item = soup.select('item')

                    for row in item:
                        daily = {}
                        for col in row:
                            daily.update({col.name: col.get_text(strip=True)})
                        monthly.append(daily)
                        data.append(daily)

                except Exception as e:
                    print(page_no, e)

        except Exception as e:
            print(period, e)

    # dataframe
    df = pd.DataFrame(data)

    return df.to_json(orient='columns', force_ascii=False)


if __name__ == '__main__':
    main()
