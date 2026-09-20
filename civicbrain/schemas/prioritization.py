"""Pydantic schemas for Phase 6 Prioritization Engine API."""

import uuid

from pydantic import BaseModel, Field

from civicbrain.domain.intake.models import IncidentStatus


class AHPMatrixConfigRequest(BaseModel):
    """Payload to configure or update the 5x5 Saaty AHP matrix."""

    matrix: list[list[float]] = Field(
        ...,
        description="5x5 positive reciprocal matrix [Severity, Risk, Exposure, Criticality, Urgency]",
    )


class AHPMatrixConfigResponse(BaseModel):
    """Active AHP configuration details."""

    id: uuid.UUID
    organization_id: uuid.UUID
    matrix: list[list[float]]
    weights: dict[str, float]
    lambda_max: float
    consistency_index: float
    consistency_ratio: float
    is_active: bool


class WardEquityResponse(BaseModel):
    """Ward equity credibility parameters."""

    ward_id: uuid.UUID
    organization_id: uuid.UUID
    verified_incident_count: int
    historical_incident_rate: float
    credibility_factor: float
    expected_issue_rate: float
    observed_issue_rate: float
    equity_gap: float
    equity_boost: float


class PrioritizationEvaluationRequest(BaseModel):
    """Payload to evaluate priority for an incident across 5 orthogonal sub-scores."""

    severity: float = Field(..., ge=0.0, le=1.0)
    risk: float = Field(..., ge=0.0, le=1.0)
    exposure: float = Field(..., ge=0.0, le=1.0)
    criticality: float = Field(..., ge=0.0, le=1.0)
    urgency: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    ward_id: uuid.UUID | None = None
    custom_equity_boost: float | None = Field(default=None, ge=0.0, le=1.0)


class PrioritizationEvaluationResponse(BaseModel):
    """Itemized glass-box evaluation breakdown with confidence gating."""

    subscores: dict[str, float]
    weights_used: dict[str, float]
    raw_priority_score: float
    equity_boost: float
    final_priority_score: float
    confidence_score: float
    requires_human_review: bool
    review_reason: str | None
    target_status: IncidentStatus
