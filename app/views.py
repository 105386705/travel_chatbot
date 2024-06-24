# views.py

from flask import Blueprint, render_template, request, jsonify, current_app
import requests
import logging

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
            weather_response = f"Weather forecast for {location}: "
            for day in weather_forecast:
                weather_response += f"\n{day['date']}: {day['temp']}°C, {day['description']}"
            data['response'] = weather_response
            lat, lon = get_coordinates(location)  # Get coordinates for the location
            data['lat'] = lat
            data['lon'] = lon
            news_articles = get_news(location)  # Fetch news based on location
            if news_articles:
                data['news_articles'] = news_articles
            data['command'] = 'update_all'  # Ensure the command is set to update all
            data['weather_response'] = weather_response
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
        return forecast
    logging.debug(f"Failed to fetch weather data, response code: {response.status_code}, response: {response.text}")
    return None

def get_coordinates(location):
    # Dummy implementation, replace with actual geocoding logic
    if location.lower() == 'london':
        return 51.5074, -0.1278
    elif location.lower() == 'melbourne':
        return -37.8136, 144.9631
    # Add more locations as needed
    return 0, 0

def get_news(location):
    api_key = current_app.config.get('NEWS_API_KEY')
    if not api_key:
        logging.error('NEWS_API_KEY is not set')
        return None
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
        return articles
    logging.debug(f"Failed to fetch news data, response code: {response.status_code}, response: {response.text}")
    return None
