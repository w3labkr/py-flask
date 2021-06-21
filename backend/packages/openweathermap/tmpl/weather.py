# Miscellaneous operating system interfaces
import os

# A simple, yet elegant HTTP library.
import requests

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()

# Get API Key
API_PATH = os.path.join(appdir.configs, 'openweathermapapikey.txt')
with open(API_PATH, 'r') as f:
    API_KEY = f.read().strip()

def weather(**kwargs):
    return result(**kwargs)


def results(**kwargs):
    endpoint = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': 'Seoul, KR',
        'units': 'metric',
        'lang': 'kr',
        'appid': API_KEY
    }
    for k, v in kwargs.items():
        params.update({k: v})

    response = requests.get(endpoint, params=params).json()
    response.update({
        'name': translate(response['name'], 'ko')
    })

    return response


def result(**kwargs):
    endpoint = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': 'Seoul, KR',
        'units': 'metric',
        'lang': 'kr',
        'appid': API_KEY
    }
    for k, v in kwargs.items():
        params.update({k: v})

    response = requests.get(endpoint, params=params).json()
    response.update({
        'name': translate(response['name'], 'ko'),
        'weather': response['weather'][0]
    })

    return response


def translate(location, language='ko', country='KR'):
    po = {
        'KR': {
            'KR': {'en': 'Korean', 'ko': '대한민국'},
            'Seoul': {'en': 'Seoul', 'ko': '서울'},
            'Busan': {'en': 'Busan', 'ko': '부산'},
            'Daegu': {'en': 'Daegu', 'ko': '대구'},
            'Incheon': {'en': 'Incheon', 'ko': '인천'},
            'Gwangju': {'en': 'Gwangju', 'ko': '광주'},
            'Daejeon': {'en': 'Daejeon', 'ko': '대전'},
            'Ulsan': {'en': 'Ulsan', 'ko': '울산'},
            'Sejong': {'en': 'Sejong', 'ko': '세종'},
            'Gyeonggi': {'en': 'Gyeonggi', 'ko': '경기'},
            'Gangwon': {'en': 'Gangwon', 'ko': '강원'},
            'Chungcheongbuk': {'en': 'Chungcheongbuk', 'ko': '충북'},
            'Chungcheongnam': {'en': 'Chungcheongnam', 'ko': '충남'},
            'Jeollabuk': {'en': 'Jeollabuk', 'ko': '전북'},
            'Jeollanam': {'en': 'Jeollanam', 'ko': '전남'},
            'Gyeongsangbuk': {'en': 'Gyeongsangbuk', 'ko': '경북'},
            'Gyeongsangnam': {'en': 'Gyeongsangnam', 'ko': '경남'},
            'Jeju': {'en': 'Jeju', 'ko': '제주'},
        },
    }
    return po[country][location][language]
