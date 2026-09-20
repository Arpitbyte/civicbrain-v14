"""Unit & Integration Tests for Phase 8 Evidence-Gated Dispatch & Satisfaction Loop (§A14, §A16)."""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from civicbrain.domain.dispatch.models import WorkOrder, WorkOrderStatus
from civicbrain.domain.dispatch.services import (
    resolve_work_order,
    start_work_order,
)
from civicbrain.infra.config import settings
from civicbrain.main import app
from tests.test_hierarchy_api import create_test_token


@pytest.mark.asyncio
async def test_dispatch_work_orders_unauthorized():
    """Verify dispatching a work order without token returns 401."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post(
            "/v1/dispatch/work-orders",
            json={
                "incident_id": str(uuid.uuid4()),
                "department_id": str(uuid.uuid4()),
            },
        )
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_dispatch_work_orders_forbidden_role():
    """Verify non-dispatcher/admin role (e.g. field_worker) cannot create work orders."""
    token = create_test_token(uuid.uuid4(), "field_worker", uuid.uuid4())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post(
            "/v1/dispatch/work-orders",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "incident_id": str(uuid.uuid4()),
                "department_id": str(uuid.uuid4()),
            },
        )
        assert res.status_code == 403


@pytest.mark.asyncio
async def test_cron_auto_confirm_unauthorized():
    """Verify cron endpoint returns 401 without secret or admin credentials."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/v1/dispatch/cron/auto-confirm")
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_cron_auto_confirm_with_header():
    """Verify cron endpoint succeeds with valid X-Cron-Secret header."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post(
            "/v1/dispatch/cron/auto-confirm",
            headers={"X-Cron-Secret": settings.CRON_SECRET},
        )
        # Should succeed or return 200 with AutoConfirmResponse
        assert res.status_code == 200
        data = res.json()
        assert "confirmed_count" in data
        assert isinstance(data["confirmed_incident_ids"], list)


@pytest.mark.asyncio
async def test_resolve_work_order_empty_evidence_raises_422():
    """Verify resolve_work_order rejects empty resolution_media_urls with 422."""
    db = AsyncMock()
    wo_id = uuid.uuid4()
    worker_id = uuid.uuid4()

    mock_wo = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=worker_id,
        status=WorkOrderStatus.IN_PROGRESS,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_wo
    db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await resolve_work_order(
            db=db,
            work_order_id=wo_id,
            worker_user_id=worker_id,
            resolution_notes="Repaired potholes",
            resolution_media_urls=[],  # Empty media list
            latitude=12.95,
            longitude=77.55,
        )
    assert exc_info.value.status_code == 422
    assert "Resolution proof media URLs cannot be empty" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_resolve_work_order_empty_notes_raises_422():
    """Verify resolve_work_order rejects whitespace-only notes with 422."""
    db = AsyncMock()
    wo_id = uuid.uuid4()
    worker_id = uuid.uuid4()

    mock_wo = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=worker_id,
        status=WorkOrderStatus.IN_PROGRESS,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_wo
    db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await resolve_work_order(
            db=db,
            work_order_id=wo_id,
            worker_user_id=worker_id,
            resolution_notes="   ",  # Whitespace notes
            resolution_media_urls=["https://img.example.com/pothole.jpg"],
            latitude=12.95,
            longitude=77.55,
        )
    assert exc_info.value.status_code == 422
    assert "Resolution notes cannot be empty" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_resolve_work_order_unauthorized_worker_raises_403():
    """Verify field worker attempting to resolve another worker's work order raises 403."""
    db = AsyncMock()
    wo_id = uuid.uuid4()
    actual_worker = uuid.uuid4()
    rogue_worker = uuid.uuid4()

    mock_wo = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=actual_worker,
        status=WorkOrderStatus.IN_PROGRESS,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_wo
    db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await resolve_work_order(
            db=db,
            work_order_id=wo_id,
            worker_user_id=rogue_worker,
            resolution_notes="Some notes",
            resolution_media_urls=["https://img.example.com/pothole.jpg"],
            latitude=12.95,
            longitude=77.55,
        )
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_start_work_order_unauthorized_worker_raises_403():
    """Verify unauthorized field worker cannot start another worker's work order."""
    db = AsyncMock()
    wo_id = uuid.uuid4()
    assigned_worker = uuid.uuid4()
    wrong_worker = uuid.uuid4()

    mock_wo = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=assigned_worker,
        status=WorkOrderStatus.DISPATCHED,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_wo
    db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await start_work_order(db=db, work_order_id=wo_id, worker_user_id=wrong_worker)
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_resolve_work_order_out_of_bounds_raises_422():
    """Verify resolve_work_order rejects coordinates > 50m away with resolution_out_of_bounds."""
    db = AsyncMock()
    wo_id = uuid.uuid4()
    worker_id = uuid.uuid4()

    mock_wo = WorkOrder(
        id=wo_id,
        organization_id=uuid.uuid4(),
        incident_id=uuid.uuid4(),
        department_id=uuid.uuid4(),
        assigned_worker_id=worker_id,
        status=WorkOrderStatus.IN_PROGRESS,
    )
    wo_result = MagicMock()
    wo_result.scalar_one_or_none.return_value = mock_wo

    # Proximity query returns False (out of bounds)
    prox_result = MagicMock()
    prox_result.scalar.return_value = False

    db.execute.side_effect = [wo_result, prox_result]

    with pytest.raises(HTTPException) as exc_info:
        await resolve_work_order(
            db=db,
            work_order_id=wo_id,
            worker_user_id=worker_id,
            resolution_notes="Fixed away from location",
            resolution_media_urls=["https://img.example.com/pothole.jpg"],
            latitude=13.50,  # ~60km away
            longitude=78.00,
        )
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "resolution_out_of_bounds"


@pytest.mark.asyncio
async def test_citizen_confirm_report_not_found():
    """Verify citizen confirm returns 404 for invalid tracking token."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/v1/intake/reports/invalid_token_99999/confirm")
        assert res.status_code == 404


@pytest.mark.asyncio
async def test_citizen_dispute_report_not_found():
    """Verify citizen dispute returns 404 for invalid tracking token."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post(
            "/v1/intake/reports/invalid_token_99999/dispute",
            json={"reason": "Did not fix"},
        )
        assert res.status_code == 404
