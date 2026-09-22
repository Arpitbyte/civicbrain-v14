"""Living Taxonomy Governance REST Endpoints (§A11, Standing Invariant 1)."""

import logging
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.identity.jwt import (
    CurrentUserClaims,
    SupabaseClaims,
    get_current_user_claims,
    get_optional_user_claims,
    require_roles,
)
from civicbrain.domain.identity.models import Department, Organization, StaffRole
from civicbrain.domain.intake.taxonomy import (
    CategoryStatus,
    TaxonomyCategory,
    create_default_rubric,
)
from civicbrain.infra.cache import cache_delete, cache_get, cache_set
from civicbrain.infra.database import get_db
from civicbrain.schemas.taxonomy import (
    TaxonomyCategoryApprove,
    TaxonomyCategoryPropose,
    TaxonomyCategoryResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/taxonomy", tags=["Taxonomy & Governance"])


@router.get(
    "/categories",
    response_model=list[TaxonomyCategoryResponse],
    summary="List civic taxonomy categories",
)
async def list_categories(
    organization_id: uuid.UUID = Query(...),
    category_status: CategoryStatus | None = None,
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_optional_user_claims),
) -> list[TaxonomyCategoryResponse]:
    """List taxonomy categories.

    Public/citizens see only approved active categories.
    Admins can query proposed or deprecated categories.
    """
    stmt = (
        select(TaxonomyCategory)
        .where(TaxonomyCategory.organization_id == organization_id)
        .order_by(TaxonomyCategory.code.asc())
    )

    is_admin = False
    if claims and claims.role == "authenticated":
        # Check if user has admin role in this organization
        if (
            getattr(claims, "org_id", None) == organization_id
            and getattr(claims, "user_role", None) == StaffRole.ADMIN
        ):
            is_admin = True

    if not is_admin:
        stmt = stmt.where(
            TaxonomyCategory.status == CategoryStatus.APPROVED,
            TaxonomyCategory.is_active.is_(True),
        )
    elif category_status:
        stmt = stmt.where(TaxonomyCategory.status == category_status)
    # Check cache for public approved categories
    cache_key = f"cache:taxonomy:{organization_id}:approved"
    if not is_admin and not category_status:
        cached = await cache_get(cache_key)
        if cached is not None:
            return [TaxonomyCategoryResponse.model_validate(c) for c in cached]

    res = await db.execute(stmt)
    cats = list(res.scalars().all())
    result_models = [TaxonomyCategoryResponse.model_validate(c) for c in cats]

    if not is_admin and not category_status:
        await cache_set(cache_key, [m.model_dump() for m in result_models], ttl_seconds=120)

    return result_models


@router.post(
    "/categories",
    response_model=TaxonomyCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Propose a new taxonomy category",
)
async def propose_category(
    payload: TaxonomyCategoryPropose,
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_current_user_claims),
) -> TaxonomyCategoryResponse:
    """Staff/Citizen proposes a new civic category in 'proposed' state.

    Strictly sets status = 'proposed' to comply with RLS policy:
    WITH CHECK (status = 'proposed').
    """
    # Verify organization
    org = await db.get(Organization, payload.organization_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Verify department
    dept = await db.get(Department, payload.department_id)
    if not dept or dept.organization_id != payload.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department does not belong to the specified organization",
        )

    # Check unique code in organization
    existing_stmt = (
        select(TaxonomyCategory)
        .where(TaxonomyCategory.organization_id == payload.organization_id)
        .where(TaxonomyCategory.code == payload.code.strip().upper())
    )
    existing_res = await db.execute(existing_stmt)
    if existing_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category code '{payload.code}' already exists for this organization",
        )

    # Default rubric if not provided
    rubric_dict = (
        payload.severity_rubric.model_dump()
        if payload.severity_rubric
        else create_default_rubric(payload.name).model_dump()
    )

    category = TaxonomyCategory(
        organization_id=payload.organization_id,
        department_id=payload.department_id,
        code=payload.code.strip().upper(),
        name=payload.name.strip(),
        description=payload.description,
        severity_rubric=rubric_dict,
        status=CategoryStatus.PROPOSED,  # Guaranteed proposed
        is_active=True,
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return TaxonomyCategoryResponse.model_validate(category)


@router.patch(
    "/categories/{category_id}/approve",
    response_model=TaxonomyCategoryResponse,
    summary="Approve category with validated 5-level severity rubric (Admin only)",
)
async def approve_category(
    category_id: uuid.UUID,
    payload: TaxonomyCategoryApprove,
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
) -> TaxonomyCategoryResponse:
    """Admin approves category (§A11, Standing Invariant 1).

    Approval strictly requires a complete 5-level severity rubric.
    Decoupled from static AHP criteria weights.
    """
    category = await db.get(TaxonomyCategory, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Taxonomy category not found",
        )

    # Ensure admin belongs to same organization
    if claims.org_id and claims.org_id != category.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin jurisdiction mismatch for this category's organization",
        )

    # Update category status and severity rubric
    category.severity_rubric = payload.severity_rubric.model_dump()
    category.status = CategoryStatus.APPROVED
    category.updated_at = datetime.now(UTC)

    await db.commit()
    await db.refresh(category)
    await cache_delete(f"cache:taxonomy:{category.organization_id}:approved")

    return TaxonomyCategoryResponse.model_validate(category)
