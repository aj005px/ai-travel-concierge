import requests
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather and 3-day forecast for a travel destination city."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=10)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"City '{city}' not found. Please check the city name."

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        country = location.get("country", "")

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
            f"&daily=temperature_2m_max,temperature_2m_min"
            f"&timezone=auto&forecast_days=3"
        )
        weather_response = requests.get(weather_url, timeout=10)
        weather_data = weather_response.json()

        current = weather_data["current"]
        daily = weather_data["daily"]

        return f"""
🌤️ Weather in {city}, {country}:
- Temperature: {current['temperature_2m']}°C
- Humidity: {current['relative_humidity_2m']}%
- Wind Speed: {current['wind_speed_10m']} km/h

📅 3-Day Forecast:
- Today: {daily['temperature_2m_min'][0]}°C to {daily['temperature_2m_max'][0]}°C
- Tomorrow: {daily['temperature_2m_min'][1]}°C to {daily['temperature_2m_max'][1]}°C
- Day 3: {daily['temperature_2m_min'][2]}°C to {daily['temperature_2m_max'][2]}°C
"""
    except requests.exceptions.Timeout:
        return "Weather request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Cannot connect to weather service."
    except Exception as e:
        return f"Weather error: {str(e)}"
