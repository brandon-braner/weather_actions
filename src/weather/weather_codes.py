WEATHER_CODES = {
    "Thunderstorm": {
        "200": "thunderstorm with light rain",
        "201": "thunderstorm with rain",
        "202": "thunderstorm with heavy rain",
        "210": "light thunderstorm",
        "211": "thunderstorm",
        "212": "heavy thunderstorm",
        "221": "ragged thunderstorm",
        "230": "thunderstorm with light drizzle",
        "231": "thunderstorm with drizzle",
        "232": "thunderstorm with heavy drizzle"
    },
    "Drizzle": {
        "300": "light intensity drizzle",
        "301": "drizzle",
        "302": "heavy intensity drizzle",
        "310": "light intensity drizzle rain",
        "311": "drizzle rain",
        "312": "heavy intensity drizzle rain",
        "313": "shower rain and drizzle",
        "314": "heavy shower rain and drizzle",
        "321": "shower drizzle"
    },
    "Rain": {
        "500": "light rain",
        "501": "moderate rain",
        "502": "heavy intensity rain",
        "503": "very heavy rain",
        "504": "extreme rain",
        "511": "freezing rain",
        "520": "light intensity shower rain",
        "521": "shower rain",
        "522": "heavy intensity shower rain",
        "531": "ragged shower rain"
    },
    "Snow": {
        "600": "light snow",
        "601": "snow",
        "602": "heavy snow",
        "611": "sleet",
        "612": "light shower sleet",
        "613": "shower sleet",
        "615": "light rain and snow",
        "616": "rain and snow",
        "620": "light shower snow",
        "621": "shower snow",
        "622": "heavy shower snow"
    },
    "Clear": {
        "800": "clear sky"
    },
    "Clouds": {
        "801": "few clouds: 11-25%",
        "802": "scattered clouds: 25-50%",
        "803": "broken clouds: 51-84%",
        "804": "overcast clouds: 85-100%"
    }
}

def get_weather_type(weather_id: str) -> str:
    """
    Get the main weather type based on the weather ID
    Returns the main weather type (Thunderstorm, Drizzle, Rain, Snow, Clear, or Clouds)
    """
    weather_id_str = str(weather_id)
    for weather_type, codes in WEATHER_CODES.items():
        if weather_id_str in codes:
            return weather_type
    return "Unknown"

def get_weather_description(weather_id: str) -> str:
    """
    Get the weather description based on the weather ID
    Returns the detailed weather description
    """
    weather_id_str = str(weather_id)
    for weather_type, codes in WEATHER_CODES.items():
        if weather_id_str in codes:
            return codes[weather_id_str]
    return "Unknown weather condition"

def is_valid_weather_type(weather_type: str) -> bool:
    return weather_type in WEATHER_CODES.keys()
