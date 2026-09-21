"""FastAPI Citizen Transparency, Jan Sunwai Ledger & Civic Assistant Endpoints (§A21, §A23)."""

import logging
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.transparency.models import JanSunwaiLedgerEntry
from civicbrain.domain.transparency.services import (
    compute_nagar_pragati,
    extract_coordinates,
    get_incident_ledger_chain,
    process_civic_assistant_query,
)
from civicbrain.infra.database import get_db
from civicbrain.schemas.transparency import (
    CivicAssistantQueryRequest,
    CivicAssistantQueryResponse,
    IncidentLedgerChainResponse,
    JanSunwaiLedgerResponse,
    NagarPragatiResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transparency", tags=["Citizen Transparency & Jan Sunwai Ledger"])


@router.get(
    "/ledger",
    response_model=list[JanSunwaiLedgerResponse],
    summary="Browse public Jan Sunwai civic grievance ledger with differential privacy",
)
async def get_public_ledger(
    ward_id: uuid.UUID | None = Query(
        default=None, description="Optional filter by municipal ward"
    ),
    category_code: str | None = Query(default=None, description="Optional filter by category"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=50, ge=1, le=200, description="Page size"),
    db: AsyncSession = Depends(get_db),
) -> list[JanSunwaiLedgerResponse]:
    """Publicly accessible civic grievance ledger perturbed with 2D Laplace differential privacy (§A23)."""
    offset = (page - 1) * page_size
    stmt = select(JanSunwaiLedgerEntry)

    if ward_id:
        stmt = stmt.where(JanSunwaiLedgerEntry.ward_id == ward_id)
    if category_code:
        stmt = stmt.where(JanSunwaiLedgerEntry.category_code == category_code)

    stmt = stmt.order_by(JanSunwaiLedgerEntry.dp_timestamp.desc()).offset(offset).limit(page_size)
    res = await db.execute(stmt)
    entries = list(res.scalars().all())

    response_items: list[JanSunwaiLedgerResponse] = []
    for e in entries:
        lon, lat = extract_coordinates(e.dp_geom)
        response_items.append(
            JanSunwaiLedgerResponse(
                id=e.id,
                organization_id=e.organization_id,
                incident_id=e.incident_id,
                sequence_num=e.sequence_num,
                public_tracking_code=e.public_tracking_code,
                category_code=e.category_code,
                department_id=e.department_id,
                ward_id=e.ward_id,
                dp_latitude=lat,
                dp_longitude=lon,
                dp_timestamp=e.dp_timestamp,
                lifecycle_status=e.lifecycle_status,
                sla_status=e.sla_status,
                predicted_eta_hours=e.predicted_eta_hours,
                resolution_media_count=e.resolution_media_count,
                is_appealed=e.is_appealed,
                prev_hash=e.prev_hash,
                entry_hash=e.entry_hash,
                created_at=e.created_at,
            )
        )
    return response_items


@router.get(
    "/ledger/incidents/{incident_id}/chain",
    response_model=IncidentLedgerChainResponse,
    summary="Inspect cryptographic milestone hash chain for an incident",
)
async def get_incident_chain(
    incident_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> IncidentLedgerChainResponse:
    """Verifies and returns the full cryptographic milestone hash chain for an incident (§A23)."""
    return await get_incident_ledger_chain(db=db, incident_id=incident_id)


@router.get(
    "/pragati",
    response_model=NagarPragatiResponse,
    summary="Nagar Pragati city-wide progress and macro transparency dashboard",
)
async def get_nagar_pragati(
    organization_id: uuid.UUID = Query(..., description="Target municipality / organization ID"),
    period_type: str = Query(
        default="monthly", description="Period type: weekly, monthly, quarterly"
    ),
    persist: bool = Query(default=True, description="Persist snapshot to database"),
    db: AsyncSession = Depends(get_db),
) -> NagarPragatiResponse:
    """Public city-wide transparency scorecard comparing wards and departments (§A21)."""
    return await compute_nagar_pragati(
        db=db,
        organization_id=organization_id,
        period_type=period_type,
        persist=persist,
    )


@router.post(
    "/assistant/query",
    response_model=CivicAssistantQueryResponse,
    summary="Multilingual Citizen Assistant natural language grievance Q&A",
)
async def ask_civic_assistant(
    payload: CivicAssistantQueryRequest,
    db: AsyncSession = Depends(get_db),
) -> CivicAssistantQueryResponse:
    """Multilingual citizen service assistant operating with zero external LLM API cost (§A23, Bootstrap Principle §A3)."""
    return await process_civic_assistant_query(db=db, request=payload)
