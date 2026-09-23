# Specification: Admin Bulk-Import System & Department Administration

**Date:** 2026-09-23  
**Status:** PROPOSED / APPROVED FOR IMPLEMENTATION  
**Target:** CivicBrain v14 Control Room API  

---

## 1. Executive Summary & Core Requirements

This specification defines the architecture, data structures, security controls, and endpoint behavior for:
1. **Control Room Department Management (`POST /v1/orgs/{org_id}/departments`)**: Missing administrative endpoint required to manage tenant department taxonomies.
2. **Staff Bulk Import (`POST /v1/admin/users/import`)**: A hardened, production-grade CSV import system designed strictly for the five non-admin operational roles.
3. **Passwordless Setup-Link Onboarding Flow**: Elimination of admin-visible generated credentials in favor of one-time cryptographic setup tokens delivered via notification adapters.
4. **Dry-Run Default & Idempotency Safeguards**: Safe pre-flight validation by default and cryptographic SHA-256 file-hash deduplication.
5. **Dedicated Import Audit Log**: A dedicated, permanent database audit table tracking every import event, distinct from individual user profile tables.
6. **Explicit Citizen Exclusion**: Preservation of Hard Rule 5 (no citizen bulk-import with generated credentials; citizens only self-provision via Phone OTP).

---

## 2. The Six Corrected Design Pillars

### Pillar 1: Non-Admin Role Restriction
- Bulk import is restricted exclusively to the 5 operational staff roles:
  1. `dispatcher`
  2. `department_staff`
  3. `zonal_supervisor`
  4. `field_worker`
  5. `corporator`
- **Hard Invariant:** `admin` accounts can **never** be provisioned via this endpoint. If any CSV row specifies `role == "admin"`, that row is immediately rejected with reason: `"Admin accounts cannot be provisioned via bulk import."`.

### Pillar 2: Setup-Token & User-Sets-Own-Password Flow (Zero Admin-Visible Passwords)
- Replaces admin-generated passwords with a secure password setup link.
- For each valid row:
  - Generates a cryptographically secure setup token (`secrets.token_urlsafe(32)`).
  - Persists token with a 72-hour expiration in Redis / cache (`setup_token:{token} -> {user_id, org_id}`).
  - Dispatches an account setup notification link (`{settings.FRONTEND_BASE_URL}?token=...`) via `civicbrain.domain.notifications.service` (SMS / WhatsApp / Email adapters). `FRONTEND_BASE_URL` is configured in `civicbrain/infra/config.py` defaulting to `http://localhost:5173/setup-password`.
  - The admin receives an audit of dispatched invitations (`setup_link_dispatched: true`), but **never sees, handles, or receives any password**.
  - PII logging filter in `civicbrain/infra/logging.py` is strengthened with regex patterns redacting any token or password keys if mistakenly passed to log handlers.

### Pillar 3: Explicit Duplicate-Phone & Identity Handling
- Validates phone format against standard Indian telecom format (`+91` prefix or 10-digit format starting with `[6-9]`).
- Pre-checks `phone` against existing records in `public.user_account`.
- Pre-checks `phone` against previous rows within the same uploaded CSV.
- If a duplicate phone is encountered:
  - The row is skipped with explicit reason: `"Phone number {phone} is already registered to an existing account."` (or `"Duplicate phone number within the same import file."`).
  - **No silent overwrites, no duplicate row insertions, and no partial account corruption.**

### Pillar 4: Dry-Run Mode as the Default First Pass
- The endpoint parameter `dry_run: bool = Query(default=True)` mandates that unflagged calls perform validation only:
  - Validates CSV syntax and row limit (maximum 500 rows).
  - Sanitizes all string values against CSV/formula injection.
  - Checks required fields per role.
  - Resolves foreign keys against the database: `department_code` (against `department`), `zone_code` (against `zone`), and `ward_number` (against `ward`).
  - Verifies phone and email uniqueness.
  - Simulates the entire process with zero writes to Supabase Auth and zero writes to PostgreSQL.
  - Returns per-row `status: "would_create"` or `status: "skipped"` with exact diagnostic error reasons.
- Real account creation only occurs when the caller explicitly passes `dry_run=false`.

### Pillar 5: Idempotency Protection via Cryptographic File Hash
- Upon upload, the server computes `file_hash = hashlib.sha256(raw_bytes).hexdigest()`.
- When `dry_run=false`, the server checks whether an import with `file_hash` has already succeeded for the caller's `organization_id`.
- If a matching hash exists, execution aborts with `HTTP 409 Conflict`:
  `"File with SHA-256 hash {file_hash} has already been processed for this organization on {timestamp}."`.

### Pillar 6: Permanent Audit Logging for Import Events
- Introduces migration `0015_staff_bulk_import_audit.sql` defining `public.staff_bulk_import_log`.
- Records top-level batch metadata:
  - `id`: UUID Primary Key
  - `organization_id`: UUID References `organization(id)`
  - `admin_user_id`: UUID References `user_account(id)`
  - `file_name`: String
  - `file_hash`: String (SHA-256)
  - `total_rows`: Integer
  - `created_count`: Integer
  - `skipped_count`: Integer
  - `is_dry_run`: Boolean
  - `created_at`: Timestamp with Time Zone
- Guarded by PostgreSQL Row-Level Security (RLS) and scoped table grants.

---

## 3. Database Schema Changes (`migrations/0015_staff_bulk_import_audit.sql`)

```sql
-- CivicBrain v14 — Admin Bulk Import Audit Table & User Account Extensions
-- Migration 0015: staff_bulk_import_log and user_account flags

-- 1. Create Staff Bulk Import Log Table
CREATE TABLE IF NOT EXISTS public.staff_bulk_import_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    admin_user_id UUID NOT NULL REFERENCES public.user_account(id) ON DELETE RESTRICT,
    file_name VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    total_rows INT NOT NULL,
    created_count INT NOT NULL,
    skipped_count INT NOT NULL,
    is_dry_run BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for organizational audit history and idempotency lookups
CREATE INDEX IF NOT EXISTS idx_import_log_org ON public.staff_bulk_import_log (organization_id);
CREATE INDEX IF NOT EXISTS idx_import_log_admin ON public.staff_bulk_import_log (admin_user_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_import_org_hash_live
    ON public.staff_bulk_import_log (organization_id, file_hash)
    WHERE is_dry_run = false;

-- 2. Scoped Grants (Standing Invariant 4)
REVOKE ALL ON TABLE public.staff_bulk_import_log FROM PUBLIC;
GRANT SELECT, INSERT ON public.staff_bulk_import_log TO authenticated;
GRANT ALL ON TABLE public.staff_bulk_import_log TO service_role;

-- 3. Row-Level Security
ALTER TABLE public.staff_bulk_import_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "import_log_admin_select"
    ON public.staff_bulk_import_log
    FOR SELECT
    TO authenticated
    USING (is_org_admin(organization_id));

CREATE POLICY "import_log_admin_insert"
    ON public.staff_bulk_import_log
    FOR INSERT
    TO authenticated
    WITH CHECK (is_org_admin(organization_id));
```

---

## 4. API Surface & Schemas

### 1. Department Creation Endpoint
- **Route:** `POST /v1/orgs/{org_id}/departments`
- **Auth:** `require_roles([StaffRole.ADMIN])` (Admin must belong to `{org_id}`).
- **Request Body:**
  ```json
  {
    "name": "Health & Sanitation",
    "code": "HEALTH",
    "is_active": true
  }
  ```
- **Response:** `201 Created` with `DepartmentResponse`.
- **Validation:** Uniqueness on `(organization_id, code)`. If code exists, returns `409 Conflict`.

### 2. Staff Bulk Import Endpoint
- **Route:** `POST /v1/admin/users/import`
- **Query Parameter:** `dry_run: bool = True` (Default is dry-run mode).
- **Rate Limit:** `RateLimiter(max_requests=5, window_seconds=60, prefix="admin_import")` via Upstash Redis.
- **Payload Constraints:**
  - Content-Type: `multipart/form-data` with `file: UploadFile`.
  - Max File Size: 2 MB (streaming chunk verification).
  - Max Rows: 500 rows (excluding header).
- **Required CSV Header:**
  `full_name,phone,email,role,department_code,zone_code,ward_number`
- **Role Scoping Matrix:**
  | Role | Required Scopes |
  |---|---|
  | `dispatcher` | None (organization-wide) |
  | `department_staff` | `department_code` |
  | `zonal_supervisor` | `zone_code` |
  | `field_worker` | `department_code`, `ward_number` |
  | `corporator` | `ward_number` |
  | `admin` | **REJECTED (HTTP 400 or skipped row)** |

- **Response Schema (`BulkImportResponse`):**
  ```json
  {
    "file_name": "field_staff_batch_1.csv",
    "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "dry_run": true,
    "total_rows": 3,
    "created_count": 2,
    "skipped_count": 1,
    "results": [
      {
        "row_number": 2,
        "full_name": "Ramesh Kumar",
        "phone": "+919876543210",
        "email": "ramesh@bbmp.gov.in",
        "role": "field_worker",
        "status": "would_create",
        "reason": null,
        "setup_link_dispatched": false
      },
      {
        "row_number": 3,
        "full_name": "Suresh Rao",
        "phone": "+919876543211",
        "email": null,
        "role": "admin",
        "status": "skipped",
        "reason": "Admin accounts cannot be provisioned via bulk import.",
        "setup_link_dispatched": false
      }
    ]
  }
  ```

---

## 5. Security & Defensive Hardening

### CSV Formula Injection Neutralization
Any string cell in CSV starting with `=`, `+`, `-`, `@`, `\t`, or `\r` is sanitized by prefixing with `'` (single quote) via `civicbrain.infra.security.sanitize_csv_cell` before database storage or reflection in response payloads.

### PII & Secret Scrubbing in Application Logs
- Endpoint logic explicitly forbids logging CSV raw contents, user contact details, setup tokens, or passwords.
- `civicbrain.infra.logging.PIIScrubbingFilter` is updated with `PASSWORD_TOKEN_PATTERN` to catch any leak attempt.

---

## 6. Verification Plan & Test Strategy

Dedicated test suite: [`tests/test_admin_bulk_import.py`](file:///e:/CivicBrain/tests/test_admin_bulk_import.py)
1. `test_create_department_endpoint`: Admin creates a department; non-admin receives 403; duplicate code returns 409.
2. `test_bulk_import_dry_run_default`: Uploads CSV without flags. Confirms `dry_run=True`, accounts are NOT created in DB, and diagnostic report returns `would_create`.
3. `test_bulk_import_admin_role_rejected`: Confirms any row with `role == 'admin'` is rejected.
4. `test_bulk_import_duplicate_phone_skipped`: Confirms duplicate phone in file or DB is skipped with explicit reason.
5. `test_bulk_import_idempotency_hash_rejection`: Uploads same file twice with `dry_run=False`. Second upload receives HTTP 409 Conflict.
6. `test_bulk_import_live_execution_and_audit_log`: Uploads valid 5-role CSV with `dry_run=False`. Confirms users created in DB and `staff_bulk_import_log` entry persisted.
7. `test_bulk_import_csv_formula_injection`: Confirms `=cmd|'/C calc'!A0` is sanitized to `'=cmd|'/C calc'!A0`.
8. `test_bulk_import_rate_limit`: Confirms > 5 uploads in 60s triggers HTTP 429.
