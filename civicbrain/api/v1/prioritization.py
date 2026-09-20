"""API endpoints for Phase 6 AHP Prioritization, Equity Compensator & Confidence Gating."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.identity.jwt import CurrentUserClaims, get_current_user_claims
from civicbrain.domain.identity.models import StaffRole
from civicbrain.domain.prioritization.ahp import (
    AHPMatrix,
    CriteriaSubscores,
)
from civicbrain.domain.prioritization.equity import BuhlmannEquityCompensator
from civicbrain.domain.prioritization.gate import evaluate_confidence_gate
from civicbrain.domain.prioritization.models import AHPMatrixConfig, WardEquityCredibility
from civicbrain.infra.database import get_db
from civicbrain.schemas.prioritization import (
    AHPMatrixConfigRequest,
    AHPMatrixConfigResponse,
    PrioritizationEvaluationRequest,
    PrioritizationEvaluationResponse,
    WardEquityResponse,
)

router = APIRouter()


@router.post(
    "/ahp/matrix",
    response_model=AHPMatrixConfigResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Configure organization 5x5 AHP pairwise matrix (Admin only)",
)
async def set_ahp_matrix(
    payload: AHPMatrixConfigRequest,
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> AHPMatrixConfigResponse:
    """Configure or update the 5x5 Saaty AHP matrix. Strictly requires admin role and CR < 0.10."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization scope in token"
        )

    if claims.role != StaffRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization admin can configure AHP matrix",
        )

    try:
        solver = AHPMatrix(payload.matrix)
        result = solver.solve()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    if not result.is_consistent:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"AHP Matrix rejected: Consistency Ratio CR = {result.consistency_ratio} exceeds maximum allowed 0.10",
        )

    # Deactivate existing active matrix for org
    existing_stmt = select(AHPMatrixConfig).where(
        AHPMatrixConfig.organization_id == claims.org_id,
        AHPMatrixConfig.is_active.is_(True),
    )
    existing_res = await db.execute(existing_stmt)
    existing_config = existing_res.scalars().first()
    if existing_config:
        existing_config.is_active = False

    config = AHPMatrixConfig(
        organization_id=claims.org_id,
        matrix=payload.matrix,
        weights=result.weights,
        lambda_max=result.lambda_max,
        consistency_index=result.consistency_index,
        consistency_ratio=result.consistency_ratio,
        is_active=True,
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)

    return AHPMatrixConfigResponse(
        id=config.id,
        organization_id=config.organization_id,
        matrix=config.matrix,
        weights=config.weights,
        lambda_max=config.lambda_max,
        consistency_index=config.consistency_index,
        consistency_ratio=config.consistency_ratio,
        is_active=config.is_active,
    )


@router.get(
    "/ahp/matrix/active",
    response_model=AHPMatrixConfigResponse,
    summary="Get active 5x5 AHP matrix for organization",
)
async def get_active_ahp_matrix(
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> AHPMatrixConfigResponse:
    """Retrieve active AHP criteria weights for the caller's organization."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization scope in token"
        )

    stmt = select(AHPMatrixConfig).where(
        AHPMatrixConfig.organization_id == claims.org_id,
        AHPMatrixConfig.is_active.is_(True),
    )
    res = await db.execute(stmt)
    config = res.scalars().first()

    if not config:
        # Fallback to calibrated default matrix if not yet explicitly seeded
        solver = AHPMatrix()
        result = solver.solve()
        return AHPMatrixConfigResponse(
            id=uuid.uuid4(),
            organization_id=claims.org_id,
            matrix=AHPMatrix.DEFAULT_MATRIX,
            weights=result.weights,
            lambda_max=result.lambda_max,
            consistency_index=result.consistency_index,
            consistency_ratio=result.consistency_ratio,
            is_active=True,
        )

    return AHPMatrixConfigResponse(
        id=config.id,
        organization_id=config.organization_id,
        matrix=config.matrix,
        weights=config.weights,
        lambda_max=config.lambda_max,
        consistency_index=config.consistency_index,
        consistency_ratio=config.consistency_ratio,
        is_active=config.is_active,
    )


@router.get(
    "/equity/wards/{ward_id}",
    response_model=WardEquityResponse,
    summary="Get ward equity credibility and expected-vs-observed gap",
)
async def get_ward_equity(
    ward_id: uuid.UUID,
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> WardEquityResponse:
    """Retrieve ward equity stats, credibility factor, and equity boost."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization scope in token"
        )

    stmt = select(WardEquityCredibility).where(
        WardEquityCredibility.ward_id == ward_id,
        WardEquityCredibility.organization_id == claims.org_id,
    )
    res = await db.execute(stmt)
    ward_stat = res.scalars().first()

    if not ward_stat:
        # Cold start default
        compensator = BuhlmannEquityCompensator()
        result = compensator.evaluate_ward(
            verified_incident_count=0,
            historical_incident_rate=0.0,
            observed_issue_rate=0.0,
            city_prior_rate=10.0,
        )
        return WardEquityResponse(
            ward_id=ward_id,
            organization_id=claims.org_id,
            verified_incident_count=0,
            historical_incident_rate=0.0,
            credibility_factor=result.credibility_factor,
            expected_issue_rate=result.expected_issue_rate,
            observed_issue_rate=result.observed_issue_rate,
            equity_gap=result.equity_gap,
            equity_boost=result.equity_boost,
        )

    return WardEquityResponse(
        ward_id=ward_stat.ward_id,
        organization_id=ward_stat.organization_id,
        verified_incident_count=ward_stat.verified_incident_count,
        historical_incident_rate=ward_stat.historical_incident_rate,
        credibility_factor=ward_stat.credibility_factor,
        expected_issue_rate=ward_stat.expected_issue_rate,
        observed_issue_rate=ward_stat.observed_issue_rate,
        equity_gap=ward_stat.equity_gap,
        equity_boost=ward_stat.equity_boost,
    )


@router.post(
    "/evaluate",
    response_model=PrioritizationEvaluationResponse,
    summary="Evaluate 5 AHP subscores with equity boost and confidence gating",
)
async def evaluate_incident_priority(
    payload: PrioritizationEvaluationRequest,
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> PrioritizationEvaluationResponse:
    """Compute deterministic glass-box priority score across 5 dimensions and apply confidence gate."""
    if not claims.org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization scope in token"
        )

    # Fetch active weights or default
    stmt = select(AHPMatrixConfig).where(
        AHPMatrixConfig.organization_id == claims.org_id,
        AHPMatrixConfig.is_active.is_(True),
    )
    res = await db.execute(stmt)
    config = res.scalars().first()

    if config:
        weights = config.weights
    else:
        solver = AHPMatrix()
        weights = solver.solve().weights

    subscores = CriteriaSubscores(
        severity=payload.severity,
        risk=payload.risk,
        exposure=payload.exposure,
        criticality=payload.criticality,
        urgency=payload.urgency,
    )

    # Determine equity boost
    equity_boost = 0.0
    if payload.custom_equity_boost is not None:
        equity_boost = payload.custom_equity_boost
    elif payload.ward_id:
        ward_stmt = select(WardEquityCredibility).where(
            WardEquityCredibility.ward_id == payload.ward_id,
            WardEquityCredibility.organization_id == claims.org_id,
        )
        ward_res = await db.execute(ward_stmt)
        w_stat = ward_res.scalars().first()
        if w_stat:
            equity_boost = w_stat.equity_boost

    eval_result = evaluate_confidence_gate(
        subscores=subscores,
        weights=weights,
        equity_boost=equity_boost,
        confidence_score=payload.confidence_score,
    )

    return PrioritizationEvaluationResponse(
        subscores={
            "severity": payload.severity,
            "risk": payload.risk,
            "exposure": payload.exposure,
            "criticality": payload.criticality,
            "urgency": payload.urgency,
        },
        weights_used=weights,
        raw_priority_score=eval_result.raw_priority_score,
        equity_boost=eval_result.equity_boost,
        final_priority_score=eval_result.final_priority_score,
        confidence_score=eval_result.confidence_score,
        requires_human_review=eval_result.requires_human_review,
        review_reason=eval_result.review_reason,
        target_status=eval_result.target_status,
    )
