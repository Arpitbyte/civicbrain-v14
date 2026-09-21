"""Unit tests for Phase 9 Karmi Sahayak Offline Sync & Conflict Adjudication (§A15)."""

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from civicbrain.domain.dispatch.models import (
    ConflictReviewStatus,
    DispatchConflictReview,
    SyncMutationLog,
    SyncMutationStatus,
    WorkOrder,
    WorkOrderStatus,
)
from civicbrain.domain.dispatch.services import (
    adjudicate_dispatch_conflict,
    process_field_sync,
)
from civicbrain.domain.intake.models import Incident, IncidentStatus
from civicbrain.schemas.dispatch import (
    ClientMutationItem,
    ConflictDecision,
    FieldSyncPushRequest,
)


@pytest.mark.asyncio
async def test_sync_idempotent_retry():
    """Verify duplicate client_mutation_id returns cached outcome without re-executing."""
    db = AsyncMock()
    worker_id = uuid.uuid4()
    mutation_id = uuid.uuid4()

    existing_log = SyncMutationLog(
        client_mutation_id=mutation_id,
        organization_id=uuid.uuid4(),
        worker_id=worker_id,
        entity_type="work_order",
        entity_id=uuid.uuid4(),
        action="resolve",
        status=SyncMutationStatus.APPLIED,
    )
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = existing_log
    db.execute.return_value = mock_res

    req = FieldSyncPushRequest(
        mutations=[
            ClientMutationItem(
                client_mutation_id=mutation_id,
                entity_id=uuid.uuid4(),
                action="resolve",
                captured_at=datetime.now(UTC),
                payload={"resolution_notes": "Done", "resolution_media_urls": ["url1"]},
            )
        ]
    )

    resp = await process_field_sync(db, worker_id, req)
    assert len(resp.mutation_results) == 1
    assert resp.mutation_results[0].status == SyncMutationStatus.APPLIED
    assert resp.mutation_results[0].client_mutation_id == mutation_id


@pytest.mark.asyncio
async def test_sync_resolve_missing_evidence_rejected():
    """Verify resolve mutation with empty media or notes is rejected with missing_evidence."""
    db = AsyncMock()
    worker_id = uuid.uuid4()
    mutation_id = uuid.uuid4()
    wo_id = uuid.uuid4()

    # No existing log
    idemp_res = MagicMock()
    idemp_res.scalar_one_or_none.return_value = None

    # Work order found
    work_order = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=worker_id,
        status=WorkOrderStatus.IN_PROGRESS,
        version=1,
    )
    wo_res = MagicMock()
    wo_res.scalar_one_or_none.return_value = work_order

    # Changes query
    changes_res = MagicMock()
    changes_res.scalars.return_value.all.return_value = []

    db.execute.side_effect = [idemp_res, wo_res, changes_res]

    req = FieldSyncPushRequest(
        mutations=[
            ClientMutationItem(
                client_mutation_id=mutation_id,
                entity_id=wo_id,
                action="resolve",
                captured_at=datetime.now(UTC),
                payload={"resolution_notes": "", "resolution_media_urls": []},
            )
        ]
    )

    resp = await process_field_sync(db, worker_id, req)
    assert len(resp.mutation_results) == 1
    assert resp.mutation_results[0].status == SyncMutationStatus.REJECTED
    assert resp.mutation_results[0].conflict_reason == "missing_evidence"


@pytest.mark.asyncio
async def test_sync_resolve_out_of_bounds_rejected():
    """Verify resolve mutation > 50m away is rejected with resolution_out_of_bounds."""
    db = AsyncMock()
    worker_id = uuid.uuid4()
    mutation_id = uuid.uuid4()
    wo_id = uuid.uuid4()

    idemp_res = MagicMock()
    idemp_res.scalar_one_or_none.return_value = None

    work_order = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=worker_id,
        status=WorkOrderStatus.IN_PROGRESS,
        version=1,
    )
    wo_res = MagicMock()
    wo_res.scalar_one_or_none.return_value = work_order

    # Proximity query returns False
    prox_res = MagicMock()
    prox_res.scalar.return_value = False

    changes_res = MagicMock()
    changes_res.scalars.return_value.all.return_value = []

    db.execute.side_effect = [idemp_res, wo_res, prox_res, changes_res]

    req = FieldSyncPushRequest(
        mutations=[
            ClientMutationItem(
                client_mutation_id=mutation_id,
                entity_id=wo_id,
                action="resolve",
                captured_at=datetime.now(UTC),
                payload={
                    "resolution_notes": "Filled pothole",
                    "resolution_media_urls": ["https://cdn.example.com/pothole.jpg"],
                    "latitude": 13.50,
                    "longitude": 78.00,
                },
            )
        ]
    )

    resp = await process_field_sync(db, worker_id, req)
    assert len(resp.mutation_results) == 1
    assert resp.mutation_results[0].status == SyncMutationStatus.REJECTED
    assert resp.mutation_results[0].conflict_reason == "resolution_out_of_bounds"


@pytest.mark.asyncio
async def test_sync_dispatcher_cancelled_preserves_evidence_in_review_queue():
    """Verify Case 4: resolve against cancelled work order preserves evidence in dispatch_conflict_review."""
    db = AsyncMock()
    worker_id = uuid.uuid4()
    mutation_id = uuid.uuid4()
    wo_id = uuid.uuid4()
    inc_id = uuid.uuid4()

    idemp_res = MagicMock()
    idemp_res.scalar_one_or_none.return_value = None

    work_order = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=inc_id,
        department_id=uuid.uuid4(),
        assigned_worker_id=worker_id,
        status=WorkOrderStatus.CANCELLED,  # Cancelled by dispatcher
        version=2,
    )
    wo_res = MagicMock()
    wo_res.scalar_one_or_none.return_value = work_order

    # Proximity query returns True (valid evidence!)
    prox_res = MagicMock()
    prox_res.scalar.return_value = True

    changes_res = MagicMock()
    changes_res.scalars.return_value.all.return_value = []

    db.execute.side_effect = [idemp_res, wo_res, prox_res, changes_res]

    req = FieldSyncPushRequest(
        mutations=[
            ClientMutationItem(
                client_mutation_id=mutation_id,
                entity_id=wo_id,
                action="resolve",
                captured_at=datetime.now(UTC),
                payload={
                    "resolution_notes": "Completed before seeing cancellation",
                    "resolution_media_urls": ["https://cdn.example.com/proof.jpg"],
                    "latitude": 12.95,
                    "longitude": 77.55,
                },
            )
        ]
    )

    resp = await process_field_sync(db, worker_id, req)
    assert len(resp.mutation_results) == 1
    assert resp.mutation_results[0].status == SyncMutationStatus.CONFLICT
    assert resp.mutation_results[0].conflict_reason == "cancelled_by_dispatcher"
    assert resp.mutation_results[0].conflict_review_id is not None
    # Verify DispatchConflictReview was added to db
    assert any(isinstance(call.args[0], DispatchConflictReview) for call in db.add.call_args_list)


@pytest.mark.asyncio
async def test_sync_peer_race_already_completed():
    """Verify Case 5: peer race where work order is already completed returns conflict without review queue."""
    db = AsyncMock()
    worker_id = uuid.uuid4()
    mutation_id = uuid.uuid4()
    wo_id = uuid.uuid4()

    idemp_res = MagicMock()
    idemp_res.scalar_one_or_none.return_value = None

    work_order = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=worker_id,
        status=WorkOrderStatus.COMPLETED,  # Already completed
        version=2,
    )
    wo_res = MagicMock()
    wo_res.scalar_one_or_none.return_value = work_order

    prox_res = MagicMock()
    prox_res.scalar.return_value = True

    changes_res = MagicMock()
    changes_res.scalars.return_value.all.return_value = []

    db.execute.side_effect = [idemp_res, wo_res, prox_res, changes_res]

    req = FieldSyncPushRequest(
        mutations=[
            ClientMutationItem(
                client_mutation_id=mutation_id,
                entity_id=wo_id,
                action="resolve",
                captured_at=datetime.now(UTC),
                payload={
                    "resolution_notes": "Completed too",
                    "resolution_media_urls": ["https://cdn.example.com/proof2.jpg"],
                    "latitude": 12.95,
                    "longitude": 77.55,
                },
            )
        ]
    )

    resp = await process_field_sync(db, worker_id, req)
    assert len(resp.mutation_results) == 1
    assert resp.mutation_results[0].status == SyncMutationStatus.CONFLICT
    assert resp.mutation_results[0].conflict_reason == "conflict_already_completed"
    assert resp.mutation_results[0].conflict_review_id is None


@pytest.mark.asyncio
async def test_adjudicate_accept_worker_evidence():
    """Verify supervisor accepting worker evidence marks work order completed and incident resolved."""
    db = AsyncMock()
    reviewer_id = uuid.uuid4()
    conflict_id = uuid.uuid4()
    wo_id = uuid.uuid4()
    inc_id = uuid.uuid4()
    worker_id = uuid.uuid4()

    conflict = DispatchConflictReview(
        id=conflict_id,
        organization_id=uuid.uuid4(),
        work_order_id=wo_id,
        incident_id=inc_id,
        worker_id=worker_id,
        client_mutation_id=uuid.uuid4(),
        conflict_type="cancelled_by_dispatcher",
        submitted_notes="Repaired asphalt surface",
        submitted_media_urls=["https://img.civicbrain.org/proof.jpg"],
        submitted_geom=None,
        captured_at=datetime.now(UTC),
        status=ConflictReviewStatus.PENDING,
    )
    work_order = WorkOrder(
        id=wo_id,
        organization_id=conflict.organization_id,
        incident_id=inc_id,
        department_id=uuid.uuid4(),
        status=WorkOrderStatus.CANCELLED,
        version=1,
    )
    incident = Incident(
        id=inc_id,
        organization_id=conflict.organization_id,
        department_id=uuid.uuid4(),
        ward_id=uuid.uuid4(),
        category_code="POTHOLE",
        geom=None,
        status=IncidentStatus.ASSIGNED,
    )

    c_res = MagicMock()
    c_res.scalar_one_or_none.return_value = conflict
    wo_res = MagicMock()
    wo_res.scalar_one_or_none.return_value = work_order
    inc_res = MagicMock()
    inc_res.scalar_one_or_none.return_value = incident
    obs_res = MagicMock()
    obs_res.scalars.return_value.all.return_value = []

    db.execute.side_effect = [c_res, wo_res, inc_res, obs_res]

    adj_res = await adjudicate_dispatch_conflict(
        db=db,
        conflict_id=conflict_id,
        reviewer_id=reviewer_id,
        decision=ConflictDecision.ACCEPT_WORKER_EVIDENCE,
        notes="Evidence verified legitimate",
    )

    assert adj_res.status == ConflictReviewStatus.ACCEPTED
    assert conflict.status == ConflictReviewStatus.ACCEPTED
    assert work_order.status == WorkOrderStatus.COMPLETED
    assert incident.status == IncidentStatus.RESOLVED


@pytest.mark.asyncio
async def test_adjudicate_uphold_dispatcher_action():
    """Verify supervisor upholding dispatcher action marks conflict dismissed without altering work order."""
    db = AsyncMock()
    reviewer_id = uuid.uuid4()
    conflict_id = uuid.uuid4()

    conflict = DispatchConflictReview(
        id=conflict_id,
        organization_id=uuid.uuid4(),
        work_order_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        worker_id=uuid.uuid4(),
        client_mutation_id=uuid.uuid4(),
        conflict_type="cancelled_by_dispatcher",
        submitted_notes="Some notes",
        submitted_media_urls=["https://img.civicbrain.org/proof.jpg"],
        submitted_geom=None,
        captured_at=datetime.now(UTC),
        status=ConflictReviewStatus.PENDING,
    )
    c_res = MagicMock()
    c_res.scalar_one_or_none.return_value = conflict
    db.execute.return_value = c_res

    adj_res = await adjudicate_dispatch_conflict(
        db=db,
        conflict_id=conflict_id,
        reviewer_id=reviewer_id,
        decision=ConflictDecision.UPHOLD_DISPATCHER_ACTION,
        notes="Work was rejected as defective",
    )

    assert adj_res.status == ConflictReviewStatus.DISMISSED
    assert conflict.status == ConflictReviewStatus.DISMISSED
    assert conflict.review_notes == "Work was rejected as defective"
