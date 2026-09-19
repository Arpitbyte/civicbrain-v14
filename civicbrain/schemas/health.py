"""Schemas for health and readiness probes."""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Liveness probe response model."""

    status: str = Field(default="healthy", description="Application health status")
    version: str = Field(description="CivicBrain system version")
    environment: str = Field(description="Operational environment")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="UTC timestamp of response"
    )


class ReadinessResponse(BaseModel):
    """Readiness probe response model."""

    status: str = Field(description="Overall readiness: ready | degraded | unavailable")
    database_connected: bool = Field(description="Database connectivity verification")
    redis_connected: bool = Field(description="Redis connectivity verification")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="UTC timestamp of response"
    )
    details: dict[str, Any] = Field(
        default_factory=dict, description="Component level diagnostic details"
    )
