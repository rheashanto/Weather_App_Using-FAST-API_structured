"""Weather service - fetch data from OpenWeatherMap API."""
import httpx

from fast_api.settings import settings

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"


async def fetch_weather(city: str) -> dict:
    """Fetch current weather data from OpenWeatherMap API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{OPENWEATHER_BASE_URL}/weather",
            params={
                "q": city,
                "appid": settings.openweather_api_key,
                "units": "metric",
            },
        )
        response.raise_for_status()
        data = response.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize(),
        "wind_speed": data["wind"]["speed"],
        "icon": data["weather"][0]["icon"],
    }