import os
from flask import Flask, jsonify, request,send_from_directory
from backend import db, migrate, cors
from apscheduler.schedulers.background import BackgroundScheduler
import logging

def create_app():
    app = Flask(__name__,static_folder="../frontend/dist")
    
    # Configuration settings
    basedir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(basedir)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(parent_dir, 'instance', 'news.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with the Flask app
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app,resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Import routes and models after db initialization
    from backend.models import Article
    from backend.detector import predict_news
    from backend.summerizer import summarize_text
    
    @app.route('/')
    def home():
        return "Fake News Detection & Summarization API is Running!"
    

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
      if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
      else:
        return send_from_directory(app.static_folder, "index.html")

    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = predict_news(text)
        return jsonify({"prediction": result})

    @app.route('/summarize', methods=['POST'])
    def summarize():
        data = request.json
        text = data.get("text", "")
        num_sentences = data.get("num_sentences", 2)
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        summary = summarize_text(text, num_sentences)
        return jsonify({"summary": summary})

    @app.route('/api/news')
    def get_news():
        try:
            articles = Article.query.order_by(Article.published_at.desc()).limit(100).all()
            article_list = [{
                'title': a.title,
                'content': a.content,
                'source': a.source,
                'published_at': a.published_at.isoformat() if a.published_at else None,
                'category': a.category,
                'author': a.author
            } for a in articles]
            return jsonify(article_list)
        except Exception as e:
            app.logger.error(f"Error fetching news: {str(e)}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
        

    # Setup background task for fetching news
    def scheduled_fetch():
        with app.app_context():
            try:
                from backend.aggregator.fetcher import fetch_news
                from backend.aggregator.storage import store_articles
                print("Scheduled fetch started...")
                articles = fetch_news()
                new_count = store_articles(articles)
                print(f"Added {new_count} new articles")
            except Exception as e:
                print(f"Error in scheduled fetch: {str(e)}")

    # Initialize scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_fetch, 'interval', hours=1)
    scheduler.start()

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
