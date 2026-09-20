"""Pydantic Schemas for Dispatch, Work Orders, and Satisfaction Verification."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from civicbrain.domain.dispatch.models import WorkOrderStatus


class WorkOrderCreate(BaseModel):
    """Payload to create and dispatch a new work order."""

    incident_id: uuid.UUID
    department_id: uuid.UUID
    assigned_worker_id: uuid.UUID | None = None


class WorkOrderResolveRequest(BaseModel):
    """Field worker resolution submission with photographic evidence and GPS coordinates."""

    resolution_notes: str = Field(..., min_length=1, description="Field repair summary and notes")
    resolution_media_urls: list[str] = Field(
        ..., min_length=1, description="Array of photographic proof URLs (must not be empty)"
    )
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Field worker completion latitude")
    longitude: float = Field(
        ..., ge=-180.0, le=180.0, description="Field worker completion longitude"
    )


class WorkOrderResponse(BaseModel):
    """Work order representation."""

    id: uuid.UUID
    organization_id: uuid.UUID
    incident_id: uuid.UUID
    department_id: uuid.UUID
    assigned_worker_id: uuid.UUID | None
    status: WorkOrderStatus
    dispatched_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    resolution_notes: str | None
    resolution_media_urls: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DisputeRequest(BaseModel):
    """Citizen dispute request payload."""

    reason: str = Field(
        ..., min_length=1, description="Citizen reason for rejecting submitted resolution proof"
    )


class DisputeResponse(BaseModel):
    """Result of citizen dispute submission."""

    report_id: uuid.UUID
    status: str
    appealed_incident_ids: list[uuid.UUID]
    message: str


class ConfirmResponse(BaseModel):
    """Result of citizen confirmation."""

    report_id: uuid.UUID
    status: str
    confirmed_incident_ids: list[uuid.UUID]
    message: str


class AutoConfirmResponse(BaseModel):
    """Summary of automated 72-hour confirmation batch."""

    confirmed_count: int
    confirmed_incident_ids: list[uuid.UUID]
