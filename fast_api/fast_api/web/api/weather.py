"""Weather API routes - fetch, save, list, delete."""
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.db.dependencies import get_db_session
from fast_api.db.models.saved_weather import SavedWeather
from fast_api.db.models.user import User
from fast_api.services.dependencies import get_current_user
from fast_api.services.weather import fetch_weather

router = APIRouter(prefix="/weather", tags=["weather"])


class WeatherData(BaseModel):
    """Weather data schema."""

    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    icon: str


class SavedWeatherResponse(WeatherData):
    """Saved weather entry with metadata."""

    id: uuid.UUID
    saved_at: datetime

    model_config = {"from_attributes": True}


@router.get("/current", response_model=WeatherData)
async def get_current_weather(
    city: str,
    current_user: User = Depends(get_current_user),
) -> WeatherData:
    """Fetch live weather for a city (requires auth)."""
    try:
        data = await fetch_weather(city)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find weather for '{city}'. Check the city name.",
        )
    return WeatherData(**data)


@router.post("/save", response_model=SavedWeatherResponse, status_code=status.HTTP_201_CREATED)
async def save_weather(
    body: WeatherData,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> SavedWeatherResponse:
    """Save a weather snapshot for the current user."""
    entry = SavedWeather(
        user_id=current_user.id,
        **body.model_dump(),
    )
    db.add(entry)
    await db.flush()
    await db.refresh(entry)
    return SavedWeatherResponse.model_validate(entry)


@router.get("/saved", response_model=list[SavedWeatherResponse])
async def get_saved_weather(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[SavedWeatherResponse]:
    """Get all weather entries saved by the current user."""
    result = await db.execute(
        select(SavedWeather)
        .where(SavedWeather.user_id == current_user.id)
        .order_by(SavedWeather.saved_at.desc()),
    )
    entries = result.scalars().all()
    return [SavedWeatherResponse.model_validate(e) for e in entries]


@router.delete("/saved/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_weather(
    entry_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete a saved weather entry belonging to the current user."""
    result = await db.execute(
        select(SavedWeather).where(
            SavedWeather.id == entry_id,
            SavedWeather.user_id == current_user.id,
        ),
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    await db.delete(entry)