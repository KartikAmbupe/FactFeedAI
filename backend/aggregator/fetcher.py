import requests
import feedparser
from datetime import datetime
import logging
from backend.aggregator.news_sources import SOURCES
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_news():
    articles = []
    for source in SOURCES:
        time.sleep(random.uniform(0.5, 1.5))
        if source['type'] == 'api':
            try:
                logger.info(f"Fetching from API: {source['url']}")
                response = requests.get(source['url'], params=source.get('params', {}), timeout=15)
                if response.status_code == 429:
                    logger.warning(f"[RATE LIMITED] Skipping {source.get('name', source['url'])} due to 429 Too Many Requests.")
                    continue
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('articles') or data.get('results') or []
                    for item in items:
                        try:
                            # Date parsing
                            date_str = item.get('publishedAt') or item.get('pubDate')
                            date_format = "%Y-%m-%dT%H:%M:%SZ" if 'publishedAt' in item else "%Y-%m-%d %H:%M:%S"
                            published_at = datetime.strptime(date_str, date_format) if date_str else datetime.now()
                            # Author extraction
                            author = item.get('author') or 'Unknown'
                            if 'creator' in item:
                                author = item['creator'][0] if isinstance(item['creator'], list) else item['creator']
                            # Category assignment
                            category = item.get('category') or source.get('category', 'general')
                            if isinstance(category, list):
                                category = category[0] if category else 'general'
                            if source.get('name') == 'NewsAPI US':
                                # Try to infer category from source name if not present
                                if not category or category == 'all':
                                    sname = item.get('source', {}).get('name', '').lower()
                                    if 'tech' in sname:
                                        category = 'technology'
                                    elif 'politic' in sname:
                                        category = 'politics'
                                    elif 'business' in sname:
                                        category = 'business'
                                    elif 'general' in sname or not sname:
                                        category = 'general'
                                    else:
                                        category = 'general'
                            articles.append({
                                'title': item.get('title', 'No Title'),
                                'content': item.get('description') or item.get('content') or 'No content available',
                                'source': item.get('source', {}).get('name') or source.get('name', 'API Source'),
                                'published_at': published_at,
                                'category': category.lower() if category else 'general',
                                'author': author,
                                'url': item.get('url') or item.get('link', '#'),
                                'image': item.get('urlToImage') or item.get('image_url') or item.get('image')
                            })
                        except Exception as e:
                            logger.error(f"Error processing API item: {str(e)}")
                else:
                    logger.error(f"API request failed for {source.get('name', source['url'])} with status code: {response.status_code}")
            except Exception as e:
                logger.error(f"API Error for {source.get('name', source['url'])}: {str(e)}")
        elif source['type'] == 'rss':
            try:
                logger.info(f"Fetching from RSS: {source['url']}")
                feed = feedparser.parse(source['url'])
                for entry in feed.entries:
                    try:
                        content = getattr(entry, 'description', None) or getattr(entry, 'summary', '') or ''
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            published_at = datetime(*entry.published_parsed[:6])
                        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                            published_at = datetime(*entry.updated_parsed[:6])
                        else:
                            published_at = datetime.now()
                        author = entry.get('author', 'Unknown')
                        if hasattr(entry, 'authors') and entry.authors:
                            author = entry.authors[0].get('name', author)
                        image_url = None
                        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                            image_url = entry.media_thumbnail[0].get('url')
                        elif hasattr(entry, 'media_content') and entry.media_content:
                            media_content = [m for m in entry.media_content if 'image' in m.get('type', '')]
                            if media_content:
                                image_url = media_content[0].get('url')
                        elif hasattr(entry, 'enclosures') and entry.enclosures:
                            for enc in entry.enclosures:
                                if enc.get('type', '').startswith('image/'):
                                    image_url = enc.get('href')
                                    break
                        if not image_url and content:
                            import re
                            img_match = re.search(r'<img.*?src=["\'](.*?)["\']', content)
                            if img_match:
                                image_url = img_match.group(1)
                        articles.append({
                            'title': entry.title,
                            'content': content,
                            'source': feed.feed.get('title', source.get('name', 'RSS Source')),
                            'published_at': published_at,
                            'category': source['category'],
                            'author': author,
                            'url': entry.link,
                            'image': image_url
                        })
                    except Exception as e:
                        logger.error(f"Error processing RSS entry: {str(e)}")
            except Exception as e:
                logger.error(f"RSS Error: {str(e)}")
    logger.info(f"Fetched {len(articles)} articles total")
    return articles

if __name__ == "__main__":
    from backend.app import create_app
    app = create_app()
    with app.app_context():
        print("Fetching news articles...")
        articles = fetch_news()
        print(f"Fetched {len(articles)} articles")
        from backend.aggregator.storage import store_articles
        new_count = store_articles(articles)
        print(f"Added {new_count} new articles to database")
