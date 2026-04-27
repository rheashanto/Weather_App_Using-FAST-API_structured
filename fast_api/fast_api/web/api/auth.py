"""Auth API routes - signup and login endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.db.dependencies import get_db_session
from fast_api.db.models.user import User
from fast_api.services.auth import (
    authenticate_user,
    create_access_token,
    get_user_by_email,
    hash_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    """Signup request body."""

    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    """Login request body."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response."""

    access_token: str
    token_type: str = "bearer"
    username: str


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: SignupRequest,
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """Register a new user."""
    existing = await get_user_by_email(db, body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=body.email,
        username=body.username,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, username=user.username)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """Login and get an access token."""
    user = await authenticate_user(db, body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, username=user.username)