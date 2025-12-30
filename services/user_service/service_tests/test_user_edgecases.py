import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from services.user_service.app.main import create_app


@pytest.mark.asyncio
async def test_create_user_missing_fields_returns_422():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # missing email
        r = await client.post("/users/", json={"name": "NoEmail"})
        assert r.status_code == 422

        # missing name
        r2 = await client.post("/users/", json={"email": "no-name@example.com"})
        assert r2.status_code == 422


@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_404():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/users/nonexistent-id")
        assert r.status_code == 404
