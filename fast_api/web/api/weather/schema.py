"""Pydantic schemas for the weather feature module."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class WeatherData(BaseModel):
    """Live weather data returned from OpenWeatherMap."""

    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    icon: str


class SavedWeatherResponse(WeatherData):
    """A saved weather snapshot with metadata."""

    id: uuid.UUID
    saved_at: datetime

    model_config = {"from_attributes": True}
