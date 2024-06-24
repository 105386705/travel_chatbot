import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
OPENWEATHER_API_KEY = 'b710ebc3b9e2b171a89cdae316167899'
NEWS_API_KEY = '93fe34b301c4496ab82738f821b76915'