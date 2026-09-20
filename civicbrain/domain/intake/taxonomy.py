"""Living Taxonomy Governance (§A11, Standing Invariant 1).

Decoupled from static AHP criteria weights.
Requires structured 1-5 severity rubric for approval.
"""

import enum
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from civicbrain.infra.database import Base


class CategoryStatus(enum.StrEnum):
    """Lifecycle status for a taxonomy category."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    DEPRECATED = "deprecated"


class RubricLevel(BaseModel):
    """Concrete physical criteria and baseline severity score for a single rubric tier."""

    level: int = Field(ge=1, le=5, description="Severity tier from 1 to 5")
    criteria: str = Field(min_length=10, description="Observable physical failure threshold")
    baseline_score: float = Field(ge=1.0, le=5.0, description="Initial calibrated score")


class SeverityRubric(BaseModel):
    """Complete 5-level severity rubric (§A11, Standing Invariant 1).

    Approval of a category strictly requires all 5 levels to be defined.
    Buhlmann credibility parameter defaults to 10.0 for blending with inspection data.
    """

    model_config = ConfigDict(extra="forbid")

    levels: list[RubricLevel] = Field(min_length=5, max_length=5)
    buhlmann_k: float = Field(default=10.0, ge=1.0)

    @field_validator("levels")
    @classmethod
    def validate_levels_complete(cls, levels: list[RubricLevel]) -> list[RubricLevel]:
        tier_set = {item.level for item in levels}
        if tier_set != {1, 2, 3, 4, 5}:
            raise ValueError(
                f"Severity rubric must contain exactly tiers 1 through 5, received {sorted(tier_set)}"
            )
        return sorted(levels, key=lambda x: x.level)


def create_default_rubric(category_name: str) -> SeverityRubric:
    """Generate a standard calibrated 5-level rubric for seed categories."""
    return SeverityRubric(
        levels=[
            RubricLevel(
                level=1,
                criteria=f"Minor cosmetic or superficial issue with {category_name}; no safety impact.",
                baseline_score=1.0,
            ),
            RubricLevel(
                level=2,
                criteria=f"Noticeable defect in {category_name}; slight inconvenience, minimal hazard.",
                baseline_score=2.0,
            ),
            RubricLevel(
                level=3,
                criteria=f"Moderate impairment of {category_name}; impedes normal usage or civic flow.",
                baseline_score=3.0,
            ),
            RubricLevel(
                level=4,
                criteria=f"Severe degradation of {category_name}; active risk to public health or mobility.",
                baseline_score=4.0,
            ),
            RubricLevel(
                level=5,
                criteria=f"Critical emergency or failure of {category_name}; immediate danger to life/property.",
                baseline_score=5.0,
            ),
        ],
        buhlmann_k=10.0,
    )


class TaxonomyCategory(Base):
    """Categorical classification entity governed by living taxonomy rules."""

    __tablename__ = "taxonomy_category"
    __table_args__ = (UniqueConstraint("organization_id", "code", name="uq_taxonomy_org_code"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("department.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity_rubric: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    status: Mapped[CategoryStatus] = mapped_column(
        Enum(
            CategoryStatus,
            name="category_status_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=CategoryStatus.PROPOSED,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
