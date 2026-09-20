"""Dispatch domain services (§A14, §A16)."""

import logging
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.dispatch.models import WorkOrder, WorkOrderStatus
from civicbrain.domain.identity.models import Department
from civicbrain.domain.intake.models import (
    Incident,
    IncidentStatus,
    IntakeReport,
    IntakeStatus,
    Observation,
)
from civicbrain.domain.intake.services import recompute_intake_report_status
from civicbrain.schemas.dispatch import (
    AutoConfirmResponse,
    ConfirmResponse,
    DisputeResponse,
)

logger = logging.getLogger(__name__)


async def create_work_order(
    db: AsyncSession,
    organization_id: uuid.UUID,
    incident_id: uuid.UUID,
    department_id: uuid.UUID,
    assigned_worker_id: uuid.UUID | None = None,
) -> WorkOrder:
    """Creates a work order and dispatches it, advancing incident to ASSIGNED."""
    # Verify incident
    inc_stmt = select(Incident).where(
        Incident.id == incident_id, Incident.organization_id == organization_id
    )
    inc_res = await db.execute(inc_stmt)
    incident = inc_res.scalar_one_or_none()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found in organization {organization_id}.",
        )

    # Verify department
    dept_stmt = select(Department).where(
        Department.id == department_id, Department.organization_id == organization_id
    )
    dept_res = await db.execute(dept_stmt)
    if not dept_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department {department_id} not found.",
        )

    now = datetime.now(UTC)
    wo_status = WorkOrderStatus.DISPATCHED if assigned_worker_id else WorkOrderStatus.CREATED

    work_order = WorkOrder(
        organization_id=organization_id,
        incident_id=incident_id,
        department_id=department_id,
        assigned_worker_id=assigned_worker_id,
        status=wo_status,
        dispatched_at=now if assigned_worker_id else None,
    )
    db.add(work_order)

    # Sync with incident lifecycle (§A16)
    if assigned_worker_id:
        incident.status = IncidentStatus.ASSIGNED
        incident.assigned_at = now
        incident.assigned_worker_id = assigned_worker_id

        # Recompute parent reports if linked
        await _recompute_reports_for_incident(db, incident.id)

    await db.flush()
    return work_order


async def start_work_order(
    db: AsyncSession,
    work_order_id: uuid.UUID,
    worker_user_id: uuid.UUID,
) -> WorkOrder:
    """Field worker marks arrival/start; transitions work order and incident to IN_PROGRESS."""
    stmt = select(WorkOrder).where(WorkOrder.id == work_order_id)
    res = await db.execute(stmt)
    work_order = res.scalar_one_or_none()
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order {work_order_id} not found.",
        )

    if work_order.assigned_worker_id and work_order.assigned_worker_id != worker_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the assigned field worker for this work order.",
        )

    if work_order.status == WorkOrderStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot start an already completed work order.",
        )

    now = datetime.now(UTC)
    work_order.status = WorkOrderStatus.IN_PROGRESS
    work_order.started_at = now

    inc_stmt = select(Incident).where(Incident.id == work_order.incident_id)
    inc_res = await db.execute(inc_stmt)
    incident = inc_res.scalar_one_or_none()
    if incident:
        incident.status = IncidentStatus.IN_PROGRESS
        incident.in_progress_at = now
        await _recompute_reports_for_incident(db, incident.id)

    await db.flush()
    return work_order


async def resolve_work_order(
    db: AsyncSession,
    work_order_id: uuid.UUID,
    worker_user_id: uuid.UUID,
    resolution_notes: str,
    resolution_media_urls: list[str],
    latitude: float,
    longitude: float,
) -> WorkOrder:
    """Submits evidence-gated resolution.

    Enforces:
    1. Non-empty photographic evidence (resolution_media_urls)
    2. Non-empty notes (resolution_notes)
    3. PostGIS ST_DWithin <= 50.0m proximity gate
    """
    stmt = select(WorkOrder).where(WorkOrder.id == work_order_id)
    res = await db.execute(stmt)
    work_order = res.scalar_one_or_none()
    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order {work_order_id} not found.",
        )

    if work_order.assigned_worker_id and work_order.assigned_worker_id != worker_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the assigned field worker for this work order.",
        )

    if work_order.status == WorkOrderStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Work order is already completed.",
        )

    # 1. Evidence Check
    if not resolution_media_urls or len(resolution_media_urls) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Resolution proof media URLs cannot be empty.",
        )
    if not resolution_notes or not resolution_notes.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Resolution notes cannot be empty.",
        )

    # 2. PostGIS ST_DWithin 50.0m Geographic Proximity Check
    proximity_query = text(
        "SELECT ST_DWithin(geom::geography, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, 50.0) "
        "FROM incident WHERE id = :incident_id"
    )
    prox_res = await db.execute(
        proximity_query,
        {"lon": longitude, "lat": latitude, "incident_id": work_order.incident_id},
    )
    is_within = prox_res.scalar()
    if not is_within:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="resolution_out_of_bounds",
        )

    now = datetime.now(UTC)
    point_geom = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

    # Complete Work Order
    work_order.status = WorkOrderStatus.COMPLETED
    work_order.completed_at = now
    work_order.resolution_notes = resolution_notes
    work_order.resolution_media_urls = resolution_media_urls
    work_order.resolution_geom = point_geom

    # Resolve Incident
    inc_stmt = select(Incident).where(Incident.id == work_order.incident_id)
    inc_res = await db.execute(inc_stmt)
    incident = inc_res.scalar_one_or_none()
    if incident:
        incident.status = IncidentStatus.RESOLVED
        incident.resolved_at = now
        incident.resolution_notes = resolution_notes
        incident.resolution_proof_urls = resolution_media_urls
        incident.resolution_geom = point_geom
        incident.auto_confirm_deadline = now + timedelta(hours=72)
        await _recompute_reports_for_incident(db, incident.id)

    await db.flush()
    return work_order


async def citizen_confirm_report(
    db: AsyncSession,
    tracking_token: str,
) -> ConfirmResponse:
    """Citizen confirms satisfaction with resolution; sets child incidents to CONFIRMED and report to CLOSED."""
    rep_stmt = select(IntakeReport).where(IntakeReport.tracking_token == tracking_token)
    rep_res = await db.execute(rep_stmt)
    report = rep_res.scalar_one_or_none()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intake report not found for tracking token.",
        )

    incidents = await _get_incidents_for_report(db, report.id)
    resolved_incidents = [inc for inc in incidents if inc.status == IncidentStatus.RESOLVED]
    if not resolved_incidents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resolved incidents found to confirm.",
        )

    now = datetime.now(UTC)
    confirmed_ids: list[uuid.UUID] = []
    for inc in resolved_incidents:
        inc.status = IncidentStatus.CONFIRMED
        inc.confirmed_at = now
        confirmed_ids.append(inc.id)

    report.status = IntakeStatus.CLOSED
    await db.flush()

    return ConfirmResponse(
        report_id=report.id,
        status=report.status.value,
        confirmed_incident_ids=confirmed_ids,
        message="Citizen resolution confirmed successfully.",
    )


async def citizen_dispute_report(
    db: AsyncSession,
    tracking_token: str,
    reason: str,
) -> DisputeResponse:
    """Citizen disputes resolution proof; strictly routes child incidents to APPEALED and report to IN_PROGRESS."""
    rep_stmt = select(IntakeReport).where(IntakeReport.tracking_token == tracking_token)
    rep_res = await db.execute(rep_stmt)
    report = rep_res.scalar_one_or_none()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intake report not found for tracking token.",
        )

    incidents = await _get_incidents_for_report(db, report.id)
    resolved_incidents = [inc for inc in incidents if inc.status == IncidentStatus.RESOLVED]
    if not resolved_incidents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resolved incidents found to dispute.",
        )

    now = datetime.now(UTC)
    appealed_ids: list[uuid.UUID] = []
    for inc in resolved_incidents:
        inc.status = IncidentStatus.APPEALED
        inc.appealed_at = now
        inc.appeal_reason = reason
        appealed_ids.append(inc.id)

    report.status = IntakeStatus.IN_PROGRESS
    logger.warning(
        "Citizen dispute filed for report %s on incidents %s. Reason: %s",
        report.id,
        appealed_ids,
        reason,
    )
    await db.flush()

    return DisputeResponse(
        report_id=report.id,
        status=report.status.value,
        appealed_incident_ids=appealed_ids,
        message="Resolution disputed. Case routed to supervisory review (APPEALED).",
    )


async def evaluate_auto_confirm_cron(
    db: AsyncSession,
) -> AutoConfirmResponse:
    """Evaluates all incidents in RESOLVED state where auto_confirm_deadline has elapsed."""
    now = datetime.now(UTC)
    stmt = select(Incident).where(
        Incident.status == IncidentStatus.RESOLVED,
        Incident.auto_confirm_deadline <= now,
    )
    res = await db.execute(stmt)
    expired_incidents = list(res.scalars().all())

    confirmed_ids: list[uuid.UUID] = []
    for inc in expired_incidents:
        inc.status = IncidentStatus.CONFIRMED
        inc.confirmed_at = now
        confirmed_ids.append(inc.id)
        await _recompute_reports_for_incident(db, inc.id)

    await db.flush()
    return AutoConfirmResponse(
        confirmed_count=len(confirmed_ids),
        confirmed_incident_ids=confirmed_ids,
    )


async def _get_incidents_for_report(db: AsyncSession, report_id: uuid.UUID) -> list[Incident]:
    """Helper retrieving all child incidents associated with an intake report."""
    stmt = (
        select(Incident)
        .join(Observation, Observation.incident_id == Incident.id)
        .where(Observation.intake_report_id == report_id)
        .distinct()
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def _recompute_reports_for_incident(db: AsyncSession, incident_id: uuid.UUID) -> None:
    """Helper recomputing all intake reports containing observations for the incident."""
    obs_stmt = (
        select(Observation.intake_report_id)
        .where(Observation.incident_id == incident_id)
        .distinct()
    )
    obs_res = await db.execute(obs_stmt)
    report_ids = [r for r in obs_res.scalars().all() if r is not None]
    for rep_id in report_ids:
        await recompute_intake_report_status(db, rep_id)
