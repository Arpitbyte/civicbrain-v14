import logging
import secrets
import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.identity.models import Department, Organization, Ward
from civicbrain.domain.intake.dedup import (
    calculate_jaro_winkler_similarity,
    evaluate_splink_record_linkage,
)
from civicbrain.domain.intake.models import (
    DedupDecision,
    Incident,
    IncidentDedupLink,
    IncidentStatus,
    IntakeChannel,
    IntakeReport,
    IntakeStatus,
    Observation,
    ObservationStatus,
)
from civicbrain.domain.intake.taxonomy import CategoryStatus, TaxonomyCategory
from civicbrain.domain.intake.vision import VisionDetector, get_vision_detector

logger = logging.getLogger(__name__)

# §A16 Linear progression order
PROGRESSION_RANK = {
    IncidentStatus.REPORTED: 1,
    IncidentStatus.TRIAGED: 2,
    IncidentStatus.VERIFIED: 3,
    IncidentStatus.PRIORITIZED: 4,
    IncidentStatus.ASSIGNED: 5,
    IncidentStatus.IN_PROGRESS: 6,
    IncidentStatus.REOPENED: 6,  # Reopened defects resume active remediation
    IncidentStatus.APPEALED: 6,  # Under active supervisory re-inspection
    IncidentStatus.RESOLVED: 7,
    IncidentStatus.CONFIRMED: 8,
}


def calculate_intake_status_from_children(child_statuses: list[IncidentStatus]) -> IntakeStatus:
    """Calculates parent intake_report.status based on the least-advanced active child status.

    In accordance with §A7 & Standing Invariant 3:
    - If all children are REJECTED -> REJECTED
    - Rejected children in mixed sets are excluded from active evaluation
    - Maps the minimum active rank to corresponding IntakeStatus
    - Detects PARTIALLY_RESOLVED when at least one child is resolved and others remain active
    """
    if not child_statuses:
        return IntakeStatus.SUBMITTED

    # If all children are rejected
    if all(s == IncidentStatus.REJECTED for s in child_statuses):
        return IntakeStatus.REJECTED

    # Filter out rejected children
    active_statuses = [s for s in child_statuses if s != IncidentStatus.REJECTED]
    if not active_statuses:
        return IntakeStatus.REJECTED

    has_resolved = any(
        PROGRESSION_RANK[s] >= PROGRESSION_RANK[IncidentStatus.RESOLVED] for s in active_statuses
    )
    has_unresolved = any(
        PROGRESSION_RANK[s] < PROGRESSION_RANK[IncidentStatus.RESOLVED] for s in active_statuses
    )

    # Multi-child partial resolution
    if has_resolved and has_unresolved:
        return IntakeStatus.PARTIALLY_RESOLVED

    # Find minimum rank child
    least_child = min(active_statuses, key=lambda s: PROGRESSION_RANK[s])

    # Direct 1-to-1 mapping
    mapping = {
        IncidentStatus.REPORTED: IntakeStatus.SUBMITTED,
        IncidentStatus.TRIAGED: IntakeStatus.PROCESSING,
        IncidentStatus.VERIFIED: IntakeStatus.TRIAGED,
        IncidentStatus.PRIORITIZED: IntakeStatus.TRIAGED,
        IncidentStatus.ASSIGNED: IntakeStatus.IN_PROGRESS,
        IncidentStatus.IN_PROGRESS: IntakeStatus.IN_PROGRESS,
        IncidentStatus.REOPENED: IntakeStatus.IN_PROGRESS,
        IncidentStatus.APPEALED: IntakeStatus.IN_PROGRESS,
        IncidentStatus.RESOLVED: IntakeStatus.RESOLVED,
        IncidentStatus.CONFIRMED: IntakeStatus.CLOSED,
    }
    return mapping.get(least_child, IntakeStatus.IN_PROGRESS)


async def resolve_ward_for_point(
    session: AsyncSession, organization_id: uuid.UUID, latitude: float, longitude: float
) -> uuid.UUID | None:
    """Finds the containing ward for given GPS coordinates via PostGIS ST_Contains."""
    point_geom = f"SRID=4326;POINT({longitude} {latitude})"
    stmt = (
        select(Ward.id)
        .where(Ward.organization_id == organization_id)
        .where(func.ST_Contains(Ward.geom, func.ST_GeomFromText(point_geom, 4326)))
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def route_and_deduplicate_observation(
    session: AsyncSession,
    organization_id: uuid.UUID,
    ward_id: uuid.UUID,
    observation: Observation,
    description: str | None,
    latitude: float,
    longitude: float,
) -> Incident:
    """Evaluates candidate open incidents in the same ward and department using Splink.

    If an exact/probable match is found (P(M|gamma) >= 0.85), links the observation to it.
    Otherwise, spawns a new authoritative operational Incident.
    """
    obs_geom_text = f"SRID=4326;POINT({longitude} {latitude})"

    # Find active candidate incidents in same org, department, ward
    stmt = (
        select(Incident)
        .where(Incident.organization_id == organization_id)
        .where(Incident.department_id == observation.department_id)
        .where(Incident.status.notin_([IncidentStatus.CONFIRMED, IncidentStatus.REJECTED]))
    )
    res = await session.execute(stmt)
    candidates = list(res.scalars().all())

    best_match_incident: Incident | None = None
    highest_prob = 0.0

    for cand in candidates:
        # Calculate spatial distance via PostGIS
        dist_stmt = select(
            func.ST_Distance(
                func.ST_GeomFromText(obs_geom_text, 4326),
                cand.geom,
                True,  # use spheroid for meters
            )
        )
        dist_res = await session.execute(dist_stmt)
        distance_meters = dist_res.scalar() or 0.0

        # Temporal diff
        diff_seconds = abs((datetime.now(UTC) - cand.created_at).total_seconds())

        # Category match
        cat_match = observation.category_code == cand.category_code

        # Text similarity
        text_sim = calculate_jaro_winkler_similarity(description, cand.category_code)

        weight, prob, decision = evaluate_splink_record_linkage(
            distance_meters, diff_seconds, cat_match, text_sim
        )

        # Audit link record
        dedup_link = IncidentDedupLink(
            organization_id=organization_id,
            observation_id=observation.id,
            candidate_incident_id=cand.id,
            spatial_distance_meters=distance_meters,
            temporal_diff_seconds=diff_seconds,
            category_match=cat_match,
            text_similarity=text_sim,
            match_weight=weight,
            match_probability=prob,
            decision=decision,
            model_version="splink_v4_cold_start",
        )
        session.add(dedup_link)

        if decision in (DedupDecision.EXACT_MATCH, DedupDecision.PROBABLE_MATCH):
            if prob > highest_prob:
                highest_prob = prob
                best_match_incident = cand

    if best_match_incident is not None:
        observation.incident_id = best_match_incident.id
        observation.status = ObservationStatus.LINKED_TO_INCIDENT
        return best_match_incident

    # Create new authoritative operational Incident
    new_incident = Incident(
        organization_id=organization_id,
        department_id=observation.department_id,
        ward_id=ward_id,
        category_code=observation.category_code,
        geom=f"SRID=4326;POINT({longitude} {latitude})",
        status=IncidentStatus.REPORTED,
        severity=observation.severity_score,
    )
    session.add(new_incident)
    await session.flush()

    observation.incident_id = new_incident.id
    observation.status = ObservationStatus.LINKED_TO_INCIDENT
    return new_incident


async def recompute_intake_report_status(
    session: AsyncSession, intake_report_id: uuid.UUID
) -> IntakeStatus:
    """Recomputes parent intake report status from all its linked observations' child incidents."""
    stmt = (
        select(Incident.status)
        .join(Observation, Observation.incident_id == Incident.id)
        .where(Observation.intake_report_id == intake_report_id)
    )
    res = await session.execute(stmt)
    statuses = list(res.scalars().all())

    new_status = calculate_intake_status_from_children(statuses)

    report_stmt = select(IntakeReport).where(IntakeReport.id == intake_report_id)
    report_res = await session.execute(report_stmt)
    report = report_res.scalar_one_or_none()
    if report:
        report.status = new_status
        await session.flush()
    return new_status


async def process_photo_intake(
    session: AsyncSession,
    organization_id: uuid.UUID,
    image_bytes: bytes,
    filename: str,
    latitude: float,
    longitude: float,
    channel: IntakeChannel = IntakeChannel.PWA,
    citizen_id: uuid.UUID | None = None,
    citizen_categories: list[str] | None = None,
    description: str | None = None,
    address_text: str | None = None,
    detector: VisionDetector | None = None,
) -> tuple[IntakeReport, list[Observation]]:
    """Multi-issue photo splitting pipeline (§A6, §A7).

    1. Checks spatial containment in ward via PostGIS.
    2. Runs VisionDetector protocol (Honest cold start by default, never fabricating scores).
    3. Splits photo into atomic observations routed to departmental queues.
    4. Resolves departments via Living Taxonomy categories.
    5. Evaluates Splink record linkage against open ward incidents.
    6. Aggregates parent intake report status using least-advanced child status invariant.
    """
    # Verify organization exists
    org_res = await session.execute(
        select(Organization.id).where(Organization.id == organization_id)
    )
    if not org_res.scalar_one_or_none():
        raise ValueError("Organization not found")

    # Resolve containing ward via PostGIS ST_Contains
    ward_id = await resolve_ward_for_point(session, organization_id, latitude, longitude)

    # Invoke vision detector protocol
    active_detector = detector or get_vision_detector()
    detected_defects = await active_detector.detect(image_bytes, filename, citizen_categories)

    # Generate 256 bits of entropy tracking token
    tracking_token = secrets.token_urlsafe(32)
    point_geom = f"SRID=4326;POINT({longitude} {latitude})"

    report = IntakeReport(
        organization_id=organization_id,
        citizen_id=citizen_id,
        channel=channel,
        description=description,
        media_urls=[filename] if filename else [],
        geom=point_geom,
        address_text=address_text,
        ward_id=ward_id,
        status=IntakeStatus.SUBMITTED,
        tracking_token=tracking_token,
    )
    session.add(report)
    await session.flush()

    created_observations: list[Observation] = []
    child_incident_statuses: list[IncidentStatus] = []

    for defect in detected_defects:
        # Resolve responsible department via TaxonomyCategory
        cat_stmt = (
            select(TaxonomyCategory.department_id)
            .where(TaxonomyCategory.organization_id == organization_id)
            .where(TaxonomyCategory.code == defect.category_code)
            .where(TaxonomyCategory.status == CategoryStatus.APPROVED)
        )
        cat_res = await session.execute(cat_stmt)
        dept_id = cat_res.scalar_one_or_none()

        if not dept_id:
            # Check by department code match directly (e.g. ROADS, SWM)
            dept_stmt = (
                select(Department.id)
                .where(Department.organization_id == organization_id)
                .where(Department.code == defect.category_code)
            )
            dept_res = await session.execute(dept_stmt)
            dept_id = dept_res.scalar_one_or_none()

        if not dept_id:
            # Fallback to General Admin or first available department
            fallback_stmt = (
                select(Department.id)
                .where(Department.organization_id == organization_id)
                .order_by(Department.created_at.asc())
                .limit(1)
            )
            fallback_res = await session.execute(fallback_stmt)
            dept_id = fallback_res.scalar_one_or_none()

        if not dept_id:
            raise ValueError(f"No department found for organization {organization_id}")

        obs = Observation(
            organization_id=organization_id,
            intake_report_id=report.id,
            department_id=dept_id,
            category_code=defect.category_code,
            source_media_url=filename,
            image_url=filename,
            bbox=defect.bbox,
            bounding_box=defect.bbox,
            confidence=defect.confidence,  # Nullable: None for cold start or citizen declared
            severity_score=defect.severity_hint or 1,
            detection_source=defect.detection_source,
            needs_manual_triage=defect.needs_manual_triage,
            status=ObservationStatus.DETECTED,
        )
        session.add(obs)
        await session.flush()

        # If not flagged for manual triage and ward is known, deduplicate and route
        if not defect.needs_manual_triage and ward_id is not None:
            incident = await route_and_deduplicate_observation(
                session=session,
                organization_id=organization_id,
                ward_id=ward_id,
                observation=obs,
                description=description,
                latitude=latitude,
                longitude=longitude,
            )
            child_incident_statuses.append(incident.status)

        created_observations.append(obs)

    # Compute parent status via least-advanced child invariant
    if child_incident_statuses:
        report.status = calculate_intake_status_from_children(child_incident_statuses)
    elif all(d.needs_manual_triage for d in detected_defects):
        report.status = IntakeStatus.SUBMITTED
    await session.flush()

    return report, created_observations
