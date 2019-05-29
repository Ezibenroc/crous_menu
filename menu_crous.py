import datetime
from bs4 import BeautifulSoup
import requests


today = datetime.datetime.now().day
URL = 'http://www.crous-grenoble.fr/restaurant/ru-barnave-etudiant/'


class HTTPError(Exception):
    pass


def get_page(url=URL):
    req = requests.get(url)
    if req.status_code != 200:
        raise HTTPError('Got status code %d' % req.status_code)
    return BeautifulSoup(req.text, 'html.parser')


def extract_week_menu(page):
    menu = page.find('div', {'id': 'menu-repas'})
    menu = menu.find('ul')
    menu = [entry for entry in menu.find_all('li') if len(entry) > 1]
    return menu


def process_menu(menu):
    result = []
    for entry in menu:
        title = entry.find('h3').contents
        assert len(title) == 1
        title = title[0]
        items = []
        for item in entry.find_all('li'):
            item = item.contents
            assert len(item) == 1
            items.append(item[0])
        result.append((title, items))
    return result


def pretty_menu(menu):
    for title, items in menu:
        if len(items) > 0:
            print(title)
            print('\n'.join(items))


if __name__ == '__main__':
    pretty_menu(process_menu(extract_week_menu(get_page())))
