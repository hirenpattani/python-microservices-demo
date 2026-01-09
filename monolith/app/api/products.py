from typing import List

from fastapi import APIRouter, Depends, HTTPException

from libs.common.models import ProductCreate, Product
from monolith.app.crud.products import ProductRepository

router = APIRouter()

_repo = ProductRepository()


def get_repo() -> ProductRepository:
    """Dependency injection for ProductRepository."""
    return _repo


@router.post("", response_model=Product)
async def create_product(
    payload: ProductCreate, repo: ProductRepository = Depends(get_repo)
):
    """Create a new product.

    In monolith, validation is local (same database).

    Args:
        payload: ProductCreate with name, price, optional user_id.
        repo: Injected ProductRepository.

    Returns:
        Product: Created product with ID.
    """
    # In monolith, we skip external user validation
    # since everything is in-process (same database)
    return await repo.create(payload)


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str, repo: ProductRepository = Depends(get_repo)):
    """Get a product by ID.

    Args:
        product_id: Product ID to retrieve.
        repo: Injected ProductRepository.

    Returns:
        Product: Product details.

    Raises:
        HTTPException: 404 if product not found.
    """
    product = await repo.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("", response_model=List[Product])
async def list_products(repo: ProductRepository = Depends(get_repo)):
    """List all products.

    Args:
        repo: Injected ProductRepository.

    Returns:
        List[Product]: All products in the system.
    """
    return await repo.list_all()
