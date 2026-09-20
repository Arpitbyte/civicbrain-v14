"""Pydantic schemas for citizen intake, observation breakdown, and incident management."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from civicbrain.domain.intake.models import (
    IncidentStatus,
    IntakeChannel,
    IntakeStatus,
    ObservationStatus,
)


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ObservationCreate(BaseModel):
    """Observation item provided during report ingestion."""

    category_code: str = Field(..., description="Taxonomy code e.g. POTHOLE, GARBAGE_DUMP")
    department_code: str = Field(..., description="Target department code e.g. ROADS, SWM")
    source_media_url: str | None = None
    bounding_box: dict[str, float] | None = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    severity_score: int = Field(default=1, ge=1, le=5)


class ObservationResponse(BaseSchema):
    """Individual observation response for Nagrik Setu transparency."""

    id: uuid.UUID
    category_code: str
    status: ObservationStatus
    severity_score: int
    confidence: float
    source_media_url: str | None
    incident_id: uuid.UUID | None
    created_at: datetime


class IntakeReportCreate(BaseModel):
    """Citizen report filing payload."""

    organization_id: uuid.UUID
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    channel: IntakeChannel = IntakeChannel.PWA
    description: str | None = None
    media_urls: list[str] = Field(default_factory=list)
    address_text: str | None = None
    observations: list[ObservationCreate] = Field(
        default_factory=list,
        description="One or more defects extracted from the submission",
    )


class IntakeReportResponse(BaseSchema):
    """Created intake report with assigned tracking token."""

    id: uuid.UUID
    organization_id: uuid.UUID
    channel: IntakeChannel
    status: IntakeStatus
    ward_id: uuid.UUID | None
    tracking_token: str | None
    created_at: datetime
    observations: list[ObservationResponse]


class AnonymousTrackingResponse(BaseModel):
    """Sanitized anonymous lookup response."""

    report_id: uuid.UUID
    organization_id: uuid.UUID
    channel: str
    status: str
    address_text: str | None
    media_urls: list[str]
    created_at: str
    updated_at: str
    observations: list[dict[str, Any]]


class IncidentStatusUpdate(BaseModel):
    """Transitioning incident state across §A16 lifecycle."""

    status: IncidentStatus
    reason: str | None = None
    resolution_notes: str | None = None


class IncidentResponse(BaseSchema):
    """Operational case response."""

    id: uuid.UUID
    organization_id: uuid.UUID
    department_id: uuid.UUID
    ward_id: uuid.UUID
    category_code: str
    status: IncidentStatus
    severity: int
    assigned_worker_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
