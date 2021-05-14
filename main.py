from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re

KEYWORDS = {'дизайн', 'фото', 'web', 'python', 'toggles'}

res = requests.get('https://habr.com/ru/all')

if not res.ok:
    print('res invalid')

soup = BeautifulSoup(res.text, features='html.parser')

for article in soup.findAll('article'):
    pattern = re.compile('([—\-\s.,:]+)')
    hubs = {h.text.lower() for h in article.findAll('a', class_='hub-link')}

    title = article.find('h2', class_='post__title')
    href = title.find('a').attrs.get('href')

    x = requests.get(href)
    d = BeautifulSoup(x.text, features='html.parser')

    if hubs & KEYWORDS:
        print(f'{datetime.now(tz=None)} | {title.text.strip()} | {href}')

    p_text = [set(pattern.sub(r' ', p.find('p').text.lower()).split())
              for p in article.findAll('div', class_='post__text_v2')]

    p_text += [set('')]

    if p_text[0] & KEYWORDS:
        print(f'{datetime.now(tz=None)} | {title.text.strip()} | {href}')

    a_text = [set(pattern.sub(r' ', a.text.lower()).split())
              for a in d.findAll('div', class_='post__text_v1')]

    a_text += [set('')]

    if a_text[0] & KEYWORDS:
        print(f'{datetime.now(tz=None)} | {title.text.strip()} | {href}')
