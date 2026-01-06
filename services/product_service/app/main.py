import time
import uuid

from fastapi import FastAPI, Request
from services.product_service.app.api.routes import router as product_router
from libs.common.logging import get_logger
from libs.common.metrics import Metrics
from libs.common.context import set_tracking_id


def create_app() -> FastAPI:
    """Create and configure the Product service FastAPI application.

    Sets up:
        - API routes for product CRUD operations.
        - Structured logging with tracking IDs.
        - Request/response metrics collection.
        - Health and metrics endpoints.

    Returns:
        A configured FastAPI application instance.
    """
    app = FastAPI(title="Product Service")
    app.include_router(product_router, prefix="/products", tags=["products"])

    # logging and metrics
    app.logger = get_logger("product_service")
    app.state.metrics = Metrics()

    @app.middleware("http")
    async def metrics_and_tracking_middleware(request: Request, call_next):
        """Middleware to track request metrics and set request tracing ID.

        Args:
            request: The incoming HTTP request.
            call_next: Callable to invoke the next middleware/handler.

        Returns:
            The HTTP response.
        """
        # Generate and set tracking ID for this request
        tracking_id = f"req_{uuid.uuid4().hex[:8]}"
        set_tracking_id(tracking_id)

        # Track metrics
        start = time.monotonic()
        app.state.metrics.inc("requests_total")
        response = await call_next(request)
        duration = time.monotonic() - start
        ms = int(duration * 1000)
        app.state.metrics.inc(f"request_ms_{ms}")

        # Add tracking ID to response headers
        response.headers["X-Tracking-ID"] = tracking_id
        return response

    @app.get("/health")
    def health():
        """Health check endpoint.

        Returns:
            JSON with status "ok".
        """
        app.logger.info("health check")
        return {"status": "ok"}

    @app.get("/metrics")
    def metrics():
        """Metrics endpoint.

        Returns:
            JSON snapshot of current metrics (uptime, request counts).
        """
        return app.state.metrics.snapshot()

    return app


app = create_app()
