"""Pydantic schemas for Phase 10 Analytics, Ward Report Card, Corporator Digest & ETA Prediction (§A21, §A23)."""

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class CategoryPriorCreate(BaseModel):
    """Payload to configure or initialize a category service-time prior."""

    category_code: str = Field(..., max_length=50)
    base_resolution_hours: float = Field(default=48.0, gt=0.0)
    p25_hours: float = Field(default=24.0, gt=0.0)
    p50_hours: float = Field(default=48.0, gt=0.0)
    p90_hours: float = Field(default=96.0, gt=0.0)
    min_hours: float = Field(default=6.0, gt=0.0)
    sample_size: int = Field(default=0, ge=0)


class CategoryPriorResponse(BaseModel):
    """Category baseline service-time response."""

    id: uuid.UUID
    organization_id: uuid.UUID
    category_code: str
    base_resolution_hours: float
    p25_hours: float
    p50_hours: float
    p90_hours: float
    min_hours: float
    sample_size: int
    created_at: datetime
    updated_at: datetime


class WardReportCardResponse(BaseModel):
    """Ward-level municipal scorecard and transparent performance metrics (§A21)."""

    ward_id: uuid.UUID
    organization_id: uuid.UUID
    snapshot_date: date
    period_type: str
    total_reported: int
    total_active: int
    total_resolved: int
    total_confirmed: int
    total_appealed: int
    mean_resolution_hours: float | None = None
    median_resolution_hours: float | None = None
    citizen_satisfaction_index: float | None = None
    sla_compliance_rate: float | None = None
    equity_observed_gap: float | None = None
    department_breakdown: dict[str, Any] = Field(default_factory=dict)


class SLABreachItem(BaseModel):
    """Incident exceeding SLA threshold (> 72 hours)."""

    incident_id: uuid.UUID
    title: str
    category_code: str
    age_hours: float
    status: str
    department_name: str | None = None


class CorporatorDigestResponse(BaseModel):
    """Executive operational digest tailored for Ward Elected Representatives (§A18, §A21)."""

    ward_id: uuid.UUID
    corporator_user_id: uuid.UUID
    generation_timestamp: datetime
    total_active_cases: int
    newly_reported_week: int
    resolved_week: int
    citizen_satisfaction_index: float | None = None
    sla_breaches_count: int
    sla_breach_alerts: list[SLABreachItem] = Field(default_factory=list)
    department_backlog_ranking: list[dict[str, Any]] = Field(default_factory=list)


class ETAPredictionResponse(BaseModel):
    """Empirical deterministic service-time estimation (§A23, Bootstrap Principle §A3)."""

    incident_id: uuid.UUID
    predicted_resolution_hours: float
    estimated_completion_time: datetime
    p25_hours: float
    p50_hours: float
    p90_hours: float
    formula_components: dict[str, float]
    explanation: str
