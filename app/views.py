# views.py

from flask import Blueprint, render_template, request, jsonify, current_app
import requests
import logging
import datetime
from .models import WeatherData, NewsData, db

main = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    chatbot = current_app.config['CHATBOT']
    response = chatbot.get_response(user_input)
    data = {'response': str(response)}

    logging.debug(f"User input: {user_input}")
    logging.debug(f"Initial bot response: {response}")

    if 'weather' in user_input.lower() and 'in' in user_input.lower():
        location = user_input.split('in')[-1].strip()
        weather_forecast = get_weather(location)
        if weather_forecast:
            weather_response = f"Here is the weather for {location}: "
            data['response'] = weather_response
            lat, lon = get_coordinates(location)  # Get coordinates for the location
            data['lat'] = lat
            data['lon'] = lon
            news_articles = get_news(location)  # Fetch news based on location
            if news_articles:
                data['news_articles'] = news_articles
            data['command'] = 'update_all'  # Ensure the command is set to update all
            data['weather_response'] = weather_response + "\n".join(
                [f"{day['date']}: {day['temp']}°C, {day['description']}" for day in weather_forecast]
            )
        else:
            data['response'] = "I couldn't fetch the weather data for that location."
    elif 'show' in user_input.lower() and 'location' in user_input.lower():
        location = user_input.split('location')[-1].strip()
        lat, lon = get_coordinates(location)
        if lat and lon:
            data['response'] = f"Showing location: {location}"
            data['command'] = 'update_map'
            data['lat'] = lat
            data['lon'] = lon
        else:
            data['response'] = "I couldn't find that location."
    elif 'news' in user_input.lower():
        data['response'] = "Fetching the latest news for you."
        data['command'] = 'fetch_news'

    logging.debug(f"Final bot response: {data['response']}")
    if 'command' in data:
        logging.debug(f"Command: {data['command']}, Additional data: {data.get('city', '')}{data.get('lat', '')}{data.get('lon', '')}")

    return jsonify(data)

def get_weather(location):
    api_key = current_app.config['OPENWEATHER_API_KEY']
    location = location.replace("?", "")  # Clean up location input
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    logging.debug(f"Fetching weather for {location} with URL: {url}")
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
        weather_data = WeatherData(location=location, timestamp=datetime.datetime.utcnow())
        weather_data.set_data(forecast)
        db.session.add(weather_data)
        db.session.commit()
        return forecast
    logging.debug(f"Failed to fetch weather data, response code: {response.status_code}, response: {response.text}")
    return None

def get_coordinates(location):
    api_key = current_app.config.get('OPENCAGE_API_KEY')
    if not api_key:
        logging.error('OPENCAGE_API_KEY is not set')
        return 0, 0
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}"
    logging.debug(f"Fetching coordinates for {location} with URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            coordinates = data['results'][0]['geometry']
            return coordinates['lat'], coordinates['lng']
    logging.debug(f"Failed to fetch coordinates, response code: {response.status_code}, response: {response.text}")
    return 0, 0

def get_news(location):
    news_data = NewsData.query.filter_by(location=location).first()
    if news_data and (datetime.datetime.utcnow() - news_data.timestamp).total_seconds() < 3600:
        return news_data.get_data()

    api_key = current_app.config.get('NEWS_API_KEY')
    url = f"https://newsapi.org/v2/everything?q={location}&apiKey={api_key}"
    logging.debug(f"Fetching news for {location} with URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = []
        for article in data['articles'][:5]:  # Limit to 5 articles for simplicity
            articles.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url']
            })
        news_data = NewsData(location=location, timestamp=datetime.datetime.utcnow())
        news_data.set_data(articles)
        db.session.add(news_data)
        db.session.commit()
        return articles
    logging.debug(f"Failed to fetch news data, response code: {response.status_code}, response: {response.text}")
    return None
