import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from services.user_service.app.main import create_app as create_user_app
from services.product_service.app.main import create_app as create_product_app


@pytest.mark.asyncio
async def test_create_user_and_product_and_list_them():
    user_app = create_user_app()
    product_app = create_product_app()

    user_transport = ASGITransport(app=user_app)
    product_transport = ASGITransport(app=product_app)

    async with AsyncClient(
        transport=user_transport, base_url="http://user"
    ) as user_client:
        async with AsyncClient(
            transport=product_transport, base_url="http://product"
        ) as product_client:
            # create a user
            rr = await user_client.post(
                "/users/", json={"name": "I1", "email": "i1@example.com"}
            )
            assert rr.status_code == 200
            uid = rr.json()["id"]

            # create a product
            rp = await product_client.post(
                "/products/", json={"name": "P1", "price": 1.23}
            )
            assert rp.status_code == 200
            pid = rp.json()["id"]

            # list users and products
            lu = await user_client.get("/users/")
            assert any(u["id"] == uid for u in lu.json())

            lp = await product_client.get("/products/")
            assert any(p["id"] == pid for p in lp.json())
