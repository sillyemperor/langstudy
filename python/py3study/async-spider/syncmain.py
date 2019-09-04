import requests
from bs4 import BeautifulSoup
import counter

c = counter.counter()

next(c)


def get(url):
    global c
    if not url.startswith('http'):
        return

    r = requests.get(url)
    s = r.text
    c.send(len(s))
    bs = BeautifulSoup(s, features="html.parser")
    list(map(get, [i.attrs['href'] if 'href' in i.attrs else '' for i in bs.find_all('a')]))

get('http://www.163.com')