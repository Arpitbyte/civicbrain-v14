"""FastAPI Analytics and ETA Prediction Endpoints (§A21, §A23)."""

import logging
import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.analytics.models import CategoryServiceTimePrior
from civicbrain.domain.analytics.services import (
    compute_ward_report_card,
    generate_corporator_digest,
    predict_incident_eta,
)
from civicbrain.domain.identity.jwt import (
    CurrentUserClaims,
    get_current_user_claims,
    get_optional_user_claims,
    require_roles,
)
from civicbrain.domain.identity.models import StaffRole
from civicbrain.infra.database import get_db
from civicbrain.schemas.analytics import (
    CategoryPriorCreate,
    CategoryPriorResponse,
    CorporatorDigestResponse,
    ETAPredictionResponse,
    WardReportCardResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["Analytics & Service-Time Prediction"])


@router.get(
    "/wards/{ward_id}/report-card",
    response_model=WardReportCardResponse,
    summary="Fetch or compute ward municipal performance report card",
)
async def get_ward_report_card(
    ward_id: uuid.UUID,
    from_date: date | None = Query(default=None, description="Start date of report window"),
    to_date: date | None = Query(default=None, description="End date of report window"),
    period_type: str = Query(default="weekly", description="Period type: daily, weekly, monthly"),
    persist: bool = Query(default=True, description="Persist snapshot to database"),
    db: AsyncSession = Depends(get_db),
    _claims: CurrentUserClaims | None = Depends(get_optional_user_claims),
) -> WardReportCardResponse:
    """Publicly accessible municipal scorecard aggregated at the ward level (§A21)."""
    return await compute_ward_report_card(
        db=db,
        ward_id=ward_id,
        from_date=from_date,
        to_date=to_date,
        period_type=period_type,
        persist=persist,
    )


@router.get(
    "/corporator/digest",
    response_model=CorporatorDigestResponse,
    summary="Generate executive operational digest for a corporator's ward",
)
async def get_corporator_digest(
    ward_id: uuid.UUID = Query(..., description="Target municipal ward ID to inspect"),
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> CorporatorDigestResponse:
    """Generates executive operational digest tailored for Ward Elected Representatives (§A18, §A21).

    Enforces strict ward ownership check against elected_representative / user_role_assignment.
    Corporators cannot inspect unauthorized wards (returns HTTP 403 Forbidden).
    """
    return await generate_corporator_digest(
        db=db,
        user_claims=claims,
        ward_id=ward_id,
    )


@router.get(
    "/incidents/{incident_id}/eta",
    response_model=ETAPredictionResponse,
    summary="Empirical parametric ETA prediction and SLA confidence bounds",
)
async def get_incident_eta_prediction(
    incident_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _claims: CurrentUserClaims | None = Depends(get_optional_user_claims),
) -> ETAPredictionResponse:
    """Estimates deterministic completion hours and confidence intervals (§A23, Bootstrap Principle §A3)."""
    return await predict_incident_eta(db=db, incident_id=incident_id)


@router.post(
    "/priors",
    response_model=CategoryPriorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Configure category service-time prior (Admin only)",
)
async def configure_category_prior(
    payload: CategoryPriorCreate,
    claims: CurrentUserClaims = Depends(require_roles([StaffRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
) -> CategoryPriorResponse:
    """Configures category baseline service-time priors."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing organization_id in token claims",
        )

    # Check if prior exists
    query = select(CategoryServiceTimePrior).where(
        CategoryServiceTimePrior.organization_id == claims.org_id,
        CategoryServiceTimePrior.category_code == payload.category_code,
    )
    res = await db.execute(query)
    prior = res.scalar_one_or_none()

    if prior:
        prior.base_resolution_hours = payload.base_resolution_hours
        prior.p25_hours = payload.p25_hours
        prior.p50_hours = payload.p50_hours
        prior.p90_hours = payload.p90_hours
        prior.min_hours = payload.min_hours
        prior.sample_size = payload.sample_size
    else:
        prior = CategoryServiceTimePrior(
            organization_id=claims.org_id,
            category_code=payload.category_code,
            base_resolution_hours=payload.base_resolution_hours,
            p25_hours=payload.p25_hours,
            p50_hours=payload.p50_hours,
            p90_hours=payload.p90_hours,
            min_hours=payload.min_hours,
            sample_size=payload.sample_size,
        )
        db.add(prior)

    await db.commit()
    await db.refresh(prior)
    return CategoryPriorResponse(
        id=prior.id,
        organization_id=prior.organization_id,
        category_code=prior.category_code,
        base_resolution_hours=prior.base_resolution_hours,
        p25_hours=prior.p25_hours,
        p50_hours=prior.p50_hours,
        p90_hours=prior.p90_hours,
        min_hours=prior.min_hours,
        sample_size=prior.sample_size,
        created_at=prior.created_at,
        updated_at=prior.updated_at,
    )


@router.get(
    "/priors",
    response_model=list[CategoryPriorResponse],
    summary="List category service-time priors",
)
async def list_category_priors(
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> list[CategoryPriorResponse]:
    """Lists category priors for the caller's organization."""
    if not claims.org_id:
        return []

    query = select(CategoryServiceTimePrior).where(
        CategoryServiceTimePrior.organization_id == claims.org_id
    )
    res = await db.execute(query)
    priors = list(res.scalars().all())

    return [
        CategoryPriorResponse(
            id=p.id,
            organization_id=p.organization_id,
            category_code=p.category_code,
            base_resolution_hours=p.base_resolution_hours,
            p25_hours=p.p25_hours,
            p50_hours=p.p50_hours,
            p90_hours=p.p90_hours,
            min_hours=p.min_hours,
            sample_size=p.sample_size,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in priors
    ]
