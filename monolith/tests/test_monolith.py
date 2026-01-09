import pytest
from httpx import AsyncClient, ASGITransport

from monolith.app.main import create_app


@pytest.fixture
async def client():
    """Create a fresh test client for the monolith app with clean repos."""
    # Create a fresh app for each test to avoid state sharing
    app = create_app()
    # Reset the app state by clearing repositories
    app.state.user_repo._store.clear()
    app.state.product_repo._store.clear()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_user(client):
    """Test creating a user in monolith."""
    payload = {"name": "Alice", "email": "alice@example.com"}
    response = await client.post("/users", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("u_")
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_get_user(client):
    """Test getting a user from monolith."""
    # Create a user
    create_response = await client.post(
        "/users", json={"name": "Bob", "email": "bob@example.com"}
    )
    user_id = create_response.json()["id"]

    # Get the user
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Bob"


@pytest.mark.asyncio
async def test_list_users(client):
    """Test listing all users in monolith."""
    # Create multiple users
    await client.post(
        "/users", json={"name": "Charlie", "email": "charlie@example.com"}
    )
    await client.post("/users", json={"name": "Diana", "email": "diana@example.com"})

    # List users
    response = await client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_create_product(client):
    """Test creating a product in monolith."""
    payload = {"name": "Laptop", "price": 999.99, "user_id": None}
    response = await client.post("/products", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("p_")
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99


@pytest.mark.asyncio
async def test_get_product(client):
    """Test getting a product from monolith."""
    # Create a product
    create_response = await client.post(
        "/products", json={"name": "Phone", "price": 499.99}
    )
    product_id = create_response.json()["id"]

    # Get the product
    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Phone"


@pytest.mark.asyncio
async def test_list_products(client):
    """Test listing all products in monolith."""
    # Create multiple products
    await client.post("/products", json={"name": "Monitor", "price": 299.99})
    await client.post("/products", json={"name": "Keyboard", "price": 79.99})

    # List products
    response = await client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_nonexistent_user(client):
    """Test getting non-existent user returns 404."""
    response = await client.get("/users/u_nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_product(client):
    """Test getting non-existent product returns 404."""
    response = await client.get("/products/p_nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    # Make some requests to generate metrics
    await client.get("/health")
    await client.get("/users")

    # Check metrics
    response = await client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "uptime_seconds" in data
    assert "counters" in data
    assert data["counters"]["requests_total"] >= 3  # health + users + metrics call


@pytest.mark.asyncio
async def test_monolith_shared_data_layer(client):
    """Test that monolith shares data layer between domains.

    This is a key difference from microservices:
    in monolith, user and product repos are in same process.
    """
    # Create a user
    user_response = await client.post(
        "/users", json={"name": "Eve", "email": "eve@example.com"}
    )
    user_id = user_response.json()["id"]

    # Create a product linked to the user (same data layer)
    product_response = await client.post(
        "/products", json={"name": "Tablet", "price": 399.99, "user_id": user_id}
    )
    product = product_response.json()

    # Verify user can still be retrieved (no separate service call needed)
    user_check = await client.get(f"/users/{user_id}")
    assert user_check.status_code == 200
    assert user_check.json()["id"] == user_id

    # Product has reference to user (all in same memory)
    # Note: Pydantic v1 includes user_id in response when it's provided
    assert product.get("user_id") == user_id or product.get("user_id") is not None
