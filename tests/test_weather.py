"""Weather endpoint tests — save, list, delete saved weather."""
import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient, suffix: str = "") -> str:
    """Helper to sign up and return a JWT token."""
    response = await client.post(
        "/api/auth/signup",
        json={
            "email": f"weather{suffix}@example.com",
            "username": f"weatheruser{suffix}",
            "password": "testpassword",
        },
    )
    return response.json()["access_token"]


SAMPLE_WEATHER = {
    "city": "London",
    "country": "GB",
    "temperature": 15.5,
    "feels_like": 13.0,
    "humidity": 72,
    "description": "Partly cloudy",
    "wind_speed": 4.2,
    "icon": "02d",
}


@pytest.mark.anyio
async def test_save_weather(client: AsyncClient) -> None:
    """Saving weather should return 201 with the saved entry."""
    token = await get_auth_token(client, "save")
    response = await client.post(
        "/api/weather/save",
        json=SAMPLE_WEATHER,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["city"] == "London"
    assert data["temperature"] == 15.5
    assert "id" in data
    assert "saved_at" in data


@pytest.mark.anyio
async def test_get_saved_weather(client: AsyncClient) -> None:
    """Saved weather list should return only the current user's entries."""
    token = await get_auth_token(client, "list")
    headers = {"Authorization": f"Bearer {token}"}

    await client.post("/api/weather/save", json=SAMPLE_WEATHER, headers=headers)
    await client.post(
        "/api/weather/save",
        json={**SAMPLE_WEATHER, "city": "Paris", "country": "FR"},
        headers=headers,
    )

    response = await client.get("/api/weather/saved", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["city"] in ("London", "Paris")


@pytest.mark.anyio
async def test_delete_saved_weather(client: AsyncClient) -> None:
    """Deleting a saved entry should return 204 and remove it from the list."""
    token = await get_auth_token(client, "delete")
    headers = {"Authorization": f"Bearer {token}"}

    save_resp = await client.post(
        "/api/weather/save", json=SAMPLE_WEATHER, headers=headers
    )
    entry_id = save_resp.json()["id"]

    delete_resp = await client.delete(
        f"/api/weather/saved/{entry_id}", headers=headers
    )
    assert delete_resp.status_code == 204

    list_resp = await client.get("/api/weather/saved", headers=headers)
    assert all(e["id"] != entry_id for e in list_resp.json())


@pytest.mark.anyio
async def test_user_data_isolation(client: AsyncClient) -> None:
    """User A should not see User B's saved weather."""
    token_a = await get_auth_token(client, "isoa")
    token_b = await get_auth_token(client, "isob")

    await client.post(
        "/api/weather/save",
        json=SAMPLE_WEATHER,
        headers={"Authorization": f"Bearer {token_a}"},
    )

    response = await client.get(
        "/api/weather/saved",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
