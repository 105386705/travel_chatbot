from flask import Flask
import logging
from .config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, OPENWEATHER_API_KEY, NEWS_API_KEY, OPENCAGE_API_KEY
from .models import db
from .views import main
from .bot import init_bot

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['OPENWEATHER_API_KEY'] = OPENWEATHER_API_KEY
    app.config['NEWS_API_KEY'] = NEWS_API_KEY
    app.config['OPENCAGE_API_KEY'] = OPENCAGE_API_KEY

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"OPENWEATHER_API_KEY: {app.config['OPENWEATHER_API_KEY']}")
    logging.debug(f"NEWS_API_KEY: {app.config['NEWS_API_KEY']}")
    logging.debug(f"OPENCAGE_API_KEY: {app.config['OPENCAGE_API_KEY']}")

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    init_bot(app)
    
    return app
