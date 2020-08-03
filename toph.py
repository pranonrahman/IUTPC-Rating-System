import requests
from bs4 import BeautifulSoup
import cx_Oracle


def tophRating(contestName):
    url = 'https://toph.co/c/' + contestName + '/standings'
    response = requests.get(url)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    print(response.text)
    table = soup.find_all('table', attrs={'class': 'table standings'})
    for rows in table[0].find_all('tr'):
        for cells in rows.find_all('td'):
            print(cells.text)
    



if __name__ == "__main__":
    tophRating('criterion-2020-round-1')
