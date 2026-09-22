"""CivicBrain application entrypoint and ASGI factory."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from civicbrain.api.middleware import SecurityHeadersMiddleware
from civicbrain.api.v1 import api_v1_router
from civicbrain.infra.config import settings
from civicbrain.infra.logging import PIIScrubbingFilter

# Configure logging with automated PII scrubbing filter
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("civicbrain")
pii_filter = PIIScrubbingFilter()
logger.addFilter(pii_filter)
for handler in logging.root.handlers:
    handler.addFilter(pii_filter)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
    logger.info(f"CORS origins configured: {settings.cors_origins_list}")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


app = FastAPI(
    title="CivicBrain API",
    description=(
        "Deterministic, glass-box civic triage and dispatch platform built for Indian Urban Local Bodies (ULBs). "
        "Operates with zero assumed government data or IoT sensors via Bühlmann credibility self-bootstrapping."
    ),
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# 1. Global Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# 2. Configure CORS with explicit allowlist
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches unhandled exceptions, logging internally without leaking stack traces or SQL."""
    logger.error(
        "Unhandled server exception on %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please contact municipal operations support.",
            "error_code": "INTERNAL_SERVER_ERROR",
        },
    )


# Mount API v1 router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect or direct reference to API docs."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "health_url": f"{settings.API_V1_STR}/health",
    }
