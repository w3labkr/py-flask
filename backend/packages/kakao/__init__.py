# Miscellaneous operating system interfaces
import os

# A simple, yet elegant HTTP library.
import requests

# Import the application's modules and packages.
from modules.os import get_app_dir

# Set the absolute directory path.
appdir = get_app_dir()

# Get API Key
API_PATH = os.path.join(appdir.configs, 'kakaomaprestapikey.txt')
with open(API_PATH, 'r') as f:
    API_KEY = f.read().strip()


def main():
    pass


def get_requests(query=''):
    if query:
        url = 'https://dapi.kakao.com/v2/local/search/address.json'
        params = {
            'query': query
        }
        headers = {"Authorization": "KakaoAK " + API_KEY}
        return requests.get(url, params=params, headers=headers).json()
    return ''


# 좌표
def get_coords(query=''):
    if query:
        r = get_requests(query)
        return {
            'x': float(r['documents'][0]['x']),
            'y': float(r['documents'][0]['y']),
        }
    return ''


# 경도
def get_lon(query=''):
    if query:
        r = get_requests(query)
        return float(r['documents'][0]['x'])
    return ''


# 위도
def get_lat(query=''):
    if query:
        r = get_requests(query)
        return float(r['documents'][0]['y'])
    return ''


if __name__ == "__main__":
    main()
