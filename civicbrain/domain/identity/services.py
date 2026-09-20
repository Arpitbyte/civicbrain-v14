"""Domain services for identity, administrative hierarchy, and role management."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from civicbrain.domain.identity.models import (
    CitizenProfile,
    Department,
    ElectedRepresentative,
    Organization,
    UserAccount,
    UserRoleAssignment,
    Zone,
)
from civicbrain.schemas.identity import (
    AuthMeResponse,
    HierarchyTreeResponse,
    UserAccountCreate,
    WardHierarchyNode,
    ZoneHierarchyNode,
)


async def get_organization_hierarchy(
    session: AsyncSession, organization_id: uuid.UUID
) -> HierarchyTreeResponse | None:
    """Fetch complete hierarchical tree of zones and wards for an organization."""
    org_res = await session.execute(select(Organization).where(Organization.id == organization_id))
    org = org_res.scalar_one_or_none()
    if not org:
        return None

    zones_res = await session.execute(
        select(Zone)
        .where(Zone.organization_id == organization_id)
        .options(selectinload(Zone.wards))
        .order_by(Zone.name)
    )
    zones = zones_res.scalars().all()

    zone_nodes: list[ZoneHierarchyNode] = []
    for z in zones:
        ward_nodes = [
            WardHierarchyNode(
                id=w.id,
                ward_number=w.ward_number,
                name=w.name,
                code=w.code,
                centroid=None,
            )
            for w in sorted(z.wards, key=lambda x: x.ward_number)
        ]
        zone_nodes.append(
            ZoneHierarchyNode(
                id=z.id,
                name=z.name,
                code=z.code,
                wards=ward_nodes,
            )
        )

    return HierarchyTreeResponse(
        organization_id=org.id,
        organization_name=org.name,
        ulb_type=org.ulb_type,
        zones=zone_nodes,
    )


async def get_departments(session: AsyncSession, organization_id: uuid.UUID) -> list[Department]:
    """List all active departments for an organization."""
    res = await session.execute(
        select(Department)
        .where(Department.organization_id == organization_id, Department.is_active.is_(True))
        .order_by(Department.name)
    )
    return list(res.scalars().all())


async def get_ward_representative(
    session: AsyncSession, ward_id: uuid.UUID
) -> ElectedRepresentative | None:
    """Retrieve the elected Corporator/Councillor record for a ward."""
    res = await session.execute(
        select(ElectedRepresentative).where(ElectedRepresentative.ward_id == ward_id)
    )
    return res.scalar_one_or_none()


async def resolve_user_profile(session: AsyncSession, user_id: uuid.UUID) -> AuthMeResponse:
    """Resolve full profile, role assignments, and active scopes for authenticated user."""
    # Check if user is staff
    staff_res = await session.execute(
        select(UserAccount)
        .where(UserAccount.id == user_id)
        .options(selectinload(UserAccount.roles))
    )
    staff = staff_res.scalar_one_or_none()
    if staff:
        roles = [r.role for r in staff.roles]
        dept_ids = [r.department_id for r in staff.roles if r.department_id]
        zone_ids = [r.zone_id for r in staff.roles if r.zone_id]
        ward_id = next((r.ward_id for r in staff.roles if r.ward_id), None)
        return AuthMeResponse(
            user_id=staff.id,
            organization_id=staff.organization_id,
            email=staff.email,
            phone=staff.phone,
            full_name=staff.full_name,
            roles=roles,
            department_ids=dept_ids,
            zone_ids=zone_ids,
            ward_id=ward_id,
            is_citizen=False,
            is_staff=True,
            mfa_enabled=staff.mfa_enabled,
        )

    # Check if citizen profile exists
    cit_res = await session.execute(select(CitizenProfile).where(CitizenProfile.id == user_id))
    citizen = cit_res.scalar_one_or_none()
    if citizen:
        return AuthMeResponse(
            user_id=citizen.id,
            organization_id=None,
            email=None,
            phone=citizen.phone,
            full_name=citizen.display_name,
            roles=[],
            department_ids=[],
            zone_ids=[],
            ward_id=None,
            is_citizen=True,
            is_staff=False,
            mfa_enabled=False,
        )

    # Minimal fallback
    return AuthMeResponse(
        user_id=user_id,
        is_citizen=True,
        is_staff=False,
    )


async def create_staff_user(
    session: AsyncSession,
    organization_id: uuid.UUID,
    user_data: UserAccountCreate,
    auth_user_id: uuid.UUID,
) -> UserAccount:
    """Create staff user record and assign initial roles."""
    staff = UserAccount(
        id=auth_user_id,
        organization_id=organization_id,
        email=user_data.email,
        phone=user_data.phone,
        full_name=user_data.full_name,
        is_active=True,
        mfa_enabled=False,
    )
    session.add(staff)
    await session.flush()

    for r in user_data.role_assignments:
        assignment = UserRoleAssignment(
            user_id=auth_user_id,
            organization_id=organization_id,
            role=r.role,
            department_id=r.department_id,
            zone_id=r.zone_id,
            ward_id=r.ward_id,
        )
        session.add(assignment)

    await session.commit()
    await session.refresh(staff)
    return staff
