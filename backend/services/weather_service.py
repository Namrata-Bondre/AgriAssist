"""
Weather service powered by the OpenWeatherMap API.

The API key is read from environment variables (loaded via python-dotenv
in main.py). No secrets are hardcoded.
"""

import os
from typing import Any

import httpx

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherServiceError(Exception):
    """Raised when weather data cannot be retrieved."""

    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def get_weather(city: str) -> dict[str, Any]:
    """Fetch current weather data for a given city from OpenWeatherMap."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherServiceError("OPENWEATHER_API_KEY is not configured in the environment.", 500)

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(OPENWEATHER_URL, params=params)
    except httpx.RequestError as exc:
        raise WeatherServiceError(f"Could not reach OpenWeatherMap API: {exc}", 502) from exc

    if response.status_code == 404:
        raise WeatherServiceError(f"City '{city}' was not found.", 404)

    if response.status_code != 200:
        raise WeatherServiceError(
            f"OpenWeatherMap API returned an error (status {response.status_code}).",
            502,
        )

    data = response.json()

    try:
        return {
            "city": data.get("name", city),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "wind_speed": data["wind"]["speed"],
        }
    except (KeyError, IndexError, TypeError) as exc:
        raise WeatherServiceError("OpenWeatherMap response was in an unexpected format.", 502) from exc
