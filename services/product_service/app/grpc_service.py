import grpc

from libs.common.logging import get_logger
from services.product_service.app.crud import ProductRepository
from services.product_service.app import product_pb2, product_pb2_grpc

logger = get_logger(__name__)


class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    """gRPC service implementation for Product operations."""

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def CreateProduct(
        self,
        request: product_pb2.ProductCreateRequest,
        context: grpc.aio.ServicerContext,
    ) -> product_pb2.Product:
        """Create a new product.

        Args:
            request: ProductCreateRequest with name, price, optional user_id.
            context: gRPC context.

        Returns:
            Product: Created product with ID.
        """
        from libs.common.models import ProductCreate

        payload = ProductCreate(
            name=request.name,
            price=request.price,
            user_id=request.user_id if request.user_id else None,
        )
        product = await self.repo.create(payload)
        logger.info(f"Created product via gRPC: {product.id}")
        return product_pb2.Product(
            id=product.id,
            name=product.name,
            price=product.price,
            user_id=product.user_id or "",
        )

    async def GetProduct(
        self,
        request: product_pb2.GetProductRequest,
        context: grpc.aio.ServicerContext,
    ) -> product_pb2.Product:
        """Get a product by ID.

        Args:
            request: GetProductRequest with product_id.
            context: gRPC context.

        Returns:
            Product: Product details.

        Raises:
            RpcError: If product not found.
        """
        product = await self.repo.get(request.product_id)
        if not product:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")
        logger.info(f"Retrieved product via gRPC: {product.id}")
        return product_pb2.Product(
            id=product.id,
            name=product.name,
            price=product.price,
            user_id=product.user_id or "",
        )

    async def ListProducts(
        self,
        request: product_pb2.ListProductsRequest,
        context: grpc.aio.ServicerContext,
    ) -> product_pb2.ListProductsResponse:
        """List all products.

        Args:
            request: ListProductsRequest.
            context: gRPC context.

        Returns:
            ListProductsResponse: List of all products.
        """
        products = await self.repo.list_all()
        product_messages = [
            product_pb2.Product(
                id=p.id,
                name=p.name,
                price=p.price,
                user_id=p.user_id or "",
            )
            for p in products
        ]
        logger.info(f"Listed {len(products)} products via gRPC")
        return product_pb2.ListProductsResponse(products=product_messages)
