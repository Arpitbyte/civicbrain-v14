"""FastAPI Operational Incidents Endpoints."""

import logging
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from civicbrain.domain.identity.jwt import SupabaseClaims, get_current_user_claims
from civicbrain.domain.intake.models import Incident, IncidentStatus, Observation
from civicbrain.domain.intake.services import recompute_intake_report_status
from civicbrain.infra.database import get_db
from civicbrain.schemas.intake import IncidentResponse, IncidentStatusUpdate, ObservationResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get("", response_model=list[IncidentResponse])
async def list_incidents(
    organization_id: uuid.UUID = Query(...),
    department_id: uuid.UUID | None = None,
    ward_id: uuid.UUID | None = None,
    incident_status: IncidentStatus | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_current_user_claims),
) -> list[IncidentResponse]:
    """Lists operational incidents, scoped by user role and filters."""
    stmt = (
        select(Incident)
        .where(Incident.organization_id == organization_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Incident.created_at.desc())
    )
    if department_id:
        stmt = stmt.where(Incident.department_id == department_id)
    if ward_id:
        stmt = stmt.where(Incident.ward_id == ward_id)
    if incident_status:
        stmt = stmt.where(Incident.status == incident_status)

    res = await db.execute(stmt)
    incidents = list(res.scalars().all())
    return [IncidentResponse.model_validate(inc) for inc in incidents]


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_current_user_claims),
) -> IncidentResponse:
    """Fetches details for a single operational incident."""
    res = await db.execute(select(Incident).where(Incident.id == incident_id))
    inc = res.scalar_one_or_none()
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return IncidentResponse.model_validate(inc)


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
async def update_incident_status(
    incident_id: uuid.UUID,
    payload: IncidentStatusUpdate,
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_current_user_claims),
) -> IncidentResponse:
    """Progresses incident state across §A16 lifecycle and triggers least-advanced parent recalculation."""
    res = await db.execute(
        select(Incident)
        .options(selectinload(Incident.observations))
        .where(Incident.id == incident_id)
    )
    inc = res.scalar_one_or_none()
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")

    new_status = payload.status
    now = datetime.now(UTC)

    # Record §A16 state timestamps
    if new_status == IncidentStatus.TRIAGED:
        inc.triaged_at = now
    elif new_status == IncidentStatus.VERIFIED:
        inc.verified_at = now
    elif new_status == IncidentStatus.PRIORITIZED:
        inc.prioritized_at = now
    elif new_status == IncidentStatus.ASSIGNED:
        inc.assigned_at = now
    elif new_status == IncidentStatus.IN_PROGRESS:
        inc.in_progress_at = now
    elif new_status == IncidentStatus.RESOLVED:
        inc.resolved_at = now
        inc.resolution_notes = payload.resolution_notes
    elif new_status == IncidentStatus.CONFIRMED:
        inc.confirmed_at = now
    elif new_status == IncidentStatus.REJECTED:
        inc.rejected_at = now
        inc.rejection_reason = payload.reason
    elif new_status == IncidentStatus.APPEALED:
        inc.appealed_at = now
        inc.appeal_reason = payload.reason
    elif new_status == IncidentStatus.REOPENED:
        inc.reopened_at = now

    inc.status = new_status
    await db.flush()

    # Automatically re-evaluate parent intake_report.status for all parent reports
    parent_report_ids = {obs.intake_report_id for obs in inc.observations}
    for report_id in parent_report_ids:
        await recompute_intake_report_status(db, report_id)

    await db.commit()
    await db.refresh(inc)
    return IncidentResponse.model_validate(inc)


@router.get("/{incident_id}/observations", response_model=list[ObservationResponse])
async def get_incident_observations(
    incident_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_current_user_claims),
) -> list[ObservationResponse]:
    """Lists all atomic citizen observations clustered into this operational incident."""
    res = await db.execute(select(Observation).where(Observation.incident_id == incident_id))
    observations = list(res.scalars().all())
    return [ObservationResponse.model_validate(o) for o in observations]
