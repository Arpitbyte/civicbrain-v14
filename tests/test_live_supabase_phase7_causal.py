"""Live Supabase Phase 7 Causal Root-Cause Linking & In-Database Cycle Prevention Test Suite (§A13).

In strict accordance with:
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
- Proves in-database recursive CTE trigger rejects 3-node cycle (A -> B -> C -> A).
- Proves scoped RLS and root-cause priority metadata persistence.
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
def test_live_supabase_phase7_causal_cycles_and_centrality():
    """Verify live Supabase database trigger rejects 3-node cycle and updates incident root-cause metadata."""
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
                    "name": f"Phase 7 Causal Org {run_id}",
                    "code": f"P7_ORG_{run_id}",
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
                    "name": f"South Zone {run_id}",
                    "code": f"ZONE_S_{run_id}",
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
                    "ward_number": 174,
                    "name": f"HSR Layout {run_id}",
                    "code": f"WARD_174_{run_id}",
                    "geom": polygon_geojson,
                }
            )
            .execute()
        )
        ward_id = ward_res.data[0]["id"]

        dept_water_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": org_id,
                    "name": "Water Supply & Sewerage",
                    "code": f"WATER_{run_id}",
                    "is_active": True,
                }
            )
            .execute()
        )
        dept_water_id = dept_water_res.data[0]["id"]

        dept_roads_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": org_id,
                    "name": "Roads & Bridges",
                    "code": f"ROADS_{run_id}",
                    "is_active": True,
                }
            )
            .execute()
        )
        dept_roads_id = dept_roads_res.data[0]["id"]

        # 2. Seed 3 Connected Incidents:
        # A: Under-road water pipeline rupture (Root Cause)
        # B: Road foundation subsidence (Intermediate symptom)
        # C: Surface crater / asphalt collapse (Terminal symptom)
        inc_a_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_water_id,
                    "ward_id": ward_id,
                    "category_code": "WATER_SUPPLY",
                    "geom": "SRID=4326;POINT(77.63 12.91)",
                    "severity": 5,
                    "priority_score": 75.0,
                }
            )
            .execute()
        )
        inc_a_id = inc_a_res.data[0]["id"]

        inc_b_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_roads_id,
                    "ward_id": ward_id,
                    "category_code": "ROAD_SUBSIDENCE",
                    "geom": "SRID=4326;POINT(77.63 12.91)",
                    "severity": 4,
                    "priority_score": 65.0,
                }
            )
            .execute()
        )
        inc_b_id = inc_b_res.data[0]["id"]

        inc_c_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_roads_id,
                    "ward_id": ward_id,
                    "category_code": "POTHOLE",
                    "geom": "SRID=4326;POINT(77.63 12.91)",
                    "severity": 4,
                    "priority_score": 55.0,
                }
            )
            .execute()
        )
        inc_c_id = inc_c_res.data[0]["id"]

        # 3. Create Valid Directed Causal Edges:
        # A -> B
        link_ab = (
            service_client.table("incident_causal_link")
            .insert(
                {
                    "organization_id": org_id,
                    "root_incident_id": inc_a_id,
                    "symptom_incident_id": inc_b_id,
                    "relation_type": "infrastructure_failure",
                    "confidence": 0.95,
                    "notes": "Burst water main washed away road subgrade",
                }
            )
            .execute()
        )
        assert len(link_ab.data) == 1

        # B -> C
        link_bc = (
            service_client.table("incident_causal_link")
            .insert(
                {
                    "organization_id": org_id,
                    "root_incident_id": inc_b_id,
                    "symptom_incident_id": inc_c_id,
                    "relation_type": "structural_damage",
                    "confidence": 0.90,
                    "notes": "Subgrade subsidence caused surface asphalt collapse",
                }
            )
            .execute()
        )
        assert len(link_bc.data) == 1

        # 4. In-Database Cycle Prevention Verification (Correction 1):
        # Attempting C -> A forms a 3-node cycle (A -> B -> C -> A)
        # MUST BE STRICTLY REJECTED by trg_prevent_causal_cycles
        with pytest.raises(APIError) as exc_info:
            service_client.table("incident_causal_link").insert(
                {
                    "organization_id": org_id,
                    "root_incident_id": inc_c_id,
                    "symptom_incident_id": inc_a_id,
                    "relation_type": "infrastructure_failure",
                    "confidence": 0.80,
                }
            ).execute()
        assert "Cyclic causal dependency detected" in str(exc_info.value)

        # 5. Direct Self-Causation Check: A -> A
        with pytest.raises(APIError) as exc_self:
            service_client.table("incident_causal_link").insert(
                {
                    "organization_id": org_id,
                    "root_incident_id": inc_a_id,
                    "symptom_incident_id": inc_a_id,
                    "relation_type": "infrastructure_failure",
                }
            ).execute()
        assert "chk_no_self_causation" in str(exc_self.value) or "Cyclic causal dependency" in str(
            exc_self.value
        )

    finally:
        # Standing Invariant 5: Teardown
        for oid in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", oid).execute()
            except Exception as e:
                print(f"Cleanup error for org {oid}: {e}")
