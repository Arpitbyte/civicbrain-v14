"""Pydantic schemas for Phase 7 Causal Root-Cause Linking API."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from civicbrain.domain.causal.models import CausalRelationType


class CreateCausalLinkRequest(BaseModel):
    """Payload to establish a directed causal link from root cause to child symptom."""

    root_incident_id: uuid.UUID = Field(..., description="ID of upstream root cause incident")
    symptom_incident_id: uuid.UUID = Field(..., description="ID of downstream symptom incident")
    relation_type: CausalRelationType = Field(
        default=CausalRelationType.INFRASTRUCTURE_FAILURE,
        description="Failure taxonomy classification",
    )
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    notes: str | None = None


class CausalLinkResponse(BaseModel):
    """Causal link record response."""

    id: uuid.UUID
    organization_id: uuid.UUID
    root_incident_id: uuid.UUID
    symptom_incident_id: uuid.UUID
    relation_type: CausalRelationType
    confidence: float
    established_by: uuid.UUID | None
    notes: str | None
    created_at: datetime


class DownstreamSymptomsResponse(BaseModel):
    """List of all downstream symptom incidents causally linked to a root cause."""

    root_incident_id: uuid.UUID
    downstream_symptom_count: int
    downstream_incident_ids: list[uuid.UUID]
    base_priority_score: float
    priority_boost: float
    final_priority_score: float
