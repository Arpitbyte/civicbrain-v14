"""Identity and Organization domain entities."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from civicbrain.infra.database import Base


class ULBType(enum.StrEnum):
    """Urban Local Body classification under 74th Constitutional Amendment Act, 1992."""

    MUNICIPAL_CORPORATION = "municipal_corporation"  # Nagar Nigam (large urban areas)
    MUNICIPAL_COUNCIL = "municipal_council"  # Nagar Palika Parishad (smaller urban areas)
    NAGAR_PANCHAYAT = "nagar_panchayat"  # Transitional / semi-urban areas


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
        Enum(ULBType, name="ulb_type_enum", native_enum=True),
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

    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, code='{self.code}', ulb_type='{self.ulb_type}')>"
