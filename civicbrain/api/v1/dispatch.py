"""FastAPI Dispatch and Field Operations Endpoints (§A14, §A15, §A16)."""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.dispatch.models import (
    ConflictReviewStatus,
    WorkOrder,
    WorkOrderStatus,
)
from civicbrain.domain.dispatch.services import (
    adjudicate_dispatch_conflict,
    create_work_order,
    evaluate_auto_confirm_cron,
    list_conflicts_for_worker,
    list_dispatch_conflicts,
    process_field_sync,
    resolve_work_order,
    start_work_order,
)
from civicbrain.domain.identity.jwt import (
    CurrentUserClaims,
    SupabaseClaims,
    get_current_user_claims,
    get_optional_user_claims,
    require_roles,
)
from civicbrain.domain.identity.models import StaffRole
from civicbrain.domain.intake.models import Incident
from civicbrain.infra.config import settings
from civicbrain.infra.database import get_db
from civicbrain.schemas.dispatch import (
    AutoConfirmResponse,
    ConflictAdjudicationRequest,
    ConflictAdjudicationResponse,
    DispatchConflictReviewResponse,
    FieldSyncPushRequest,
    FieldSyncResponse,
    MutationResult,
    WorkOrderCreate,
    WorkOrderResolveRequest,
    WorkOrderResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dispatch", tags=["Dispatch & Field Operations"])


async def verify_cron_or_admin(
    request: Request,
    claims: SupabaseClaims | None = Depends(get_optional_user_claims),
) -> None:
    """Verifies caller is an automated cron task, service role, or system admin."""
    cron_header = request.headers.get("X-Cron-Secret")
    if cron_header and (
        cron_header == settings.CRON_SECRET or cron_header == settings.SUPABASE_SERVICE_ROLE_KEY
    ):
        return

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "").strip()
        if token in (settings.SUPABASE_SERVICE_ROLE_KEY, settings.CRON_SECRET):
            return

    if claims and claims.role in (StaffRole.ADMIN, StaffRole.DISPATCHER):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized: Valid cron secret or admin authorization required.",
    )


@router.post("/work-orders", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_new_work_order(
    payload: WorkOrderCreate,
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(
        require_roles([StaffRole.ADMIN, StaffRole.DISPATCHER, StaffRole.DEPARTMENT_STAFF])
    ),
) -> WorkOrderResponse:
    """Dispatches a new field work order for an operational incident."""
    # Resolve organization from incident or claims
    inc_stmt = select(Incident).where(Incident.id == payload.incident_id)
    inc_res = await db.execute(inc_stmt)
    incident = inc_res.scalar_one_or_none()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {payload.incident_id} not found.",
        )

    org_id = claims.org_id or incident.organization_id

    work_order = await create_work_order(
        db=db,
        organization_id=org_id,
        incident_id=payload.incident_id,
        department_id=payload.department_id,
        assigned_worker_id=payload.assigned_worker_id,
    )
    await db.commit()
    await db.refresh(work_order)
    return WorkOrderResponse.model_validate(work_order)


@router.get("/work-orders/my", response_model=list[WorkOrderResponse])
async def list_my_work_orders(
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(get_current_user_claims),
) -> list[WorkOrderResponse]:
    """Retrieves all active work orders assigned to the calling field worker."""
    stmt = (
        select(WorkOrder)
        .where(
            WorkOrder.assigned_worker_id == claims.user_id,
            WorkOrder.status != WorkOrderStatus.CANCELLED,
        )
        .order_by(WorkOrder.created_at.desc())
    )
    res = await db.execute(stmt)
    work_orders = list(res.scalars().all())
    return [WorkOrderResponse.model_validate(wo) for wo in work_orders]


@router.post("/work-orders/{work_order_id}/start", response_model=WorkOrderResponse)
async def start_assigned_work_order(
    work_order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(get_current_user_claims),
) -> WorkOrderResponse:
    """Field worker marks arrival and begins active remediation."""
    work_order = await start_work_order(
        db=db,
        work_order_id=work_order_id,
        worker_user_id=claims.user_id,
    )
    await db.commit()
    await db.refresh(work_order)
    return WorkOrderResponse.model_validate(work_order)


@router.post("/work-orders/{work_order_id}/resolve", response_model=WorkOrderResponse)
async def resolve_assigned_work_order(
    work_order_id: uuid.UUID,
    payload: WorkOrderResolveRequest,
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(get_current_user_claims),
) -> WorkOrderResponse:
    """Submits evidence-gated resolution proof with 50m geographic proximity enforcement."""
    work_order = await resolve_work_order(
        db=db,
        work_order_id=work_order_id,
        worker_user_id=claims.user_id,
        resolution_notes=payload.resolution_notes,
        resolution_media_urls=payload.resolution_media_urls,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    await db.commit()
    await db.refresh(work_order)
    return WorkOrderResponse.model_validate(work_order)


@router.post(
    "/cron/auto-confirm",
    response_model=AutoConfirmResponse,
    dependencies=[Depends(verify_cron_or_admin)],
)
async def trigger_auto_confirm_cron(
    db: AsyncSession = Depends(get_db),
) -> AutoConfirmResponse:
    """Evaluates resolved incidents past 72h auto-confirm deadline and transitions them to CONFIRMED."""
    res = await evaluate_auto_confirm_cron(db)
    await db.commit()
    return res


# --- Phase 9: Karmi Sahayak Offline Sync Endpoints (§A15) ---


@router.post("/sync", response_model=FieldSyncResponse)
async def execute_field_sync(
    payload: FieldSyncPushRequest,
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(get_current_user_claims),
) -> FieldSyncResponse:
    """Two-way delta synchronization for Karmi Sahayak with conflict arbitration (§A15)."""
    res = await process_field_sync(db, claims.user_id, payload)
    await db.commit()
    return res


@router.get("/sync/conflicts", response_model=list[MutationResult])
async def get_worker_sync_conflicts(
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(get_current_user_claims),
) -> list[MutationResult]:
    """Retrieves sync mutations flagged with CONFLICT for the calling worker's device."""
    conflicts = await list_conflicts_for_worker(db, claims.user_id)
    return [
        MutationResult(
            client_mutation_id=c.client_mutation_id,
            status=c.status,
            conflict_reason=c.conflict_reason,
        )
        for c in conflicts
    ]


@router.get("/conflicts", response_model=list[DispatchConflictReviewResponse])
async def list_supervisor_conflicts(
    organization_id: uuid.UUID = Query(...),
    review_status: ConflictReviewStatus | None = Query(default=ConflictReviewStatus.PENDING),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(
        require_roles([StaffRole.ADMIN, StaffRole.DISPATCHER, StaffRole.ZONAL_SUPERVISOR])
    ),
) -> list[DispatchConflictReviewResponse]:
    """Retrieves reviewable concurrent dispatch conflicts in the supervisor queue."""
    conflicts = await list_dispatch_conflicts(
        db=db,
        organization_id=organization_id,
        review_status=review_status,
        page=page,
        page_size=page_size,
    )
    return [DispatchConflictReviewResponse.model_validate(c) for c in conflicts]


@router.post("/conflicts/{conflict_id}/adjudicate", response_model=ConflictAdjudicationResponse)
async def adjudicate_conflict(
    conflict_id: uuid.UUID,
    payload: ConflictAdjudicationRequest,
    db: AsyncSession = Depends(get_db),
    claims: CurrentUserClaims = Depends(
        require_roles([StaffRole.ADMIN, StaffRole.DISPATCHER, StaffRole.ZONAL_SUPERVISOR])
    ),
) -> ConflictAdjudicationResponse:
    """Supervisory adjudication of concurrent dispatch conflict."""
    res = await adjudicate_dispatch_conflict(
        db=db,
        conflict_id=conflict_id,
        reviewer_id=claims.user_id,
        decision=payload.decision,
        notes=payload.notes,
    )
    await db.commit()
    return res
