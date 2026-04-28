"""Weather Data Access Object."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.db.models.saved_weather_model import SavedWeather


class WeatherDAO:
    """Handles all database operations for the SavedWeather model."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(
        self,
        user_id: uuid.UUID,
        city: str,
        country: str,
        temperature: float,
        feels_like: float,
        humidity: int,
        description: str,
        wind_speed: float,
        icon: str,
    ) -> SavedWeather:
        """Save a weather snapshot for a user."""
        entry = SavedWeather(
            user_id=user_id,
            city=city,
            country=country,
            temperature=temperature,
            feels_like=feels_like,
            humidity=humidity,
            description=description,
            wind_speed=wind_speed,
            icon=icon,
        )
        self.session.add(entry)
        await self.session.flush()
        await self.session.refresh(entry)
        return entry

    async def get_by_user(self, user_id: uuid.UUID) -> list[SavedWeather]:
        """Get all saved weather entries for a user, newest first."""
        result = await self.session.execute(
            select(SavedWeather)
            .where(SavedWeather.user_id == user_id)
            .order_by(SavedWeather.saved_at.desc()),
        )
        return list(result.scalars().all())

    async def delete(self, entry_id: uuid.UUID, user_id: uuid.UUID) -> SavedWeather | None:
        """Delete a saved entry belonging to the given user."""
        result = await self.session.execute(
            select(SavedWeather).where(
                SavedWeather.id == entry_id,
                SavedWeather.user_id == user_id,
            ),
        )
        entry = result.scalar_one_or_none()
        if entry:
            await self.session.delete(entry)
            await self.session.flush()  # surface errors at DAO call site, not at commit
        return entry
