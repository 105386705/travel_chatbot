from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), nullable=False)
    data = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def set_data(self, data):
        self.data = json.dumps(data)

    def get_data(self):
        return json.loads(self.data)

class NewsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), nullable=False)
    data = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def set_data(self, data):
        self.data = json.dumps(data)

    def get_data(self):
        return json.loads(self.data)
