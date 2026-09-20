"""Phase 7 Domain Models: IncidentCausalLink, CausalRelationType."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Double,
    Enum,
    ForeignKey,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from civicbrain.infra.database import Base


class CausalRelationType(enum.StrEnum):
    """Causal taxonomy classifying upstream failure modes."""

    INFRASTRUCTURE_FAILURE = "infrastructure_failure"
    ENVIRONMENTAL_CASCADE = "environmental_cascade"
    OPERATIONAL_BLOCKAGE = "operational_blockage"
    STRUCTURAL_DAMAGE = "structural_damage"


class IncidentCausalLink(Base):
    """Directed edge in the civic causal graph from root cause to child symptom."""

    __tablename__ = "incident_causal_link"

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
    root_incident_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("incident.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    symptom_incident_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("incident.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relation_type: Mapped[CausalRelationType] = mapped_column(
        Enum(
            CausalRelationType,
            name="causal_relation_type_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=CausalRelationType.INFRASTRUCTURE_FAILURE,
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Double, default=1.0, nullable=False)
    established_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.id", ondelete="SET NULL"),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("root_incident_id", "symptom_incident_id", name="uq_causal_pair"),
        CheckConstraint("root_incident_id <> symptom_incident_id", name="chk_no_self_causation"),
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="chk_causal_confidence"),
    )
