"""Pydantic schemas for NLP Analysis API (§A11)."""

from pydantic import BaseModel, ConfigDict, Field


class TextAnalysisRequest(BaseModel):
    """Payload for text analysis endpoint."""

    model_config = ConfigDict(from_attributes=True)

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Raw citizen grievance description in any Indian language or script",
    )
    citizen_category: str | None = Field(
        None,
        max_length=50,
        description="Optional category pre-selected by citizen",
    )


class TextAnalysisResponse(BaseModel):
    """Structured linguistic and defect triage result."""

    model_config = ConfigDict(from_attributes=True)

    detected_language: str
    detected_script: str
    normalized_text: str
    suggested_category: str | None
    physical_severity_hint: int | None
    citizen_urgency_score: float
    extracted_keywords: list[str]
    requires_human_triage: bool
