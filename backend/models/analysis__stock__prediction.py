# Miscellaneous operating system interfaces
import os

# Basic date and time types
from datetime import date, datetime, timedelta

# The fundamental package for scientific computing with Python.
import numpy as np

# Flexible and powerful data analysis / manipulation library for Python, providing labeled data structures similar to R data.frame objects, statistical functions, and much more
import pandas as pd

# Extract data from a wide range of Internet sources into a pandas DataFrame.
import pandas_datareader as pdr

# Tool for producing high quality forecasts for time series data that has multiple seasonality with linear or non-linear growth.
from fbprophet import Prophet

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()


def constructor(request):

    data = {
        'iserror': False, 'errmsg': '',
        'Date':[], 'Close':[],
        'ds':[], 'trend':[],
    }

    if not request:
        return data

    # options
    obj = {
        'stockmarket': 'kospi',
        'stockcode': '095570.KS',
        'kospicode': '095570',
        'kosdaqcode': '060310',
        'learningday': 1 * 365,
        'forecastday': 5
    }

    for k, v in request.items():
        obj.update({k: v})

    if obj.get('stockmarket') in 'kospi':
        obj.update({'stockcode': obj.get('kospicode') + '.KS'})
    else:
        obj.update({'stockcode': obj.get('kosdaqcode') + '.KQ'})

    obj.update({'learningday': int(obj.get('learningday')) * 365})
    obj.update({'forecastday': int(obj.get('forecastday'))})

    # datetime
    today = datetime.now()
    start_date = today - timedelta(days=obj.get('learningday'))
    end_date = today - timedelta(days=1)

    # dataframe
    df = pd.DataFrame(columns=['Date', 'Close'], index=np.arange(1))

    try:
        df = pdr.DataReader(obj.get('stockcode'), data_source='yahoo',
                            start=start_date, end=end_date)
        df.index = df.index.strftime('%Y-%m-%d')
        df.reset_index(inplace=True)

        for column in df.columns:
            try:
                data.update({column: df[column].to_list()})
            except Exception as e:
                data.update({'iserror': True, 'errmsg': e})
                data.update({column: []})
    
    # KeyError: 'Date'
    except Exception as e:
        data.update({'iserror': True, 'errmsg': e})
        data.update({'Date':[], 'Close':[]})

    # fbprophet
    try:
        df1 = pd.DataFrame({'ds': df.get('Date'), 'y': df.get('Close')})
        m = Prophet(daily_seasonality=True)

        m.fit(df1)
        future = m.make_future_dataframe(periods=obj.get('forecastday'))

        df2 = m.predict(future)
        df2['ds'] = df2['ds'].dt.strftime('%Y-%m-%d')

        data.update({'ds': df2['ds'].to_list()})
        data.update({'trend': df2['trend'].to_list()})

    # Dataframe has less than 2 non-NaN rows.
    except Exception as e:
        data.update({'iserror': True, 'errmsg': e})
        data.update({'ds': [], 'trend': []})

    return data
