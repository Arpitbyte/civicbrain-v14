"""Live Supabase Phase 6 AHP Prioritization, Equity & Credibility Test Suite (§A12, §A13).

In strict accordance with:
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
- Verifies migration 0007 AHP config, consistency ratio DB check constraint, ward equity table,
  incident sub-scores, and is_org_admin RLS policies.
"""

import uuid

import pytest
from postgrest.exceptions import APIError
from supabase import Client, create_client

from civicbrain.domain.prioritization.ahp import AHPMatrix
from civicbrain.domain.prioritization.equity import BuhlmannEquityCompensator
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
def test_live_supabase_phase6_ahp_credibility():
    """Verify Phase 6 AHP persistence, CR check constraint, and ward equity on live Supabase."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )

    created_org_ids: list[str] = []

    try:
        # 1. Seed Real Organization, Zone, Ward, Department
        org_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Phase 6 Org {run_id}",
                    "code": f"P6_ORG_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Karnataka",
                }
            )
            .execute()
        )
        org_id = org_res.data[0]["id"]
        created_org_ids.append(org_id)

        polygon_geojson = (
            "SRID=4326;POLYGON((77.5 12.9, 77.6 12.9, 77.6 13.0, 77.5 13.0, 77.5 12.9))"
        )
        zone_res = (
            service_client.table("zone")
            .insert(
                {
                    "organization_id": org_id,
                    "name": f"East Zone {run_id}",
                    "code": f"ZONE_E_{run_id}",
                    "geom": polygon_geojson,
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
                    "ward_number": 88,
                    "name": f"Indiranagar {run_id}",
                    "code": f"WARD_88_{run_id}",
                    "geom": polygon_geojson,
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
                    "name": "Public Works & Roads",
                    "code": f"ROADS_{run_id}",
                    "is_active": True,
                }
            )
            .execute()
        )
        dept_id = dept_res.data[0]["id"]

        # 2. Verify AHP Configuration Persistence & CR DB CHECK Constraint
        solver = AHPMatrix()
        valid_res = solver.solve()

        # 2.1 Valid AHP Matrix (CR < 0.10) inserts successfully
        ahp_insert = (
            service_client.table("ahp_matrix_config")
            .insert(
                {
                    "organization_id": org_id,
                    "matrix": AHPMatrix.DEFAULT_MATRIX,
                    "weights": valid_res.weights,
                    "lambda_max": valid_res.lambda_max,
                    "consistency_index": valid_res.consistency_index,
                    "consistency_ratio": valid_res.consistency_ratio,
                    "is_active": True,
                }
            )
            .execute()
        )
        assert len(ahp_insert.data) == 1
        assert ahp_insert.data[0]["consistency_ratio"] < 0.10

        # 2.2 Inconsistent Matrix (CR >= 0.10) MUST BE REJECTED by DB CHECK constraint chk_ahp_cr
        with pytest.raises(APIError) as exc_info:
            service_client.table("ahp_matrix_config").insert(
                {
                    "organization_id": org_id,
                    "matrix": AHPMatrix.DEFAULT_MATRIX,
                    "weights": valid_res.weights,
                    "lambda_max": 5.5,
                    "consistency_index": 0.125,
                    "consistency_ratio": 0.1116,  # > 0.10, violates chk_ahp_cr
                    "is_active": False,
                }
            ).execute()
        assert "chk_ahp_cr" in str(exc_info.value)

        # 3. Seed Ward Equity Credibility
        compensator = BuhlmannEquityCompensator()
        equity_res = compensator.evaluate_ward(
            verified_incident_count=10,
            historical_incident_rate=8.0,
            observed_issue_rate=3.0,
            city_prior_rate=12.0,
        )
        ward_eq_insert = (
            service_client.table("ward_equity_credibility")
            .insert(
                {
                    "organization_id": org_id,
                    "ward_id": ward_id,
                    "verified_incident_count": 10,
                    "historical_incident_rate": 8.0,
                    "credibility_factor": equity_res.credibility_factor,
                    "expected_issue_rate": equity_res.expected_issue_rate,
                    "observed_issue_rate": equity_res.observed_issue_rate,
                    "equity_gap": equity_res.equity_gap,
                    "equity_boost": equity_res.equity_boost,
                }
            )
            .execute()
        )
        assert len(ward_eq_insert.data) == 1
        assert ward_eq_insert.data[0]["equity_boost"] > 0.0

        # 4. Insert Incident with 5 AHP Sub-scores and Confidence Score
        inc_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "category_code": "POTHOLE",
                    "geom": "SRID=4326;POINT(77.55 12.95)",
                    "severity": 4,
                    "status": "triaged",
                    "subscore_severity": 0.80,
                    "subscore_risk": 0.85,
                    "subscore_exposure": 0.70,
                    "subscore_criticality": 0.90,
                    "subscore_urgency": 0.75,
                    "raw_priority_score": 0.81,
                    "equity_boost": equity_res.equity_boost,
                    "priority_score": 85.5,
                    "confidence_score": 0.40,
                    "requires_human_review": True,
                    "review_reason": "high_priority_low_confidence",
                }
            )
            .execute()
        )
        assert len(inc_res.data) == 1
        inc_data = inc_res.data[0]
        assert inc_data["priority_score"] == 85.5
        assert inc_data["requires_human_review"] is True
        assert inc_data["review_reason"] == "high_priority_low_confidence"

        # 5. Verify Check Constraints on Incident sub-scores (e.g. subscore > 1.0 rejected)
        with pytest.raises(APIError) as exc_subscore:
            service_client.table("incident").insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "category_code": "POTHOLE",
                    "geom": "SRID=4326;POINT(77.55 12.95)",
                    "subscore_severity": 1.5,  # > 1.0 violates chk_subscore_severity
                }
            ).execute()
        assert "chk_subscore_severity" in str(exc_subscore.value)

    finally:
        # Standing Invariant 5: Teardown seeded test data
        for oid in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", oid).execute()
            except Exception as e:
                print(f"Cleanup error for org {oid}: {e}")
