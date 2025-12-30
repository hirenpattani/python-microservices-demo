import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from services.product_service.app.main import create_app


@pytest.mark.asyncio
async def test_health_and_metrics():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

        m = await client.get("/metrics")
        assert m.status_code == 200
        assert "uptime_seconds" in m.json()

        await client.get("/products/")
        m2 = await client.get("/metrics")
        assert m2.json()["counters"]["requests_total"] >= 1
