"""Phase 11 Transparency Domain Models: JanSunwaiLedgerEntry, NagarPragatiCitySnapshot (§A21, §A23)."""

import uuid
from datetime import date, datetime
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from civicbrain.infra.database import Base


class JanSunwaiLedgerEntry(Base):
    """Public, tamper-evident civic grievance ledger entry with Differential Privacy (§A23)."""

    __tablename__ = "jan_sunwai_ledger_entry"

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
    incident_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("incident.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sequence_num: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    public_tracking_code: Mapped[str] = mapped_column(String(32), nullable=False)
    category_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("department.id", ondelete="CASCADE"),
        nullable=False,
    )
    ward_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ward.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Differentially Private Perturbed Fields (Generated once at sequence 0, reused on subsequent seq)
    dp_geom: Mapped[Any] = mapped_column(Geometry("POINT", srid=4326), nullable=False)
    dp_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # Status and SLA Telemetry
    lifecycle_status: Mapped[str] = mapped_column(String(50), nullable=False)
    sla_status: Mapped[str] = mapped_column(String(20), default="within_sla", nullable=False)
    predicted_eta_hours: Mapped[float | None] = mapped_column(Double, nullable=True)
    resolution_media_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_appealed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Cryptographic Checkpoint
    prev_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    entry_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("incident_id", "sequence_num", name="uq_ledger_incident_seq"),
        UniqueConstraint("incident_id", "lifecycle_status", name="uq_ledger_incident_status"),
    )


class NagarPragatiCitySnapshot(Base):
    """City-wide municipal progress and transparency dashboard snapshot (§A21)."""

    __tablename__ = "nagar_pragati_city_snapshot"

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
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    period_type: Mapped[str] = mapped_column(String(20), default="monthly", nullable=False)
    city_mttr_hours: Mapped[float | None] = mapped_column(Double, nullable=True)
    city_csi: Mapped[float | None] = mapped_column(Double, nullable=True)
    city_sla_compliance_rate: Mapped[float | None] = mapped_column(Double, nullable=True)
    total_intake: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_resolved: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    department_rankings: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB, default=list, nullable=False
    )
    ward_equity_distribution: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "organization_id", "snapshot_date", "period_type", name="uq_nagar_pragati_org_period"
        ),
    )
