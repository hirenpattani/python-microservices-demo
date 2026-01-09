import time
import uuid

from fastapi import FastAPI, Request
from monolith.app.api import users as users_routes
from monolith.app.api import products as products_routes
from monolith.app.crud.users import UserRepository
from monolith.app.crud.products import ProductRepository
from libs.common.logging import get_logger
from libs.common.metrics import Metrics
from libs.common.context import set_tracking_id


def create_app() -> FastAPI:
    """Create and configure the monolith FastAPI application.

    A single application handling both User and Product domains.
    Demonstrates tighter coupling compared to microservices.

    Sets up:
        - Shared data layer (user and product repositories in same app)
        - API routes for both domains
        - Structured logging with tracking IDs
        - Request/response metrics collection
        - Health and metrics endpoints

    Returns:
        A configured FastAPI application instance.
    """
    app = FastAPI(
        title="Monolith Application",
        description="Single application with User and Product domains",
    )

    # Initialize repositories (shared in-memory stores)
    user_repo = UserRepository()
    product_repo = ProductRepository()
    app.state.user_repo = user_repo
    app.state.product_repo = product_repo

    # Dependency override functions that use app-level repos
    def get_user_repo():
        return user_repo

    def get_product_repo():
        return product_repo

    # Register routes with prefixes
    app.include_router(users_routes.router, prefix="/users", tags=["users"])
    app.include_router(products_routes.router, prefix="/products", tags=["products"])

    # Override dependencies to use app-level repos
    app.dependency_overrides[users_routes.get_repo] = get_user_repo
    app.dependency_overrides[products_routes.get_repo] = get_product_repo

    # logging and metrics
    app.logger = get_logger("monolith")
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
