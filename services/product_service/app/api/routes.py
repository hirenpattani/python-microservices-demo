"""Product API routes."""

from fastapi import APIRouter, Depends, HTTPException
from libs.common.models import ProductCreate, Product
from services.product_service.app.crud import ProductRepository
from typing import List

router = APIRouter()


# Single repository instance for demo/testing purposes
_repo = ProductRepository()


def get_repo():
    """Dependency that returns the shared repository instance."""
    return _repo


@router.post("/", response_model=Product)
async def create_product(
    payload: ProductCreate, repo: ProductRepository = Depends(get_repo)
) -> Product:
    product = await repo.create(payload)
    return product


@router.get("/", response_model=List[Product])
async def list_products(repo: ProductRepository = Depends(get_repo)) -> List[Product]:
    return await repo.list_all()


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str, repo: ProductRepository = Depends(get_repo)
) -> Product:
    product = await repo.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product
