encylopedia = {"123": {"1": "One", "2": "Two", "3": "Three"},"456":{"4": "Four", "5": "Five", "6": "Six"}}
check = ["012", "123", "234", "345"]
isolated = []
for d in dict:
    volumes = dict[d]
    articles = volumes.items()
    for article in articles:
         article_key = article[0]
         article_value= article[1]
for c in check:
    try:
        volumes = dict[c]
        articles = volumes.items()
        for article in articles:
            article_key = article[0]
            article_value = article[1]
            isolated.append(article_value)
    except:
        pass
