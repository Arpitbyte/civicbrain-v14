"""Phase 2 Domain Models: IntakeReport, Observation, Incident, and IncidentDedupLink."""

import enum
import uuid
from datetime import datetime
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    DateTime,
    Double,
    Enum,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from civicbrain.infra.database import Base


class IntakeChannel(enum.StrEnum):
    """Citizen reporting channels."""

    PWA = "pwa"
    WHATSAPP = "whatsapp"
    IVR = "ivr"
    CSC = "csc"
    FIELD_WORKER = "field_worker"


class IntakeStatus(enum.StrEnum):
    """Aggregate lifecycle status for parent citizen intake report."""

    SUBMITTED = "submitted"
    PROCESSING = "processing"
    TRIAGED = "triaged"
    IN_PROGRESS = "in_progress"
    PARTIALLY_RESOLVED = "partially_resolved"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"


class ObservationStatus(enum.StrEnum):
    """Atomic observation state."""

    DETECTED = "detected"
    VERIFIED = "verified"
    LINKED_TO_INCIDENT = "linked_to_incident"
    REJECTED = "rejected"
    RESOLVED = "resolved"


class IncidentStatus(enum.StrEnum):
    """Authoritative Incident Lifecycle (§A16 11-State Machine)."""

    REPORTED = "reported"
    TRIAGED = "triaged"
    VERIFIED = "verified"
    PRIORITIZED = "prioritized"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    APPEALED = "appealed"
    REOPENED = "reopened"


class DedupDecision(enum.StrEnum):
    """Record linkage determination."""

    EXACT_MATCH = "exact_match"
    PROBABLE_MATCH = "probable_match"
    DISTINCT = "distinct"
    MANUAL_REVIEW = "manual_review"


class IntakeReport(Base):
    """Citizen submission provenance container."""

    __tablename__ = "intake_report"

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
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("citizen_profile.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    channel: Mapped[IntakeChannel] = mapped_column(
        Enum(
            IntakeChannel,
            name="intake_channel_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=IntakeChannel.PWA,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    media_urls: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    geom: Mapped[Any] = mapped_column(Geometry("POINT", srid=4326), nullable=False)
    address_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    ward_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ward.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[IntakeStatus] = mapped_column(
        Enum(
            IntakeStatus,
            name="intake_status_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=IntakeStatus.SUBMITTED,
        nullable=False,
        index=True,
    )
    tracking_token: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True, index=True
    )
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSONB, default=dict, nullable=False
    )

    detected_language: Mapped[str] = mapped_column(
        String(20), default="en", server_default="en", nullable=False
    )
    detected_script: Mapped[str] = mapped_column(
        String(20), default="Latin", server_default="Latin", nullable=False
    )
    citizen_urgency_score: Mapped[float] = mapped_column(
        Double, default=0.0, server_default="0.0", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    observations: Mapped[list["Observation"]] = relationship(
        "Observation", back_populates="intake_report", cascade="all, delete-orphan"
    )


class Incident(Base):
    """Authoritative operational civic case tracked across §A16 lifecycle."""

    __tablename__ = "incident"

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
        ForeignKey("department.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ward_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ward.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    geom: Mapped[Any] = mapped_column(Geometry("POINT", srid=4326), nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(
            IncidentStatus,
            name="incident_status_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=IncidentStatus.REPORTED,
        nullable=False,
        index=True,
    )
    severity: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    assigned_worker_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.id", ondelete="SET NULL"),
        nullable=True,
    )

    triaged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    prioritized_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    in_progress_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    appealed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reopened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    appeal_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Phase 6: 5 AHP Sub-scores, Equity Boost, Priority & Confidence Gating (§A12, §A13)
    subscore_severity: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    subscore_risk: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    subscore_exposure: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    subscore_criticality: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    subscore_urgency: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    raw_priority_score: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    equity_boost: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    priority_score: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    requires_human_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    review_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    observations: Mapped[list["Observation"]] = relationship(
        "Observation", back_populates="incident"
    )


class Observation(Base):
    """Atomic localized defect extracted from citizen intake submission."""

    __tablename__ = "observation"

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
    intake_report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("intake_report.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    incident_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("incident.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("department.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_code: Mapped[str] = mapped_column(String(64), nullable=False)
    source_media_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    bounding_box: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    bbox: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Double, nullable=True)
    severity_score: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    detection_source: Mapped[str] = mapped_column(
        String(64), default="citizen_declared", nullable=False
    )
    needs_manual_triage: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    extracted_keywords: Mapped[list[str]] = mapped_column(
        ARRAY(Text), default=list, server_default="{}", nullable=False
    )
    text_severity_hint: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    status: Mapped[ObservationStatus] = mapped_column(
        Enum(
            ObservationStatus,
            name="observation_status_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=ObservationStatus.DETECTED,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    intake_report: Mapped["IntakeReport"] = relationship(
        "IntakeReport", back_populates="observations"
    )
    incident: Mapped["Incident | None"] = relationship("Incident", back_populates="observations")


class IncidentDedupLink(Base):
    """Splink probabilistic record linkage audit between observation and candidate incident."""

    __tablename__ = "incident_dedup_link"
    __table_args__ = (
        UniqueConstraint("observation_id", "candidate_incident_id", name="uq_dedup_obs_candidate"),
    )

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
    observation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("observation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    candidate_incident_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("incident.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    spatial_distance_meters: Mapped[float] = mapped_column(Double, nullable=False)
    temporal_diff_seconds: Mapped[float] = mapped_column(Double, nullable=False)
    category_match: Mapped[bool] = mapped_column(Boolean, nullable=False)
    text_similarity: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    match_weight: Mapped[float] = mapped_column(Double, nullable=False)
    match_probability: Mapped[float] = mapped_column(Double, nullable=False)
    decision: Mapped[DedupDecision] = mapped_column(
        Enum(
            DedupDecision,
            name="dedup_decision_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    model_version: Mapped[str] = mapped_column(
        String(50), default="splink_v4_cold_start", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
