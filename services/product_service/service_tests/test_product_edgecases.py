import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from services.product_service.app.main import create_app


@pytest.mark.asyncio
async def test_create_product_missing_fields_returns_422():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # missing price
        r = await client.post("/products/", json={"name": "NoPrice"})
        assert r.status_code == 422

        # missing name
        r2 = await client.post("/products/", json={"price": 9.99})
        assert r2.status_code == 422


@pytest.mark.asyncio
async def test_get_nonexistent_product_returns_404():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/products/nonexistent-id")
        assert r.status_code == 404
