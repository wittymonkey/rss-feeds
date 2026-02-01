from parsers import dense_discovery, confidencial, elpais, theatlantic, abc


feeds = [
    dense_discovery.Feed(),
    confidencial.BarnesFeed(),
    confidencial.OlmosFeed(),
    confidencial.SotoFeed(),
    abc.SotoFeed(),
    elpais.ArnauFeed(),
    elpais.FanjulFeed(),
    elpais.JuegoCienciaFeed(),
    elpais.MolinaFeed(),
    elpais.HancockFeed(),
    elpais.TorrijosFeed(),
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
    raise Exception(f"The following parsers failed: \n    {failures}")
