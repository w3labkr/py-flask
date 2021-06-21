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
            'seq': '게시글번호(국내 시도별 발생현황 고유값)',
            'createDt': '등록일시분초',
            'deathCnt': '사망자 수',
            'gubun': '시도명',  # 시도명(한글)
            'gubunCn': '시도명(중국어)',
            'gubunEn': '시도명(영어)',
            'incDec': '전일대비 증감 수',
            'isolClearCnt': '격리 해제 수',
            'qurRate': '10만명당 발생률',
            'stdDay': '기준일시',
            'updateDt': '수정일시분초',
            'defCnt': '확진자 수',
            'isolIngCnt': '격리중 환자수',
            'localOccCnt': '지역발생 수',
            'overFlowCnt': '해외유입 수',
        }, inplace=True)

        # Change the default format of the data series.
        df['기준일시'] = df['등록일시분초'].replace('\.\d+$', '', regex=True)
        df['기준일시'] = pd.to_datetime(df['기준일시'], format='%Y-%m-%d %H:%M:%S')
        df['기준일시'] = df['기준일시'].dt.strftime('%Y-%m-%d')

        nans = ['게시글번호(국내 시도별 발생현황 고유값)', '사망자 수', '전일대비 증감 수', '격리 해제 수',
                '10만명당 발생률', '확진자 수', '격리중 환자수', '지역발생 수', '해외유입 수']

        for nan in nans:
            try:
                df[nan] = df[nan].replace('-', 0, regex=True)
                # TypeError: Object of type int64 is not JSON serializable
                # df[nan] = pd.to_numeric(df[nan])
            except Exception as e:
                data.update({'iserror': True, 'errmsg': e})

        # Remove duplicate data
        denies = []
        for k, v in df[['기준일시', '시도명']].value_counts().items():
            if int(v) == 1:
                continue
            ids = df[(df['기준일시'] == k[0]) & (df['시도명'] == k[1])].index
            denies.extend(list(filter(lambda x: x != min(ids), ids)))

        df.drop(denies, axis=0, inplace=True)
        df.index = np.arange(0, len(df))

        # print dataframe
        df = df[['기준일시', '시도명', '확진자 수', '사망자 수', '격리중 환자수',
                 '지역발생 수', '해외유입 수', '전일대비 증감 수', '격리 해제 수', '10만명당 발생률']]
        df = df[df['시도명'] != '합계']

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
