"""SQLAlchemy declarative base."""
from sqlalchemy.orm import DeclarativeBase

from fast_api.db.meta import meta


class Base(DeclarativeBase):
    """Base class for all database models."""

    metadata = meta
