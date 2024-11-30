import os
import functions_framework
import requests
from datetime import datetime
from weather.weather_codes import is_valid_weather_type
from utils.secrets import get_secret
from weather import handle_weather_type
@functions_framework.http
def check_weather(request):
    """Cloud Function entry point"""
    try:
        # TODO update this to take these params from request  
        lat = os.environ.get('WEATHER_LAT', '40.7128')  # Default to NYC
        lon = os.environ.get('WEATHER_LON', '-74.0060')

        api_key = get_secret("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("OpenWeather API key not found in environment variables")

        # Call OpenWeather API
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        weather_type = weather_data['weather']['main']
        valid_weather_type = is_valid_weather_type(weather_type)

        if valid_weather_type:
            handle_weather_type(weather_type)

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}, 500
