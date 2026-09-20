"""Pydantic schemas for Living Taxonomy Governance and Rubric validation."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from civicbrain.domain.intake.taxonomy import CategoryStatus, SeverityRubric


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TaxonomyCategoryPropose(BaseModel):
    """Staff/Citizen payload proposing a new civic category."""

    organization_id: uuid.UUID
    department_id: uuid.UUID
    code: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=128)
    description: str | None = None
    severity_rubric: SeverityRubric | None = Field(
        default=None,
        description="Optional initial draft of 5-level severity rubric",
    )


class TaxonomyCategoryApprove(BaseModel):
    """Admin payload approving a proposed category (§A11, Standing Invariant 1).

    Must contain a valid 5-level severity rubric. Cannot be blank.
    Decoupled from static AHP criteria weights.
    """

    severity_rubric: SeverityRubric


class TaxonomyCategoryResponse(BaseSchema):
    """Taxonomy category output."""

    id: uuid.UUID
    organization_id: uuid.UUID
    department_id: uuid.UUID
    code: str
    name: str
    description: str | None = None
    severity_rubric: dict[str, Any]
    status: CategoryStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
