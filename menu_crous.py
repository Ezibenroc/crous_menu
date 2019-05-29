import datetime
from bs4 import BeautifulSoup
import requests


URL = 'http://www.crous-grenoble.fr/restaurant/ru-barnave-etudiant/'


class HTTPError(Exception):
    pass


class DayNotFoundError(Exception):
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


def get_today_menu(menu):
    today = datetime.datetime.now().day
    for entry in menu:
        title = entry.find('h3').contents
        assert len(title) == 1
        title = title[0]
        if str(today) in title:
            return entry
    raise DayNotFoundError('Could not find day %d in the menu' % today)


def pretty_day_menu(menu):
    for entry in menu.find_all('li'):
        entry = entry.contents
        print(entry[0])


if __name__ == '__main__':
    pretty_day_menu(get_today_menu(extract_week_menu(get_page())))
