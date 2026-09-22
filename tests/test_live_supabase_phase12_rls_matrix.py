"""Live Supabase Phase 12 Exhaustive RLS & Privilege Matrix Audit Test Suite.

In strict accordance with:
- Part B Prompt 8 (Hardening Pillar 2: Live RLS Matrix Security Audit).
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live JWTs, teardown in finally blocks.
- Positive Path Dimension: Proves that every role's legitimate write action (INSERT/UPDATE)
  succeeds when authenticated with a real JWT.
- Negative Path Dimension: Proves that unauthorized writes and cross-tenant mutations
  are strictly rejected by PostgreSQL RLS.
- Exercises Phase 9's real conflict-creation path end-to-end as a real field worker JWT.
"""

import uuid
from datetime import UTC, datetime

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
def test_live_supabase_phase12_exhaustive_rls_matrix():
    """Systematically audits positive and negative paths across all application tables."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    anon_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    created_user_ids: list[str] = []
    created_org_ids: list[str] = []

    def make_authed_user(role_suffix: str) -> tuple[str, Client]:
        email = f"user_{role_suffix}_{run_id}@civicbrain.local"
        password = f"Pass_{role_suffix}_{run_id}!2026"
        u = service_client.auth.admin.create_user(
            {"email": email, "password": password, "email_confirm": True}
        )
        uid = u.user.id
        created_user_ids.append(uid)

        login = anon_client.auth.sign_in_with_password({"email": email, "password": password})
        token = login.session.access_token
        authed = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        authed.postgrest.auth(token)
        return uid, authed

    try:
        # =========================================================================
        # 1. Seed Multi-Tenant Foundations: Org Alpha & Org Beta
        # =========================================================================
        org_alpha_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Org Alpha {run_id}",
                    "code": f"ALPHA_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Karnataka",
                }
            )
            .execute()
        )
        org_alpha_id = org_alpha_res.data[0]["id"]
        created_org_ids.append(org_alpha_id)

        org_beta_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Org Beta {run_id}",
                    "code": f"BETA_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Maharashtra",
                }
            )
            .execute()
        )
        org_beta_id = org_beta_res.data[0]["id"]
        created_org_ids.append(org_beta_id)

        # Create Authenticated Users:
        # - admin_alpha: Org Admin for Org Alpha
        # - worker_alpha: Field Worker for Org Alpha
        # - supervisor_alpha: Zonal Supervisor for Org Alpha
        # - citizen_user: Authenticated Citizen
        # - admin_beta: Org Admin for Org Beta (Cross-tenant testing)
        admin_alpha_id, admin_alpha_client = make_authed_user("adm_a")
        worker_alpha_id, worker_alpha_client = make_authed_user("wrk_a")
        supervisor_alpha_id, supervisor_alpha_client = make_authed_user("sup_a")
        citizen_id, citizen_client = make_authed_user("cit")
        admin_beta_id, admin_beta_client = make_authed_user("adm_b")

        # Create User Accounts & Role Assignments
        for uid, oid, phone in [
            (admin_alpha_id, org_alpha_id, f"+9198711{run_id[:5]}"),
            (worker_alpha_id, org_alpha_id, f"+9198722{run_id[:5]}"),
            (supervisor_alpha_id, org_alpha_id, f"+9198733{run_id[:5]}"),
            (citizen_id, org_alpha_id, f"+9198744{run_id[:5]}"),
            (admin_beta_id, org_beta_id, f"+9198755{run_id[:5]}"),
        ]:
            service_client.table("user_account").insert(
                {"id": uid, "organization_id": oid, "phone": phone, "full_name": f"User {uid[:6]}"}
            ).execute()

        service_client.table("user_role_assignment").insert(
            [
                {"user_id": admin_alpha_id, "organization_id": org_alpha_id, "role": "admin"},
                {
                    "user_id": worker_alpha_id,
                    "organization_id": org_alpha_id,
                    "role": "field_worker",
                },
                {
                    "user_id": supervisor_alpha_id,
                    "organization_id": org_alpha_id,
                    "role": "zonal_supervisor",
                },
                {"user_id": admin_beta_id, "organization_id": org_beta_id, "role": "admin"},
            ]
        ).execute()

        # =========================================================================
        # 2. Positive & Negative Paths: zone, ward, department (Admin manage)
        # =========================================================================
        # POSITIVE: Admin Alpha creates Zone, Ward, Department
        poly = "SRID=4326;POLYGON((77.5 12.9, 77.6 12.9, 77.6 13.0, 77.5 13.0, 77.5 12.9))"
        zone_res = (
            admin_alpha_client.table("zone")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "name": f"Zone Alpha {run_id}",
                    "code": f"ZA_{run_id}",
                    "geom": poly,
                }
            )
            .execute()
        )
        assert len(zone_res.data) == 1
        zone_id = zone_res.data[0]["id"]

        ward_res = (
            admin_alpha_client.table("ward")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "zone_id": zone_id,
                    "name": f"Ward 1 {run_id}",
                    "code": f"W1_{run_id}",
                    "ward_number": 9811,
                    "geom": poly,
                }
            )
            .execute()
        )
        assert len(ward_res.data) == 1
        ward_id = ward_res.data[0]["id"]

        dept_res = (
            admin_alpha_client.table("department")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "name": f"Roads Dept {run_id}",
                    "code": f"RD_{run_id}",
                }
            )
            .execute()
        )
        assert len(dept_res.data) == 1
        dept_id = dept_res.data[0]["id"]

        # NEGATIVE: Field worker cannot insert into ward
        with pytest.raises(APIError) as exc_wrk_ward:
            worker_alpha_client.table("ward").insert(
                {
                    "organization_id": org_alpha_id,
                    "zone_id": zone_id,
                    "name": "Unauthorized Ward",
                    "code": f"W_UN_{run_id}",
                    "ward_number": 9899,
                    "geom": poly,
                }
            ).execute()
        assert "42501" in str(exc_wrk_ward.value) or "row-level security" in str(exc_wrk_ward.value)

        # =========================================================================
        # 3. Positive & Negative Paths: elected_representative (Migration 0013 Fix)
        # =========================================================================
        corp_id, corp_client = make_authed_user("corp")
        service_client.table("user_account").insert(
            {
                "id": corp_id,
                "organization_id": org_alpha_id,
                "phone": f"+9198766{run_id[:5]}",
                "full_name": f"Corporator {run_id}",
            }
        ).execute()
        service_client.table("user_role_assignment").insert(
            {
                "user_id": corp_id,
                "organization_id": org_alpha_id,
                "role": "corporator",
                "ward_id": ward_id,
            }
        ).execute()

        # POSITIVE: Admin Alpha inserts and updates corporator
        rep_res = (
            admin_alpha_client.table("elected_representative")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "ward_id": ward_id,
                    "user_id": corp_id,
                    "full_name": f"Corporator {run_id}",
                    "party_affiliation": "Independent",
                    "term_start": "2026-01-01",
                    "term_end": "2031-01-01",
                }
            )
            .execute()
        )
        assert len(rep_res.data) == 1
        rep_id = rep_res.data[0]["id"]

        rep_up = (
            admin_alpha_client.table("elected_representative")
            .update({"party_affiliation": "Citizen Coalition"})
            .eq("id", rep_id)
            .execute()
        )
        assert len(rep_up.data) == 1
        assert rep_up.data[0]["party_affiliation"] == "Citizen Coalition"

        # NEGATIVE: Citizen cannot update corporator (RLS filters out row -> 0 rows updated)
        cit_up_res = (
            citizen_client.table("elected_representative")
            .update({"party_affiliation": "Unauthorized"})
            .eq("id", rep_id)
            .execute()
        )
        assert len(cit_up_res.data) == 0, "Citizen update must be blocked by RLS (0 rows updated)"

        # NEGATIVE: Citizen cannot insert corporator (raises 42501 WITH CHECK violation)
        with pytest.raises(APIError) as exc_cit_rep_ins:
            citizen_client.table("elected_representative").insert(
                {
                    "organization_id": org_alpha_id,
                    "ward_id": ward_id,
                    "user_id": citizen_id,
                    "full_name": "Unauthorized Corporator",
                    "term_start": "2026-01-01",
                    "term_end": "2031-01-01",
                }
            ).execute()
        assert "42501" in str(exc_cit_rep_ins.value) or "row-level security" in str(
            exc_cit_rep_ins.value
        )

        # =========================================================================
        # 4. Positive & Negative Paths: citizen_profile & intake_report
        # =========================================================================
        # POSITIVE: Citizen inserts and updates own profile
        cp_res = (
            citizen_client.table("citizen_profile")
            .insert(
                {"id": citizen_id, "phone": f"+9198744{run_id[:5]}", "preferred_language": "kn"}
            )
            .execute()
        )
        assert len(cp_res.data) == 1

        cp_up = (
            citizen_client.table("citizen_profile")
            .update({"preferred_language": "hi"})
            .eq("id", citizen_id)
            .execute()
        )
        assert len(cp_up.data) == 1
        assert cp_up.data[0]["preferred_language"] == "hi"

        # POSITIVE: Citizen user can insert intake_report (authenticated grievance intake)
        intake_res = (
            citizen_client.table("intake_report")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "citizen_id": citizen_id,
                    "channel": "pwa",
                    "description": "Broken water main flooding street",
                    "geom": "SRID=4326;POINT(77.5600 12.9600)",
                }
            )
            .execute()
        )
        assert len(intake_res.data) == 1
        intake_id = intake_res.data[0]["id"]

        # POSITIVE: Citizen can read own filed intake_report
        my_intake = citizen_client.table("intake_report").select("*").eq("id", intake_id).execute()
        assert len(my_intake.data) == 1

        # NEGATIVE: Worker Alpha cannot read citizen's intake_report (RLS filters it out)
        worker_view = (
            worker_alpha_client.table("intake_report").select("*").eq("id", intake_id).execute()
        )
        assert len(worker_view.data) == 0, (
            "Worker must not be able to read citizen's private intake report"
        )

        # =========================================================================
        # 5. Positive & Negative Paths: incident & work_order
        # =========================================================================
        # POSITIVE: Admin Alpha creates incident
        inc_res = (
            admin_alpha_client.table("incident")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "category_code": "WATER_LEAK",
                    "geom": "SRID=4326;POINT(77.5600 12.9600)",
                    "severity": 3,
                    "status": "assigned",
                    "assigned_worker_id": worker_alpha_id,
                }
            )
            .execute()
        )
        assert len(inc_res.data) == 1
        incident_id = inc_res.data[0]["id"]

        # POSITIVE: Admin Alpha creates work_order assigned to worker_alpha
        wo_res = (
            admin_alpha_client.table("work_order")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "incident_id": incident_id,
                    "department_id": dept_id,
                    "assigned_worker_id": worker_alpha_id,
                    "status": "dispatched",
                    "version": 1,
                }
            )
            .execute()
        )
        assert len(wo_res.data) == 1
        work_order_id = wo_res.data[0]["id"]

        # POSITIVE: Worker Alpha can update their assigned work order
        wo_up = (
            worker_alpha_client.table("work_order")
            .update({"status": "in_progress"})
            .eq("id", work_order_id)
            .execute()
        )
        assert len(wo_up.data) == 1
        assert wo_up.data[0]["status"] == "in_progress"

        # Dispatcher cancels work order (simulating offline race)
        admin_alpha_client.table("work_order").update({"status": "cancelled", "version": 2}).eq(
            "id", work_order_id
        ).execute()

        # =========================================================================
        # 6. Real Conflict-Creation Path: Field Worker JWT on dispatch_conflict_review
        # =========================================================================
        # POSITIVE: Worker Alpha inserts real conflict review entry with real JWT
        worker_mutation_id = str(uuid.uuid4())
        conflict_res = (
            worker_alpha_client.table("dispatch_conflict_review")
            .insert(
                {
                    "organization_id": org_alpha_id,
                    "work_order_id": work_order_id,
                    "incident_id": incident_id,
                    "worker_id": worker_alpha_id,
                    "client_mutation_id": worker_mutation_id,
                    "conflict_type": "cancelled_by_dispatcher",
                    "submitted_notes": "Repaired and replaced pipeline joint on site prior to sync",
                    "submitted_media_urls": ["https://storage.supabase.co/proof_p12.jpg"],
                    "submitted_geom": "SRID=4326;POINT(77.5601 12.9601)",
                    "captured_at": datetime.now(UTC).isoformat(),
                    "status": "pending",
                }
            )
            .execute()
        )
        assert len(conflict_res.data) == 1
        conflict_id = conflict_res.data[0]["id"]
        assert conflict_res.data[0]["status"] == "pending"

        # POSITIVE: Supervisor Alpha updates conflict review (accepts worker evidence)
        sup_up = (
            supervisor_alpha_client.table("dispatch_conflict_review")
            .update(
                {
                    "status": "accepted",
                    "reviewed_by": supervisor_alpha_id,
                    "reviewed_at": datetime.now(UTC).isoformat(),
                    "review_notes": "Supervisor verified geo-tagged photo evidence; repair validated.",
                }
            )
            .eq("id", conflict_id)
            .execute()
        )
        assert len(sup_up.data) == 1
        assert sup_up.data[0]["status"] == "accepted"

        # =========================================================================
        # 7. Positive & Negative Paths: sync_mutation_log
        # =========================================================================
        # POSITIVE: Worker Alpha logs mutation
        sync_res = (
            worker_alpha_client.table("sync_mutation_log")
            .insert(
                {
                    "client_mutation_id": worker_mutation_id,
                    "organization_id": org_alpha_id,
                    "worker_id": worker_alpha_id,
                    "entity_type": "work_order",
                    "entity_id": work_order_id,
                    "action": "resolve",
                    "status": "conflict",
                    "conflict_reason": "cancelled_by_dispatcher",
                    "server_version": 2,
                }
            )
            .execute()
        )
        assert len(sync_res.data) == 1

        # NEGATIVE: Worker Alpha cannot log mutation under worker_beta's ID
        with pytest.raises(APIError) as exc_sync_impersonate:
            worker_alpha_client.table("sync_mutation_log").insert(
                {
                    "client_mutation_id": str(uuid.uuid4()),
                    "organization_id": org_alpha_id,
                    "worker_id": admin_beta_id,  # Impersonation
                    "entity_type": "work_order",
                    "entity_id": work_order_id,
                    "action": "resolve",
                    "status": "applied",
                }
            ).execute()
        assert "42501" in str(exc_sync_impersonate.value) or "row-level security" in str(
            exc_sync_impersonate.value
        )

        # =========================================================================
        # 8. Cross-Tenant Isolation: Org Alpha vs Org Beta
        # =========================================================================
        # NEGATIVE: Admin Beta cannot SELECT or UPDATE Org Alpha's incident
        beta_inc_view = (
            admin_beta_client.table("incident").select("*").eq("id", incident_id).execute()
        )
        assert len(beta_inc_view.data) == 0, (
            "Cross-tenant leak: Admin Beta must not see Org Alpha incidents"
        )

        # NEGATIVE: Admin Beta cannot UPDATE Org Alpha's incident (0 rows updated)
        beta_cross_up = (
            admin_beta_client.table("incident")
            .update({"severity": 5})
            .eq("id", incident_id)
            .execute()
        )
        assert len(beta_cross_up.data) == 0, "Cross-tenant update must update 0 rows"

        # NEGATIVE: Admin Beta cannot INSERT into Org Alpha (raises 42501 WITH CHECK violation)
        with pytest.raises(APIError) as exc_cross_ins:
            admin_beta_client.table("incident").insert(
                {
                    "organization_id": org_alpha_id,
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "category_code": "WATER_LEAK",
                    "geom": "SRID=4326;POINT(77.5600 12.9600)",
                    "severity": 3,
                }
            ).execute()
        assert "42501" in str(exc_cross_ins.value) or "row-level security" in str(
            exc_cross_ins.value
        )

        # =========================================================================
        # 9. Scoped Transparency Tables (jan_sunwai_ledger_entry & nagar_pragati_city_snapshot)
        # =========================================================================
        # POSITIVE: Public unauthenticated read succeeds
        ledger_res = anon_client.table("jan_sunwai_ledger_entry").select("id").limit(1).execute()
        assert ledger_res.data is not None

        pragati_res = (
            anon_client.table("nagar_pragati_city_snapshot").select("id").limit(1).execute()
        )
        assert pragati_res.data is not None

        # NEGATIVE: Anonymous write is strictly rejected by scoped grants and RLS
        with pytest.raises(APIError) as exc_anon_ledger:
            anon_client.table("jan_sunwai_ledger_entry").insert(
                {
                    "organization_id": org_alpha_id,
                    "incident_id": incident_id,
                    "public_tracking_code": "TAMPER-001",
                    "category_code": "POTHOLE",
                    "department_id": dept_id,
                    "ward_id": ward_id,
                    "dp_geom": "SRID=4326;POINT(77.5 12.9)",
                    "dp_timestamp": datetime.now(UTC).isoformat(),
                    "lifecycle_status": "reported",
                    "sla_status": "within_sla",
                    "prev_hash": "0" * 64,
                    "entry_hash": "0" * 64,
                }
            ).execute()
        assert "42501" in str(exc_anon_ledger.value) or "permission denied" in str(
            exc_anon_ledger.value
        )

    finally:
        # =========================================================================
        # 10. Ephemeral Clean Teardown (Standing Invariant 5)
        # =========================================================================
        for oid in created_org_ids:
            # Cascade deletes remove associated zones, wards, depts, incidents, work orders, conflicts
            service_client.table("organization").delete().eq("id", oid).execute()

        for uid in created_user_ids:
            service_client.auth.admin.delete_user(uid)
