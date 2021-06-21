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
        'cols': [], 'rows': []
    }

    if not request:
        return data

    # dataframe
    df = pd.DataFrame(columns=['A', 'B'], index=np.arange(1))

    try:
        df = pd.DataFrame(json.loads(openapi.main(request), encoding='utf-8'))

        df.rename(columns={
            'accDefRate': '누적 환진률',
            'accExamCnt': '누적 검사 수',
            'accExamCompCnt': '누적 검사 완료 수',
            'careCnt': '치료중 환자 수',
            'clearCnt': '격리해제 수',
            'createDt': '등록일시분초',
            'deathCnt': '사망자 수',
            'decideCnt': '확진자 수',
            'examCnt': '검사진행 수',
            'resutlNegCnt': '결과 음성 수',
            'seq': '게시글번호(감염현황 고유값)',
            'stateDt': '기준일',
            'stateTime': '기준시간',
            'updateDt': '수정일시분초',
        }, inplace=True)

        # Change the default format of the data series.
        df['등록일시분초'] = df['등록일시분초'].replace('\.\d+$', '', regex=True)
        df['등록일시분초'] = pd.to_datetime(df['등록일시분초'], format='%Y-%m-%d %H:%M:%S')
        df['등록일시분초'] = df['등록일시분초'].dt.strftime('%Y-%m-%d %H:%M:%S')

        df['기준일'] = pd.to_datetime(df['기준일'], format='%Y%m%d')
        df['기준일'] = df['기준일'].dt.strftime('%Y-%m-%d')

        nans = ['누적 환진률', '누적 검사 수', '누적 검사 완료 수', '치료중 환자 수', '격리해제 수',
                '사망자 수', '확진자 수', '검사진행 수', '결과 음성 수', '게시글번호(감염현황 고유값)']

        for nan in nans:
            try:
                df[nan] = df[nan].replace('-', 0, regex=True)
                # TypeError: Object of type int64 is not JSON serializable
                # df[nan] = pd.to_numeric(df[nan])
            except Exception as e:
                data.update({'iserror': True, 'errmsg': e})

        # Remove duplicate data
        denies = []
        for k, v in df['기준일'].value_counts().items():
            if int(v) == 1:
                continue
            ids = df[df['기준일'] == k].index
            denies.extend(list(filter(lambda x: x != min(ids), ids)))

        df.drop(denies, axis=0, inplace=True)
        df.index = np.arange(0, len(df))

        # print dataframe
        df = df[['기준일', '확진자 수', '사망자 수', '누적 환진률', '누적 검사 수',
                 '누적 검사 완료 수', '치료중 환자 수', '격리해제 수', '검사진행 수', '결과 음성 수']]

        # head
        cols = []

        for column in df.columns:
            cols.append({'title': column})

        data.update({'cols': cols})

        # body
        rows = []

        for i in df.reset_index().index:
            row = df.iloc[i].to_list()
            rows.append(row)

        data.update({'rows': rows})

    except Exception as e:
        data.update({'iserror': True, 'errmsg': e})

    return data
