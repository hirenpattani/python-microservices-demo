from typing import Dict, List, Optional

from libs.common.models import Product, ProductCreate
from libs.common.utils import generate_id
from libs.common.logging import get_logger

logger = get_logger(__name__)


class ProductRepository:
    def __init__(self) -> None:
        self._store: Dict[str, Product] = {}

    async def create(self, payload: ProductCreate) -> Product:
        """Create a new product.

        Args:
            payload: ProductCreate model with name, price, and optional user_id.

        Returns:
            Product: Created product with generated ID.
        """
        product_id = generate_id("p_")
        product = Product(id=product_id, **payload.model_dump())
        self._store[product_id] = product
        logger.info(f"Created product: {product_id}")
        return product

    async def get(self, product_id: str) -> Optional[Product]:
        """Get a product by ID.

        Args:
            product_id: The product ID to retrieve.

        Returns:
            Product or None if not found.
        """
        return self._store.get(product_id)

    async def list_all(self) -> List[Product]:
        """List all products.

        Returns:
            List of all products in repository.
        """
        return list(self._store.values())
