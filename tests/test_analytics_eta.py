"""Unit tests for Phase 10 Analytics, Ward Report Cards, Corporator Digest & ETA Prediction (§A21, §A23)."""

import uuid
from datetime import UTC, date, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from civicbrain.domain.analytics.models import (
    CategoryServiceTimePrior,
)
from civicbrain.domain.analytics.services import (
    compute_csi,
    compute_ward_report_card,
    generate_corporator_digest,
    predict_incident_eta,
)
from civicbrain.domain.identity.jwt import CurrentUserClaims
from civicbrain.domain.identity.models import (
    Department,
    ElectedRepresentative,
)
from civicbrain.domain.intake.models import Incident, IncidentStatus


def test_csi_computation():
    """Verify Citizen Satisfaction Index (CSI) mathematical formulations."""
    # 0 cases -> None
    assert compute_csi(confirmed=0, appealed=0, resolved=0) is None

    # Uncontested resolved cases -> 1.0
    assert compute_csi(confirmed=0, appealed=0, resolved=10) == 1.0

    # 5 confirmed, 5 appealed -> 0.5
    assert compute_csi(confirmed=5, appealed=5, resolved=10) == 0.5

    # 8 confirmed, 2 appealed -> 0.8
    assert compute_csi(confirmed=8, appealed=2, resolved=10) == 0.8

    # 0 confirmed, 4 appealed -> 0.0
    assert compute_csi(confirmed=0, appealed=4, resolved=4) == 0.0


@pytest.mark.asyncio
async def test_eta_prediction_severity_scaling():
    """Verify parametric ETA scales with severity and respects confidence intervals."""
    db = AsyncMock()
    org_id = uuid.uuid4()
    ward_id = uuid.uuid4()
    dept_id = uuid.uuid4()

    # Create two incidents: one severity 1, one severity 5
    inc1 = Incident(
        id=uuid.uuid4(),
        organization_id=org_id,
        ward_id=ward_id,
        department_id=dept_id,
        category_code="ROAD_POTHOLE",
        severity=1,
        created_at=datetime.now(UTC),
    )
    inc5 = Incident(
        id=uuid.uuid4(),
        organization_id=org_id,
        ward_id=ward_id,
        department_id=dept_id,
        category_code="ROAD_POTHOLE",
        severity=5,
        created_at=datetime.now(UTC),
    )

    prior = CategoryServiceTimePrior(
        organization_id=org_id,
        category_code="ROAD_POTHOLE",
        base_resolution_hours=48.0,
        p25_hours=24.0,
        p50_hours=48.0,
        p90_hours=96.0,
        min_hours=6.0,
    )

    # Mock DB returns
    def mock_execute_side_effect(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from incident" in stmt_str:
            # Check which incident is being queried
            incident_to_return = inc1 if inc1.id in stmt.compile().params.values() else inc5
            mock_res.scalar_one_or_none.return_value = incident_to_return
        elif "from category_service_time_prior" in stmt_str:
            mock_res.scalar_one_or_none.return_value = prior
        elif "from ward_resolution_stat" in stmt_str:
            mock_res.scalar_one_or_none.return_value = None  # fallback
        elif "count(work_order.id)" in stmt_str:
            mock_res.scalar.return_value = 0
        elif "count(user_role_assignment.id)" in stmt_str:
            mock_res.scalar.return_value = 5
        return mock_res

    db.execute.side_effect = mock_execute_side_effect

    eta1 = await predict_incident_eta(db, inc1.id)
    eta5 = await predict_incident_eta(db, inc5.id)

    # Severity 1: m_sev = 0.6 + 0.2*1 = 0.8 -> 48 * 0.8 = 38.4 hours
    assert eta1.formula_components["m_sev"] == 0.8
    assert eta1.predicted_resolution_hours == 38.4
    assert eta1.p25_hours <= eta1.p50_hours <= eta1.p90_hours

    # Severity 5: m_sev = 0.6 + 0.2*5 = 1.6 -> 48 * 1.6 = 76.8 hours
    assert eta5.formula_components["m_sev"] == 1.6
    assert eta5.predicted_resolution_hours == 76.8
    assert eta5.p25_hours <= eta5.p50_hours <= eta5.p90_hours

    assert eta5.predicted_resolution_hours > eta1.predicted_resolution_hours


@pytest.mark.asyncio
async def test_eta_department_backlog_load():
    """Verify department load factor increases ETA when backlog spikes."""
    db = AsyncMock()
    org_id = uuid.uuid4()
    ward_id = uuid.uuid4()
    dept_id = uuid.uuid4()

    inc = Incident(
        id=uuid.uuid4(),
        organization_id=org_id,
        ward_id=ward_id,
        department_id=dept_id,
        category_code="WATER_LEAK",
        severity=3,
        created_at=datetime.now(UTC),
    )

    prior = CategoryServiceTimePrior(
        organization_id=org_id,
        category_code="WATER_LEAK",
        base_resolution_hours=24.0,
        p25_hours=12.0,
        p50_hours=24.0,
        p90_hours=48.0,
        min_hours=4.0,
    )

    # High backlog scenario: 60 active work orders, 2 active workers
    def mock_execute_side_effect(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from incident" in stmt_str:
            mock_res.scalar_one_or_none.return_value = inc
        elif "from category_service_time_prior" in stmt_str:
            mock_res.scalar_one_or_none.return_value = prior
        elif "from ward_resolution_stat" in stmt_str:
            mock_res.scalar_one_or_none.return_value = None
        elif "count(work_order.id)" in stmt_str:
            mock_res.scalar.return_value = 60
        elif "count(user_role_assignment.id)" in stmt_str:
            mock_res.scalar.return_value = 2
        return mock_res

    db.execute.side_effect = mock_execute_side_effect

    eta = await predict_incident_eta(db, inc.id)
    # load ratio = 60 / (20 * 2) = 1.5 -> l_dept = 1.0 + 1.5 = 2.5
    assert eta.formula_components["l_dept"] == 2.5
    # T_base = 24.0, m_sev = 0.6 + 0.6 = 1.2, e_ward = 1.0, l_dept = 2.5
    # T_hat = 24.0 * 1.2 * 1.0 * 2.5 = 72.0 hours
    assert eta.predicted_resolution_hours == 72.0


@pytest.mark.asyncio
async def test_corporator_digest_ward_boundary_rejection():
    """Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives HTTP 403."""
    db = AsyncMock()
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    ward_101 = uuid.uuid4()
    ward_102 = uuid.uuid4()

    claims = CurrentUserClaims(
        {
            "sub": str(user_id),
            "role": "corporator",
            "org_id": str(org_id),
            "ward_id": str(ward_101),
        }
    )

    rep = ElectedRepresentative(
        user_id=user_id,
        ward_id=ward_101,
        organization_id=org_id,
    )

    def mock_execute(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from elected_representative" in stmt_str:
            mock_res.scalar_one_or_none.return_value = rep
        elif "from user_role_assignment" in stmt_str:
            mock_res.scalar_one_or_none.return_value = None
        return mock_res

    db.execute.side_effect = mock_execute

    with pytest.raises(HTTPException) as exc_info:
        await generate_corporator_digest(db, claims, ward_id=ward_102)

    assert exc_info.value.status_code == 403
    assert "Corporator does not represent the requested ward" in exc_info.value.detail


@pytest.mark.asyncio
async def test_corporator_digest_authorized_ward_success():
    """Verify Corporator querying their own assigned ward succeeds with alerts and rankings."""
    db = AsyncMock()
    user_id = uuid.uuid4()
    org_id = uuid.uuid4()
    ward_101 = uuid.uuid4()
    dept_id = uuid.uuid4()

    claims = CurrentUserClaims(
        {
            "sub": str(user_id),
            "role": "corporator",
            "org_id": str(org_id),
            "ward_id": str(ward_101),
        }
    )

    rep = ElectedRepresentative(
        user_id=user_id,
        ward_id=ward_101,
        organization_id=org_id,
    )

    # Seed incidents: 1 active breach (> 72h), 1 resolved
    now = datetime.now(UTC)
    old_incident = Incident(
        id=uuid.uuid4(),
        organization_id=org_id,
        ward_id=ward_101,
        department_id=dept_id,
        category_code="SEWAGE_OVERFLOW",
        status=IncidentStatus.IN_PROGRESS,
        created_at=now - timedelta(hours=96),
    )
    resolved_incident = Incident(
        id=uuid.uuid4(),
        organization_id=org_id,
        ward_id=ward_101,
        department_id=dept_id,
        category_code="GARBAGE_DUMP",
        status=IncidentStatus.CONFIRMED,
        created_at=now - timedelta(days=2),
        resolved_at=now - timedelta(days=1),
        confirmed_at=now - timedelta(hours=12),
    )

    dept = Department(id=dept_id, organization_id=org_id, name="Public Health & Sanitation")

    def mock_execute(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from elected_representative" in stmt_str:
            mock_res.scalar_one_or_none.return_value = rep
        elif "from incident" in stmt_str:
            mock_res.scalars.return_value.all.return_value = [old_incident, resolved_incident]
        elif "from department" in stmt_str:
            mock_res.scalars.return_value.all.return_value = [dept]
        return mock_res

    db.execute.side_effect = mock_execute

    digest = await generate_corporator_digest(db, claims, ward_id=ward_101)

    assert digest.ward_id == ward_101
    assert digest.corporator_user_id == user_id
    assert digest.total_active_cases == 1
    assert digest.sla_breaches_count == 1
    assert len(digest.sla_breach_alerts) == 1
    assert digest.sla_breach_alerts[0].age_hours >= 96.0
    assert digest.citizen_satisfaction_index == 1.0
    assert len(digest.department_backlog_ranking) == 1
    assert digest.department_backlog_ranking[0]["department_name"] == "Public Health & Sanitation"


@pytest.mark.asyncio
async def test_ward_report_card_computation_and_snapshot():
    """Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot."""
    db = AsyncMock()
    org_id = uuid.uuid4()
    ward_id = uuid.uuid4()
    dept_id = uuid.uuid4()

    now = datetime.now(UTC)
    inc1 = Incident(
        id=uuid.uuid4(),
        organization_id=org_id,
        ward_id=ward_id,
        department_id=dept_id,
        category_code="ROAD_POTHOLE",
        status=IncidentStatus.CONFIRMED,
        created_at=now - timedelta(hours=48),
        resolved_at=now - timedelta(hours=24),
        confirmed_at=now - timedelta(hours=12),
    )
    inc2 = Incident(
        id=uuid.uuid4(),
        organization_id=org_id,
        ward_id=ward_id,
        department_id=dept_id,
        category_code="STREETLIGHT_OUT",
        status=IncidentStatus.APPEALED,
        created_at=now - timedelta(hours=36),
        resolved_at=now - timedelta(hours=12),
        appealed_at=now - timedelta(hours=2),
    )

    def mock_execute(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from incident" in stmt_str:
            mock_res.scalars.return_value.all.return_value = [inc1, inc2]
        elif "from ward_equity_credibility" in stmt_str:
            mock_res.scalar_one_or_none.return_value = None
        elif "from ward_report_card_snapshot" in stmt_str:
            mock_res.scalar_one_or_none.return_value = None
        return mock_res

    db.execute.side_effect = mock_execute

    card = await compute_ward_report_card(
        db,
        ward_id=ward_id,
        from_date=None,
        to_date=date.today(),
        period_type="weekly",
        persist=True,
    )

    assert card.ward_id == ward_id
    assert card.total_reported == 2
    assert card.total_resolved == 1  # inc1 is confirmed, inc2 is appealed
    assert card.total_confirmed == 1
    assert card.total_appealed == 1
    # 1 confirmed, 1 appealed -> CSI = 1 / (1 + 1) = 0.5
    assert card.citizen_satisfaction_index == 0.5
    assert db.add.called
    assert db.commit.called
