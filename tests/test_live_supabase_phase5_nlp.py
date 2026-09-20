"""Live Supabase Phase 5 NLP Pipeline & Database Constraints Test Suite (§A11).

In strict accordance with:
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
- Verifies migration 0006 check constraints (chk_citizen_urgency_range, chk_text_severity_range).
"""

import uuid

import pytest
from postgrest.exceptions import APIError
from supabase import Client, create_client

from civicbrain.infra.config import settings


def is_live_supabase_configured() -> bool:
    """Check if real Supabase credentials are provided in settings."""
    url = settings.SUPABASE_URL
    return bool(
        url
        and not url.startswith("https://mock")
        and not url.startswith("https://your-project")
        and settings.SUPABASE_ANON_KEY
        and not settings.SUPABASE_ANON_KEY.startswith("mock")
        and settings.SUPABASE_SERVICE_ROLE_KEY
        and not settings.SUPABASE_SERVICE_ROLE_KEY.startswith("mock")
    )


@pytest.mark.skipif(
    not is_live_supabase_configured(),
    reason="Requires live Supabase project credentials in .env",
)
def test_live_supabase_phase5_nlp():
    """Verify Phase 5 database columns, check constraints, and metadata persistence on live Supabase."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )

    created_org_ids: list[str] = []

    try:
        # 1. Seed Organization, Zone, Ward, Department
        org_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Phase 5 NLP Org {run_id}",
                    "code": f"P5_NLP_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Delhi",
                }
            )
            .execute()
        )
        org_id = org_res.data[0]["id"]
        created_org_ids.append(org_id)

        zone_res = (
            service_client.table("zone")
            .insert(
                {
                    "organization_id": org_id,
                    "name": f"Central Zone {run_id}",
                    "code": f"CZ_{run_id}",
                    "geom": "SRID=4326;POLYGON((77.2 28.6, 77.3 28.6, 77.3 28.7, 77.2 28.7, 77.2 28.6))",
                }
            )
            .execute()
        )
        zone_id = zone_res.data[0]["id"]

        ward_res = (
            service_client.table("ward")
            .insert(
                {
                    "organization_id": org_id,
                    "zone_id": zone_id,
                    "ward_number": 301,
                    "name": f"Ward 301 {run_id}",
                    "code": f"W301_{run_id}",
                    "geom": "SRID=4326;POLYGON((77.21 28.61, 77.29 28.61, 77.29 28.69, 77.21 28.69, 77.21 28.61))",
                    "centroid": "SRID=4326;POINT(77.25 28.65)",
                }
            )
            .execute()
        )
        ward_id = ward_res.data[0]["id"]

        dept_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": org_id,
                    "name": "Roads & Bridges",
                    "code": f"ROADS_{run_id}",
                }
            )
            .execute()
        )
        dept_id = dept_res.data[0]["id"]

        # 2. Check Constraint Verification: chk_citizen_urgency_range on intake_report
        # Score > 1.0 must fail with check constraint error (23514)
        with pytest.raises(APIError) as exc_urgency:
            service_client.table("intake_report").insert(
                {
                    "organization_id": org_id,
                    "ward_id": ward_id,
                    "channel": "whatsapp",
                    "description": "Extreme urgent complaint",
                    "geom": "SRID=4326;POINT(77.25 28.65)",
                    "status": "submitted",
                    "detected_language": "hi",
                    "detected_script": "Devanagari",
                    "citizen_urgency_score": 1.45,  # VIOLATION: > 1.0
                }
            ).execute()
        assert "chk_citizen_urgency_range" in str(
            exc_urgency.value
        ).lower() or exc_urgency.value.code in ("23514", "P0001", "42501")

        # 3. Valid intake_report insert with NLP metadata
        report_res = (
            service_client.table("intake_report")
            .insert(
                {
                    "organization_id": org_id,
                    "ward_id": ward_id,
                    "channel": "whatsapp",
                    "description": "सड़क पर बहुत बड़ा गड्ढा है",
                    "geom": "SRID=4326;POINT(77.25 28.65)",
                    "status": "submitted",
                    "detected_language": "hi",
                    "detected_script": "Devanagari",
                    "citizen_urgency_score": 0.85,
                }
            )
            .execute()
        )
        assert len(report_res.data) == 1
        report_id = report_res.data[0]["id"]
        assert report_res.data[0]["detected_language"] == "hi"
        assert report_res.data[0]["detected_script"] == "Devanagari"
        assert report_res.data[0]["citizen_urgency_score"] == 0.85

        # 4. Check Constraint Verification: chk_text_severity_range on observation
        # Severity hint > 5 must fail with check constraint error
        with pytest.raises(APIError) as exc_sev:
            service_client.table("observation").insert(
                {
                    "organization_id": org_id,
                    "intake_report_id": report_id,
                    "department_id": dept_id,
                    "category_code": "POTHOLE",
                    "confidence": None,
                    "severity_score": 3,
                    "status": "detected",
                    "text_severity_hint": 8,  # VIOLATION: > 5
                }
            ).execute()
        assert "chk_text_severity_range" in str(exc_sev.value).lower() or exc_sev.value.code in (
            "23514",
            "P0001",
            "42501",
        )

        # 5. Valid observation insert with extracted keywords and text_severity_hint
        obs_res = (
            service_client.table("observation")
            .insert(
                {
                    "organization_id": org_id,
                    "intake_report_id": report_id,
                    "department_id": dept_id,
                    "category_code": "POTHOLE",
                    "confidence": None,
                    "severity_score": 4,
                    "status": "detected",
                    "extracted_keywords": ["सड़क", "गड्ढा", "khadda"],
                    "text_severity_hint": 4,
                }
            )
            .execute()
        )
        assert len(obs_res.data) == 1
        assert obs_res.data[0]["text_severity_hint"] == 4
        assert "khadda" in obs_res.data[0]["extracted_keywords"]

    finally:
        # 6. Teardown via privileged service_role in finally block
        for oid in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", oid).execute()
            except Exception:
                pass
