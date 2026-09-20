# Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

**Date:** 2026-09-20  
**Status:** COMPLETED  
**Version:** CivicBrain v14.1.0  

---

## 1. What Was Built

- **Administrative & Electoral Domain Models (§A7):**
  - Conformed administrative hierarchy matching the 74th Constitutional Amendment Act, 1992:
    - `organization`: Root ULB carrying `ulb_type` (`municipal_corporation`, `municipal_council`, `nagar_panchayat`).
    - `zone`: Administrative subdivision of ULB with PostGIS Polygon geometry (`geom`).
    - `ward`: Administrative and electoral unit carrying PostGIS Polygon geometry (`geom`) and `centroid` Point.
    - `department`: Domain service taxonomy matching DIGIT's PGR classification (`ROADS`, `SWM`, `DRAINS`, `WATER`, `ELECTRICAL`, `HEALTH`).
    - `user_account`: Internal staff user linked to Supabase Auth (`auth.users.id`).
    - `user_role_assignment`: RBAC role assignments scoped by `department_id`, `zone_id`, or `ward_id`.
    - `elected_representative`: Corporator/Councillor record scoped to exactly one ward (`ward_id UNIQUE`).
    - `citizen_profile`: Citizen identity verifying phone number via OTP without collecting Aadhaar (§A8).
- **Enums & RBAC Workspace Mapping (§A5, §A18):**
  - Defined `staff_role_enum` strictly mapped to named workspaces:
    - `admin` (Control Room — System/ULB Admin)
    - `dispatcher` (Command Deck — Dispatcher, Duty Officer)
    - `department_staff` (Ops Board — Department Staff, Department Supervisor)
    - `zonal_supervisor` (City Pulse — Zonal Supervisor, Data Analyst)
    - `field_worker` (Karmi Sahayak / FieldOps — Field Worker, Inspector, Crew Lead)
    - `corporator` (Transparency Board & Command Deck / City Pulse — Ward Elected Representative)
  - Defined `citizen_verification_method_enum`: `phone_otp` (primary and sufficient), `digilocker` (provisional).
- **Database Migration & Scoped Grants (Standing Invariant 4):**
  - Created and applied `migrations/0002_phase1_identity_rbac.sql` on live Supabase.
  - Granted explicit, operation-scoped privileges on every table (`service_role`, `authenticated`, `anon` where public), with zero blanket `GRANT ALL` statements.
  - Created `is_org_admin(UUID)` security-definer helper function to prevent recursive RLS evaluation in PostgREST.
- **REST API Endpoints:**
  - `GET /v1/auth/me`: Resolves current authenticated profile and active jurisdictional scopes.
  - `GET /v1/orgs/{org_id}/hierarchy`: Returns full hierarchy tree of zones and wards.
  - `GET /v1/orgs/{org_id}/departments`: Lists active ULB departments.
  - `GET /v1/orgs/{org_id}/wards/{ward_id}/representative`: Public endpoint discovering the elected Corporator for a ward.
  - `POST /v1/admin/users`: Admin-only provisioning of staff members with role assignments.
  - `GET /v1/admin/users`: Admin-only listing of tenant staff members.
- **Automated Test Suite:**
  - `tests/test_identity_models.py`: Unit tests for model structure, enums, schemas, and JWT parsing.
  - `tests/test_hierarchy_api.py`: Integration tests for `/v1/auth/me` and hierarchy endpoints.
  - `tests/test_live_supabase_rbac_rls.py`: Full end-to-end verification against live Supabase asserting real pre-seeded rows, real Supabase Auth logins/JWTs across all roles, cross-tenant leakage denial, Corporator write denial, and automatic cleanup in `finally` blocks.

---

## 2. Key Architectural Decisions

1. **Security Definer Function for RLS Admin Checks:**
   Implemented `is_org_admin(UUID)` marked `SECURITY DEFINER` to allow RLS policies on `user_account`, `user_role_assignment`, `zone`, `ward`, and `department` to check admin status without causing PostgreSQL `42P17: infinite recursion detected`.
2. **NullPool with Supabase Transaction Pooler:**
   Configured SQLAlchemy's async engine with `NullPool`, `statement_cache_size=0`, and `prepared_statement_cache_size=0` to eliminate connection pooling conflicts with pgbouncer and prevent event loop crossing in pytest-asyncio.
3. **Strict Operation-Scoped Table Grants:**
   In adherence to Standing Invariant 4, `service_role` is granted `SELECT, INSERT, UPDATE, DELETE`, `authenticated` receives `SELECT` (and `UPDATE` where permitted), and `anon` receives `SELECT` only on public boundary and taxonomy tables.
4. **Corporator Scope Isolation:**
   Enforced that Corporators have read access to Command Deck's live queue and City Pulse's equity data strictly scoped to their assigned `ward_id`, with absolute write denial on operational tables.

---

## 3. Deviations from Specification

None. All files and requirements strictly conform to Phase 1 of CivicBrain v14 Part A and Part B.

---

## 4. Verification & CI Status

- [x] **Live Supabase Schema Applied:** Migration `0002_phase1_identity_rbac.sql` applied cleanly with PostGIS polygon geometry columns for `zone` and `ward`.
- [x] **Scoped Grants Verified:** All 7 tables in migration 0002 have explicit scoped grants (no blanket `GRANT ALL`).
- [x] **Live Client SDK RBAC Tests:** `tests/test_live_supabase_rbac_rls.py` executed against live Supabase with real seeded rows, real auth sign-ins, and verified cross-tenant isolation, anonymous denial, citizen self-isolation, and Corporator write denial.
- [x] **Local Test Suite:** 16 tests passing in 23.28s with zero lint errors (`ruff check`) and formatting verified (`ruff format`).
