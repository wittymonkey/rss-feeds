"""
This parses TheAtlantic
"""
import re

import arrow
from bs4 import BeautifulSoup
import requests

from base import BaseFeed


session = requests.Session()


class Feed(BaseFeed):

    def __init__(self, name='the-atlantic', url=None):
        super().__init__(name=name)
        self.url = url

    def update(self):

        # Find missing feeds in ori and add them back (with new date)
        ori_titles = set([e['title'] for e in self.feed['entries']])

        response = session.get(self.url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all(name="article")
        for article in articles:
            title = article.find(name='a', attrs={"data-event-element": "title"}).text
            if title and title not in ori_titles:
                link = article.find('a')['href']
                desc = p.text if (p := article.find('p')) else ""
                date = article.find('time')
                if not date:
                    date = arrow.utcnow().format()
                else:
                    date = date['datetime']

                self.feed['entries'].append(
                    {
                        'title': title,
                        'link': link,
                        'published': arrow.get(date).strftime("%a, %d %b %Y %H:%M:%S+00:00"),
                        'description': desc,
                    }
                )


class technology(Feed):

        def __init__(self):
            super().__init__(
                name='technology-the-atlantic',
                url ='https://www.theatlantic.com/technology/',
                )
