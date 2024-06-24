from flask import Blueprint, render_template, request, jsonify, current_app
from .bot import get_weather

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    chatbot = current_app.config['CHATBOT']
    response = chatbot.get_response(user_input)
    if 'weather' in user_input.lower():
        location = user_input.split('in')[-1].strip()
        weather_forecast = get_weather(location)
        if weather_forecast:
            response = f"Weather forecast for {location}: "
            for day in weather_forecast:
                response += f"\n{day['date']}: {day['temp']}°C, {day['description']}"
        else:
            response = "I couldn't fetch the weather data for that location."
    return jsonify({'response': str(response)})
