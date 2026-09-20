"""Live Supabase Phase 8 Evidence Gate & Dispatch Constraints Test Suite (§A14, §A16).

In strict accordance with:
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
- Proves database-level conditional CHECK constraints (chk_work_order_completed_evidence & chk_incident_resolved_evidence).
- Proves valid photographic and spatial evidence resolution.
- Proves citizen dispute routing to appealed.
"""

import uuid
from datetime import UTC, datetime, timedelta

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
def test_live_supabase_phase8_dispatch_evidence_gate():
    """Verify live Supabase database conditional CHECK constraints enforce evidence gates."""
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
                    "name": f"Phase 8 Dispatch Org {run_id}",
                    "code": f"P8_DISP_{run_id}",
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
                    "name": f"Zone {run_id}",
                    "code": f"Z_{run_id}",
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
                    "ward_number": 801,
                    "name": f"Ward {run_id}",
                    "code": f"W_{run_id}",
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
                    "name": "Road Infrastructure",
                    "code": f"ROADS_{run_id}",
                }
            )
            .execute()
        )
        dept_id = dept_res.data[0]["id"]

        # 2. Seed Incident in REPORTED status
        inc_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "category_code": "POTHOLE",
                    "geom": "SRID=4326;POINT(77.5500 12.9500)",
                    "severity": 4,
                    "status": "assigned",
                }
            )
            .execute()
        )
        incident_id = inc_res.data[0]["id"]

        # 3. Create Work Order in IN_PROGRESS status
        wo_res = (
            service_client.table("work_order")
            .insert(
                {
                    "organization_id": org_id,
                    "incident_id": incident_id,
                    "department_id": dept_id,
                    "status": "in_progress",
                }
            )
            .execute()
        )
        work_order_id = wo_res.data[0]["id"]

        # 4. Proving Work Order Evidence Gate (chk_work_order_completed_evidence)
        # Attempt to set status='completed' WITHOUT media URLs or resolution_geom
        with pytest.raises(APIError) as exc_wo:
            service_client.table("work_order").update(
                {
                    "status": "completed",
                    "resolution_notes": "Completed without photos",
                }
            ).eq("id", work_order_id).execute()
        assert "chk_work_order_completed_evidence" in str(exc_wo.value)

        # 5. Proving Incident Evidence Gate (chk_incident_resolved_evidence)
        # Attempt to set incident status='resolved' WITHOUT proof URLs or resolution_geom
        with pytest.raises(APIError) as exc_inc:
            service_client.table("incident").update(
                {
                    "status": "resolved",
                    "resolution_notes": "Resolved without evidence",
                }
            ).eq("id", incident_id).execute()
        assert "chk_incident_resolved_evidence" in str(exc_inc.value)

        # 6. Valid Work Order Completion (with evidence and resolution geom)
        valid_media = ["https://storage.supabase.co/proof_pothole_801.jpg"]
        valid_point = "SRID=4326;POINT(77.5501 12.9501)"
        now_iso = datetime.now(UTC).isoformat()

        wo_done = (
            service_client.table("work_order")
            .update(
                {
                    "status": "completed",
                    "completed_at": now_iso,
                    "resolution_notes": "Filled with bituminous cold mix",
                    "resolution_media_urls": valid_media,
                    "resolution_geom": valid_point,
                }
            )
            .eq("id", work_order_id)
            .execute()
        )
        assert len(wo_done.data) == 1
        assert wo_done.data[0]["status"] == "completed"
        assert wo_done.data[0]["resolution_media_urls"] == valid_media

        # 7. Valid Incident Resolution (with proof URLs, geom, and 72h deadline)
        deadline_iso = (datetime.now(UTC) + timedelta(hours=72)).isoformat()
        inc_done = (
            service_client.table("incident")
            .update(
                {
                    "status": "resolved",
                    "resolved_at": now_iso,
                    "resolution_notes": "Filled with bituminous cold mix",
                    "resolution_proof_urls": valid_media,
                    "resolution_geom": valid_point,
                    "auto_confirm_deadline": deadline_iso,
                }
            )
            .eq("id", incident_id)
            .execute()
        )
        assert len(inc_done.data) == 1
        assert inc_done.data[0]["status"] == "resolved"

        # 8. Dispute Routing: Transition to APPEALED
        inc_dispute = (
            service_client.table("incident")
            .update(
                {
                    "status": "appealed",
                    "appeal_reason": "Pothole patch broke open after heavy rain",
                    "appealed_at": datetime.now(UTC).isoformat(),
                }
            )
            .eq("id", incident_id)
            .execute()
        )
        assert len(inc_dispute.data) == 1
        assert inc_dispute.data[0]["status"] == "appealed"
        assert inc_dispute.data[0]["appeal_reason"] == "Pothole patch broke open after heavy rain"

    finally:
        # Standing Invariant 5: Teardown
        for oid in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", oid).execute()
            except Exception as e:
                print(f"Cleanup error for org {oid}: {e}")
