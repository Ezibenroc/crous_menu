import datetime
from bs4 import BeautifulSoup
import colorama
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
            if len(item) == 1:
                items.append('- %s' % item[0])
        result.append((title, items))
    return result


def title_to_date(title):
    def month_number(month):
        months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
                  'août', 'septembre', 'octobre', 'novembre', 'décembre'
                  ]
        return months.index(month) + 1
    date = title.split()[-3:]
    try:
        y = int(date[2])
        m = month_number(date[1])
        d = int(date[0])
        return datetime.date(y, m, d)
    except ValueError:
        raise ValueError('Could not recognize the string "%s" as a date' % ' '.join(date))


def pretty_menu(menu, highlight_today=True):
    highlight_str = colorama.Fore.BLACK + colorama.Back.WHITE + colorama.Style.BRIGHT
    for title, items in menu:
        if len(items) > 0:
            entries = [title] + items
            if highlight_today and title_to_date(title) == datetime.datetime.today().date():
                max_l = max([len(e) for e in entries])
                entries = [highlight_str + e.ljust(max_l) + colorama.Style.RESET_ALL for e in entries]
            entry = '\n'.join(entries)
            print(entry)


def main():
    pretty_menu(process_menu(extract_week_menu(get_page())))


if __name__ == '__main__':
    main()
