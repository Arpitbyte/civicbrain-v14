"""Phase 10 Analytics Domain Models: CategoryServiceTimePrior, WardReportCardSnapshot (§A21, §A23)."""

import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
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


class CategoryServiceTimePrior(Base):
    """Category baseline service-time priors (§A23, Bootstrap Principle §A3)."""

    __tablename__ = "category_service_time_prior"

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
    category_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    base_resolution_hours: Mapped[float] = mapped_column(Double, default=48.0, nullable=False)
    p25_hours: Mapped[float] = mapped_column(Double, default=24.0, nullable=False)
    p50_hours: Mapped[float] = mapped_column(Double, default=48.0, nullable=False)
    p90_hours: Mapped[float] = mapped_column(Double, default=96.0, nullable=False)
    min_hours: Mapped[float] = mapped_column(Double, default=6.0, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("organization_id", "category_code", name="uq_cat_org_prior"),
        CheckConstraint(
            "base_resolution_hours > 0 AND p25_hours > 0 AND p50_hours >= p25_hours AND p90_hours >= p50_hours AND min_hours > 0",
            name="chk_positive_hours",
        ),
    )


class WardReportCardSnapshot(Base):
    """Periodic municipal performance scorecard aggregated at the ward level (§A21)."""

    __tablename__ = "ward_report_card_snapshot"

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
    ward_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ward.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    period_type: Mapped[str] = mapped_column(String(20), default="weekly", nullable=False)
    total_reported: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_active: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_resolved: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_confirmed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_appealed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mean_resolution_hours: Mapped[float | None] = mapped_column(Double, nullable=True)
    median_resolution_hours: Mapped[float | None] = mapped_column(Double, nullable=True)
    citizen_satisfaction_index: Mapped[float | None] = mapped_column(Double, nullable=True)
    sla_compliance_rate: Mapped[float | None] = mapped_column(Double, nullable=True)
    equity_observed_gap: Mapped[float | None] = mapped_column(Double, nullable=True)
    department_breakdown: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("ward_id", "snapshot_date", "period_type", name="uq_ward_snapshot_period"),
    )
