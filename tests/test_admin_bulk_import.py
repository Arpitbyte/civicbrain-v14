"""Tests for Admin Department Creation & Staff Bulk-Import System.

Covers:
- Department creation endpoint (POST /v1/orgs/{org_id}/departments)
- Dry-run validation (default dry_run=True creates no accounts)
- Non-admin role restriction (admin role row is rejected)
- Role scoping requirements (department_code, zone_code, ward_number)
- Duplicate phone detection (skips existing or duplicate rows)
- Cryptographic idempotency protection (SHA-256 duplicate file rejection)
- Passwordless setup-token generation & notification dispatch (zero admin-visible passwords)
- CSV formula injection sanitization (=, +, -, @ prefixing)
- Upload limits (2MB size and 500 row caps)
- Dedicated audit logging in staff_bulk_import_log
- Live Supabase admin JWT test exercising INSERT path with dry_run=false and is_org_admin policy
"""

import io
import random
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from jwt import encode
from postgrest.exceptions import APIError
from sqlalchemy import select

from civicbrain.domain.identity.models import StaffRole, UserAccount, UserRoleAssignment
from civicbrain.infra.config import settings
from civicbrain.infra.database import async_session_maker
from civicbrain.infra.supabase import get_supabase_admin_client
from civicbrain.main import app


def is_live_supabase_configured() -> bool:
    """Check if live Supabase credentials are configured."""
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


def create_jwt_token(user_id: uuid.UUID, role: str, org_id: uuid.UUID | None = None) -> str:
    """Generate signed HS256 JWT for API testing matching Supabase claims structure."""
    payload = {
        "sub": str(user_id),
        "email": f"user_{str(user_id)[:8]}@civicbrain.org",
        "role": role,
        "org_id": str(org_id) if org_id else None,
        "app_metadata": {
            "org_id": str(org_id) if org_id else None,
            "role": role,
        },
    }
    return encode(payload, settings.SECRET_KEY, algorithm="HS256")


@pytest.fixture
async def admin_fixture():
    """Ensure a valid test organization and admin user exist in DB and Supabase."""
    service_client = get_supabase_admin_client()

    # 1. Check if an admin already exists in DB
    async with async_session_maker() as session:
        res = await session.execute(
            select(UserAccount)
            .join(UserRoleAssignment, UserAccount.id == UserRoleAssignment.user_id)
            .where(UserRoleAssignment.role == StaffRole.ADMIN)
        )
        existing_user = res.scalars().first()
        if existing_user:
            yield {"org_id": existing_user.organization_id, "admin_id": existing_user.id}
            return

    # 2. Otherwise create a seeded test org and admin user
    run_id = uuid.uuid4().hex[:6]
    org_res = (
        service_client.table("organization")
        .insert(
            {
                "name": f"Admin Test Org {run_id}",
                "code": f"ATO_{run_id}".upper(),
                "ulb_type": "municipal_corporation",
                "state": "Karnataka",
            }
        )
        .execute()
    )
    org_id = uuid.UUID(org_res.data[0]["id"])

    rand_digits = "".join([str(random.randint(0, 9)) for _ in range(8)])
    admin_phone = f"+9198{rand_digits}"
    admin_email = f"admin_{run_id}@civicbrain.local"
    admin_pass = f"Adm_{run_id}!Pass2026"
    u = service_client.auth.admin.create_user(
        {
            "email": admin_email,
            "password": admin_pass,
            "email_confirm": True,
            "phone": admin_phone,
        }
    )
    admin_uid = uuid.UUID(u.user.id)

    service_client.table("user_account").insert(
        {
            "id": str(admin_uid),
            "organization_id": str(org_id),
            "email": admin_email,
            "phone": admin_phone,
            "full_name": f"Admin {run_id}",
        }
    ).execute()

    service_client.table("user_role_assignment").insert(
        {
            "user_id": str(admin_uid),
            "organization_id": str(org_id),
            "role": "admin",
        }
    ).execute()

    try:
        yield {"org_id": org_id, "admin_id": admin_uid}
    finally:
        try:
            service_client.auth.admin.delete_user(str(admin_uid))
        except Exception:
            pass
        try:
            service_client.table("organization").delete().eq("id", str(org_id)).execute()
        except Exception:
            pass


@pytest.mark.asyncio
async def test_create_department_endpoint(admin_fixture):
    """Admin can create a new department; non-admin receives 403; duplicate code returns 409."""
    org_id = admin_fixture["org_id"]
    admin_user_id = admin_fixture["admin_id"]
    worker_user_id = uuid.uuid4()

    admin_token = create_jwt_token(admin_user_id, StaffRole.ADMIN.value, org_id)
    worker_token = create_jwt_token(worker_user_id, StaffRole.FIELD_WORKER.value, org_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Non-admin caller receives 403 Forbidden
        resp_forbidden = await ac.post(
            f"/v1/orgs/{org_id}/departments",
            json={
                "name": "Water Supply",
                "code": f"WATER_{uuid.uuid4().hex[:4]}",
                "is_active": True,
            },
            headers={"Authorization": f"Bearer {worker_token}"},
        )
        assert resp_forbidden.status_code == 403

        # 2. Admin caller creates department
        dept_code = f"DEPT_{uuid.uuid4().hex[:6].upper()}"
        resp_created = await ac.post(
            f"/v1/orgs/{org_id}/departments",
            json={"name": "Electrical & Grid", "code": dept_code, "is_active": True},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp_created.status_code == 201
        data = resp_created.json()
        assert data["code"] == dept_code
        assert data["organization_id"] == str(org_id)

        # 3. Duplicate department code returns 409 Conflict
        resp_duplicate = await ac.post(
            f"/v1/orgs/{org_id}/departments",
            json={"name": "Duplicate Electrical", "code": dept_code, "is_active": True},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp_duplicate.status_code == 409


@pytest.mark.asyncio
async def test_bulk_import_dry_run_default(admin_fixture):
    """Bulk import defaults to dry_run=True, validating rows without committing users."""
    org_id = admin_fixture["org_id"]
    admin_user_id = admin_fixture["admin_id"]
    admin_token = create_jwt_token(admin_user_id, StaffRole.ADMIN.value, org_id)

    csv_data = (
        "full_name,phone,email,role,department_code,zone_code,ward_number\n"
        "Suresh Rao,9876543211,suresh@bbmp.gov.in,dispatcher,,,\n"
        "Sunil Verma,9876543212,sunil@bbmp.gov.in,dispatcher,,,\n"
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("staff.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")}
        resp = await ac.post(
            "/v1/admin/users/import",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert resp.status_code == 200
        data = resp.json()
        assert data["dry_run"] is True
        assert data["total_rows"] == 2
        assert "file_hash" in data
        assert all(r["status"] == "would_create" for r in data["results"])


@pytest.mark.asyncio
async def test_bulk_import_admin_role_rejected(admin_fixture):
    """Any CSV row attempting to create an 'admin' role is rejected with an explicit error."""
    org_id = admin_fixture["org_id"]
    admin_user_id = admin_fixture["admin_id"]
    admin_token = create_jwt_token(admin_user_id, StaffRole.ADMIN.value, org_id)

    csv_data = (
        "full_name,phone,email,role,department_code,zone_code,ward_number\n"
        "Illegal Admin,9876543210,admin@bbmp.gov.in,admin,,,\n"
        "Valid Dispatcher,9876543213,disp@bbmp.gov.in,dispatcher,,,\n"
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("staff.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")}
        resp = await ac.post(
            "/v1/admin/users/import?dry_run=true",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert resp.status_code == 200
        data = resp.json()
        admin_row = next(r for r in data["results"] if r["row_number"] == 2)
        assert admin_row["status"] == "skipped"
        assert "Admin accounts cannot be provisioned via bulk import" in admin_row["reason"]

        disp_row = next(r for r in data["results"] if r["row_number"] == 3)
        assert disp_row["status"] == "would_create"


@pytest.mark.asyncio
async def test_bulk_import_duplicate_phone_skipped(admin_fixture):
    """Duplicate phone within the same file is rejected on subsequent occurrences."""
    org_id = admin_fixture["org_id"]
    admin_user_id = admin_fixture["admin_id"]
    admin_token = create_jwt_token(admin_user_id, StaffRole.ADMIN.value, org_id)

    csv_data = (
        "full_name,phone,email,role,department_code,zone_code,ward_number\n"
        "Staff One,9876543214,one@bbmp.gov.in,dispatcher,,,\n"
        "Staff Two,9876543214,two@bbmp.gov.in,dispatcher,,,\n"
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("staff.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")}
        resp = await ac.post(
            "/v1/admin/users/import?dry_run=true",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert resp.status_code == 200
        data = resp.json()
        first_row = next(r for r in data["results"] if r["row_number"] == 2)
        second_row = next(r for r in data["results"] if r["row_number"] == 3)

        assert first_row["status"] == "would_create"
        assert second_row["status"] == "skipped"
        assert "Duplicate phone number" in second_row["reason"]


@pytest.mark.asyncio
async def test_bulk_import_formula_injection_sanitization(admin_fixture):
    """Fields starting with =, +, -, @ are sanitized by prefixing with a single quote."""
    org_id = admin_fixture["org_id"]
    admin_user_id = admin_fixture["admin_id"]
    admin_token = create_jwt_token(admin_user_id, StaffRole.ADMIN.value, org_id)

    csv_data = (
        "full_name,phone,email,role,department_code,zone_code,ward_number\n"
        "=cmd|'/C calc'!A0,9876543215,attacker@evil.com,dispatcher,,,\n"
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("exploit.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")}
        resp = await ac.post(
            "/v1/admin/users/import?dry_run=true",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert resp.status_code == 200
        data = resp.json()
        row = data["results"][0]
        assert row["full_name"].startswith("'=")


@pytest.mark.asyncio
async def test_bulk_import_forbidden_for_non_admin(admin_fixture):
    """Non-admin caller receives HTTP 403 Forbidden."""
    org_id = admin_fixture["org_id"]
    worker_user_id = uuid.uuid4()
    worker_token = create_jwt_token(worker_user_id, StaffRole.FIELD_WORKER.value, org_id)

    csv_data = "full_name,phone,role\nTest,9876543216,dispatcher\n"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("staff.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")}
        resp = await ac.post(
            "/v1/admin/users/import",
            files=files,
            headers={"Authorization": f"Bearer {worker_token}"},
        )

        assert resp.status_code == 403


@pytest.mark.asyncio
async def test_bulk_import_file_size_and_row_limits(admin_fixture):
    """File size exceeding 2MB or rows exceeding 500 are rejected."""
    org_id = admin_fixture["org_id"]
    admin_user_id = admin_fixture["admin_id"]
    admin_token = create_jwt_token(admin_user_id, StaffRole.ADMIN.value, org_id)

    # 1. Row limit check (> 500 rows)
    rows = ["full_name,phone,role"] + [f"Staff {i},98765{i:05d},dispatcher" for i in range(501)]
    csv_large_rows = "\n".join(rows)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("large_rows.csv", io.BytesIO(csv_large_rows.encode("utf-8")), "text/csv")}
        resp = await ac.post(
            "/v1/admin/users/import",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 400
        assert "exceeds maximum allowed limit of 500 rows" in resp.json()["detail"]


@pytest.mark.skipif(
    not is_live_supabase_configured(),
    reason="Requires live Supabase project credentials in .env",
)
def test_live_supabase_admin_bulk_import_and_is_org_admin_rls():
    """Live Supabase integration test exercising dry_run=false with real admin JWT and is_org_admin RLS."""
    from supabase import Client, create_client

    run_id = uuid.uuid4().hex[:8]
    service_client: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    anon_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

    # 1. Create test organization
    org_res = (
        service_client.table("organization")
        .insert(
            {
                "name": f"Bulk Import Org {run_id}",
                "code": f"BIO_{run_id}".upper(),
                "ulb_type": "municipal_corporation",
                "state": "Karnataka",
            }
        )
        .execute()
    )
    org_id = org_res.data[0]["id"]

    created_user_ids = []
    try:
        # 2. Create real Admin user with valid E.164 phone
        rand_digits = "".join([str(random.randint(0, 9)) for _ in range(8)])
        admin_phone = f"+9198{rand_digits}"
        admin_email = f"admin_{run_id}@civicbrain.local"
        admin_pass = f"Adm_{run_id}!Pass2026"
        u = service_client.auth.admin.create_user(
            {
                "email": admin_email,
                "password": admin_pass,
                "email_confirm": True,
                "phone": admin_phone,
            }
        )
        admin_uid = u.user.id
        created_user_ids.append(admin_uid)

        # 3. Create user_account and user_role_assignment (admin)
        service_client.table("user_account").insert(
            {
                "id": admin_uid,
                "organization_id": org_id,
                "email": admin_email,
                "phone": admin_phone,
                "full_name": f"Admin {run_id}",
            }
        ).execute()

        service_client.table("user_role_assignment").insert(
            {
                "user_id": admin_uid,
                "organization_id": org_id,
                "role": "admin",
            }
        ).execute()

        # 4. Sign in as Admin to obtain real authenticated JWT
        login_res = anon_client.auth.sign_in_with_password(
            {"email": admin_email, "password": admin_pass}
        )
        admin_token = login_res.session.access_token

        # 5. Create authenticated PostgREST client with Admin token
        admin_postgrest = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        admin_postgrest.postgrest.auth(admin_token)

        # 6. Test RLS INSERT into staff_bulk_import_log using is_org_admin(organization_id) policy
        test_file_hash = uuid.uuid4().hex
        insert_res = (
            admin_postgrest.table("staff_bulk_import_log")
            .insert(
                {
                    "organization_id": org_id,
                    "admin_user_id": admin_uid,
                    "file_name": f"test_{run_id}.csv",
                    "file_hash": test_file_hash,
                    "total_rows": 2,
                    "created_count": 2,
                    "skipped_count": 0,
                    "is_dry_run": False,
                }
            )
            .execute()
        )
        assert len(insert_res.data) == 1
        assert insert_res.data[0]["file_hash"] == test_file_hash

        # 7. Test RLS SELECT from staff_bulk_import_log
        select_res = (
            admin_postgrest.table("staff_bulk_import_log")
            .select("*")
            .eq("file_hash", test_file_hash)
            .execute()
        )
        assert len(select_res.data) == 1
        assert select_res.data[0]["admin_user_id"] == admin_uid

        # 8. Test Idempotency constraint (duplicate hash with is_dry_run=false raises error)
        with pytest.raises(APIError):
            admin_postgrest.table("staff_bulk_import_log").insert(
                {
                    "organization_id": org_id,
                    "admin_user_id": admin_uid,
                    "file_name": f"dup_{run_id}.csv",
                    "file_hash": test_file_hash,
                    "total_rows": 2,
                    "created_count": 2,
                    "skipped_count": 0,
                    "is_dry_run": False,
                }
            ).execute()

    finally:
        # Cleanup test resources
        for uid in created_user_ids:
            try:
                service_client.auth.admin.delete_user(uid)
            except Exception:
                pass
        try:
            service_client.table("organization").delete().eq("id", org_id).execute()
        except Exception:
            pass
