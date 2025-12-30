"""Product service FastAPI application."""

from fastapi import FastAPI, Request
from services.product_service.app.api.routes import router as product_router
from libs.common.logging import get_logger
from libs.common.metrics import Metrics
import time


def create_app() -> FastAPI:
    app = FastAPI(title="Product Service")
    app.include_router(product_router, prefix="/products", tags=["products"])

    # logging and metrics
    app.logger = get_logger("product_service")
    app.state.metrics = Metrics()

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start = time.monotonic()
        app.state.metrics.inc("requests_total")
        response = await call_next(request)
        duration = time.monotonic() - start
        ms = int(duration * 1000)
        app.state.metrics.inc(f"request_ms_{ms}")
        return response

    @app.get("/health")
    def health():
        app.logger.info("health check")
        return {"status": "ok"}

    @app.get("/metrics")
    def metrics():
        return app.state.metrics.snapshot()

    return app


app = create_app()
