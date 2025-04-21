from backend.models import Article, db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def store_articles(articles):
    new_count = 0
    for article in articles:
        try:
            if not article.get('title'):
                continue
            # Enhanced duplicate check using title + url + source
            exists = Article.query.filter(
                Article.title == article['title'],
                Article.url == article.get('url', ''),
                Article.source == article.get('source', '')
            ).first()
            if not exists:
                new_article = Article(
                    title=article['title'],
                    content=article.get('content', 'No content'),
                    source=article.get('source', 'Unknown Source'),
                    published_at=article.get('published_at'),
                    category=article.get('category', 'general'),
                    author=article.get('author', 'Unknown'),
                    url=article.get('url', '#'),
                    image_url=article.get('image')
                )
                db.session.add(new_article)
                new_count += 1
        except Exception as e:
            logger.error(f"Error storing article: {str(e)}")
    try:
        db.session.commit()
        logger.info(f"Successfully added {new_count} new articles")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database commit error: {str(e)}")
        raise
    return new_count
