"""Pydantic schemas for Phase 11 Transparency, Jan Sunwai Ledger & Civic Assistant (§A21, §A23)."""

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class JanSunwaiLedgerResponse(BaseModel):
    """Publicly accessible, differentially private civic ledger milestone entry (§A23)."""

    id: uuid.UUID
    organization_id: uuid.UUID
    incident_id: uuid.UUID
    sequence_num: int
    public_tracking_code: str
    category_code: str
    department_id: uuid.UUID
    ward_id: uuid.UUID
    dp_latitude: float
    dp_longitude: float
    dp_timestamp: datetime
    lifecycle_status: str
    sla_status: str
    predicted_eta_hours: float | None = None
    resolution_media_count: int = 0
    is_appealed: bool = False
    prev_hash: str
    entry_hash: str
    created_at: datetime


class IncidentLedgerChainResponse(BaseModel):
    """Chronological cryptographic ledger chain for an incident (§A23)."""

    incident_id: uuid.UUID
    public_tracking_code: str
    chain_length: int
    is_valid: bool
    error_message: str | None = None
    entries: list[JanSunwaiLedgerResponse] = Field(default_factory=list)


class NagarPragatiResponse(BaseModel):
    """City-wide municipal progress and macro performance scorecard (§A21)."""

    organization_id: uuid.UUID
    snapshot_date: date
    period_type: str
    city_mttr_hours: float | None = None
    city_csi: float | None = None
    city_sla_compliance_rate: float | None = None
    total_intake: int
    total_resolved: int
    department_rankings: list[dict[str, Any]] = Field(default_factory=list)
    ward_equity_distribution: dict[str, Any] = Field(default_factory=dict)


class CivicAssistantQueryRequest(BaseModel):
    """Citizen multilingual query request payload."""

    query_text: str = Field(..., min_length=1, max_length=1000)
    language_code: str = Field(default="en", max_length=10)
    tracking_code: str | None = Field(default=None, max_length=50)
    ward_id: uuid.UUID | None = None


class CivicAssistantQueryResponse(BaseModel):
    """Deterministic multilingual response from the Civic Assistant (§A23)."""

    query_text: str
    detected_language: str
    intent: str
    response_text: str
    tracking_code: str | None = None
    eta_explanation: str | None = None
    next_actions: list[str] = Field(default_factory=list)
