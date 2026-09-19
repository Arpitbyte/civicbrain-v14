"""Health and readiness diagnostic endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from civicbrain.infra.config import settings
from civicbrain.infra.database import check_database_connection
from civicbrain.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Liveness Probe",
    description="Returns basic system liveness status, version, and current environment.",
)
async def health_check() -> HealthResponse:
    """Liveness probe to confirm that the FastAPI process is running."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(UTC),
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Readiness Probe",
    description="Validates that database and backing infrastructure dependencies are reachable.",
)
async def readiness_check():
    """Readiness probe checking database connectivity."""
    db_ok, db_msg = await check_database_connection()

    # Redis check placeholder for Phase 0 (Upstash Redis)
    redis_ok = True
    redis_msg = "Redis check deferred to worker configuration"

    is_ready = db_ok
    status_str = "ready" if is_ready else "degraded"
    http_status = status.HTTP_200_OK if is_ready else status.HTTP_503_SERVICE_UNAVAILABLE

    response_data = ReadinessResponse(
        status=status_str,
        database_connected=db_ok,
        redis_connected=redis_ok,
        timestamp=datetime.now(UTC),
        details={
            "database": db_msg,
            "redis": redis_msg,
        },
    )

    if not is_ready:
        return JSONResponse(
            status_code=http_status,
            content=response_data.model_dump(mode="json"),
        )

    return response_data
