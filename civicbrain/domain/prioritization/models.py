"""Phase 6 Prioritization Domain Models: AHPMatrixConfig, WardEquityCredibility, WardResolutionStat."""

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
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


class AHPMatrixConfig(Base):
    """Organization-level AHP pairwise criteria comparison matrix & derived weights."""

    __tablename__ = "ahp_matrix_config"

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
    matrix: Mapped[list[list[float]]] = mapped_column(JSONB, nullable=False)
    weights: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)
    lambda_max: Mapped[float] = mapped_column(Double, nullable=False)
    consistency_index: Mapped[float] = mapped_column(Double, nullable=False)
    consistency_ratio: Mapped[float] = mapped_column(Double, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("organization_id", "is_active", name="uq_ahp_org_active"),
        CheckConstraint("consistency_ratio < 0.10", name="chk_ahp_cr"),
    )


class WardEquityCredibility(Base):
    """Bühlmann credibility blending expected-vs-observed incident rates per ward."""

    __tablename__ = "ward_equity_credibility"

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
    verified_incident_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    historical_incident_rate: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    credibility_factor: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    expected_issue_rate: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    observed_issue_rate: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    equity_gap: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)
    equity_boost: Mapped[float] = mapped_column(Double, default=0.0, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("organization_id", "ward_id", name="uq_ward_equity_org_ward"),
    )


class WardResolutionStat(Base):
    """Ward operational SLA and historical resolution telemetry."""

    __tablename__ = "ward_resolution_stat"

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
    category_code: Mapped[str] = mapped_column(String(50), nullable=False)
    resolved_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mean_resolution_hours: Mapped[float] = mapped_column(Double, default=48.0, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (UniqueConstraint("ward_id", "category_code", name="uq_ward_res_stat"),)
