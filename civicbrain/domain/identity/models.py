"""Identity and Organization domain entities."""

import enum
import uuid
from datetime import date, datetime
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from civicbrain.infra.database import Base


class ULBType(enum.StrEnum):
    """Urban Local Body classification under 74th Constitutional Amendment Act, 1992."""

    MUNICIPAL_CORPORATION = "municipal_corporation"  # Nagar Nigam (large urban areas)
    MUNICIPAL_COUNCIL = "municipal_council"  # Nagar Palika Parishad (smaller urban areas)
    NAGAR_PANCHAYAT = "nagar_panchayat"  # Transitional / semi-urban areas


class StaffRole(enum.StrEnum):
    """Staff roles mapped to §A18 named workspaces."""

    ADMIN = "admin"  # Control Room — System/ULB Admin
    DISPATCHER = "dispatcher"  # Command Deck — Dispatcher, Duty Officer
    DEPARTMENT_STAFF = "department_staff"  # Ops Board — Department Staff, Department Supervisor
    ZONAL_SUPERVISOR = "zonal_supervisor"  # City Pulse — Zonal Supervisor, Data Analyst
    FIELD_WORKER = "field_worker"  # Karmi Sahayak / FieldOps — Field Worker, Inspector, Crew Lead
    CORPORATOR = (
        "corporator"  # Transparency Board & Command Deck / City Pulse — Ward Elected Representative
    )


class CitizenVerificationMethod(enum.StrEnum):
    """Citizen identity verification methods per §A8."""

    PHONE_OTP = "phone_otp"  # Primary and sufficient
    DIGILOCKER = "digilocker"  # Provisional extension point


class Organization(Base):
    """Root tenant representing an Urban Local Body (ULB) or multi-ULB state deployment."""

    __tablename__ = "organization"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    ulb_type: Mapped[ULBType] = mapped_column(
        Enum(
            ULBType,
            name="ulb_type_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=ULBType.MUNICIPAL_CORPORATION,
    )
    state: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    zones: Mapped[list["Zone"]] = relationship(
        "Zone", back_populates="organization", cascade="all, delete-orphan"
    )
    wards: Mapped[list["Ward"]] = relationship(
        "Ward", back_populates="organization", cascade="all, delete-orphan"
    )
    departments: Mapped[list["Department"]] = relationship(
        "Department", back_populates="organization", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, code='{self.code}', ulb_type='{self.ulb_type}')>"


class Zone(Base):
    """Administrative subdivision of a ULB."""

    __tablename__ = "zone"
    __table_args__ = (UniqueConstraint("organization_id", "code", name="uq_zone_org_code"),)

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    geom: Mapped[Any] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    organization: Mapped["Organization"] = relationship("Organization", back_populates="zones")
    wards: Mapped[list["Ward"]] = relationship(
        "Ward", back_populates="zone", cascade="all, delete-orphan"
    )


class Ward(Base):
    """Administrative and electoral unit of a ULB representing a Corporator constituency."""

    __tablename__ = "ward"
    __table_args__ = (
        UniqueConstraint("organization_id", "ward_number", name="uq_ward_org_number"),
        UniqueConstraint("organization_id", "code", name="uq_ward_org_code"),
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
    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("zone.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ward_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    geom: Mapped[Any] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326),
        nullable=False,
    )
    centroid: Mapped[Any | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    organization: Mapped["Organization"] = relationship("Organization", back_populates="wards")
    zone: Mapped["Zone"] = relationship("Zone", back_populates="wards")
    elected_representative: Mapped["ElectedRepresentative | None"] = relationship(
        "ElectedRepresentative",
        back_populates="ward",
        uselist=False,
    )


class Department(Base):
    """Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains, Electrical, Health)."""

    __tablename__ = "department"
    __table_args__ = (UniqueConstraint("organization_id", "code", name="uq_department_org_code"),)

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="departments"
    )


class UserAccount(Base):
    """Staff user account linked to Supabase Auth auth.users."""

    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    roles: Mapped[list["UserRoleAssignment"]] = relationship(
        "UserRoleAssignment",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserRoleAssignment(Base):
    """Explicit role assignment for staff users with optional department, zone, or ward scopes."""

    __tablename__ = "user_role_assignment"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "role",
            "department_id",
            "zone_id",
            "ward_id",
            name="uq_user_role_assignment",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[StaffRole] = mapped_column(
        Enum(
            StaffRole,
            name="staff_role_enum",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("department.id", ondelete="SET NULL"),
        nullable=True,
    )
    zone_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("zone.id", ondelete="SET NULL"),
        nullable=True,
    )
    ward_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ward.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["UserAccount"] = relationship("UserAccount", back_populates="roles")


class ElectedRepresentative(Base):
    """Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992."""

    __tablename__ = "elected_representative"
    __table_args__ = (
        UniqueConstraint("ward_id", name="uq_elected_representative_ward"),
        UniqueConstraint("user_id", name="uq_elected_representative_user"),
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
    ward_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ward.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    party_affiliation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    term_start: Mapped[date] = mapped_column(Date, nullable=False)
    term_end: Mapped[date] = mapped_column(Date, nullable=False)
    office_contact: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    ward: Mapped["Ward"] = relationship("Ward", back_populates="elected_representative")


class CitizenProfile(Base):
    """Citizen identity record verifying phone number without collecting Aadhaar (§A8)."""

    __tablename__ = "citizen_profile"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    verification_method: Mapped[CitizenVerificationMethod] = mapped_column(
        Enum(CitizenVerificationMethod, name="citizen_verification_method_enum", native_enum=True),
        default=CitizenVerificationMethod.PHONE_OTP,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class StaffBulkImportLog(Base):
    """Audit record for administrative staff bulk-import events."""

    __tablename__ = "staff_bulk_import_log"

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
    admin_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_account.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    total_rows: Mapped[int] = mapped_column(nullable=False)
    created_count: Mapped[int] = mapped_column(nullable=False)
    skipped_count: Mapped[int] = mapped_column(nullable=False)
    is_dry_run: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
