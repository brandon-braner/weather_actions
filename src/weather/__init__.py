from . import handle_snow

def handle_weather_type(weather_type: str):
    match weather_type:
        case "snow":
            handle_snow.handle_snow()
        case "Clouds":
            print("Handling Clouds")
        case "Clear":
            print("Handling Clear")
        case "Rain":
            print("Handling Rain")
        case "Drizzle":
            print("Handling Drizzle")
        case "Thunderstorm":
            print("Handling Thunderstorm")
        case _:
            print("Unknown weather type")
    