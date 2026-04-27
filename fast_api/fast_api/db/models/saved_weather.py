"""SavedWeather database model."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_api.db.base import Base


class SavedWeather(Base):
    """Saved weather snapshot for a user."""

    __tablename__ = "saved_weather"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(10), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    feels_like: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    icon: Mapped[str] = mapped_column(String(20), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship("User", back_populates="saved_weather")