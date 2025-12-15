"""
This parses El Confidencial authors, and adds date
"""

import re

import arrow
from bs4 import BeautifulSoup
import requests

from base import BaseFeed


session = requests.Session()


class Feed(BaseFeed):
    def __init__(self, name="confidencial", url=None):
        super().__init__(name=name)
        self.url = url

    def update(self):
        # Find missing feeds in ori and add them back (with new date)
        ori_titles = set([e["title"] for e in self.feed["entries"]])

        response = session.get(self.url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all(name="article", attrs={"class": "archive-article"})
        for article in articles:
            e = article.find(name="a", attrs={"class": "archive-article-link"})
            title = e.get("title", None)
            if title and title not in ori_titles:
                desc = article.find(attrs={"class": "archive-article-leadin-tit"}).text
                date = re.search(r"\d{4}-\d{2}-\d{2}", e["href"]).group()
                self.feed["entries"].append(
                    {
                        "title": title,
                        "link": e["href"],
                        "published": arrow.get(date).strftime(
                            "%a, %d %b %Y %H:%M:%S+00:00"
                        ),
                        "description": desc,
                    }
                )


class BarnesFeed(Feed):
    def __init__(self):
        super().__init__(
            name="hector-g-barnes-confidencial",
            url="https://www.elconfidencial.com/autores/hector-g-barnes-120/",
        )


class OlmosFeed(Feed):
    def __init__(self):
        super().__init__(
            name="alberto-olmos-confidencial",
            url="https://www.elconfidencial.com/autores/alberto-olmos-1137/",
        )


class SotoFeed(Feed):
    def __init__(self):
        super().__init__(
            name="soto-ivars-confidencial",
            url="https://www.elconfidencial.com/autores/juan-soto-ivars-203/",
        )
