"""Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing."""

import uuid

from civicbrain.domain.identity.jwt import CurrentUserClaims
from civicbrain.domain.identity.models import (
    CitizenVerificationMethod,
    StaffRole,
)
from civicbrain.schemas.identity import (
    CitizenProfileCreate,
    DepartmentCreate,
    WardCreate,
    ZoneCreate,
)


def test_staff_role_enum_values():
    """Verify staff_role_enum matches §A18 named workspaces."""
    assert StaffRole.ADMIN == "admin"
    assert StaffRole.DISPATCHER == "dispatcher"
    assert StaffRole.DEPARTMENT_STAFF == "department_staff"
    assert StaffRole.ZONAL_SUPERVISOR == "zonal_supervisor"
    assert StaffRole.FIELD_WORKER == "field_worker"
    assert StaffRole.CORPORATOR == "corporator"
    assert len(StaffRole) == 6


def test_citizen_verification_enum_values():
    """Verify citizen verification methods per §A8."""
    assert CitizenVerificationMethod.PHONE_OTP == "phone_otp"
    assert CitizenVerificationMethod.DIGILOCKER == "digilocker"


def test_jwt_claims_parsing():
    """Verify CurrentUserClaims parses custom Supabase app_metadata."""
    uid = uuid.uuid4()
    org_id = uuid.uuid4()
    dept_id = uuid.uuid4()
    zone_id = uuid.uuid4()
    ward_id = uuid.uuid4()

    token_payload = {
        "sub": str(uid),
        "email": "officer@civicbrain.org",
        "app_metadata": {
            "org_id": str(org_id),
            "role": "department_staff",
            "department_ids": [str(dept_id)],
            "zone_ids": [str(zone_id)],
            "ward_id": str(ward_id),
        },
    }

    claims = CurrentUserClaims(token_payload)
    assert claims.user_id == uid
    assert claims.org_id == org_id
    assert claims.role == StaffRole.DEPARTMENT_STAFF
    assert claims.department_ids == [dept_id]
    assert claims.zone_ids == [zone_id]
    assert claims.ward_id == ward_id


def test_pydantic_schemas_validation():
    """Verify Pydantic request and response schemas."""
    zone_in = ZoneCreate(
        name="South Zone",
        code="ZONE_SOUTH",
        geom={
            "type": "Polygon",
            "coordinates": [[[77.5, 12.9], [77.6, 12.9], [77.6, 13.0], [77.5, 13.0], [77.5, 12.9]]],
        },
    )
    assert zone_in.code == "ZONE_SOUTH"

    ward_in = WardCreate(
        zone_id=uuid.uuid4(),
        ward_number=150,
        name="Bellandur",
        code="WARD_150",
        geom={
            "type": "Polygon",
            "coordinates": [
                [[77.55, 12.92], [77.58, 12.92], [77.58, 12.95], [77.55, 12.95], [77.55, 12.92]]
            ],
        },
    )
    assert ward_in.ward_number == 150

    dept_in = DepartmentCreate(name="Roads & Infrastructure", code="ROADS")
    assert dept_in.is_active is True

    cit_in = CitizenProfileCreate(phone="+919876543210", display_name="Ramesh Kumar")
    assert cit_in.preferred_language == "en"
