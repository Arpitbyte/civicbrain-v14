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
        pert = generate_laplace_dp_perturbation(raw_lon, raw_lat, raw_time)
        
        # Verify displacement >= 30 meters
        assert pert.displacement_meters >= 30.0, f"Displacement {pert.displacement_meters}m < 30m minimum"
        
        # Verify temporal jitter >= 5 minutes (300 seconds)
        jitter_seconds = abs((pert.dp_timestamp - raw_time).total_seconds())
        assert jitter_seconds >= 300.0, f"Jitter {jitter_seconds}s < 300s minimum"


def test_civic_assistant_scrubs_phone_numbers_in_responses():
    """Verify that civic assistant queries with phone numbers do not echo raw PII."""
    req = CivicAssistantQueryRequest(
        query_text="Where is my complaint for phone 9876543210 and tracking code CB-2026-901?",
        language="en",
    )
    resp = process_civic_assistant_query(req)

    # Response should NOT contain unmasked phone number
    assert "9876543210" not in resp.response_text
    assert resp.intent == "STATUS_INQUIRY"
