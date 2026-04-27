"""Weather endpoint handlers — fetch, save, list, delete."""
import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.db.dao.weather_dao import WeatherDAO
from fast_api.db.dependencies import get_db_session
from fast_api.db.models.user_model import User
from fast_api.services.dependencies import get_current_user
from fast_api.services.weather import fetch_weather
from fast_api.web.api.weather.schema import SavedWeatherResponse, WeatherData

router = APIRouter()


@router.get("/current", response_model=WeatherData)
async def get_current_weather(
    city: str,
    current_user: User = Depends(get_current_user),
) -> WeatherData:
    """Fetch live weather for a city from OpenWeatherMap (requires auth)."""
    try:
        data = await fetch_weather(city)
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find weather for '{city}'. Check the city name.",
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weather service is currently unavailable. Try again later.",
        )
    return WeatherData(**data)


@router.post("/save", response_model=SavedWeatherResponse, status_code=status.HTTP_201_CREATED)
async def save_weather(
    body: WeatherData,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> SavedWeatherResponse:
    """Save a weather snapshot for the currently authenticated user."""
    weather_dao = WeatherDAO(db)
    entry = await weather_dao.save(
        user_id=current_user.id,
        **body.model_dump(),
    )
    return SavedWeatherResponse.model_validate(entry)


@router.get("/saved", response_model=list[SavedWeatherResponse])
async def get_saved_weather(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[SavedWeatherResponse]:
    """Return all weather entries saved by the current user."""
    weather_dao = WeatherDAO(db)
    entries = await weather_dao.get_by_user(current_user.id)
    return [SavedWeatherResponse.model_validate(e) for e in entries]


@router.delete("/saved/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_weather(
    entry_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete a saved weather entry belonging to the current user."""
    weather_dao = WeatherDAO(db)
    entry = await weather_dao.delete(entry_id, current_user.id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )
