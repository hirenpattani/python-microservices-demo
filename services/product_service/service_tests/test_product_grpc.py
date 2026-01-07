import pytest
from services.product_service.app.crud import ProductRepository
from services.product_service.app.grpc_service import ProductServicer
from services.product_service.app import product_pb2
from libs.common.models import ProductCreate


@pytest.fixture
def product_repo():
    """Create a fresh ProductRepository for each test."""
    return ProductRepository()


@pytest.fixture
async def grpc_servicer(product_repo):
    """Create a gRPC ProductServicer."""
    return ProductServicer(product_repo)


@pytest.mark.asyncio
async def test_create_product_grpc(product_repo):
    """Test creating a product via gRPC."""
    servicer = ProductServicer(product_repo)

    request = product_pb2.ProductCreateRequest(
        name="Laptop", price=999.99, user_id="u_alice"
    )
    response = await servicer.CreateProduct(request, None)

    assert response.id.startswith("p_")
    assert response.name == "Laptop"
    assert response.price == 999.99
    assert response.user_id == "u_alice"


@pytest.mark.asyncio
async def test_create_product_without_user_grpc(product_repo):
    """Test creating a product without user_id via gRPC."""
    servicer = ProductServicer(product_repo)

    request = product_pb2.ProductCreateRequest(name="Phone", price=499.99)
    response = await servicer.CreateProduct(request, None)

    assert response.id.startswith("p_")
    assert response.name == "Phone"
    assert response.price == 499.99
    assert response.user_id == ""


@pytest.mark.asyncio
async def test_get_product_grpc(product_repo):
    """Test getting a product via gRPC."""
    servicer = ProductServicer(product_repo)

    # Create product
    product = await product_repo.create(
        ProductCreate(name="Tablet", price=399.99, user_id="u_bob")
    )

    # Get product via gRPC
    request = product_pb2.GetProductRequest(product_id=product.id)
    response = await servicer.GetProduct(request, None)

    assert response.id == product.id
    assert response.name == "Tablet"
    assert response.price == 399.99
    assert response.user_id == "u_bob"


@pytest.mark.asyncio
async def test_list_products_grpc(product_repo):
    """Test listing products via gRPC."""
    servicer = ProductServicer(product_repo)

    # Create products
    await product_repo.create(
        ProductCreate(name="Monitor", price=299.99, user_id="u_charlie")
    )
    await product_repo.create(
        ProductCreate(name="Keyboard", price=79.99, user_id="u_diana")
    )

    # List products via gRPC
    request = product_pb2.ListProductsRequest()
    response = await servicer.ListProducts(request, None)

    assert len(response.products) == 2
    assert response.products[0].name in ["Monitor", "Keyboard"]
    assert response.products[1].name in ["Monitor", "Keyboard"]
