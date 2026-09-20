"""Live Supabase Phase 3 Living Taxonomy RLS & Scoped Grants Test Suite.

In strict accordance with:
- Hard Rule 5: RLS is the real authorization boundary, tested via client SDK using real per-role JWTs.
- Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL.
- Standing Invariant 5: Real seeded data, live command executions, teardown in finally blocks.
- Correction 2: WITH CHECK (status = 'proposed') on authenticated INSERT policy on taxonomy_category,
  verifying that non-admins cannot insert pre-approved categories.
"""

import uuid

import pytest
from postgrest.exceptions import APIError
from supabase import Client, create_client

from civicbrain.domain.intake.taxonomy import create_default_rubric
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
def test_live_supabase_phase3_rls():
    """Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin approval."""
    run_id = str(uuid.uuid4())[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    anon_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    created_user_ids: list[str] = []
    created_org_ids: list[str] = []

    try:
        # 1. Seed Organization & Department via service_role
        org_res = (
            service_client.table("organization")
            .insert(
                {
                    "name": f"Phase3 Org {run_id}",
                    "code": f"P3_{run_id}",
                    "ulb_type": "municipal_corporation",
                    "state": "Karnataka",
                }
            )
            .execute()
        )
        org_id = org_res.data[0]["id"]
        created_org_ids.append(org_id)

        dept_res = (
            service_client.table("department")
            .insert(
                {
                    "organization_id": org_id,
                    "name": "Roads & Civil Infrastructure",
                    "code": f"ROADS_{run_id}",
                }
            )
            .execute()
        )
        dept_id = dept_res.data[0]["id"]

        # Helper to create and authenticate users
        def create_and_login_user(role_name: str, app_meta: dict) -> tuple[str, str, Client]:
            email = f"user_{role_name}_{run_id}@civicbrain.local"
            password = f"P3Pass_{role_name}_{run_id}!2026"
            user_res = service_client.auth.admin.create_user(
                {
                    "email": email,
                    "password": password,
                    "email_confirm": True,
                    "app_metadata": app_meta,
                }
            )
            uid = user_res.user.id
            created_user_ids.append(uid)

            login_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            login_res = login_client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
            token = login_res.session.access_token
            assert token, f"Must obtain real JWT for role {role_name}"

            authed_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            authed_client.postgrest.auth(token)
            return uid, token, authed_client

        # 2. Create Admin and Staff Users
        admin_uid, admin_jwt, admin_client = create_and_login_user(
            "admin",
            {"org_id": org_id, "role": "admin"},
        )
        service_client.table("user_account").insert(
            {
                "id": admin_uid,
                "organization_id": org_id,
                "phone": f"+919800{run_id[:4]}11",
                "full_name": f"Admin User {run_id}",
            }
        ).execute()
        service_client.table("user_role_assignment").insert(
            {
                "user_id": admin_uid,
                "organization_id": org_id,
                "role": "admin",
            }
        ).execute()

        staff_uid, staff_jwt, staff_client = create_and_login_user(
            "staff",
            {"org_id": org_id, "role": "department_staff", "department_id": dept_id},
        )
        service_client.table("user_account").insert(
            {
                "id": staff_uid,
                "organization_id": org_id,
                "phone": f"+919800{run_id[:4]}22",
                "full_name": f"Staff User {run_id}",
            }
        ).execute()
        service_client.table("user_role_assignment").insert(
            {
                "user_id": staff_uid,
                "organization_id": org_id,
                "role": "department_staff",
                "department_id": dept_id,
            }
        ).execute()

        # 3. Seed initial approved category and proposed category via service_role
        rubric_data = create_default_rubric("Pothole").model_dump()
        approved_cat_res = (
            service_client.table("taxonomy_category")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "code": f"POTHOLE_{run_id}",
                    "name": "Pothole Defect",
                    "description": "Road surface defect",
                    "severity_rubric": rubric_data,
                    "status": "approved",
                    "is_active": True,
                }
            )
            .execute()
        )
        approved_cat_id = approved_cat_res.data[0]["id"]

        proposed_cat_res = (
            service_client.table("taxonomy_category")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "code": f"DRAINAGE_{run_id}",
                    "name": "Blocked Storm Drain",
                    "description": "Drainage overflow",
                    "severity_rubric": rubric_data,
                    "status": "proposed",
                    "is_active": True,
                }
            )
            .execute()
        )
        proposed_cat_id = proposed_cat_res.data[0]["id"]

        # =====================================================================
        # 4. Assert RLS Boundaries
        # =====================================================================

        # 4.1 Anon user can read approved active category
        anon_read = (
            anon_client.table("taxonomy_category").select("*").eq("id", approved_cat_id).execute()
        )
        assert len(anon_read.data) == 1, "Public should be able to read approved category"
        assert anon_read.data[0]["id"] == approved_cat_id

        # 4.2 Anon user CANNOT read proposed category
        anon_proposed_read = (
            anon_client.table("taxonomy_category").select("*").eq("id", proposed_cat_id).execute()
        )
        assert len(anon_proposed_read.data) == 0, (
            "Public must not see categories in 'proposed' state"
        )

        # 4.3 Correction 2: Non-admin CANNOT insert a pre-approved category
        # Must fail with RLS check violation because status = 'approved' violates WITH CHECK (status = 'proposed')
        with pytest.raises(APIError) as exc_info:
            staff_client.table("taxonomy_category").insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "code": f"SNEAKY_{run_id}",
                    "name": "Sneaky Approved Category",
                    "severity_rubric": rubric_data,
                    "status": "approved",  # VIOLATION of WITH CHECK (status = 'proposed')
                    "is_active": True,
                }
            ).execute()
        # Verify check violation error was raised by Postgres RLS policy
        assert "row-level security policy" in str(
            exc_info.value
        ).lower() or exc_info.value.code in ("42501", "P0001", "44000")

        # 4.4 Staff CAN insert category with status = 'proposed'
        staff_propose_res = (
            staff_client.table("taxonomy_category")
            .insert(
                {
                    "organization_id": org_id,
                    "department_id": dept_id,
                    "code": f"PROPOSED_BY_STAFF_{run_id}",
                    "name": "Staff Proposed Issue",
                    "severity_rubric": rubric_data,
                    "status": "proposed",  # Complies with WITH CHECK (status = 'proposed')
                    "is_active": True,
                }
            )
            .execute()
        )
        assert len(staff_propose_res.data) == 1
        staff_cat_id = staff_propose_res.data[0]["id"]
        assert staff_propose_res.data[0]["status"] == "proposed"

        # 4.5 Staff CANNOT update category status to 'approved' (Admin only)
        staff_update_res = (
            staff_client.table("taxonomy_category")
            .update({"status": "approved"})
            .eq("id", staff_cat_id)
            .execute()
        )
        # RLS USING/CHECK policy filters out rows where user is not org admin, resulting in 0 rows updated
        assert len(staff_update_res.data) == 0, (
            "Non-admin staff update should not affect any rows due to RLS"
        )

        # 4.6 Org Admin CAN update category status to 'approved'
        admin_update_res = (
            admin_client.table("taxonomy_category")
            .update({"status": "approved"})
            .eq("id", staff_cat_id)
            .execute()
        )
        assert len(admin_update_res.data) == 1, "Admin should successfully approve category"
        assert admin_update_res.data[0]["status"] == "approved"

        # 4.7 Once approved, anon can now read the newly approved category
        anon_after_approval = (
            anon_client.table("taxonomy_category").select("*").eq("id", staff_cat_id).execute()
        )
        assert len(anon_after_approval.data) == 1, (
            "Public should now be able to read the approved category"
        )

    finally:
        # =====================================================================
        # 5. Teardown via service_role in finally block
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
