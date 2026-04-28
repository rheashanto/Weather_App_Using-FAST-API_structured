"""Weather service — fetches live weather from OpenWeatherMap API."""
import httpx

from fast_api.settings import settings

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"


async def fetch_weather(city: str) -> dict:
    """
    Fetch current weather data for a city from OpenWeatherMap.

    :param city: city name to search for.
    :return: dict with weather fields.
    :raises httpx.HTTPStatusError: if the API returns 4xx/5xx.
    :raises httpx.RequestError: if a network error occurs.
    """
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
