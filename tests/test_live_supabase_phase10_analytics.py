"""Live Supabase Phase 10 Analytics, Ward Report Card & Corporator Digest Test Suite (§A21, §A23).

In strict accordance with:
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
- Proves database-level public anon read on ward_report_card_snapshot.
- Proves corporator ward boundary enforcement (authorized ward 200, unauthorized ward 403).
- Proves parametric ETA prediction grounded in live database priors.
"""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
from fastapi import HTTPException
from postgrest.exceptions import APIError
from supabase import Client, create_client

from civicbrain.domain.analytics.services import (
    compute_ward_report_card,
    generate_corporator_digest,
    predict_incident_eta,
)
from civicbrain.domain.identity.jwt import CurrentUserClaims
from civicbrain.domain.identity.models import StaffRole
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
async def test_live_supabase_phase10_analytics_and_corporator_digest():
    """Verify live Supabase report card snapshotting, public anon reads, and corporator ward security."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    anon_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    created_user_ids: list[str] = []
    created_org_ids: list[str] = []

    try:
        # 1. Seed Organization, Zone, Wards, Department
        org_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Phase 10 Analytics Org {run_id}",
                    "code": f"P10_ORG_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Maharashtra",
                }
            )
            .execute()
        )
        org_id = uuid.UUID(org_res.data[0]["id"])
        created_org_ids.append(str(org_id))

        polygon_geojson = (
            "SRID=4326;POLYGON((73.8 18.5, 73.9 18.5, 73.9 18.6, 73.8 18.6, 73.8 18.5))"
        )
        zone_res = (
            service_client.table("zone")
            .insert(
                {
                    "organization_id": str(org_id),
                    "name": f"Zone {run_id}",
                    "code": f"Z10_{run_id}",
                    "geom": polygon_geojson,
                }
            )
            .execute()
        )
        zone_id = zone_res.data[0]["id"]

        # Ward 101 (Assigned to Corporator)
        w1_res = (
            service_client.table("ward")
            .insert(
                {
                    "organization_id": str(org_id),
                    "zone_id": zone_id,
                    "ward_number": 101,
                    "name": f"Ward 101 {run_id}",
                    "code": f"W101_{run_id}",
                    "geom": polygon_geojson,
                }
            )
            .execute()
        )
        ward_101_id = uuid.UUID(w1_res.data[0]["id"])

        # Ward 102 (Unassigned / Other Ward)
        w2_res = (
            service_client.table("ward")
            .insert(
                {
                    "organization_id": str(org_id),
                    "zone_id": zone_id,
                    "ward_number": 102,
                    "name": f"Ward 102 {run_id}",
                    "code": f"W102_{run_id}",
                    "geom": polygon_geojson,
                }
            )
            .execute()
        )
        ward_102_id = uuid.UUID(w2_res.data[0]["id"])

        dept_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": str(org_id),
                    "name": f"Electrical & Lighting {run_id}",
                    "code": f"LIGHT_{run_id}",
                }
            )
            .execute()
        )
        dept_id = uuid.UUID(dept_res.data[0]["id"])

        # 2. Seed Real Corporator Auth User and Elected Representative
        corp_auth = service_client.auth.admin.create_user(
            {
                "email": f"corporator_{run_id}@civicbrain.local",
                "password": f"CorpP10_{run_id}!2026",
                "email_confirm": True,
            }
        )
        corp_user_id = uuid.UUID(corp_auth.user.id)
        created_user_ids.append(str(corp_user_id))

        service_client.table("user_account").insert(
            {
                "id": str(corp_user_id),
                "organization_id": str(org_id),
                "phone": f"+9198755{run_id[:5]}",
                "full_name": f"Corporator {run_id}",
            }
        ).execute()

        # Scoped to Ward 101
        service_client.table("elected_representative").insert(
            {
                "organization_id": str(org_id),
                "ward_id": str(ward_101_id),
                "user_id": str(corp_user_id),
                "full_name": f"Corporator {run_id}",
                "term_start": "2024-01-01",
                "term_end": "2029-01-01",
            }
        ).execute()


        # 3. Seed Category Service-Time Prior (base=24.0h, p25=12.0h, p50=24.0h, p90=48.0h)
        cat_prior_res = (
            service_client.table("category_service_time_prior")
            .insert(
                {
                    "organization_id": str(org_id),
                    "category_code": f"LIGHT_POLE_{run_id}",
                    "base_resolution_hours": 24.0,
                    "p25_hours": 12.0,
                    "p50_hours": 24.0,
                    "p90_hours": 48.0,
                    "min_hours": 4.0,
                    "sample_size": 25,
                }
            )
            .execute()
        )
        assert len(cat_prior_res.data) == 1

        # 4. Seed Incident in Ward 101 with severity 4
        inc_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": str(org_id),
                    "department_id": str(dept_id),
                    "ward_id": str(ward_101_id),
                    "category_code": f"LIGHT_POLE_{run_id}",
                    "geom": "SRID=4326;POINT(73.8500 18.5200)",
                    "severity": 4,
                    "status": "assigned",
                }
            )
            .execute()
        )
        incident_id = uuid.UUID(inc_res.data[0]["id"])

        # 5. Live DB Test: Predict Incident ETA via Domain Service
        async with async_session_maker() as session:
            eta = await predict_incident_eta(session, incident_id)
            # T_base = 24.0, sev=4 -> m_sev = 0.6 + 0.8 = 1.4 -> 24 * 1.4 = 33.6 hours
            assert eta.formula_components["t_base"] == 24.0
            assert eta.formula_components["m_sev"] == 1.4
            assert eta.predicted_resolution_hours == 33.6
            assert eta.p25_hours <= eta.p50_hours <= eta.p90_hours

            # 6. Live DB Test: Compute Ward Report Card & Snapshot Persistence
            report_card = await compute_ward_report_card(
                session,
                ward_id=ward_101_id,
                period_type="weekly",
                persist=True,
            )
            assert report_card.ward_id == ward_101_id
            assert report_card.total_reported >= 1
            assert report_card.total_active >= 1

        # 7. Live Supabase RLS Test: Public Anonymous SELECT on Snapshot Table
        anon_res = (
            anon_client.table("ward_report_card_snapshot")
            .select("*")
            .eq("ward_id", str(ward_101_id))
            .execute()
        )
        assert len(anon_res.data) >= 1
        assert anon_res.data[0]["total_reported"] >= 1
        assert anon_res.data[0]["period_type"] == "weekly"

        # 8. Live DB Test: Corporator Jurisdictional Boundary Enforcement
        claims = CurrentUserClaims(
            {
                "sub": str(corp_user_id),
                "role": "corporator",
                "org_id": str(org_id),
                "ward_id": str(ward_101_id),
            }
        )

        async with async_session_maker() as session:
            # Authorized ward: Ward 101 -> 200 OK with digest
            digest_ok = await generate_corporator_digest(
                db=session,
                user_claims=claims,
                ward_id=ward_101_id,
            )
            assert digest_ok.ward_id == ward_101_id
            assert digest_ok.corporator_user_id == corp_user_id
            assert digest_ok.total_active_cases >= 1

            # Unauthorized ward: Ward 102 -> 403 Forbidden
            with pytest.raises(HTTPException) as exc_info:
                await generate_corporator_digest(
                    db=session,
                    user_claims=claims,
                    ward_id=ward_102_id,
                )
            assert exc_info.value.status_code == 403
            assert "Corporator does not represent the requested ward" in exc_info.value.detail

    finally:
        # Strict Standing Invariant 5: Teardown seeded data and auth users
        for org_id_str in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", org_id_str).execute()
            except Exception:
                pass

        for uid in created_user_ids:
            try:
                service_client.auth.admin.delete_user(uid)
            except Exception:
                pass
