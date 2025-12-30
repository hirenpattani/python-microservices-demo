"""User service FastAPI application."""

from fastapi import FastAPI, Request
from services.user_service.app.api.routes import router as user_router
from libs.common.logging import get_logger
from libs.common.metrics import Metrics
import time


def create_app() -> FastAPI:
    app = FastAPI(title="User Service")
    app.include_router(user_router, prefix="/users", tags=["users"])

    # logging and metrics
    app.logger = get_logger("user_service")
    app.state.metrics = Metrics()

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start = time.monotonic()
        app.state.metrics.inc("requests_total")
        response = await call_next(request)
        duration = time.monotonic() - start
        # record quick duration metric (rounded ms)
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
