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

# Import a custom module file.
import packages.openapi as openapi

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()


def constructor(request):

    data = {
        'iserror': False, 'errmsg': '',
        'age': {'cols': [], 'rows': []},
        'gender': {'cols': [], 'rows': []},
    }

    if not request:
        return data

    # dataframe
    df = pd.DataFrame(columns=['A', 'B'], index=np.arange(1))

    try:
        df = pd.DataFrame(json.loads(openapi.main(request), encoding='utf-8'))

        df.rename(columns={
            'confCase': '확진자',
            'confCaseRate': '확진률',
            'createDt': '등록일시분초',
            'criticalRate': '치명률',
            'death': '사망자',
            'deathRate': '사망률',
            'gubun': '구분',  # 구분(성별, 연령별)
            'seq': '게시글번호(확진자 성별,연령별 고유값)',
            'updateDt': '수정일시분초',
        }, inplace=True)

        # Change the default format of the data series.
        df['기준일시'] = df['등록일시분초'].replace('\.\d+$', '', regex=True)
        df['기준일시'] = pd.to_datetime(df['기준일시'], format='%Y-%m-%d %H:%M:%S')
        df['기준일시'] = df['기준일시'].dt.strftime('%Y-%m-%d')

        nans = ['확진자', '확진률', '치명률', '사망자', '사망률']

        for nan in nans:
            try:
                df[nan] = df[nan].replace('-', 0, regex=True)
                # TypeError: Object of type int64 is not JSON serializable
                # df[nan] = pd.to_numeric(df[nan])
            except Exception as e:
                data.update({'iserror': True, 'errmsg': e})

        # Remove duplicate data
        denies = []
        for k, v in df[['기준일시', '구분']].value_counts().items():
            if int(v) == 1:
                continue
            ids = df[(df['기준일시'] == k[0]) & (df['구분'] == k[1])].index
            denies.extend(list(filter(lambda x: x != min(ids), ids)))

        df.drop(denies, axis=0, inplace=True)
        df.index = np.arange(0, len(df))

        # print dataframe
        df = df[['기준일시', '구분', '확진자', '확진률', '치명률', '사망자', '사망률']]

        # head
        cols = []

        for column in df.columns:
            cols.append({'title': column})

        data['age'].update({'cols': cols})
        data['gender'].update({'cols': cols})

        # body - age
        rows = []

        for i in df.reset_index().query("구분 not in ['남성', '여성']").index:
            row = df.iloc[i].to_list()
            rows.append(row)

        data['age'].update({'rows': rows})

        # body - gender
        rows = []

        for i in df.reset_index().query("구분 in ['남성', '여성']").index:
            row = df.iloc[i].to_list()
            rows.append(row)

        data['gender'].update({'rows': rows})

    except Exception as e:
        data.update({'iserror': True, 'errmsg': e})

    return data
