import os
import functions_framework
import requests
from datetime import datetime
from weather.weather_codes import get_weather_type, get_weather_description

def check_for_snow(weather_data):
    """Check if current weather conditions include snow"""
    if 'weather' not in weather_data or not weather_data['weather']:
        return False
    
    # Get the weather ID from the first weather condition
    weather_id = str(weather_data['weather'][0]['id'])
    weather_type = get_weather_type(weather_id)
    
    return weather_type == "Snow"

def notify_ifttt():
    """Mock function to notify IFTTT"""
    # TODO: Implement actual IFTTT integration
    print("IFTTT notification sent: It's snowing!")
    return True

@functions_framework.http
def check_weather(request):
    """Cloud Function entry point"""
    try:
        # Get environment variables
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        lat = os.environ.get('WEATHER_LAT', '40.7128')  # Default to NYC
        lon = os.environ.get('WEATHER_LON', '-74.0060')

        if not api_key:
            raise ValueError("OpenWeather API key not found in environment variables")

        # Call OpenWeather API
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        # Check if it's snowing
        if check_for_snow(weather_data):
            notify_ifttt()
            return {
                "message": "Snow detected! IFTTT notification sent.",
                "weather": {
                    "type": "Snow",
                    "description": get_weather_description(weather_data['weather'][0]['id'])
                },
                "timestamp": datetime.now().isoformat()
            }
        
        # Return current weather info even if it's not snowing
        return {
            "message": "No snow detected",
            "weather": {
                "type": get_weather_type(weather_data['weather'][0]['id']),
                "description": get_weather_description(weather_data['weather'][0]['id'])
            },
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}, 500
