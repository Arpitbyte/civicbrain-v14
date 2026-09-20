"""Administrative hierarchy, department taxonomy, and representative discovery endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from civicbrain.domain.identity.jwt import CurrentUserClaims, require_roles
from civicbrain.domain.identity.models import StaffRole, UserAccount
from civicbrain.domain.identity.services import (
    create_staff_user,
    get_departments,
    get_organization_hierarchy,
    get_ward_representative,
)
from civicbrain.infra.database import get_db
from civicbrain.schemas.identity import (
    DepartmentResponse,
    ElectedRepresentativeResponse,
    HierarchyTreeResponse,
    UserAccountCreate,
    UserAccountResponse,
)

router = APIRouter(tags=["Hierarchy & Administration"])


@router.get(
    "/orgs/{org_id}/hierarchy",
    response_model=HierarchyTreeResponse,
    summary="Get zonal and ward hierarchy tree",
)
async def get_hierarchy(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> HierarchyTreeResponse:
    """Retrieve complete tree of zones and wards for an organization."""
    tree = await get_organization_hierarchy(db, org_id)
    if not tree:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return tree


@router.get(
    "/orgs/{org_id}/departments",
    response_model=list[DepartmentResponse],
    summary="List active ULB departments",
)
async def list_departments(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[DepartmentResponse]:
    """List all active departments within the ULB."""
    depts = await get_departments(db, org_id)
    return [DepartmentResponse.model_validate(d) for d in depts]


@router.get(
    "/orgs/{org_id}/wards/{ward_id}/representative",
    response_model=ElectedRepresentativeResponse,
    summary="Get elected Corporator/Councillor for a ward",
)
async def get_representative(
    org_id: uuid.UUID,
    ward_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ElectedRepresentativeResponse:
    """Public endpoint to discover the elected representative for a specific ward."""
    rep = await get_ward_representative(db, ward_id)
    if not rep or rep.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elected representative not found for this ward",
        )
    return ElectedRepresentativeResponse.model_validate(rep)


@router.post(
    "/admin/users",
    response_model=UserAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register staff user and assign role (Admin only)",
)
async def create_staff_member(
    user_in: UserAccountCreate,
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
) -> UserAccountResponse:
    """Register staff account and assign role with jurisdictional scope within admin's tenant."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin must belong to an organization to provision staff",
        )

    # In production, Supabase Auth user is created via Auth Admin API
    # Generate placeholder or real auth ID
    auth_user_id = uuid.uuid4()
    staff = await create_staff_user(db, claims.org_id, user_in, auth_user_id)
    return UserAccountResponse.model_validate(staff)


@router.get(
    "/admin/users",
    response_model=list[UserAccountResponse],
    summary="List staff users in organization (Admin only)",
)
async def list_staff_members(
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
) -> list[UserAccountResponse]:
    """List staff accounts within the admin's tenant organization."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin must belong to an organization to list staff",
        )

    res = await db.execute(
        select(UserAccount)
        .where(UserAccount.organization_id == claims.org_id)
        .options(selectinload(UserAccount.roles))
    )
    users = res.scalars().all()
    return [UserAccountResponse.model_validate(u) for u in users]
