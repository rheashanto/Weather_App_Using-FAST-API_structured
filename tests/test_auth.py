"""Auth endpoint tests — signup and login."""
import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_signup_success(client: AsyncClient) -> None:
    """Signup with valid data should return 201 and a token."""
    response = await client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "testuser"


@pytest.mark.anyio
async def test_signup_duplicate_email(client: AsyncClient) -> None:
    """Signing up with an already registered email should return 400."""
    payload = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "password123",
    }
    await client.post("/api/auth/signup", json=payload)
    response = await client.post(
        "/api/auth/signup",
        json={**payload, "username": "user2"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_success(client: AsyncClient) -> None:
    """Login with correct credentials should return a token."""
    await client.post(
        "/api/auth/signup",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "mypassword",
        },
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "mypassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.anyio
async def test_login_wrong_password(client: AsyncClient) -> None:
    """Login with wrong password should return 401."""
    await client.post(
        "/api/auth/signup",
        json={
            "email": "wrong@example.com",
            "username": "wronguser",
            "password": "correctpass",
        },
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_protected_route_without_token(client: AsyncClient) -> None:
    """Accessing a protected route without token should return 401."""
    response = await client.get("/api/weather/saved")
    assert response.status_code == 401
