"""User Data Access Object."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.db.models.user_model import User


class UserDAO:
    """Handles all database operations for the User model."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email address."""
        result = await self.session.execute(
            select(User).where(User.email == email),
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Fetch a user by their UUID."""
        result = await self.session.execute(
            select(User).where(User.id == user_id),
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        username: str,
        hashed_password: str,
    ) -> User:
        """Create and persist a new user."""
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
