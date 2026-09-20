# Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Implementation Log

**Date:** 2026-09-21  
**Status:** COMPLETED  
**Version:** CivicBrain v14.8.0  

---

## 1. What Was Built

- **Work Order Progression & Lifecycle Sync (§A14, §A16):**
  - Implemented `work_order` table tracking field operations across states: `created`, `dispatched`, `accepted`, `in_progress`, `completed`, and `cancelled`.
  - Full synchronization with parent incident 11-state machine:
    - Work order dispatched $\to$ `incident.status = 'assigned'`
    - Work order started $\to$ `incident.status = 'in_progress'`
    - Evidence-gated resolution $\to$ `incident.status = 'resolved'`
    - Citizen satisfaction confirmation $\to$ `incident.status = 'confirmed'` (and `intake_report.status = 'closed'`)
    - Citizen contestation/dispute $\to$ `incident.status = 'appealed'` (and `intake_report.status = 'in_progress'`)
    - 72-hour automated confirmation cron $\to$ `incident.status = 'confirmed'`

- **Database-Level Evidence Gate Constraints (`migrations/0009_phase8_dispatch_evidence.sql`):**
  - Real conditional `CHECK` constraint on `work_order`:
    ```sql
    CONSTRAINT chk_work_order_completed_evidence CHECK (
        status <> 'completed' OR (
            array_length(resolution_media_urls, 1) > 0 
            AND resolution_geom IS NOT NULL
            AND resolution_notes IS NOT NULL
        )
    )
    ```
  - Real conditional `CHECK` constraint on `incident`:
    ```sql
    CONSTRAINT chk_incident_resolved_evidence CHECK (
        status <> 'resolved' OR (
            array_length(resolution_proof_urls, 1) > 0 
            AND resolution_geom IS NOT NULL
            AND resolution_notes IS NOT NULL
        )
    )
    ```
  - Eliminates prose invariants: Any attempt to transition to `completed` or `resolved` without photo proof, resolution notes, and coordinates raises PostgreSQL error `23514 (check_violation)`.

- **50-Meter Geographic Proximity Gate:**
  - Implemented PostGIS geodetic proximity check in `civicbrain.domain.dispatch.services.resolve_work_order`:
    `ST_DWithin(geom::geography, ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography, 50.0)`
  - Rejects submissions outside 50 meters with HTTP 422 `resolution_out_of_bounds`.

- **Satisfaction Loop & Auto-Confirm Cron Workflow:**
  - Added citizen satisfaction endpoints in `civicbrain/api/v1/intake.py`:
    - `POST /v1/intake/reports/{tracking_token}/confirm`
    - `POST /v1/intake/reports/{tracking_token}/dispute`
  - Added dispatch endpoints in `civicbrain/api/v1/dispatch.py`:
    - `POST /v1/dispatch/work-orders`
    - `GET /v1/dispatch/work-orders/my`
    - `POST /v1/dispatch/work-orders/{id}/start`
    - `POST /v1/dispatch/work-orders/{id}/resolve`
    - `POST /v1/dispatch/cron/auto-confirm`
  - Created `.github/workflows/auto_confirm_cron.yml` with hourly `on: schedule` trigger invoking `POST /v1/dispatch/cron/auto-confirm` via Bearer token / `X-Cron-Secret`.

---

## 2. Verification & Test Evidence

1. **Unit & Integration Suite (`tests/test_dispatch_workflow.py`):**
   - Unauthorized access blocked (401).
   - Non-admin/non-dispatcher creation forbidden (403).
   - Empty resolution photos or whitespace notes rejected (422).
   - Out-of-bounds resolution coordinate (> 50m) rejected with HTTP 422 `resolution_out_of_bounds`.
   - Unauthorized worker attempting to resolve or start another worker's order rejected (403).
   - Citizen confirm and dispute validation verified.
   - Cron secret verification verified.

2. **Live Supabase Integration (`tests/test_live_supabase_phase8_dispatch.py`):**
   - Seeded real organization, zone, ward, department, incident, and work order on live Supabase (`isqepbxkzxfpvfdkcntw`).
   - Proved database check constraint `chk_work_order_completed_evidence` rejects incomplete completion.
   - Proved database check constraint `chk_incident_resolved_evidence` rejects incomplete resolution.
   - Verified valid resolution with photographic proof and geodetic coordinates.
   - Verified citizen dispute transition to `appealed` with reason.
   - Clean teardown in `finally` block.

3. **Static Quality Gates & Full Suite:**
   - 75 tests passing across entire test suite.
   - `ruff check` and `ruff format --check` clean with 0 errors.
   - `mypy civicbrain` clean with 0 errors across 57 source files.
