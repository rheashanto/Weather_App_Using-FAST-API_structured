"""Pydantic schemas for the auth feature module."""
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    """Request body for user signup."""

    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response returned after successful signup or login."""

    access_token: str
    token_type: str = "bearer"
    username: str
