"""Auth endpoint handlers — signup and login."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.db.dao.user_dao import UserDAO
from fast_api.db.dependencies import get_db_session
from fast_api.services.auth import (
    create_access_token,
    hash_password,
    verify_password,
)
from fast_api.web.api.auth.schema import LoginRequest, SignupRequest, TokenResponse

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: SignupRequest,
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """Register a new user and return a JWT token."""
    user_dao = UserDAO(db)

    existing = await user_dao.get_by_email(body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = await user_dao.create(
        email=body.email,
        username=body.username,
        hashed_password=hash_password(body.password),
    )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, username=user.username)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """Authenticate a user and return a JWT token."""
    user_dao = UserDAO(db)

    user = await user_dao.get_by_email(body.email)
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, username=user.username)
