import requests
from bs4 import BeautifulSoup
import json
import cx_Oracle as Cx


def cfRating(username):
    url1 = url1 = 'https://codeforces.com/api/user.info?handles=' + username
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url1, headers=headers)
    if response.status_code != 200:
        return -1
    res = json.loads(response.text)
    try:
        return res['result'][0]['rating']
    except KeyError:
        return 1000


# print(cfRating('synapse.official'))
# print(cfRating('pranonraian'))
