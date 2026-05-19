"""
FastAPI main application.

Defines the API application, middleware, and health check endpoint.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import uvicorn

from thermaguard.config import settings
from thermaguard.logger import logger
from thermaguard.api.routes import ingest, forecast, alerts, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    yield
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Predictive Cold-Chain Monitoring System with AI",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include routers
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(forecast.router, prefix="/api/v1", tags=["forecast"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
app.include_router(status.router, prefix="/api/v1", tags=["status"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-15T10:30:00Z",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


def run_server():
    """Run the FastAPI server with Uvicorn."""
    uvicorn.run(
        "thermaguard.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers if not settings.debug else 1,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run_server()
