"""
Base Feed definition

Child Feeds only have to define the update() method:
load new content, compare with existing feed and add entries
"""

from pathlib import Path

from feedgen.feed import FeedGenerator
import feedparser
import requests


feeds_dir = Path(__file__).parents[1].resolve() / "feeds"


class BaseFeed:
    def __init__(self, name="base"):
        self.name = name

        # Load existing feed or load sample otherwise
        self.feed_pth = feeds_dir / f"{name}.xml"
        if not self.feed_pth.is_file():
            d = feedparser.parse(feeds_dir / "sample.xml")
        else:
            d = feedparser.parse(self.feed_pth)

        # Convert to dict
        self.feed = self.feed2dict(d)

        # Create a session with nice headers
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def feed2dict(self, f):
        d = {
            "feed": f.feed,
            "entries": f.entries,
        }
        return d

    def update(self):
        pass

    def save(self):
        # Write dict to feed
        fg = FeedGenerator()
        fg.title(self.name)
        fg.link(href="http://example.com", rel="alternate")
        fg.subtitle("This is a cool feed!")
        for e in self.feed["entries"]:
            fe = fg.add_entry()
            fe.title(e["title"])
            fe.link(href=e["link"])
            fe.published(e["published"])
            fe.description(e.get("description", ""))

        # Save feed to file
        fg.rss_file(
            filename=str(self.feed_pth),
            pretty=True,
        )
