"""In-memory repository for product objects (demo only)."""

from typing import Dict, List, Optional
from libs.common.models import Product, ProductCreate
from libs.common.utils import generate_id


class ProductRepository:
    def __init__(self) -> None:
        self._store: Dict[str, Product] = {}

    async def create(self, payload: ProductCreate) -> Product:
        product_id = generate_id("p_")
        # Use `model_dump()` for Pydantic v2 compatibility (replaces `dict()`)
        product = Product(id=product_id, **payload.model_dump())
        self._store[product_id] = product
        try:
            from libs.common.logging import get_logger

            get_logger(__name__).info("created product %s", product_id)
        except Exception:
            pass
        return product

    async def get(self, product_id: str) -> Optional[Product]:
        return self._store.get(product_id)

    async def list_all(self) -> List[Product]:
        return list(self._store.values())
