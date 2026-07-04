import pytest
from httpx import AsyncClient
from app.core.settings import get_settings

settings = get_settings()

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project": settings.PROJECT_NAME}
