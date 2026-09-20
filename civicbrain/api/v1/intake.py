"""FastAPI Ingestion and Anonymous Tracking Endpoints."""

import logging
import secrets
import uuid
from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.identity.jwt import SupabaseClaims, get_current_user_claims
from civicbrain.domain.identity.models import Department, Organization
from civicbrain.domain.intake.models import (
    IncidentStatus,
    IntakeChannel,
    IntakeReport,
    IntakeStatus,
    Observation,
    ObservationStatus,
)
from civicbrain.domain.intake.services import (
    calculate_intake_status_from_children,
    process_photo_intake,
    resolve_ward_for_point,
    route_and_deduplicate_observation,
)
from civicbrain.infra.database import get_db
from civicbrain.infra.redis import get_redis_client
from civicbrain.schemas.intake import (
    AnonymousTrackingResponse,
    IntakeReportCreate,
    IntakeReportResponse,
    ObservationResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/intake", tags=["Intake"])

# Upstash Redis IP rate limiter for anonymous tracking token lookups
# Allows max 10 requests per minute per client IP
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 10


async def check_rate_limit(request: Request) -> None:
    """Enforces max 10 tracking requests per minute per IP address via Upstash Redis."""
    client_ip = request.client.host if request.client else "unknown_client"
    key = f"rate_limit:track:{client_ip}"

    redis_client = get_redis_client()
    try:
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, RATE_LIMIT_WINDOW_SECONDS)

        if current > RATE_LIMIT_MAX_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: maximum 10 tracking lookups per minute. Please try again later.",
            )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Redis rate limiter error for IP {client_ip}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Rate limit verification service unavailable.",
        ) from exc


@router.post("/reports", response_model=IntakeReportResponse, status_code=status.HTTP_201_CREATED)
async def submit_intake_report(
    payload: IntakeReportCreate,
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_current_user_claims),
) -> IntakeReportResponse:
    """Citizen or channel ingestion endpoint creating multi-issue reports.

    Automatically executes:
    1. Spatial containment check against ward boundary via PostGIS.
    2. Multi-observation splitting per detected defect.
    3. Departmental resolution and Splink deduplication against active open incidents.
    4. Least-advanced child status aggregation.
    """
    # Verify organization exists
    org_res = await db.execute(
        select(Organization).where(Organization.id == payload.organization_id)
    )
    if not org_res.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    # Resolve ward via PostGIS
    ward_id = await resolve_ward_for_point(
        db, payload.organization_id, payload.latitude, payload.longitude
    )

    # 256 bits of cryptographic entropy for anonymous tracking token
    tracking_token = secrets.token_urlsafe(32)

    point_geom = f"SRID=4326;POINT({payload.longitude} {payload.latitude})"
    citizen_id = claims.user_id if claims else None

    intake_report = IntakeReport(
        organization_id=payload.organization_id,
        citizen_id=citizen_id,
        channel=payload.channel,
        description=payload.description,
        media_urls=payload.media_urls,
        geom=point_geom,
        address_text=payload.address_text,
        ward_id=ward_id,
        status=IntakeStatus.SUBMITTED,
        tracking_token=tracking_token,
    )
    db.add(intake_report)
    await db.flush()

    created_observations: list[Observation] = []
    child_incident_statuses: list[IncidentStatus] = []

    # Map departmental observations
    for obs_in in payload.observations:
        dept_stmt = (
            select(Department.id)
            .where(Department.organization_id == payload.organization_id)
            .where(Department.code == obs_in.department_code.upper())
        )
        dept_res = await db.execute(dept_stmt)
        dept_id = dept_res.scalar_one_or_none()
        if not dept_id:
            # Fallback or create department representation
            continue

        obs = Observation(
            organization_id=payload.organization_id,
            intake_report_id=intake_report.id,
            department_id=dept_id,
            category_code=obs_in.category_code,
            source_media_url=obs_in.source_media_url,
            bounding_box=obs_in.bounding_box,
            confidence=obs_in.confidence,
            severity_score=obs_in.severity_score,
            status=ObservationStatus.DETECTED,
        )
        db.add(obs)
        await db.flush()

        # If ward resolved, evaluate Splink deduplication and route to incident
        if ward_id is not None:
            incident = await route_and_deduplicate_observation(
                session=db,
                organization_id=payload.organization_id,
                ward_id=ward_id,
                observation=obs,
                description=payload.description,
                latitude=payload.latitude,
                longitude=payload.longitude,
            )
            child_incident_statuses.append(incident.status)

        created_observations.append(obs)

    # Compute least-advanced child status
    if child_incident_statuses:
        intake_report.status = calculate_intake_status_from_children(child_incident_statuses)
        await db.flush()

    await db.commit()

    return IntakeReportResponse(
        id=intake_report.id,
        organization_id=intake_report.organization_id,
        channel=intake_report.channel,
        status=intake_report.status,
        ward_id=intake_report.ward_id,
        tracking_token=intake_report.tracking_token,
        created_at=intake_report.created_at,
        observations=[
            ObservationResponse(
                id=o.id,
                category_code=o.category_code,
                status=o.status,
                severity_score=o.severity_score,
                confidence=o.confidence,
                source_media_url=o.source_media_url,
                image_url=o.image_url,
                bbox=o.bbox,
                detection_source=o.detection_source,
                needs_manual_triage=o.needs_manual_triage,
                incident_id=o.incident_id,
                created_at=o.created_at,
            )
            for o in created_observations
        ],
    )


@router.post(
    "/reports/photo",
    response_model=IntakeReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit multi-issue photo intake",
)
async def submit_photo_intake(
    organization_id: uuid.UUID = Form(...),
    latitude: float = Form(..., ge=-90.0, le=90.0),
    longitude: float = Form(..., ge=-180.0, le=180.0),
    channel: IntakeChannel = Form(default=IntakeChannel.PWA),
    image: UploadFile = File(...),
    citizen_categories: str | None = Form(
        default=None, description="Comma-separated category codes e.g. POTHOLE,GARBAGE"
    ),
    description: str | None = Form(default=None),
    address_text: str | None = Form(default=None),
    db: AsyncSession = Depends(get_db),
    claims: SupabaseClaims | None = Depends(get_current_user_claims),
) -> IntakeReportResponse:
    """Submit photo report.

    1. Executes spatial containment in ward boundary via PostGIS.
    2. Runs Computer Vision protocol (Honest cold-start: zero fabricated confidence scores).
    3. Splits photo into atomic departmental observations.
    4. Routes via Living Taxonomy and evaluates Splink deduplication.
    5. Computes parent intake report status via least-advanced child invariant.
    """
    image_bytes = await image.read()
    filename = image.filename or "upload.jpg"

    cats_list: list[str] | None = None
    if citizen_categories:
        cats_list = [c.strip() for c in citizen_categories.split(",") if c.strip()]

    citizen_id = claims.user_id if claims else None

    report, observations = await process_photo_intake(
        session=db,
        organization_id=organization_id,
        image_bytes=image_bytes,
        filename=filename,
        latitude=latitude,
        longitude=longitude,
        channel=channel,
        citizen_id=citizen_id,
        citizen_categories=cats_list,
        description=description,
        address_text=address_text,
    )
    await db.commit()
    await db.refresh(report)

    return IntakeReportResponse(
        id=report.id,
        organization_id=report.organization_id,
        channel=report.channel,
        status=report.status,
        ward_id=report.ward_id,
        tracking_token=report.tracking_token,
        created_at=report.created_at,
        observations=[
            ObservationResponse(
                id=o.id,
                category_code=o.category_code,
                status=o.status,
                severity_score=o.severity_score,
                confidence=o.confidence,
                source_media_url=o.source_media_url,
                image_url=o.image_url,
                bbox=o.bbox,
                detection_source=o.detection_source,
                needs_manual_triage=o.needs_manual_triage,
                incident_id=o.incident_id,
                created_at=o.created_at,
            )
            for o in observations
        ],
    )


@router.get("/reports/track", response_model=AnonymousTrackingResponse)
async def track_anonymous_report(
    request: Request,
    token: str = Query(
        ..., min_length=16, description="Cryptographic tracking token issued at submission"
    ),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY DEFINER RPC.

    Enforces IP-based rate limiting (10 req/min) to prevent token brute-forcing.
    """
    await check_rate_limit(request)

    rpc_stmt = text("SELECT get_anonymous_intake_report(:token)")
    result = await db.execute(rpc_stmt, {"token": token})
    report_data = result.scalar()

    if not report_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intake report not found for the provided tracking token.",
        )

    return report_data
