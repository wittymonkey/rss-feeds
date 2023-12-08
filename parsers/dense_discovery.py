"""
This parser is basically a patch on the official feed, in order to add a `pubDate`
https://www.densediscovery.com/feed/
"""

import datetime

import feedparser

from base import BaseFeed


class Feed(BaseFeed):

    def __init__(self):
        super().__init__(name='dense-discovery')

    def update(self):
        # Load official feed
        new = feedparser.parse('https://www.densediscovery.com/feed/')
        new = self.feed2dict(new)

        # Find missing feeds in ori and add them back (with new date)
        ori_titles = set([e['title'] for e in self.feed['entries']])
        for e in new['entries']:
            if e['title'] not in ori_titles:
                self.feed['entries'].append(
                    {
                        'title': e['title'],
                        'link': e['link'],
                        'published': datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S+00:00"),
                    }
                )
