"""Pydantic Schemas for Dispatch, Work Orders, and Karmi Sahayak Offline Sync."""

import enum
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from civicbrain.domain.dispatch.models import (
    ConflictReviewStatus,
    SyncMutationStatus,
    WorkOrderStatus,
)


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
    version: int = 1
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


# --- Phase 9: Offline Sync Schemas (§A15) ---


class ClientMutationItem(BaseModel):
    """A single queued offline mutation pushed by Karmi Sahayak client."""

    client_mutation_id: uuid.UUID
    entity_type: str = Field(default="work_order")
    entity_id: uuid.UUID
    action: str  # 'start', 'resolve', 'update_notes'
    base_version: int = Field(default=1, ge=1)
    captured_at: datetime
    payload: dict[str, Any] = Field(default_factory=dict)


class FieldSyncPushRequest(BaseModel):
    """Two-way delta sync request containing queued offline mutations."""

    since_cursor: datetime | None = None
    mutations: list[ClientMutationItem] = Field(default_factory=list)


class MutationResult(BaseModel):
    """Outcome for a single client mutation."""

    client_mutation_id: uuid.UUID
    status: SyncMutationStatus
    conflict_reason: str | None = None
    conflict_review_id: uuid.UUID | None = None


class FieldSyncResponse(BaseModel):
    """Delta synchronization response returning mutation outcomes and server changes."""

    mutation_results: list[MutationResult]
    server_changes: list[WorkOrderResponse]
    new_cursor: datetime


class DispatchConflictReviewResponse(BaseModel):
    """Reviewable concurrent dispatch conflict record for Control Room supervisors."""

    id: uuid.UUID
    organization_id: uuid.UUID
    work_order_id: uuid.UUID
    incident_id: uuid.UUID
    worker_id: uuid.UUID
    client_mutation_id: uuid.UUID
    conflict_type: str
    submitted_notes: str
    submitted_media_urls: list[str]
    status: ConflictReviewStatus
    reviewed_by: uuid.UUID | None
    reviewed_at: datetime | None
    review_notes: str | None
    captured_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConflictDecision(enum.StrEnum):
    """Supervisor decision on concurrent dispatch conflict."""

    ACCEPT_WORKER_EVIDENCE = "accept_worker_evidence"
    UPHOLD_DISPATCHER_ACTION = "uphold_dispatcher_action"


class ConflictAdjudicationRequest(BaseModel):
    """Supervisor adjudication action."""

    decision: ConflictDecision
    notes: str | None = None


class ConflictAdjudicationResponse(BaseModel):
    """Result of supervisor adjudication."""

    id: uuid.UUID
    status: ConflictReviewStatus
    reviewed_by: uuid.UUID | None
    reviewed_at: datetime | None
    review_notes: str | None
    message: str
