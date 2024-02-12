from parsers import dense_discovery, confidencial, elpais, theatlantic


feeds = [
    dense_discovery.Feed(),
    confidencial.BarnesFeed(),
    confidencial.OlmosFeed(),
    confidencial.SotoFeed(),
    elpais.ArnauFeed(),
    elpais.FanjulFeed(),
    elpais.JuegoCienciaFeed(),
    elpais.MolinaFeed(),
    theatlantic.technology(),
]
failures = []

for feed in feeds:
    try:
        feed.update()
        feed.save()
    except Exception as e:  # ignore Exception to complete all feeds
        print(e)
        failures.append(feed.name)

# Raise an Exception for the Github Action fail status
if failures:
    raise Exception(
        "The following parsers failed: \n" \
        f"    {failures}"
    )
