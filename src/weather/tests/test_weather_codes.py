from ..weather_codes import is_valid_weather_type

def test_invalid_weather_types():
    """Test that invalid weather types return False"""
    invalid_types = [
        "Thunder",  # Partial match
        "SNOW",    # Case sensitive
        "rain",    # Case sensitive
        "Foggy",   # Non-existent type
        "",        # Empty string
        "123",     # Numbers
        " Clouds", # Leading space
        "Clouds ", # Trailing space
    ]
    
    for weather_type in invalid_types:
        assert not is_valid_weather_type(weather_type), f"{weather_type} should not be a valid weather type"

def test_each_weather_type_individually():
    """Test each weather type individually for better test failure reporting"""
    assert is_valid_weather_type("Thunderstorm"), "Thunderstorm should be valid"
    assert is_valid_weather_type("Drizzle"), "Drizzle should be valid"
    assert is_valid_weather_type("Rain"), "Rain should be valid"
    assert is_valid_weather_type("Snow"), "Snow should be valid"
    assert is_valid_weather_type("Clear"), "Clear should be valid"
    assert is_valid_weather_type("Clouds"), "Clouds should be valid"
