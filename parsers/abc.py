"""
ABC parser
"""

from datetime import datetime

from bs4 import BeautifulSoup

from base import BaseFeed


class Feed(BaseFeed):
    def __init__(self, name="abc", url=None):
        super().__init__(name=name)
        self.url = url

    def update(self):
        # Find missing feeds in ori and add them back (with new date)
        ori_titles = set([e["title"] for e in self.feed["entries"]])

        response = self.session.get(self.url, verify=True)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all(name="div", attrs={"class": "voc-article-container"})
        for article in articles:
            e = article.find(name="h2", attrs={"class": "voc-title"})
            title = e.text.strip()
            link = e.find("a").get("href")
            link = f"https://archive.ph/{link}"  # bypass paywall
            desc = article.find(name="p", attrs={"class": "voc-p"}).text.strip()
            date = article.find("span", attrs={"class": "s__day"})
            if not date:
                # Ignore header article with no date
                continue
            date = date.text.strip()
            formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime(
                "%a, %d %b %Y %H:%M:%S+00:00"
            )
            if title and title not in ori_titles and link:
                self.feed["entries"].append(
                    {
                        "title": title,
                        "link": link,
                        "published": formatted_date,
                        "description": desc,
                    }
                )


class SotoFeed(Feed):
    def __init__(self):
        super().__init__(
            name="soto-ivars-abc",
            url="https://www.abc.es/autor/juan-soto-ivars-7455/",
        )
