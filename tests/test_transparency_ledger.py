"""Unit tests for Phase 11 Transparency, Jan Sunwai Ledger, Differential Privacy & Civic Assistant (§A21, §A23)."""

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from civicbrain.domain.identity.models import Department
from civicbrain.domain.intake.models import Incident, IncidentStatus
from civicbrain.domain.transparency.models import JanSunwaiLedgerEntry
from civicbrain.domain.transparency.services import (
    compute_entry_hash,
    extract_coordinates,
    generate_laplace_dp_perturbation,
    process_civic_assistant_query,
    record_ledger_checkpoint,
    verify_incident_ledger_chain,
)
from civicbrain.schemas.transparency import CivicAssistantQueryRequest


def test_laplace_dp_perturbation_bounds():
    """Verify 2D Laplace spatial and 1D Laplace temporal noise respect bounds and invariants (§A23)."""
    true_lon = 77.5946
    true_lat = 12.9716
    now = datetime.now(UTC)

    for _ in range(50):
        dp_lon, dp_lat, time_offset = generate_laplace_dp_perturbation(true_lon, true_lat, now)

        # 1. Exact coordinate is NEVER returned
        assert (dp_lon, dp_lat) != (true_lon, true_lat)

        # 2. Planar distance in meters
        d_lon_m = (dp_lon - true_lon) * 111000.0 * 0.974
        d_lat_m = (dp_lat - true_lat) * 111000.0
        dist = (d_lon_m**2 + d_lat_m**2) ** 0.5

        # Guaranteed minimal displacement (30m) and upper bound (<= 400m)
        assert 30.0 <= dist <= 400.0

        # 3. 1D Laplace temporal jitter bounded to [-120 min, +120 min]
        total_sec = abs(time_offset.total_seconds())
        assert 300.0 <= total_sec <= 7200.0


@pytest.mark.asyncio
async def test_dp_single_draw_anti_composition_reuse():
    """Verify anti-composition rule: dp_geom and delta_t are drawn once and strictly reused across checkpoints."""
    db = AsyncMock()
    org_id = uuid.uuid4()
    incident_id = uuid.uuid4()
    dept_id = uuid.uuid4()
    ward_id = uuid.uuid4()

    now = datetime.now(UTC)
    incident = Incident(
        id=incident_id,
        organization_id=org_id,
        department_id=dept_id,
        ward_id=ward_id,
        category_code="ROAD_POTHOLE",
        geom="SRID=4326;POINT(77.594600 12.971600)",
        status=IncidentStatus.REPORTED,
        created_at=now,
    )

    # 1. Checkpoint 0: REPORTED
    mock_res_empty = MagicMock()
    mock_res_empty.scalars.return_value.all.return_value = []

    def mock_exec_seq0(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from incident" in stmt_str:
            mock_res.scalar_one_or_none.return_value = incident
        elif "from jan_sunwai_ledger_entry" in stmt_str:
            mock_res.scalars.return_value.all.return_value = []
        return mock_res

    db.execute.side_effect = mock_exec_seq0

    entry0 = await record_ledger_checkpoint(
        db=db,
        incident_id=incident_id,
        lifecycle_status="reported",
    )
    assert entry0.sequence_num == 0
    assert entry0.prev_hash == "0" * 64

    # 2. Checkpoint 1: ASSIGNED (Simulate DB having entry0)
    def mock_exec_seq1(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from incident" in stmt_str:
            mock_res.scalar_one_or_none.return_value = incident
        elif "from jan_sunwai_ledger_entry" in stmt_str:
            mock_res.scalars.return_value.all.return_value = [entry0]
        return mock_res

    db.execute.side_effect = mock_exec_seq1

    entry1 = await record_ledger_checkpoint(
        db=db,
        incident_id=incident_id,
        lifecycle_status="assigned",
        milestone_time=now + timedelta(hours=2),
    )
    assert entry1.sequence_num == 1
    assert entry1.prev_hash == entry0.entry_hash

    # Single-draw assertion: entry1 has IDENTICAL dp_geom as entry0
    lon0, lat0 = extract_coordinates(entry0.dp_geom)
    lon1, lat1 = extract_coordinates(entry1.dp_geom)
    assert (lon0, lat0) == (lon1, lat1)

    # Single-draw assertion: time jitter offset delta_t is identical
    offset0 = entry0.dp_timestamp - incident.created_at
    offset1 = entry1.dp_timestamp - (now + timedelta(hours=2))
    assert abs((offset0 - offset1).total_seconds()) < 1.0


def test_cryptographic_hash_chain_and_tamper_detection():
    """Verify linear per-incident hash chain validity and explicit tamper detection (§A23)."""
    incident_id = uuid.uuid4()
    org_id = uuid.uuid4()
    dept_id = uuid.uuid4()
    ward_id = uuid.uuid4()
    tracking_code = "CB-A1B2C3D4"

    dp_lon = 77.595000
    dp_lat = 12.972000
    wkt = f"SRID=4326;POINT({dp_lon:.6f} {dp_lat:.6f})"
    t0 = datetime(2026, 9, 21, 10, 0, 0, tzinfo=UTC)

    # Build sequence 0
    h0 = compute_entry_hash(
        prev_hash="0" * 64,
        incident_id=incident_id,
        sequence_num=0,
        lifecycle_status="reported",
        dp_lon=dp_lon,
        dp_lat=dp_lat,
        dp_timestamp=t0,
        public_tracking_code=tracking_code,
    )
    entry0 = JanSunwaiLedgerEntry(
        organization_id=org_id,
        incident_id=incident_id,
        sequence_num=0,
        public_tracking_code=tracking_code,
        category_code="ROAD_POTHOLE",
        department_id=dept_id,
        ward_id=ward_id,
        dp_geom=wkt,
        dp_timestamp=t0,
        lifecycle_status="reported",
        sla_status="within_sla",
        prev_hash="0" * 64,
        entry_hash=h0,
    )

    # Build sequence 1
    t1 = t0 + timedelta(hours=2)
    h1 = compute_entry_hash(
        prev_hash=h0,
        incident_id=incident_id,
        sequence_num=1,
        lifecycle_status="assigned",
        dp_lon=dp_lon,
        dp_lat=dp_lat,
        dp_timestamp=t1,
        public_tracking_code=tracking_code,
    )
    entry1 = JanSunwaiLedgerEntry(
        organization_id=org_id,
        incident_id=incident_id,
        sequence_num=1,
        public_tracking_code=tracking_code,
        category_code="ROAD_POTHOLE",
        department_id=dept_id,
        ward_id=ward_id,
        dp_geom=wkt,
        dp_timestamp=t1,
        lifecycle_status="assigned",
        sla_status="within_sla",
        prev_hash=h0,
        entry_hash=h1,
    )

    # Build sequence 2
    t2 = t0 + timedelta(hours=24)
    h2 = compute_entry_hash(
        prev_hash=h1,
        incident_id=incident_id,
        sequence_num=2,
        lifecycle_status="resolved",
        dp_lon=dp_lon,
        dp_lat=dp_lat,
        dp_timestamp=t2,
        public_tracking_code=tracking_code,
    )
    entry2 = JanSunwaiLedgerEntry(
        organization_id=org_id,
        incident_id=incident_id,
        sequence_num=2,
        public_tracking_code=tracking_code,
        category_code="ROAD_POTHOLE",
        department_id=dept_id,
        ward_id=ward_id,
        dp_geom=wkt,
        dp_timestamp=t2,
        lifecycle_status="resolved",
        sla_status="within_sla",
        prev_hash=h1,
        entry_hash=h2,
    )

    # Valid chain passes verification
    is_valid, err = verify_incident_ledger_chain([entry0, entry1, entry2])
    assert is_valid is True
    assert err is None

    # TAMPER TEST: Modify lifecycle_status in checkpoint 1
    entry1_tampered = JanSunwaiLedgerEntry(
        organization_id=org_id,
        incident_id=incident_id,
        sequence_num=1,
        public_tracking_code=tracking_code,
        category_code="ROAD_POTHOLE",
        department_id=dept_id,
        ward_id=ward_id,
        dp_geom=wkt,
        dp_timestamp=t1,
        lifecycle_status="tampered_status",  # Altered!
        sla_status="within_sla",
        prev_hash=h0,
        entry_hash=h1,  # Unmatched!
    )

    is_valid_tampered, err_tampered = verify_incident_ledger_chain(
        [entry0, entry1_tampered, entry2]
    )
    assert is_valid_tampered is False
    assert err_tampered is not None
    assert "Tamper detected at seq 1" in err_tampered


@pytest.mark.asyncio
async def test_civic_assistant_multilingual_templates():
    """Verify deterministic multilingual assistance for English, Hindi, and Kannada."""
    db = AsyncMock()
    code = "CB-1234ABCD"
    dept_id = uuid.uuid4()

    entry = JanSunwaiLedgerEntry(
        public_tracking_code=code,
        lifecycle_status="in_progress",
        department_id=dept_id,
        predicted_eta_hours=36.0,
    )
    dept = Department(id=dept_id, name="Roads & Infrastructure")

    def mock_exec(stmt):
        mock_res = MagicMock()
        stmt_str = str(stmt).lower()
        if "from jan_sunwai_ledger_entry" in stmt_str:
            mock_res.scalars.return_value.first.return_value = entry
        elif "from department" in stmt_str:
            mock_res.scalar_one_or_none.return_value = dept
        return mock_res

    db.execute.side_effect = mock_exec

    # English query
    resp_en = await process_civic_assistant_query(
        db,
        CivicAssistantQueryRequest(
            query_text=f"Status of complaint {code}",
            language_code="en",
        ),
    )
    assert resp_en.intent == "STATUS_INQUIRY"
    assert "Roads & Infrastructure" in resp_en.response_text
    assert "36.0 hours" in resp_en.response_text

    # Hindi query
    resp_hi = await process_civic_assistant_query(
        db,
        CivicAssistantQueryRequest(
            query_text=f"मेरी शिकायत {code} का क्या हुआ?",
            language_code="hi",
        ),
    )
    assert "अनुमानित समाधान समय" in resp_hi.response_text
    assert "36.0" in resp_hi.response_text

    # Kannada intake query
    resp_kn = await process_civic_assistant_query(
        db,
        CivicAssistantQueryRequest(
            query_text="ನಾನು ಹೊಸ ಗುಂಡಿ ದೂರು ನೀಡಬೇಕು",
            language_code="kn",
        ),
    )
    assert resp_kn.intent == "INTAKE_GUIDANCE"
    assert "ದೂರು ಸಲ್ಲಿಸಲು" in resp_kn.response_text
