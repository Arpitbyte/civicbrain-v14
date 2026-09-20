# Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification

**Version:** CivicBrain v14.9.0  
**Phase:** 9  
**Status:** SPECIFICATION PENDING REVIEW  

---

## 1. Executive Summary & Scope

Phase 9 establishes the offline synchronization engine and optimistic concurrency architecture for **Karmi Sahayak** (CivicBrain's Field Companion application, §A15). Ground workers operate in harsh urban environments—underground drainage culverts, remote informal settlements, basement utility rooms, and congested transit hubs—where continuous mobile connectivity cannot be guaranteed.

Phase 9 provides:
1. **Two-Way Delta Synchronization (§A15):**
   - Efficient delta pull: Workers receive only work orders and incidents created or updated since their last synchronization checkpoint (`since_cursor`).
   - Batched push: Queued local mutations (status transitions, photos, GPS timestamps, field notes) are flushed to the server when network reconnects.
2. **Deterministic Mutation Idempotency & Revision Vectors (§A15):**
   - Cryptographic `client_mutation_id` (UUID) guarantees that repeated flushes over unstable connections do not duplicate status changes or evidence entries.
   - Monotonic entity revision tracking (`version: int`) on `work_order` detects concurrent modifications and stale offline state.
3. **Deterministic Conflict Arbitration Matrix (§A15):**
   - **Dispatcher Precedence:** Administrative cancellation or reassignment by the central Control Room takes precedence over offline field worker state updates.
   - **First-Valid-Evidence Wins:** If concurrent completion claims occur, the first verified proof satisfying proximity and evidence gates persists; subsequent attempts are logged with `conflict_already_completed`.
   - **Safe Offline Progression:** Offline transitions from `dispatched` $\to$ `in_progress` are accepted provided the assignment was not revoked.
4. **Auditability & Sync Logging:**
   - Database table `sync_mutation_log` records every client mutation, status (`applied`, `conflict`, `rejected`), server timestamp, and arbitration resolution.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Strict Idempotency (Standing Invariant):**
   - Every mutation submitted by a client device MUST include a unique `client_mutation_id`. Submitting the same `client_mutation_id` multiple times yields the cached outcome without re-executing state transitions.
2. **Offline Spatial Integrity:**
   - Geolocation coordinates (`latitude`, `longitude`) and capture timestamp (`captured_at`) are captured at the point of physical repair and signed locally by the Karmi Sahayak client. The server verifies the 50-meter proximity gate against the incident's coordinate.
3. **Explicit Conflict Transparency:**
   - Conflicts are NEVER silently dropped. Every conflicting mutation receives an explicit rejection status code and diagnostic reason in the sync response.
4. **Scoped Role-Based Access & Grants (Standing Invariant 4):**
   - Field workers can only pull and mutate work orders assigned to them or within their authorized department/ward.
   - Scoped PostgreSQL table grants with zero `GRANT ALL`.

---

## 3. Database Schema (`migrations/0010_phase9_offline_sync.sql`)

```sql
-- Migration 0010: Karmi Sahayak Offline Sync & Mutation Logging (§A15)

-- 1. Sync Mutation Status Enum
DO $$ BEGIN
    CREATE TYPE sync_mutation_status_enum AS ENUM (
        'applied',
        'conflict',
        'rejected'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Add Monotonic Version Column to Work Order
ALTER TABLE public.work_order
    ADD COLUMN IF NOT EXISTS version INT NOT NULL DEFAULT 1;

-- 3. Sync Mutation Log Table
CREATE TABLE IF NOT EXISTS public.sync_mutation_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_mutation_id UUID NOT NULL,
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    worker_id UUID NOT NULL REFERENCES public.user_account(id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL, -- e.g. 'work_order'
    entity_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,      -- 'start', 'resolve', 'update_notes'
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    status sync_mutation_status_enum NOT NULL,
    conflict_reason TEXT,
    server_version INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_worker_mutation_id UNIQUE (worker_id, client_mutation_id)
);

CREATE INDEX IF NOT EXISTS idx_sync_log_worker ON public.sync_mutation_log(worker_id);
CREATE INDEX IF NOT EXISTS idx_sync_log_entity ON public.sync_mutation_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_sync_log_created ON public.sync_mutation_log(created_at);

-- 4. Row-Level Security & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.sync_mutation_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY service_role_sync_log_all ON public.sync_mutation_log
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Field workers can view and insert their own sync mutation logs
CREATE POLICY sync_log_worker_access ON public.sync_mutation_log
    FOR ALL TO authenticated
    USING (
        worker_id = auth.uid()
        OR is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = sync_mutation_log.organization_id
              AND ura.role IN ('admin', 'dispatcher')
        )
    )
    WITH CHECK (
        worker_id = auth.uid()
        OR is_org_admin(organization_id)
    );

-- Scoped table grants
REVOKE ALL ON TABLE public.sync_mutation_log FROM PUBLIC;
GRANT SELECT ON TABLE public.sync_mutation_log TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.sync_mutation_log TO service_role;
GRANT SELECT, INSERT ON TABLE public.sync_mutation_log TO authenticated;
```

---

## 4. Conflict Arbitration Logic (§A15)

When a client pushes a mutation queue:

$$\text{Mutation} = (\text{client\_mutation\_id}, \text{entity\_id}, \text{action}, \text{base\_version}, \text{payload}, \text{captured\_at})$$

The engine arbitrates as follows:

| Case | Scenario | Arbitration Outcome | Resulting State |
| :--- | :--- | :--- | :--- |
| **1. Idempotent Retry** | `client_mutation_id` already exists in `sync_mutation_log` | Return previously logged result | No re-execution |
| **2. Clean Progression** | Server `work_order.version == base_version` and status matches prerequisite | Apply transition, increment server `version` | `status = 'applied'` |
| **3. Dispatcher Reassigned** | Server reassigned worker (`assigned_worker_id != caller`) | Reject mutation | `status = 'conflict'`, `reason = 'reassigned_by_dispatcher'` |
| **4. Dispatcher Cancelled** | Server work order `status == 'cancelled'` | Reject mutation | `status = 'conflict'`, `reason = 'cancelled_by_dispatcher'` |
| **5. Already Completed** | Action is `resolve`, but server `status == 'completed'` | Reject second completion | `status = 'conflict'`, `reason = 'conflict_already_completed'` |
| **6. Proximity Violation** | Action is `resolve`, but GPS proof $> 50$m | Reject with validation error | `status = 'rejected'`, `reason = 'resolution_out_of_bounds'` |
| **7. Missing Photos** | Action is `resolve`, but `resolution_media_urls` empty | Reject with validation error | `status = 'rejected'`, `reason = 'missing_evidence'` |

---

## 5. REST API Endpoints

### 5.1 Two-Way Delta Sync (`/v1/field/sync`)

- `POST /v1/field/sync`:
  - **Auth:** Authenticated Field Worker (`StaffRole.FIELD_WORKER` or Admin/Dispatcher).
  - **Request Body (`FieldSyncPushRequest`):**
    ```json
    {
      "since_cursor": "2026-09-20T12:00:00Z",
      "mutations": [
        {
          "client_mutation_id": "c1f7a240-3490-4a81-9b16-527e023be699",
          "entity_type": "work_order",
          "entity_id": "93699c22-b9b5-41e9-91ee-bbf4f7fafe6b",
          "action": "start",
          "base_version": 1,
          "captured_at": "2026-09-20T14:15:00Z",
          "payload": {}
        },
        {
          "client_mutation_id": "b3e8c110-2180-4991-8c12-421e021aa711",
          "entity_type": "work_order",
          "entity_id": "93699c22-b9b5-41e9-91ee-bbf4f7fafe6b",
          "action": "resolve",
          "base_version": 2,
          "captured_at": "2026-09-20T14:45:00Z",
          "payload": {
            "resolution_notes": "Patched pothole with cold asphalt",
            "resolution_media_urls": ["https://storage.civicbrain.org/p801.jpg"],
            "latitude": 12.9500,
            "longitude": 77.5500
          }
        }
      ]
    }
    ```
  - **Response (`FieldSyncResponse`):**
    - `mutation_results: list[MutationResult]` indicating `applied`, `conflict`, or `rejected` per `client_mutation_id`.
    - `server_changes: list[WorkOrderResponse]` containing all work orders assigned to the worker updated since `since_cursor`.
    - `new_cursor: datetime` (current server timestamp).

### 5.2 Field State & Conflict Diagnostics

- `GET /v1/field/sync/conflicts`:
  - **Auth:** Authenticated Field Worker.
  - **Action:** Lists past unresolved sync conflicts for the worker's device to assist in offline triage and UI badge notifications.

---

## 6. Verification Plan

1. **Unit Tests (`tests/test_offline_sync.py`):**
   - Verify idempotent deduplication: sending identical mutation batch twice returns identical results without duplicate DB operations.
   - Verify clean sequential mutation application: `start` followed by `resolve` in a single batch executes correctly and increments version.
   - Verify dispatcher override: worker attempting to `resolve` a work order cancelled by a dispatcher receives `conflict` with reason `cancelled_by_dispatcher`.
   - Verify stale version conflict: mutating against `base_version < server_version` produces conflict when actions are incompatible.
   - Verify delta sync cursor: `since_cursor` returns only items modified after timestamp.

2. **Live Supabase Integration (`tests/test_live_supabase_phase9_sync.py`):**
   - Seed real organization, ward, department, field worker, incident, and work order on live Supabase.
   - Prove `sync_mutation_log` unique constraint `uq_worker_mutation_id` blocks duplicate insertions.
   - Execute live 2-way delta sync push and pull.
   - Clean teardown in `finally` block.

3. **CI & Static Quality Gates:**
   - `ruff check`, `ruff format --check`, `mypy civicbrain` clean across all modules.
