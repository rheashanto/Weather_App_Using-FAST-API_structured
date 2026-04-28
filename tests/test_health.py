"""Health check endpoint tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_check(client: AsyncClient) -> None:
    """Health endpoint should return 200 with status ok."""
    response = await client.get("/api/monitoring/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
