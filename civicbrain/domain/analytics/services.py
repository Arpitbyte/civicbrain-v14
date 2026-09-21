"""Analytical and Predictive Domain Services (§A21, §A23)."""

import logging
import statistics
import uuid
from datetime import UTC, date, datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.analytics.models import (
    CategoryServiceTimePrior,
    WardReportCardSnapshot,
)
from civicbrain.domain.dispatch.models import WorkOrder, WorkOrderStatus
from civicbrain.domain.identity.jwt import CurrentUserClaims
from civicbrain.domain.identity.models import (
    Department,
    ElectedRepresentative,
    StaffRole,
    UserRoleAssignment,
)
from civicbrain.domain.intake.models import Incident, IncidentStatus
from civicbrain.domain.prioritization.models import (
    WardEquityCredibility,
    WardResolutionStat,
)
from civicbrain.schemas.analytics import (
    CorporatorDigestResponse,
    ETAPredictionResponse,
    SLABreachItem,
    WardReportCardResponse,
)

logger = logging.getLogger(__name__)

ACTIVE_INCIDENT_STATUSES = [
    IncidentStatus.REPORTED,
    IncidentStatus.TRIAGED,
    IncidentStatus.VERIFIED,
    IncidentStatus.PRIORITIZED,
    IncidentStatus.ASSIGNED,
    IncidentStatus.IN_PROGRESS,
    IncidentStatus.APPEALED,
    IncidentStatus.REOPENED,
]


def compute_csi(confirmed: int, appealed: int, resolved: int) -> float | None:
    """Computes Citizen Satisfaction Index (CSI).

    CSI = N_confirmed / (N_confirmed + N_appealed).
    If confirmed + appealed == 0 but resolved > 0, returns 1.0 (uncontested).
    If no resolved cases exist, returns None.
    """
    if confirmed + appealed > 0:
        return round(float(confirmed) / float(confirmed + appealed), 4)
    if resolved > 0 and appealed == 0:
        return 1.0
    return None


async def compute_ward_report_card(
    db: AsyncSession,
    ward_id: uuid.UUID,
    from_date: date | None = None,
    to_date: date | None = None,
    period_type: str = "weekly",
    persist: bool = True,
) -> WardReportCardResponse:
    """Calculates ward performance scorecard and optionally persists snapshot (§A21)."""
    snapshot_date = to_date or date.today()
    start_dt = (
        datetime.combine(from_date, datetime.min.time(), tzinfo=UTC)
        if from_date
        else datetime.now(UTC) - timedelta(days=7)
    )
    end_dt = (
        datetime.combine(snapshot_date, datetime.max.time(), tzinfo=UTC)
        if to_date
        else datetime.now(UTC)
    )

    # 1. Fetch incidents in ward
    query = select(Incident).where(Incident.ward_id == ward_id)
    res = await db.execute(query)
    incidents = list(res.scalars().all())

    if not incidents:
        # Check ward existence to obtain organization_id
        from civicbrain.domain.identity.models import Ward

        w_res = await db.execute(select(Ward).where(Ward.id == ward_id))
        w = w_res.scalar_one_or_none()
        if not w:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ward {ward_id} not found",
            )
        org_id = w.organization_id
    else:
        org_id = incidents[0].organization_id

    # Filter incidents within the reporting window
    window_incidents = [
        inc for inc in incidents if inc.created_at and start_dt <= inc.created_at <= end_dt
    ]
    total_reported = len(window_incidents) if from_date else len(incidents)

    total_active = sum(1 for inc in incidents if inc.status in ACTIVE_INCIDENT_STATUSES)
    resolved_incidents = [
        inc
        for inc in incidents
        if inc.status in (IncidentStatus.RESOLVED, IncidentStatus.CONFIRMED)
    ]
    total_resolved = len(resolved_incidents)
    total_confirmed = sum(
        1
        for inc in incidents
        if inc.status == IncidentStatus.CONFIRMED or inc.confirmed_at is not None
    )
    total_appealed = sum(
        1
        for inc in incidents
        if inc.status == IncidentStatus.APPEALED or inc.appealed_at is not None
    )

    # Resolution times
    resolution_hours: list[float] = []
    within_sla_count = 0
    for inc in resolved_incidents:
        if inc.resolved_at and inc.created_at:
            delta_h = (inc.resolved_at - inc.created_at).total_seconds() / 3600.0
            resolution_hours.append(delta_h)
            if delta_h <= 72.0:  # 72 hour default SLA threshold
                within_sla_count += 1

    mean_res_hours = (
        round(sum(resolution_hours) / len(resolution_hours), 2) if resolution_hours else None
    )
    median_res_hours = (
        round(float(statistics.median(resolution_hours)), 2) if resolution_hours else None
    )
    sla_compliance = (
        round(float(within_sla_count) / float(len(resolution_hours)), 4)
        if resolution_hours
        else None
    )
    csi = compute_csi(total_confirmed, total_appealed, total_resolved)

    # 2. Equity credibility gap from Phase 6
    equity_gap = None
    eq_res = await db.execute(
        select(WardEquityCredibility).where(WardEquityCredibility.ward_id == ward_id)
    )
    eq = eq_res.scalar_one_or_none()
    if eq:
        equity_gap = round(eq.equity_gap, 4)

    # 3. Department breakdown
    dept_breakdown: dict[str, Any] = {}
    for inc in incidents:
        dept_key = str(inc.department_id)
        if dept_key not in dept_breakdown:
            dept_breakdown[dept_key] = {
                "total_reported": 0,
                "total_active": 0,
                "total_resolved": 0,
            }
        dept_breakdown[dept_key]["total_reported"] += 1
        if inc.status in ACTIVE_INCIDENT_STATUSES:
            dept_breakdown[dept_key]["total_active"] += 1
        elif inc.status in (IncidentStatus.RESOLVED, IncidentStatus.CONFIRMED):
            dept_breakdown[dept_key]["total_resolved"] += 1

    # 4. Snapshot persistence
    if persist:
        # Check existing snapshot
        snap_query = select(WardReportCardSnapshot).where(
            WardReportCardSnapshot.ward_id == ward_id,
            WardReportCardSnapshot.snapshot_date == snapshot_date,
            WardReportCardSnapshot.period_type == period_type,
        )
        snap_res = await db.execute(snap_query)
        snapshot = snap_res.scalar_one_or_none()

        if snapshot:
            snapshot.total_reported = total_reported
            snapshot.total_active = total_active
            snapshot.total_resolved = total_resolved
            snapshot.total_confirmed = total_confirmed
            snapshot.total_appealed = total_appealed
            snapshot.mean_resolution_hours = mean_res_hours
            snapshot.median_resolution_hours = median_res_hours
            snapshot.citizen_satisfaction_index = csi
            snapshot.sla_compliance_rate = sla_compliance
            snapshot.equity_observed_gap = equity_gap
            snapshot.department_breakdown = dept_breakdown
        else:
            snapshot = WardReportCardSnapshot(
                organization_id=org_id,
                ward_id=ward_id,
                snapshot_date=snapshot_date,
                period_type=period_type,
                total_reported=total_reported,
                total_active=total_active,
                total_resolved=total_resolved,
                total_confirmed=total_confirmed,
                total_appealed=total_appealed,
                mean_resolution_hours=mean_res_hours,
                median_resolution_hours=median_res_hours,
                citizen_satisfaction_index=csi,
                sla_compliance_rate=sla_compliance,
                equity_observed_gap=equity_gap,
                department_breakdown=dept_breakdown,
            )
            db.add(snapshot)
        await db.commit()

    return WardReportCardResponse(
        ward_id=ward_id,
        organization_id=org_id,
        snapshot_date=snapshot_date,
        period_type=period_type,
        total_reported=total_reported,
        total_active=total_active,
        total_resolved=total_resolved,
        total_confirmed=total_confirmed,
        total_appealed=total_appealed,
        mean_resolution_hours=mean_res_hours,
        median_resolution_hours=median_res_hours,
        citizen_satisfaction_index=csi,
        sla_compliance_rate=sla_compliance,
        equity_observed_gap=equity_gap,
        department_breakdown=dept_breakdown,
    )


async def generate_corporator_digest(
    db: AsyncSession,
    user_claims: CurrentUserClaims,
    ward_id: uuid.UUID,
) -> CorporatorDigestResponse:
    """Generates an executive operational digest for an elected Corporator (§A18, §A21).

    Enforces strict ward ownership check against elected_representative / user_role_assignment.
    """
    # 1. Role and Jurisdictional Verification (Standing Invariant 4)
    admin_roles = {
        StaffRole.ADMIN,
        StaffRole.ZONAL_SUPERVISOR,
    }

    if user_claims.role == StaffRole.CORPORATOR:
        # Check elected_representative mapping
        rep_query = select(ElectedRepresentative).where(
            ElectedRepresentative.user_id == user_claims.user_id
        )
        rep_res = await db.execute(rep_query)
        rep = rep_res.scalar_one_or_none()

        ura_query = select(UserRoleAssignment).where(
            UserRoleAssignment.user_id == user_claims.user_id,
            UserRoleAssignment.role == StaffRole.CORPORATOR,
        )
        ura_res = await db.execute(ura_query)
        ura = ura_res.scalar_one_or_none()

        is_authorized = (rep and rep.ward_id == ward_id) or (ura and ura.ward_id == ward_id)
        if not is_authorized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Corporator does not represent the requested ward",
            )
    elif user_claims.role not in admin_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to Corporators and Municipal Administrators",
        )

    # 2. Query ward incidents
    now = datetime.now(UTC)
    week_ago = now - timedelta(days=7)
    sla_cutoff = now - timedelta(hours=72)

    query = select(Incident).where(Incident.ward_id == ward_id)
    res = await db.execute(query)
    incidents = list(res.scalars().all())

    total_active = 0
    newly_reported_week = 0
    resolved_week = 0
    total_confirmed = 0
    total_appealed = 0
    total_resolved = 0
    sla_breaches: list[SLABreachItem] = []
    dept_backlogs: dict[uuid.UUID, int] = {}

    for inc in incidents:
        if inc.created_at and inc.created_at >= week_ago:
            newly_reported_week += 1

        if inc.status in ACTIVE_INCIDENT_STATUSES:
            total_active += 1
            dept_backlogs[inc.department_id] = dept_backlogs.get(inc.department_id, 0) + 1

            if inc.created_at and inc.created_at <= sla_cutoff:
                age_h = round((now - inc.created_at).total_seconds() / 3600.0, 1)
                sla_breaches.append(
                    SLABreachItem(
                        incident_id=inc.id,
                        title=f"{inc.category_code} in ward {ward_id}",
                        category_code=inc.category_code,
                        age_hours=age_h,
                        status=inc.status.value,
                        department_name=None,
                    )
                )
        elif inc.status in (IncidentStatus.RESOLVED, IncidentStatus.CONFIRMED):
            total_resolved += 1
            if inc.resolved_at and inc.resolved_at >= week_ago:
                resolved_week += 1
            if inc.status == IncidentStatus.CONFIRMED or inc.confirmed_at:
                total_confirmed += 1

        if inc.status == IncidentStatus.APPEALED or inc.appealed_at:
            total_appealed += 1

    # Sort breaches descending by age
    sla_breaches.sort(key=lambda x: x.age_hours, reverse=True)

    # Resolve department names for backlog ranking
    dept_rankings: list[dict[str, Any]] = []
    if dept_backlogs:
        dept_ids = list(dept_backlogs.keys())
        d_res = await db.execute(select(Department).where(Department.id.in_(dept_ids)))
        depts = {d.id: d.name for d in d_res.scalars().all()}
        for d_id, count in sorted(dept_backlogs.items(), key=lambda item: item[1], reverse=True):
            dept_rankings.append(
                {
                    "department_id": str(d_id),
                    "department_name": depts.get(d_id, "Unknown Department"),
                    "active_backlog": count,
                }
            )

    csi = compute_csi(total_confirmed, total_appealed, total_resolved)

    return CorporatorDigestResponse(
        ward_id=ward_id,
        corporator_user_id=user_claims.user_id,
        generation_timestamp=now,
        total_active_cases=total_active,
        newly_reported_week=newly_reported_week,
        resolved_week=resolved_week,
        citizen_satisfaction_index=csi,
        sla_breaches_count=len(sla_breaches),
        sla_breach_alerts=sla_breaches,
        department_backlog_ranking=dept_rankings,
    )


async def predict_incident_eta(
    db: AsyncSession,
    incident_id: uuid.UUID,
) -> ETAPredictionResponse:
    """Predicts deterministic empirical resolution hours (ETA) and confidence bounds (§A23)."""
    # 1. Fetch incident
    inc_res = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = inc_res.scalar_one_or_none()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found",
        )

    # 2. Category Baseline Prior (T_base)
    prior_res = await db.execute(
        select(CategoryServiceTimePrior).where(
            CategoryServiceTimePrior.organization_id == incident.organization_id,
            CategoryServiceTimePrior.category_code == incident.category_code,
        )
    )
    prior = prior_res.scalar_one_or_none()
    if prior:
        t_base = prior.base_resolution_hours
        p25_base = prior.p25_hours
        p90_base = prior.p90_hours
    else:
        t_base = 48.0
        p25_base = 24.0
        p90_base = 96.0

    # 3. Severity Multiplier: M_sev(s) = 0.6 + (s * 0.2)
    sev = max(1, min(5, incident.severity or 3))
    m_sev = round(0.6 + (sev * 0.2), 2)

    # 4. Ward Efficiency Factor (E_ward)
    stat_res = await db.execute(
        select(WardResolutionStat).where(
            WardResolutionStat.ward_id == incident.ward_id,
            WardResolutionStat.category_code == incident.category_code,
        )
    )
    stat = stat_res.scalar_one_or_none()
    if stat and stat.resolved_count >= 5 and t_base > 0:
        ratio = stat.mean_resolution_hours / t_base
        e_ward = round(max(0.5, min(2.0, ratio)), 3)
    else:
        e_ward = 1.0

    # 5. Department Load Factor (L_dept)
    # Count active work orders in this department
    wo_count_res = await db.execute(
        select(func.count(WorkOrder.id))
        .join(Incident, WorkOrder.incident_id == Incident.id)
        .where(
            Incident.department_id == incident.department_id,
            WorkOrder.status.in_(
                [
                    WorkOrderStatus.CREATED,
                    WorkOrderStatus.DISPATCHED,
                    WorkOrderStatus.ACCEPTED,
                    WorkOrderStatus.IN_PROGRESS,
                ]
            ),
        )
    )
    active_wo_count = wo_count_res.scalar() or 0

    # Count active workers in department
    worker_count_res = await db.execute(
        select(func.count(UserRoleAssignment.id)).where(
            UserRoleAssignment.department_id == incident.department_id,
            UserRoleAssignment.role == StaffRole.FIELD_WORKER,
        )
    )
    active_workers = worker_count_res.scalar() or 1
    load_ratio = float(active_wo_count) / float(20.0 * max(1, active_workers))
    l_dept = round(1.0 + min(1.5, load_ratio), 3)

    # 6. Predict Resolution Hours (T_hat)
    t_hat = max(4.0, round(t_base * m_sev * e_ward * l_dept, 2))
    p25 = max(2.0, round(p25_base * m_sev * e_ward, 2))
    p50 = t_hat
    p90 = max(round(p50 * 1.5, 2), round(p90_base * m_sev * e_ward * l_dept, 2))

    base_time = incident.created_at or datetime.now(UTC)
    estimated_completion = base_time + timedelta(hours=t_hat)

    explanation = (
        f"Base {t_base}h ({incident.category_code}) scaled by severity {sev} (x{m_sev}), "
        f"ward efficiency (x{e_ward}), and department load (x{l_dept})."
    )

    return ETAPredictionResponse(
        incident_id=incident.id,
        predicted_resolution_hours=t_hat,
        estimated_completion_time=estimated_completion,
        p25_hours=p25,
        p50_hours=p50,
        p90_hours=p90,
        formula_components={
            "t_base": t_base,
            "m_sev": m_sev,
            "e_ward": e_ward,
            "l_dept": l_dept,
        },
        explanation=explanation,
    )
