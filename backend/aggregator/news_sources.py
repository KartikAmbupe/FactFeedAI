from backend.aggregator.config import API_KEYS

SOURCES = [
    # RSS Sources
    {'type': 'rss', 'url': 'http://feeds.bbci.co.uk/news/rss.xml', 'category': 'general', 'name': 'BBC News'},
    {'type': 'rss', 'url': 'http://rss.cnn.com/rss/edition.rss', 'category': 'general', 'name': 'CNN'},
    {'type': 'rss', 'url': 'https://techcrunch.com/feed/', 'category': 'technology', 'name': 'TechCrunch'},
    {'type': 'rss', 'url': 'https://www.wired.com/feed/rss', 'category': 'technology', 'name': 'Wired'},
    {'type': 'rss', 'url': 'https://feeds.npr.org/1001/rss.xml', 'category': 'general', 'name': 'NPR'},
    {'type': 'rss', 'url': 'https://www.theguardian.com/environment/rss', 'category': 'environment', 'name': 'The Guardian - Environment'},
    {'type': 'rss', 'url': 'https://feeds.nbcnews.com/nbcnews/public/politics', 'category': 'politics', 'name': 'NBC Politics'},

    # US NewsAPI.org - fetch all major categories in one go
    {
        'type': 'api',
        'url': 'https://newsapi.org/v2/top-headlines',
        'params': {
            'apiKey': API_KEYS['newsapi'],
            'country': 'us',
            'pageSize': 100  # fetch max articles per call
        },
        'category': 'all',
        'name': 'NewsAPI US'
    },

    # NewsData.io - Indian news, per category
    {'type': 'api', 'url': 'https://newsdata.io/api/1/news', 'params': {'apikey': API_KEYS['newsdata'], 'country': 'in', 'language': 'en', 'category': 'general'}, 'category': 'general', 'name': 'NewsData.io India General'},
    {'type': 'api', 'url': 'https://newsdata.io/api/1/news', 'params': {'apikey': API_KEYS['newsdata'], 'country': 'in', 'language': 'en', 'category': 'technology'}, 'category': 'technology', 'name': 'NewsData.io India Technology'},
    {'type': 'api', 'url': 'https://newsdata.io/api/1/news', 'params': {'apikey': API_KEYS['newsdata'], 'country': 'in', 'language': 'en', 'category': 'politics'}, 'category': 'politics', 'name': 'NewsData.io India Politics'},
    {'type': 'api', 'url': 'https://newsdata.io/api/1/news', 'params': {'apikey': API_KEYS['newsdata'], 'country': 'in', 'language': 'en', 'category': 'business'}, 'category': 'business', 'name': 'NewsData.io India Business'},
    {'type': 'api', 'url': 'https://newsdata.io/api/1/news', 'params': {'apikey': API_KEYS['newsdata'], 'country': 'in', 'language': 'en', 'category': 'top'}, 'category': 'top', 'name': 'NewsData.io India Top'},
]
