from typing import List

from fastapi import APIRouter, Depends, HTTPException

from libs.common.models import ProductCreate, Product
from libs.common.http_client import check_user_exists
from services.product_service.app.crud import ProductRepository

router = APIRouter()


# Single repository instance for demo/testing purposes
_repo = ProductRepository()


def get_repo() -> ProductRepository:
    """Dependency that returns the shared repository instance.

    Returns:
        The shared ProductRepository instance.
    """
    return _repo


@router.post("/", response_model=Product)
async def create_product(
    payload: ProductCreate, repo: ProductRepository = Depends(get_repo)
) -> Product:
    """Create a new product.

    Args:
        payload: Product data (name, price, optional user_id).
        repo: Injected repository instance.

    Returns:
        The created product with a unique ID.

    Raises:
        HTTPException: If user_id is provided but user doesn't exist.
    """
    # If user_id is provided, validate it exists (inter-service call)
    if payload.user_id:
        user_exists = await check_user_exists(payload.user_id)
        if not user_exists:
            raise HTTPException(status_code=422, detail="user not found")

    product = await repo.create(payload)
    return product


@router.get("/", response_model=List[Product])
async def list_products(repo: ProductRepository = Depends(get_repo)) -> List[Product]:
    """List all products.

    Args:
        repo: Injected repository instance.

    Returns:
        List of all products.
    """
    return await repo.list_all()


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str, repo: ProductRepository = Depends(get_repo)
) -> Product:
    """Get a specific product by ID.

    Args:
        product_id: The product ID.
        repo: Injected repository instance.

    Returns:
        The product with the given ID.

    Raises:
        HTTPException: If product not found.
    """
    product = await repo.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product
