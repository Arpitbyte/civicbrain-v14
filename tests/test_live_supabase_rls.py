"""Live Supabase RLS and Auth integration test.

In strict accordance with Phase 0 acceptance criterion:
1. Seeds an organization row via privileged service_role connection.
2. Asserts anonymous client receives 0 rows via client SDK (RLS blocks unauthorized read despite row existing).
3. Signs in as a real Supabase Auth user, obtains the real returned JWT.
4. Asserts authenticated client SDK query succeeds and returns the seeded row.
5. Cleans up seeded data via service_role.
"""

import uuid

import pytest

from civicbrain.infra.config import settings
from supabase import Client, create_client


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
    reason="Requires live Supabase project credentials in .env (SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY)",
)
def test_live_supabase_rls_boundary():
    """End-to-end verification of RLS and Auth against a live Supabase project."""
    test_id = str(uuid.uuid4())[:8]
    test_code = f"TEST_{test_id}"
    test_email = f"tester_{test_id}@civicbrain.org"
    test_password = f"SecurePass_{test_id}!2026"

    # 1. Privileged service_role client to seed data
    admin_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

    seed_data = {
        "name": f"Test Organization {test_id}",
        "code": test_code,
        "ulb_type": "municipal_corporation",
        "state": "Karnataka",
    }
    insert_res = admin_client.table("organization").insert(seed_data).execute()
    assert insert_res.data, "Service role must be able to seed organization row"
    seeded_id = insert_res.data[0]["id"]

    try:
        # 2. Anonymous client query (Hard Rule 5: anonymous denial check)
        anon_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        anon_res = anon_client.table("organization").select("*").eq("code", test_code).execute()
        # Row exists in DB, but anonymous client must receive 0 rows due to RLS
        assert len(anon_res.data) == 0, "RLS must filter out the seeded row for anonymous client"

        # 3. Create real user & sign in via Supabase Auth
        signup_res = admin_client.auth.admin.create_user(
            {
                "email": test_email,
                "password": test_password,
                "email_confirm": True,
            }
        )
        user_id = signup_res.user.id

        # Sign in with the anon client to obtain a real Supabase Auth session JWT
        auth_res = anon_client.auth.sign_in_with_password(
            {
                "email": test_email,
                "password": test_password,
            }
        )
        real_jwt = auth_res.session.access_token
        assert real_jwt, "Must obtain real JWT from live Supabase Auth sign-in"

        # 4. Authenticated client query using the real JWT
        auth_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        auth_client.postgrest.auth(real_jwt)

        auth_query_res = (
            auth_client.table("organization").select("*").eq("code", test_code).execute()
        )
        assert len(auth_query_res.data) == 1, (
            "Authenticated client must see permitted row under RLS"
        )
        assert auth_query_res.data[0]["code"] == test_code

    finally:
        # 5. Clean up seeded data and test user via service role
        admin_client.table("organization").delete().eq("id", seeded_id).execute()
        try:
            admin_client.auth.admin.delete_user(user_id)
        except Exception:
            pass
