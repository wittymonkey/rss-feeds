"""
This parses ElPaís authors, and adds date
"""
import re

import arrow
from bs4 import BeautifulSoup
import requests

from base import BaseFeed


session = requests.Session()


class Feed(BaseFeed):

    def __init__(self, name='elpais', url=None):
        super().__init__(name=name)
        self.url = url

    def update(self):

        # Find missing feeds in ori and add them back (with new date)
        ori_titles = set([e['title'].strip() for e in self.feed['entries']])

        response = session.get(self.url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all(name="article", attrs={"class": "c-d"})
        for article in articles:
            e = article.find(attrs={"class": "c_t"})
            title = e.text.strip()
            if title not in ori_titles:
                link = e.find('a')['href']
                if m := re.search(r'\d{4}-\d{2}-\d{2}', link):
                    date = m.group()
                elif m := re.search(r'\d{4}/\d{2}/\d{2}', link):
                    # old articles (before Nov 2020) have different URL date pattern
                    date = m.group()
                else:
                    raise Exception('Could not find date pattern')
                desc = article.find(attrs={"class": "c_d"}).text
                self.feed['entries'].append(
                    {
                        'title': e.text,
                        'link': link,
                        'published': arrow.get(date).strftime("%a, %d %b %Y %H:%M:%S+00:00"),
                        'description': desc,
                    }
                )


class ArnauFeed(Feed):

        def __init__(self):
            super().__init__(
                name='juan-arnau-elpais',
                url ='https://elpais.com/autor/juan-maria-arnau-navarro/',
                )


class FanjulFeed(Feed):

        def __init__(self):
            super().__init__(
                name='sergio-fanjul-elpais',
                url ='https://elpais.com/autor/sergio-cuadrado-fanjul',
                )


class JuegoCienciaFeed(Feed):

        def __init__(self):
            super().__init__(
                name='juego-ciencia-elpais',
                url ='https://elpais.com/ciencia/el-juego-de-la-ciencia/',
                )


class MolinaFeed(Feed):

        def __init__(self):
            super().__init__(
                name='munoz-molina-elpais',
                url ='https://elpais.com/autor/antonio-munoz-molina/',
                )


class HancockFeed(Feed):

        def __init__(self):
            super().__init__(
                name='rubio-hancock-elpais',
                url ='https://elpais.com/autor/jaime-rubio-hancock/',
                )

class TorrijosFeed(Feed):

        def __init__(self):
            super().__init__(
                name='pedro-torrijos-elpais',
                url ='https://elpais.com/autor/pedro-torrijos-leon/',
                )
