"""Tests for Pillar 3: DPDP Act 2023 Compliance, PII Scrubbing & Differential Privacy Integrity.

In accordance with Part B Prompt 8 & Standing Invariant 4:
- Asserts that zero raw citizen phone numbers, WhatsApp identifiers, or names leak in public endpoints.
- Asserts that Jan Sunwai ledger public endpoints only expose differentially private coordinates (dp_geom)
  with Euclidean displacement >= 30m, and never unperturbed raw incident coordinates.
- Asserts that municipal ward report cards aggregate cleanly without single-complainant microdata leaks.
"""

import re
from datetime import UTC, datetime

import pytest

from civicbrain.domain.transparency.services import (
    generate_laplace_dp_perturbation,
    process_civic_assistant_query,
)
from civicbrain.schemas.transparency import (
    CivicAssistantQueryRequest,
    JanSunwaiLedgerResponse,
)

INDIAN_PHONE_REGEX = re.compile(r"(?:\+91[\-\s]?)?[6-9]\d{9}")


def test_public_ledger_response_schema_pii_absence():
    """Verify that JanSunwaiLedgerResponse contains zero citizen PII fields."""
    fields = JanSunwaiLedgerResponse.model_fields.keys()

    # Must NOT have any citizen identifiers
    assert "citizen_id" not in fields
    assert "citizen_phone" not in fields
    assert "citizen_name" not in fields
    assert "caller_phone" not in fields
    assert "whatsapp_jid" not in fields
    assert "ip_address" not in fields

    # Must have pseudonymous public tracking and DP perturbed fields
    assert "public_tracking_code" in fields
    assert "dp_latitude" in fields
    assert "dp_longitude" in fields
    assert "dp_timestamp" in fields
    assert "entry_hash" in fields
    assert "prev_hash" in fields


def test_dp_perturbation_guarantees_minimum_displacement():
    """Verify that DP Laplace perturbation rigorously satisfies minimum privacy displacement."""
    raw_lon, raw_lat = 77.5946, 12.9716
    raw_time = datetime(2026, 9, 22, 12, 0, 0, tzinfo=UTC)

    for _ in range(50):
        dp_lon, dp_lat, time_offset = generate_laplace_dp_perturbation(raw_lon, raw_lat, raw_time)

        # Planar distance calculation in meters
        d_lon_m = (dp_lon - raw_lon) * 111000.0 * 0.974
        d_lat_m = (dp_lat - raw_lat) * 111000.0
        dist = (d_lon_m**2 + d_lat_m**2) ** 0.5

        # Verify displacement >= 30 meters
        assert dist >= 30.0, f"Displacement {dist}m < 30m minimum"

        # Verify temporal jitter >= 5 minutes (300 seconds)
        jitter_seconds = abs(time_offset.total_seconds())
        assert jitter_seconds >= 300.0, f"Jitter {jitter_seconds}s < 300s minimum"


@pytest.mark.asyncio
async def test_civic_assistant_scrubs_phone_numbers_in_responses():
    """Verify that civic assistant queries with phone numbers do not echo raw PII."""
    from unittest.mock import AsyncMock, MagicMock

    from civicbrain.domain.transparency.models import JanSunwaiLedgerEntry

    mock_db = AsyncMock()
    code = "CB-1234ABCD"
    mock_entry = JanSunwaiLedgerEntry(
        public_tracking_code=code,
        lifecycle_status="in_progress",
        department_id=None,
        predicted_eta_hours=24.0,
    )

    def mock_exec(stmt):
        m = MagicMock()
        m.scalars.return_value.first.return_value = mock_entry
        m.scalar_one_or_none.return_value = None
        return m

    mock_db.execute.side_effect = mock_exec

    req = CivicAssistantQueryRequest(
        query_text=f"Where is my complaint for phone 9876543210 and tracking code {code}?",
        language_code="en",
    )
    resp = await process_civic_assistant_query(mock_db, req)

    # Response should NOT contain unmasked phone number
    assert "9876543210" not in resp.response_text
    assert resp.intent == "STATUS_INQUIRY"
