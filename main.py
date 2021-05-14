from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re

KEYWORDS = {'дизайн', 'фото', 'web', 'python', 'toggles'}



res = requests.get('https://habr.com/ru/all/')

if not res.ok:
    print('res invalid')

soup = BeautifulSoup(res.text, features='html.parser')

for article in soup.findAll('article'):
    pattern = re.compile('([—\-\s.,:]+)')
    hubs = {h.text.lower() for h in article.findAll('a', class_='hub-link')}
    try:
        p_text = [set(pattern.sub(r' ', p.find('p').text.lower()).split())
                  for p in article.findAll('div', class_='post__text_v2')][0]
    except IndexError:
        continue

    if hubs & KEYWORDS:
        title = article.find('h2', class_='post__title')
        href = title.find('a').attrs.get('href')
        print(f'{datetime.now(tz=None)} | {title.text.strip()} | {href}')
    elif p_text & KEYWORDS:
        title = article.find('h2', class_='post__title')
        href = title.find('a').attrs.get('href')
        print(f'{datetime.now(tz=None)} | {title.text.strip()} | {href}')
    else:
        print('Нет совпадений')







