from flask import Flask
from .bot import init_bot
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    init_bot(app)
    
    from .views import main
    app.register_blueprint(main)
    
    return app
