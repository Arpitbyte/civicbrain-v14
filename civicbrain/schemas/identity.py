"""Pydantic schemas for identity, administrative hierarchy, and RBAC."""

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from civicbrain.domain.identity.models import CitizenVerificationMethod, StaffRole, ULBType


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrganizationResponse(BaseSchema):
    id: uuid.UUID
    name: str
    code: str
    ulb_type: ULBType
    state: str
    created_at: datetime
    updated_at: datetime


class DepartmentBase(BaseModel):
    name: str
    code: str
    is_active: bool = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase, BaseSchema):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ZoneBase(BaseModel):
    name: str
    code: str
    geom: dict[str, Any] = Field(description="GeoJSON Polygon geometry")


class ZoneCreate(ZoneBase):
    pass


class ZoneResponse(BaseSchema):
    id: uuid.UUID
    organization_id: uuid.UUID
    name: str
    code: str
    geom: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime


class WardBase(BaseModel):
    ward_number: int
    name: str
    code: str
    geom: dict[str, Any] = Field(description="GeoJSON Polygon geometry")
    centroid: dict[str, Any] | None = Field(default=None, description="GeoJSON Point geometry")


class WardCreate(WardBase):
    zone_id: uuid.UUID


class WardResponse(BaseSchema):
    id: uuid.UUID
    organization_id: uuid.UUID
    zone_id: uuid.UUID
    ward_number: int
    name: str
    code: str
    geom: dict[str, Any] | None = None
    centroid: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime


class ElectedRepresentativeBase(BaseModel):
    full_name: str
    party_affiliation: str | None = None
    term_start: date
    term_end: date
    office_contact: str | None = None


class ElectedRepresentativeCreate(ElectedRepresentativeBase):
    ward_id: uuid.UUID
    user_id: uuid.UUID


class ElectedRepresentativeResponse(ElectedRepresentativeBase, BaseSchema):
    id: uuid.UUID
    organization_id: uuid.UUID
    ward_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserRoleAssignmentCreate(BaseModel):
    role: StaffRole
    department_id: uuid.UUID | None = None
    zone_id: uuid.UUID | None = None
    ward_id: uuid.UUID | None = None


class UserRoleAssignmentResponse(BaseSchema):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID
    role: StaffRole
    department_id: uuid.UUID | None = None
    zone_id: uuid.UUID | None = None
    ward_id: uuid.UUID | None = None
    created_at: datetime


class UserAccountCreate(BaseModel):
    email: str | None = None
    phone: str
    full_name: str
    password: str = Field(min_length=8, description="Initial temporary password for staff account")
    role_assignments: list[UserRoleAssignmentCreate] = Field(default_factory=list)


class UserAccountResponse(BaseSchema):
    id: uuid.UUID
    organization_id: uuid.UUID
    email: str | None = None
    phone: str
    full_name: str
    is_active: bool
    mfa_enabled: bool
    last_login_at: datetime | None = None
    created_at: datetime
    roles: list[UserRoleAssignmentResponse] = Field(default_factory=list)


class CitizenProfileCreate(BaseModel):
    phone: str
    display_name: str | None = None
    preferred_language: str = "en"


class CitizenProfileResponse(BaseSchema):
    id: uuid.UUID
    phone: str
    display_name: str | None = None
    preferred_language: str
    verification_method: CitizenVerificationMethod
    created_at: datetime
    updated_at: datetime


class AuthMeResponse(BaseModel):
    """Current authenticated user profile and resolved RBAC scopes."""

    user_id: uuid.UUID
    organization_id: uuid.UUID | None = None
    email: str | None = None
    phone: str | None = None
    full_name: str | None = None
    roles: list[StaffRole] = Field(default_factory=list)
    department_ids: list[uuid.UUID] = Field(default_factory=list)
    zone_ids: list[uuid.UUID] = Field(default_factory=list)
    ward_id: uuid.UUID | None = None
    is_citizen: bool = False
    is_staff: bool = True
    mfa_enabled: bool = False


class WardHierarchyNode(BaseModel):
    id: uuid.UUID
    ward_number: int
    name: str
    code: str
    centroid: dict[str, Any] | None = None


class ZoneHierarchyNode(BaseModel):
    id: uuid.UUID
    name: str
    code: str
    wards: list[WardHierarchyNode] = Field(default_factory=list)


class HierarchyTreeResponse(BaseModel):
    organization_id: uuid.UUID
    organization_name: str
    ulb_type: ULBType
    zones: list[ZoneHierarchyNode] = Field(default_factory=list)


class BulkImportRowResult(BaseModel):
    row_number: int
    full_name: str
    phone: str
    email: str | None = None
    role: str
    status: str  # "created", "would_create", "skipped"
    reason: str | None = None
    setup_link_dispatched: bool = False


class BulkImportResponse(BaseModel):
    file_name: str
    file_hash: str
    dry_run: bool
    total_rows: int
    created_count: int
    skipped_count: int
    results: list[BulkImportRowResult]
