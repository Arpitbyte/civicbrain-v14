"""Live Supabase Phase 11 Transparency, Jan Sunwai Ledger & Nagar Pragati Test Suite (§A21, §A23).

In strict accordance with:
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
- Proves database-level public anon read on jan_sunwai_ledger_entry and nagar_pragati_city_snapshot.
- Proves anonymous insert rejection (scoped grants: SELECT only).
- Proves single-draw DP anti-composition (identical dp_geom across sequence 0 and 1).
- Proves live cryptographic hash chain integrity and tamper detection.
"""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from postgrest.exceptions import APIError
from supabase import Client, create_client

from civicbrain.domain.transparency.models import JanSunwaiLedgerEntry
from civicbrain.domain.transparency.services import (
    compute_nagar_pragati,
    extract_coordinates,
    record_ledger_checkpoint,
    verify_incident_ledger_chain,
)
from civicbrain.infra.config import settings
from civicbrain.infra.database import async_session_maker


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


@pytest.mark.asyncio
@pytest.mark.skipif(
    not is_live_supabase_configured(),
    reason="Requires live Supabase project credentials in .env",
)
async def test_live_supabase_phase11_transparency_and_tamper_detection():
    """Verify live Supabase Jan Sunwai ledger, DP anti-composition, public reads, and tamper detection."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    anon_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    created_org_ids: list[str] = []

    try:
        # 1. Seed Organization, Zone, Ward, Department
        org_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Phase 11 Transparency Org {run_id}",
                    "code": f"P11_ORG_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Karnataka",
                }
            )
            .execute()
        )
        org_id = uuid.UUID(org_res.data[0]["id"])
        created_org_ids.append(str(org_id))

        polygon_geojson = (
            "SRID=4326;POLYGON((77.5 12.9, 77.6 12.9, 77.6 13.0, 77.5 13.0, 77.5 12.9))"
        )
        zone_res = (
            service_client.table("zone")
            .insert(
                {
                    "organization_id": str(org_id),
                    "name": f"Zone 11 {run_id}",
                    "code": f"Z11_{run_id}",
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
                    "organization_id": str(org_id),
                    "zone_id": zone_id,
                    "ward_number": 1101,
                    "name": f"Ward 1101 {run_id}",
                    "code": f"W1101_{run_id}",
                    "geom": polygon_geojson,
                }
            )
            .execute()
        )
        ward_id = uuid.UUID(ward_res.data[0]["id"])

        dept_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": str(org_id),
                    "name": f"Solid Waste Management {run_id}",
                    "code": f"SWM_{run_id}",
                }
            )
            .execute()
        )
        dept_id = uuid.UUID(dept_res.data[0]["id"])

        # 2. Seed Incident
        inc_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": str(org_id),
                    "department_id": str(dept_id),
                    "ward_id": str(ward_id),
                    "category_code": f"GARBAGE_{run_id}",
                    "geom": "SRID=4326;POINT(77.5800 12.9700)",
                    "severity": 3,
                    "status": "reported",
                }
            )
            .execute()
        )
        incident_id = uuid.UUID(inc_res.data[0]["id"])

        # 3. Publish Checkpoint 0 (REPORTED) and Checkpoint 1 (ASSIGNED) via Domain Service
        async with async_session_maker() as session:
            entry0 = await record_ledger_checkpoint(
                db=session,
                incident_id=incident_id,
                lifecycle_status="reported",
                sla_status="within_sla",
                predicted_eta_hours=48.0,
            )
            assert entry0.sequence_num == 0
            assert entry0.prev_hash == "0" * 64

            entry1 = await record_ledger_checkpoint(
                db=session,
                incident_id=incident_id,
                lifecycle_status="assigned",
                sla_status="within_sla",
                predicted_eta_hours=46.0,
                milestone_time=datetime.now(UTC) + timedelta(hours=2),
            )
            assert entry1.sequence_num == 1
            assert entry1.prev_hash == entry0.entry_hash

            # Anti-composition invariant: identical dp_geom coordinates
            lon0, lat0 = extract_coordinates(entry0.dp_geom)
            lon1, lat1 = extract_coordinates(entry1.dp_geom)
            assert (lon0, lat0) == (lon1, lat1)

            # Cryptographic chain verification on live records
            is_valid, err = verify_incident_ledger_chain([entry0, entry1])
            assert is_valid is True
            assert err is None

            # Live Tamper Detection Test: alter lifecycle_status on entry1 clone
            tampered_entry = JanSunwaiLedgerEntry(
                organization_id=entry1.organization_id,
                incident_id=entry1.incident_id,
                sequence_num=entry1.sequence_num,
                public_tracking_code=entry1.public_tracking_code,
                category_code=entry1.category_code,
                department_id=entry1.department_id,
                ward_id=entry1.ward_id,
                dp_geom=entry1.dp_geom,
                dp_timestamp=entry1.dp_timestamp,
                lifecycle_status="tampered_status",
                sla_status=entry1.sla_status,
                prev_hash=entry1.prev_hash,
                entry_hash=entry1.entry_hash,
            )
            is_tampered_valid, tamper_err = verify_incident_ledger_chain([entry0, tampered_entry])
            assert is_tampered_valid is False
            assert "Tamper detected at seq 1" in str(tamper_err)

        # 4. Live Supabase RLS & Scoped Grants Test: Public Anon SELECT
        anon_res = (
            anon_client.table("jan_sunwai_ledger_entry")
            .select("*")
            .eq("incident_id", str(incident_id))
            .execute()
        )
        assert len(anon_res.data) == 2
        assert anon_res.data[0]["public_tracking_code"] == entry0.public_tracking_code

        # 5. Scoped Grants Verification: Anonymous INSERT MUST be rejected by DB permissions
        with pytest.raises(APIError):
            anon_client.table("jan_sunwai_ledger_entry").insert(
                {
                    "organization_id": str(org_id),
                    "incident_id": str(incident_id),
                    "sequence_num": 99,
                    "public_tracking_code": "TAMPER-TEST",
                    "category_code": "TEST",
                    "department_id": str(dept_id),
                    "ward_id": str(ward_id),
                    "dp_geom": "SRID=4326;POINT(77.58 12.97)",
                    "dp_timestamp": datetime.now(UTC).isoformat(),
                    "lifecycle_status": "unauthorized",
                    "sla_status": "within_sla",
                    "prev_hash": "0" * 64,
                    "entry_hash": "abc",
                }
            ).execute()

        # 6. Nagar Pragati City Progress Snapshot
        async with async_session_maker() as session:
            pragati = await compute_nagar_pragati(
                db=session,
                organization_id=org_id,
                period_type="monthly",
                persist=True,
            )
            assert pragati.organization_id == org_id
            assert pragati.total_intake >= 1

        # Public anon read on Nagar Pragati
        pragati_anon = (
            anon_client.table("nagar_pragati_city_snapshot")
            .select("*")
            .eq("organization_id", str(org_id))
            .execute()
        )
        assert len(pragati_anon.data) >= 1
        assert pragati_anon.data[0]["period_type"] == "monthly"

    finally:
        # Strict Standing Invariant 5: Teardown seeded data
        for org_id_str in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", org_id_str).execute()
            except Exception:
                pass
