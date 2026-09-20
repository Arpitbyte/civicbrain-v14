"""Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.

In strict accordance with:
- Hard Rule 5: RLS is the real authorization boundary, tested via client SDK using real per-role JWTs.
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
"""

import uuid

import pytest
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
def test_live_supabase_phase2_rls():
    """Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    anon_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    created_user_ids: list[str] = []
    created_org_ids: list[str] = []

    try:
        # 1. Seed Organization & Ward via service_role
        org_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Phase2 Org {run_id}",
                    "code": f"P2_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Karnataka",
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
                    "name": f"Zone {run_id}",
                    "code": f"Z_{run_id}",
                    "geom": "SRID=4326;POLYGON((77.5 12.9, 77.6 12.9, 77.6 13.0, 77.5 13.0, 77.5 12.9))",
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
                    "ward_number": 201,
                    "name": f"Ward 201 {run_id}",
                    "code": f"W201_{run_id}",
                    "geom": "SRID=4326;POLYGON((77.51 12.91, 77.59 12.91, 77.59 12.99, 77.51 12.99, 77.51 12.91))",
                    "centroid": "SRID=4326;POINT(77.55 12.95)",
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
                    "name": "Roads & Infrastructure",
                    "code": f"ROADS_{run_id}",
                }
            )
            .execute()
        )
        dept_id = dept_res.data[0]["id"]

        # 2. Create Real Auth User for Citizen
        citizen_email = f"citizen_{run_id}@civicbrain.local"
        citizen_pwd = f"CitizenPass_{run_id}!2026"
        c_auth = service_client.auth.admin.create_user(
            {
                "email": citizen_email,
                "password": citizen_pwd,
                "email_confirm": True,
            }
        )
        citizen_uid = c_auth.user.id
        created_user_ids.append(citizen_uid)

        # Citizen Sign-In via separate login_client to obtain real JWT
        # This keeps anon_client and service_client completely unmutated
        login_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        c_session = login_client.auth.sign_in_with_password(
            {
                "email": citizen_email,
                "password": citizen_pwd,
            }
        )
        citizen_jwt = c_session.session.access_token
        citizen_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        citizen_client.postgrest.auth(citizen_jwt)

        # Insert citizen_profile for foreign key constraint
        service_client.table("citizen_profile").insert(
            {
                "id": citizen_uid,
                "phone": f"+919900{run_id[:4]}01",
                "display_name": f"Citizen {run_id}",
                "verification_method": "phone_otp",
            }
        ).execute()

        # 3. Seed Intake Report & Observation via service_role
        tracking_token = f"secret_token_{run_id}_abcdef1234567890"
        report_res = (
            service_client.table("intake_report")
            .insert(
                {
                    "organization_id": org_id,
                    "citizen_id": citizen_uid,
                    "channel": "pwa",
                    "description": f"Pothole report {run_id}",
                    "geom": "SRID=4326;POINT(77.55 12.95)",
                    "ward_id": ward_id,
                    "status": "submitted",
                    "tracking_token": tracking_token,
                }
            )
            .execute()
        )
        report_id = report_res.data[0]["id"]

        obs_res = (
            service_client.table("observation")
            .insert(
                {
                    "organization_id": org_id,
                    "intake_report_id": report_id,
                    "department_id": dept_id,
                    "category_code": "POTHOLE",
                    "confidence": 0.95,
                    "severity_score": 3,
                    "status": "detected",
                }
            )
            .execute()
        )
        obs_id = obs_res.data[0]["id"]

        # 4. Seed Incident via service_role
        inc_res = (
            service_client.table("incident")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "category_code": "POTHOLE",
                    "geom": "SRID=4326;POINT(77.55 12.95)",
                    "status": "reported",
                    "severity": 3,
                }
            )
            .execute()
        )
        incident_id = inc_res.data[0]["id"]

        # Link observation to incident
        service_client.table("observation").update({"incident_id": incident_id}).eq(
            "id", obs_id
        ).execute()

        # =====================================================================
        # 5. Assert RLS Boundaries & Scoped Grants
        # =====================================================================

        # 5.1 Anonymous user cannot query intake_report table directly (SELECT denied by scoped grants)
        from postgrest.exceptions import APIError

        with pytest.raises(APIError) as exc_info:
            anon_client.table("intake_report").select("*").eq("id", report_id).execute()
        assert exc_info.value.code == "42501" or "permission denied" in str(exc_info.value)

        # 5.2 Anonymous user can execute get_anonymous_intake_report RPC with valid token
        rpc_res = anon_client.rpc(
            "get_anonymous_intake_report", {"p_tracking_token": tracking_token}
        ).execute()
        assert rpc_res.data is not None, (
            "Anonymous RPC should return report data with valid tracking token"
        )
        assert rpc_res.data["report_id"] == report_id
        assert len(rpc_res.data["observations"]) == 1
        assert rpc_res.data["observations"][0]["category_code"] == "POTHOLE"

        # 5.3 Anonymous RPC with invalid token returns null
        rpc_invalid = anon_client.rpc(
            "get_anonymous_intake_report", {"p_tracking_token": "invalid_fake_token_123"}
        ).execute()
        assert rpc_invalid.data is None, "Invalid token must return null"

        # 5.4 Authenticated Citizen can query own intake_report
        citizen_read = (
            citizen_client.table("intake_report").select("*").eq("id", report_id).execute()
        )
        assert len(citizen_read.data) == 1, "Citizen should read their own intake report"
        assert citizen_read.data[0]["id"] == report_id

        # 5.5 Authenticated Citizen can query own observation
        citizen_obs = citizen_client.table("observation").select("*").eq("id", obs_id).execute()
        assert len(citizen_obs.data) == 1, "Citizen should read observation linked to their report"

        # 5.6 Public can read incident table (transparency feed)
        public_inc = anon_client.table("incident").select("*").eq("id", incident_id).execute()
        assert len(public_inc.data) == 1, "Public should read sanitized incident"

        # 5.7 Anonymous write to incident is rejected
        from postgrest.exceptions import APIError

        with pytest.raises(APIError):
            anon_client.table("incident").insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "category_code": "POTHOLE",
                    "geom": "SRID=4326;POINT(77.55 12.95)",
                }
            ).execute()

    finally:
        # =====================================================================
        # 6. Teardown via service_role in finally block
        # =====================================================================
        for oid in created_org_ids:
            try:
                service_client.table("organization").delete().eq("id", oid).execute()
            except Exception:
                pass
        for uid in created_user_ids:
            try:
                service_client.auth.admin.delete_user(uid)
            except Exception:
                pass
