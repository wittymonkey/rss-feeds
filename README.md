# RSS feeds

[![reload-feeds](https://github.com/wittymonkey/rss-feeds/actions/workflows/main.yml/badge.svg)](https://github.com/wittymonkey/rss-feeds/actions/workflows/main.yml)

<!--
[!] Use:
```
git config --local credential.helper ""
git config --local user.name "wittymonkey"
git config --local user.email "random@email.com"
```
to avoid pushing with your main account and remove your personal information from commits
-->

Generate custom RSS feeds from webpages. If the webpage structure is simple enough, better use [rss-proxy](https://github.com/damoeb/rss-proxy) or [feedless](https://github.com/damoeb/feedless), for automatic feed generation from HTML. This repo is used for trickier setups.

Each feed follows the following workflow:
1. Load previous feed (or start a new one from scratch)
2. Parse webpage and compare content to feed
3. Update feed and save
4. Repeat [1-3] daily via Github actions

Because we use one Python package to read feeds ([feedparser](https://github.com/kurtmckee/feedparser)) and another one to write them ([feedgen](https://github.com/lkiesow/python-feedgen)), the state of the feed in between is kept as a Python dict.
