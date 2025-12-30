import pytest
from httpx import AsyncClient
from services.user_service.app.main import create_app


@pytest.mark.asyncio
async def test_create_and_get_user():
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        # create
        r = await client.post(
            "/users/", json={"name": "Alice", "email": "alice@example.com"}
        )
        assert r.status_code == 200
        body = r.json()
        assert "id" in body
        user_id = body["id"]

        # get
        r2 = await client.get(f"/users/{user_id}")
        assert r2.status_code == 200
        assert r2.json()["email"] == "alice@example.com"

        # list
        r3 = await client.get("/users/")
        assert r3.status_code == 200
        assert len(r3.json()) >= 1
