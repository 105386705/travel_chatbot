# bot.py

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

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
