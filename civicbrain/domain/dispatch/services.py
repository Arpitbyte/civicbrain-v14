"""Dispatch domain services (§A14, §A15, §A16)."""

import logging
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.dispatch.models import (
    ConflictReviewStatus,
    DispatchConflictReview,
    SyncMutationLog,
    SyncMutationStatus,
    WorkOrder,
    WorkOrderStatus,
)
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
    ConflictAdjudicationResponse,
    ConflictDecision,
    DisputeResponse,
    FieldSyncPushRequest,
    FieldSyncResponse,
    MutationResult,
    WorkOrderResponse,
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
        version=1,
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
    work_order.version += 1

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
    work_order.version += 1

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
        "Citizen dispute filed for report %s on incidents %s. Reason length: %d chars",
        report.id,
        appealed_ids,
        len(reason),
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


# --- Phase 9: Karmi Sahayak Offline Sync & Conflict Adjudication (§A15) ---


async def process_field_sync(
    db: AsyncSession,
    worker_id: uuid.UUID,
    push_request: FieldSyncPushRequest,
) -> FieldSyncResponse:
    """Executes two-way delta sync for Karmi Sahayak with strict idempotency and conflict arbitration."""
    mutation_results: list[MutationResult] = []

    for mut in push_request.mutations:
        # 1. Idempotency Check (Case 1)
        idemp_stmt = select(SyncMutationLog).where(
            SyncMutationLog.worker_id == worker_id,
            SyncMutationLog.client_mutation_id == mut.client_mutation_id,
        )
        idemp_res = await db.execute(idemp_stmt)
        logged_mut = idemp_res.scalar_one_or_none()
        if logged_mut:
            review_id = None
            if logged_mut.status == SyncMutationStatus.CONFLICT:
                cr_stmt = select(DispatchConflictReview.id).where(
                    DispatchConflictReview.client_mutation_id == mut.client_mutation_id
                )
                cr_res = await db.execute(cr_stmt)
                review_id = cr_res.scalar_one_or_none()

            mutation_results.append(
                MutationResult(
                    client_mutation_id=mut.client_mutation_id,
                    status=logged_mut.status,
                    conflict_reason=logged_mut.conflict_reason,
                    conflict_review_id=review_id,
                )
            )
            continue

        # Process new mutation on work_order
        wo_stmt = select(WorkOrder).where(WorkOrder.id == mut.entity_id)
        wo_res = await db.execute(wo_stmt)
        work_order = wo_res.scalar_one_or_none()

        if not work_order:
            # Entity missing
            log_entry = SyncMutationLog(
                client_mutation_id=mut.client_mutation_id,
                organization_id=uuid.uuid4(),  # Fallback if unresolvable
                worker_id=worker_id,
                entity_type=mut.entity_type,
                entity_id=mut.entity_id,
                action=mut.action,
                payload=mut.payload,
                status=SyncMutationStatus.REJECTED,
                conflict_reason="work_order_not_found",
            )
            db.add(log_entry)
            await db.flush()
            mutation_results.append(
                MutationResult(
                    client_mutation_id=mut.client_mutation_id,
                    status=SyncMutationStatus.REJECTED,
                    conflict_reason="work_order_not_found",
                )
            )
            continue

        org_id = work_order.organization_id

        # Dispatch action handling
        if mut.action == "start":
            if work_order.assigned_worker_id and work_order.assigned_worker_id != worker_id:
                # Reassigned
                log_entry = SyncMutationLog(
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.CONFLICT,
                    conflict_reason="reassigned_by_dispatcher",
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.CONFLICT,
                        conflict_reason="reassigned_by_dispatcher",
                    )
                )
            elif work_order.status == WorkOrderStatus.CANCELLED:
                # Cancelled
                log_entry = SyncMutationLog(
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.CONFLICT,
                    conflict_reason="cancelled_by_dispatcher",
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.CONFLICT,
                        conflict_reason="cancelled_by_dispatcher",
                    )
                )
            else:
                # Clean Progression (Case 2)
                work_order.status = WorkOrderStatus.IN_PROGRESS
                work_order.started_at = mut.captured_at
                work_order.version += 1

                inc_stmt = select(Incident).where(Incident.id == work_order.incident_id)
                inc_res = await db.execute(inc_stmt)
                incident = inc_res.scalar_one_or_none()
                if incident:
                    incident.status = IncidentStatus.IN_PROGRESS
                    incident.in_progress_at = mut.captured_at
                    await _recompute_reports_for_incident(db, incident.id)

                log_entry = SyncMutationLog(
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.APPLIED,
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.APPLIED,
                    )
                )

        elif mut.action == "resolve":
            res_notes = mut.payload.get("resolution_notes", "")
            res_media = mut.payload.get("resolution_media_urls", [])
            lat = mut.payload.get("latitude")
            lon = mut.payload.get("longitude")

            # Validate Evidence (Case 7)
            if not res_notes or not str(res_notes).strip() or not res_media or len(res_media) == 0:
                log_entry = SyncMutationLog(
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.REJECTED,
                    conflict_reason="missing_evidence",
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.REJECTED,
                        conflict_reason="missing_evidence",
                    )
                )
                continue

            # Validate Proximity (Case 6)
            prox_query = text(
                "SELECT ST_DWithin(geom::geography, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, 50.0) "
                "FROM incident WHERE id = :incident_id"
            )
            prox_res = await db.execute(
                prox_query,
                {"lon": lon, "lat": lat, "incident_id": work_order.incident_id},
            )
            is_within = prox_res.scalar()
            if not is_within:
                log_entry = SyncMutationLog(
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.REJECTED,
                    conflict_reason="resolution_out_of_bounds",
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.REJECTED,
                        conflict_reason="resolution_out_of_bounds",
                    )
                )
                continue

            point_geom = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

            # Evidence passed validation. Check concurrency cases:
            if work_order.status == WorkOrderStatus.COMPLETED:
                # Peer Race: Already completed by another worker (Case 5)
                log_entry = SyncMutationLog(
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.CONFLICT,
                    conflict_reason="conflict_already_completed",
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.CONFLICT,
                        conflict_reason="conflict_already_completed",
                    )
                )

            elif work_order.assigned_worker_id and work_order.assigned_worker_id != worker_id:
                # Case 3: Reassigned by Dispatcher with VALID Evidence -> Preserve in Review Queue
                conflict_review = DispatchConflictReview(
                    id=uuid.uuid4(),
                    organization_id=org_id,
                    work_order_id=work_order.id,
                    incident_id=work_order.incident_id,
                    worker_id=worker_id,
                    client_mutation_id=mut.client_mutation_id,
                    conflict_type="reassigned_by_dispatcher",
                    submitted_notes=str(res_notes),
                    submitted_media_urls=list(res_media),
                    submitted_geom=point_geom,
                    captured_at=mut.captured_at,
                    status=ConflictReviewStatus.PENDING,
                )
                db.add(conflict_review)
                await db.flush()

                log_entry = SyncMutationLog(
                    id=uuid.uuid4(),
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.CONFLICT,
                    conflict_reason="reassigned_by_dispatcher",
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.CONFLICT,
                        conflict_reason="reassigned_by_dispatcher",
                        conflict_review_id=conflict_review.id,
                    )
                )

            elif work_order.status == WorkOrderStatus.CANCELLED:
                # Case 4: Cancelled by Dispatcher with VALID Evidence -> Preserve in Review Queue
                conflict_review = DispatchConflictReview(
                    id=uuid.uuid4(),
                    organization_id=org_id,
                    work_order_id=work_order.id,
                    incident_id=work_order.incident_id,
                    worker_id=worker_id,
                    client_mutation_id=mut.client_mutation_id,
                    conflict_type="cancelled_by_dispatcher",
                    submitted_notes=str(res_notes),
                    submitted_media_urls=list(res_media),
                    submitted_geom=point_geom,
                    captured_at=mut.captured_at,
                    status=ConflictReviewStatus.PENDING,
                )
                db.add(conflict_review)
                await db.flush()

                log_entry = SyncMutationLog(
                    id=uuid.uuid4(),
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.CONFLICT,
                    conflict_reason="cancelled_by_dispatcher",
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.CONFLICT,
                        conflict_reason="cancelled_by_dispatcher",
                        conflict_review_id=conflict_review.id,
                    )
                )

            else:
                # Case 2: Clean Progression
                work_order.status = WorkOrderStatus.COMPLETED
                work_order.completed_at = mut.captured_at
                work_order.resolution_notes = str(res_notes)
                work_order.resolution_media_urls = list(res_media)
                work_order.resolution_geom = point_geom
                work_order.version += 1

                inc_stmt = select(Incident).where(Incident.id == work_order.incident_id)
                inc_res = await db.execute(inc_stmt)
                incident = inc_res.scalar_one_or_none()
                if incident:
                    incident.status = IncidentStatus.RESOLVED
                    incident.resolved_at = mut.captured_at
                    incident.resolution_notes = str(res_notes)
                    incident.resolution_proof_urls = list(res_media)
                    incident.resolution_geom = point_geom
                    incident.auto_confirm_deadline = mut.captured_at + timedelta(hours=72)
                    await _recompute_reports_for_incident(db, incident.id)

                log_entry = SyncMutationLog(
                    client_mutation_id=mut.client_mutation_id,
                    organization_id=org_id,
                    worker_id=worker_id,
                    entity_type=mut.entity_type,
                    entity_id=mut.entity_id,
                    action=mut.action,
                    payload=mut.payload,
                    status=SyncMutationStatus.APPLIED,
                    server_version=work_order.version,
                )
                db.add(log_entry)
                await db.flush()
                mutation_results.append(
                    MutationResult(
                        client_mutation_id=mut.client_mutation_id,
                        status=SyncMutationStatus.APPLIED,
                    )
                )

        else:
            # Unknown action
            log_entry = SyncMutationLog(
                client_mutation_id=mut.client_mutation_id,
                organization_id=org_id,
                worker_id=worker_id,
                entity_type=mut.entity_type,
                entity_id=mut.entity_id,
                action=mut.action,
                payload=mut.payload,
                status=SyncMutationStatus.REJECTED,
                conflict_reason="unsupported_action",
                server_version=work_order.version,
            )
            db.add(log_entry)
            await db.flush()
            mutation_results.append(
                MutationResult(
                    client_mutation_id=mut.client_mutation_id,
                    status=SyncMutationStatus.REJECTED,
                    conflict_reason="unsupported_action",
                )
            )

    # Pull server changes since cursor
    server_query = select(WorkOrder).where(WorkOrder.assigned_worker_id == worker_id)
    if push_request.since_cursor:
        server_query = server_query.where(WorkOrder.updated_at >= push_request.since_cursor)
    server_res = await db.execute(server_query)
    server_changes = [WorkOrderResponse.model_validate(wo) for wo in server_res.scalars().all()]

    return FieldSyncResponse(
        mutation_results=mutation_results,
        server_changes=server_changes,
        new_cursor=datetime.now(UTC),
    )


async def list_conflicts_for_worker(
    db: AsyncSession,
    worker_id: uuid.UUID,
) -> list[SyncMutationLog]:
    """Retrieves sync mutations flagged with CONFLICT for the given field worker."""
    stmt = (
        select(SyncMutationLog)
        .where(
            SyncMutationLog.worker_id == worker_id,
            SyncMutationLog.status == SyncMutationStatus.CONFLICT,
        )
        .order_by(SyncMutationLog.created_at.desc())
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def list_dispatch_conflicts(
    db: AsyncSession,
    organization_id: uuid.UUID,
    review_status: ConflictReviewStatus | None = ConflictReviewStatus.PENDING,
    page: int = 1,
    page_size: int = 50,
) -> list[DispatchConflictReview]:
    """Lists reviewable concurrent dispatch conflicts in the supervisor review queue."""
    stmt = (
        select(DispatchConflictReview)
        .where(DispatchConflictReview.organization_id == organization_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(DispatchConflictReview.created_at.desc())
    )
    if review_status:
        stmt = stmt.where(DispatchConflictReview.status == review_status)

    res = await db.execute(stmt)
    return list(res.scalars().all())


async def adjudicate_dispatch_conflict(
    db: AsyncSession,
    conflict_id: uuid.UUID,
    reviewer_id: uuid.UUID,
    decision: ConflictDecision,
    notes: str | None = None,
) -> ConflictAdjudicationResponse:
    """Supervisory adjudication of concurrent dispatch conflict.

    - accept_worker_evidence: Worker's preserved resolution evidence stands, completing work order and resolving incident.
    - uphold_dispatcher_action: Dispatcher cancellation/reassignment stands.
    """
    stmt = select(DispatchConflictReview).where(DispatchConflictReview.id == conflict_id)
    res = await db.execute(stmt)
    conflict = res.scalar_one_or_none()
    if not conflict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conflict review {conflict_id} not found.",
        )

    if conflict.status != ConflictReviewStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conflict review has already been adjudicated.",
        )

    now = datetime.now(UTC)

    if decision == ConflictDecision.ACCEPT_WORKER_EVIDENCE:
        conflict.status = ConflictReviewStatus.ACCEPTED
        conflict.reviewed_by = reviewer_id
        conflict.reviewed_at = now
        conflict.review_notes = notes

        # Worker evidence stands: complete work order
        wo_stmt = select(WorkOrder).where(WorkOrder.id == conflict.work_order_id)
        wo_res = await db.execute(wo_stmt)
        work_order = wo_res.scalar_one_or_none()
        if work_order:
            work_order.status = WorkOrderStatus.COMPLETED
            work_order.assigned_worker_id = conflict.worker_id
            work_order.completed_at = conflict.captured_at
            work_order.resolution_notes = conflict.submitted_notes
            work_order.resolution_media_urls = conflict.submitted_media_urls
            work_order.resolution_geom = conflict.submitted_geom
            work_order.version += 1

        # Resolve parent incident
        inc_stmt = select(Incident).where(Incident.id == conflict.incident_id)
        inc_res = await db.execute(inc_stmt)
        incident = inc_res.scalar_one_or_none()
        if incident:
            incident.status = IncidentStatus.RESOLVED
            incident.assigned_worker_id = conflict.worker_id
            incident.resolved_at = conflict.captured_at
            incident.resolution_notes = conflict.submitted_notes
            incident.resolution_proof_urls = conflict.submitted_media_urls
            incident.resolution_geom = conflict.submitted_geom
            incident.auto_confirm_deadline = now + timedelta(hours=72)
            await _recompute_reports_for_incident(db, incident.id)

        msg = "Worker evidence accepted: work order completed and incident resolved."

    else:
        # Uphold dispatcher action
        conflict.status = ConflictReviewStatus.DISMISSED
        conflict.reviewed_by = reviewer_id
        conflict.reviewed_at = now
        conflict.review_notes = notes
        msg = "Dispatcher action upheld: conflict dismissed."

    await db.flush()
    return ConflictAdjudicationResponse(
        id=conflict.id,
        status=conflict.status,
        reviewed_by=conflict.reviewed_by,
        reviewed_at=conflict.reviewed_at,
        review_notes=conflict.review_notes,
        message=msg,
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
