from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import current_app
import requests

def init_bot(app):
    chatbot = ChatBot(
        'TravelBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri=app.config['SQLALCHEMY_DATABASE_URI'],
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.TimeLogicAdapter'
            },
            {
                'import_path': 'chatterbot.logic.MathematicalEvaluation'
            }
        ],
    )
    
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.english')
    
    app.config['CHATBOT'] = chatbot

def get_weather(location):
    api_key = current_app.config['OPENWEATHER_API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for item in data['list'][:5]:
            day_forecast = {
                'date': item['dt_txt'],
                'temp': item['main']['temp'],
                'description': item['weather'][0]['description']
            }
            forecast.append(day_forecast)
        return forecast
    return None
