import pytest
from httpx import AsyncClient
from services.product_service.app.main import create_app


@pytest.mark.asyncio
async def test_create_and_get_product():
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.post("/products/", json={"name": "Widget", "price": 12.5})
        assert r.status_code == 200
        body = r.json()
        assert "id" in body
        product_id = body["id"]

        r2 = await client.get(f"/products/{product_id}")
        assert r2.status_code == 200
        assert r2.json()["name"] == "Widget"

        r3 = await client.get("/products/")
        assert r3.status_code == 200
        assert len(r3.json()) >= 1
