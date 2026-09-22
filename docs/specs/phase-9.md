# Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification

**Version:** CivicBrain v14.9.0  
**Phase:** 9  
**Status:** APPROVED & IMPLEMENTED  

---

## 1. Executive Summary & Scope

Phase 9 establishes the offline synchronization engine, optimistic concurrency architecture, and supervisory conflict review queue for **Karmi Sahayak** (CivicBrain's Field Companion application, §A15). Ground workers operate in harsh urban environments—underground drainage culverts, remote informal settlements, basement utility rooms, and congested transit hubs—where continuous mobile connectivity cannot be guaranteed.

Phase 9 provides:
1. **Two-Way Delta Synchronization (§A15):**
   - Efficient delta pull: Workers receive only work orders and incidents created or updated since their last synchronization checkpoint (`since_cursor`).
   - Batched push: Queued local mutations (status transitions, photos, GPS timestamps, field notes) are flushed to the server when network reconnects.
2. **Deterministic Mutation Idempotency & Revision Vectors (§A15):**
   - Cryptographic `client_mutation_id` (UUID) guarantees that repeated flushes over unstable connections do not duplicate status changes or evidence entries.
   - Monotonic entity revision tracking (`version: int`) on `work_order` detects concurrent modifications and stale offline state.
3. **Preserved Evidence & Supervisory Adjudication Queue (Correction 1 & 2):**
   - When an offline worker submits a `resolve` mutation carrying valid evidence (passed proximity and non-empty photo checks), but the server work order was cancelled or reassigned by a dispatcher while the worker was offline:
     - The system **does not unilaterally drop the worker's evidence**.
     - The worker's submitted evidence (`resolution_media_urls`, `resolution_notes`, `resolution_geom`, `captured_at`) is **preserved in full**.
     - A reviewable record is created in the `dispatch_conflict_review` table, surfacing in the Command Deck / Control Room queue.
     - A supervisor or dispatcher reviews the conflict and adjudicates whether the worker's evidence stands (`accept_worker_evidence`) or the dispatcher's cancellation/reassignment stands (`uphold_dispatcher_action`).
4. **Append-Only Sync Mutation Logging (Correction 3):**
   - Database table `sync_mutation_log` records every client mutation, status (`applied`, `conflict`, `rejected`), server timestamp, and arbitration resolution.
   - RLS policies and table grants strictly enforce append-only `SELECT` and `INSERT` semantics.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Strict Idempotency (Standing Invariant):**
   - Every mutation submitted by a client device MUST include a unique `client_mutation_id`. Submitting the same `client_mutation_id` multiple times yields the cached outcome without re-executing state transitions.
2. **Offline Spatial & Evidence Preservation:**
   - Geolocation coordinates (`latitude`, `longitude`), capture timestamp (`captured_at`), and photos submitted by field workers are captured at the point of physical repair. Even when conflicting with dispatcher actions, valid evidence is never discarded.
3. **Supervisor-in-the-Loop Conflict Adjudication:**
   - Concurrent-dispatch conflicts (Cases 3 & 4) require human supervisor adjudication. The system remains neutral and records the full state for human decision-making.
4. **Append-Only Audit Trail (Standing Invariant 4):**
   - `sync_mutation_log` is strictly append-only. RLS policies and table grants are narrowed to `SELECT` and `INSERT` only for authenticated users; `UPDATE` and `DELETE` are blocked.

---

## 3. Database Schema (`migrations/0010_phase9_offline_sync.sql`)

```sql
-- Migration 0010: Karmi Sahayak Offline Sync & Conflict Adjudication Queue (§A15)

-- 1. Enums for Sync & Conflict Adjudication
DO $$ BEGIN
    CREATE TYPE sync_mutation_status_enum AS ENUM (
        'applied',
        'conflict',
        'rejected'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE conflict_review_status_enum AS ENUM (
        'pending',
        'accepted',
        'dismissed'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Add Monotonic Version Column to Work Order
ALTER TABLE public.work_order
    ADD COLUMN IF NOT EXISTS version INT NOT NULL DEFAULT 1;

-- 3. Append-Only Sync Mutation Log Table
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

-- 4. Supervisor Conflict Review Queue (Command Deck / Control Room)
CREATE TABLE IF NOT EXISTS public.dispatch_conflict_review (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    work_order_id UUID NOT NULL REFERENCES public.work_order(id) ON DELETE CASCADE,
    incident_id UUID NOT NULL REFERENCES public.incident(id) ON DELETE CASCADE,
    worker_id UUID NOT NULL REFERENCES public.user_account(id) ON DELETE CASCADE,
    client_mutation_id UUID NOT NULL,
    conflict_type VARCHAR(50) NOT NULL, -- 'cancelled_by_dispatcher' or 'reassigned_by_dispatcher'
    submitted_notes TEXT NOT NULL,
    submitted_media_urls TEXT[] NOT NULL DEFAULT '{}',
    submitted_geom geometry(Point, 4326) NOT NULL,
    captured_at TIMESTAMPTZ NOT NULL,
    status conflict_review_status_enum NOT NULL DEFAULT 'pending',
    reviewed_by UUID REFERENCES public.user_account(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMPTZ,
    review_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_conflict_review_org ON public.dispatch_conflict_review(organization_id);
CREATE INDEX IF NOT EXISTS idx_conflict_review_status ON public.dispatch_conflict_review(status);
CREATE INDEX IF NOT EXISTS idx_conflict_review_wo ON public.dispatch_conflict_review(work_order_id);

-- 5. Row-Level Security & Scoped Grants (Standing Invariant 4 & Correction 3)
ALTER TABLE public.sync_mutation_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dispatch_conflict_review ENABLE ROW LEVEL SECURITY;

-- Service role bypass
CREATE POLICY service_role_sync_log_all ON public.sync_mutation_log
    FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY service_role_conflict_review_all ON public.dispatch_conflict_review
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- sync_mutation_log: Strictly SELECT and INSERT (Append-Only)
CREATE POLICY sync_log_select_policy ON public.sync_mutation_log
    FOR SELECT TO authenticated
    USING (
        worker_id = auth.uid()
        OR is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = sync_mutation_log.organization_id
              AND ura.role IN ('admin', 'dispatcher', 'zonal_supervisor')
        )
    );

CREATE POLICY sync_log_insert_policy ON public.sync_mutation_log
    FOR INSERT TO authenticated
    WITH CHECK (
        worker_id = auth.uid()
        OR is_org_admin(organization_id)
    );

-- dispatch_conflict_review: SELECT for staff; UPDATE for supervisors/admins
CREATE POLICY conflict_review_select_policy ON public.dispatch_conflict_review
    FOR SELECT TO authenticated
    USING (
        worker_id = auth.uid()
        OR is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = dispatch_conflict_review.organization_id
              AND ura.role IN ('admin', 'dispatcher', 'zonal_supervisor')
        )
    );

CREATE POLICY conflict_review_update_policy ON public.dispatch_conflict_review
    FOR UPDATE TO authenticated
    USING (
        is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = dispatch_conflict_review.organization_id
              AND ura.role IN ('admin', 'dispatcher', 'zonal_supervisor')
        )
    )
    WITH CHECK (
        is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = dispatch_conflict_review.organization_id
              AND ura.role IN ('admin', 'dispatcher', 'zonal_supervisor')
        )
    );

-- Scoped Grants (Standing Invariant 4)
REVOKE ALL ON TABLE public.sync_mutation_log FROM PUBLIC;
REVOKE ALL ON TABLE public.dispatch_conflict_review FROM PUBLIC;

GRANT SELECT ON TABLE public.sync_mutation_log TO anon, authenticated;
GRANT SELECT, INSERT ON TABLE public.sync_mutation_log TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.sync_mutation_log TO service_role;

GRANT SELECT ON TABLE public.dispatch_conflict_review TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.dispatch_conflict_review TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.dispatch_conflict_review TO service_role;
```

---

## 4. Conflict Arbitration Matrix (§A15)

When a field worker pushes offline mutations:

$$\text{Mutation} = (\text{client\_mutation\_id}, \text{entity\_id}, \text{action}, \text{base\_version}, \text{payload}, \text{captured\_at})$$

The engine arbitrates as follows:

| Case | Scenario | Arbitration Outcome | Resulting State |
| :--- | :--- | :--- | :--- |
| **1. Idempotent Retry** | `client_mutation_id` already recorded in `sync_mutation_log` | Return previously recorded outcome | No re-execution |
| **2. Clean Progression** | Server `work_order.version == base_version` and status matches prerequisite | Apply transition, increment server `version` | `status = 'applied'` |
| **3. Dispatcher Reassigned (with valid evidence)** | Worker resolved offline, but dispatcher reassigned `assigned_worker_id != caller` while offline | **Preserve evidence in full.** Create `dispatch_conflict_review` row (`status = 'pending'`). Mark mutation as `conflict` (`reason = 'reassigned_by_dispatcher'`). | Reviewable row in Command Deck queue; pending supervisor review |
| **4. Dispatcher Cancelled (with valid evidence)** | Worker resolved offline, but dispatcher cancelled work order (`status == 'cancelled'`) while offline | **Preserve evidence in full.** Create `dispatch_conflict_review` row (`status = 'pending'`). Mark mutation as `conflict` (`reason = 'cancelled_by_dispatcher'`). | Reviewable row in Command Deck queue; pending supervisor review |
| **5. Already Completed Race** | Action is `resolve`, but work order `status == 'completed'` by another worker (peer race) | Reject second completion; peer evidence already verified | `status = 'conflict'`, `reason = 'conflict_already_completed'` |
| **6. Proximity Violation** | Action is `resolve`, but GPS proof $> 50$m | Reject with validation error | `status = 'rejected'`, `reason = 'resolution_out_of_bounds'` |
| **7. Missing Photos / Notes** | Action is `resolve`, but `resolution_media_urls` or notes empty | Reject with validation error | `status = 'rejected'`, `reason = 'missing_evidence'` |

---

## 5. REST API Endpoints

### 5.1 Field Worker Two-Way Delta Sync (`/v1/field/sync`)

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
    - `mutation_results: list[MutationResult]` (`client_mutation_id`, `status: applied|conflict|rejected`, `conflict_reason`, `conflict_review_id: UUID | None`).
    - `server_changes: list[WorkOrderResponse]` containing work orders assigned to the worker updated since `since_cursor`.
    - `new_cursor: datetime` (current server timestamp).

- `GET /v1/field/sync/conflicts`:
  - **Auth:** Authenticated Field Worker.
  - **Action:** Lists unresolved sync conflicts for the calling worker's device to assist in client-side badge indicators.

### 5.2 Supervisor Adjudication Queue (`/v1/dispatch/conflicts`)

- `GET /v1/dispatch/conflicts`:
  - **Auth:** Dispatcher, Zonal Supervisor, Admin (`StaffRole.DISPATCHER`, `StaffRole.ZONAL_SUPERVISOR`, `StaffRole.ADMIN`).
  - **Query Parameters:** `organization_id: UUID`, `status: conflict_review_status_enum = 'pending'`, `page: int = 1`, `page_size: int = 50`.
  - **Response:** List of reviewable concurrent dispatch conflicts with full preserved evidence:
    ```json
    [
      {
        "id": "5fa23bc0-3490-4a81-9b16-527e023be701",
        "organization_id": "8a329d44-2450-4ba1-b991-9e5c412ae801",
        "work_order_id": "93699c22-b9b5-41e9-91ee-bbf4f7fafe6b",
        "incident_id": "e0b9c331-5081-4209-a1b7-7ff7635c0211",
        "worker_id": "7b218cd0-6210-4821-bc10-189f315ab321",
        "conflict_type": "cancelled_by_dispatcher",
        "submitted_notes": "Repaired road crater with 40mm aggregate and emulsion",
        "submitted_media_urls": ["https://storage.civicbrain.org/crater_fixed.jpg"],
        "submitted_coordinates": {"latitude": 12.9501, "longitude": 77.5501},
        "captured_at": "2026-09-20T14:45:00Z",
        "status": "pending",
        "created_at": "2026-09-20T15:00:00Z"
      }
    ]
    ```

- `POST /v1/dispatch/conflicts/{conflict_id}/adjudicate`:
  - **Auth:** Dispatcher, Zonal Supervisor, Admin.
  - **Request Body (`ConflictAdjudicationRequest`):**
    ```json
    {
      "decision": "accept_worker_evidence",
      "notes": "Verified field photos: work was indeed performed prior to cancellation."
    }
    ```
    *(Options: `"accept_worker_evidence"` or `"uphold_dispatcher_action"`)*
  - **Execution & Side-Effects:**
    - If `accept_worker_evidence`:
      - The worker's preserved evidence stands: `work_order.status = 'completed'`, `completed_at = captured_at`, resolution notes, media URLs, and geom updated.
      - Incident transitions to `status = 'resolved'`, setting `resolved_at = captured_at`, resolution proof URLs, geom, and `auto_confirm_deadline = now() + 72 hours`.
      - Parent intake report status recomputed.
      - `dispatch_conflict_review.status = 'accepted'`, `reviewed_by = claims.user_id`, `reviewed_at = now()`.
    - If `uphold_dispatcher_action`:
      - The dispatcher's action stands (work order remains cancelled or reassigned).
      - `dispatch_conflict_review.status = 'dismissed'`, `reviewed_by = claims.user_id`, `reviewed_at = now()`, `review_notes = notes`.
  - **Response (`ConflictAdjudicationResponse`):** Updated conflict review record with final resolution status.

---

## 6. Verification Plan

1. **Unit Tests (`tests/test_offline_sync.py`):**
   - Verify idempotent deduplication: sending identical mutation batch twice returns identical results without duplicate DB operations.
   - Verify clean sequential mutation application: `start` followed by `resolve` in a single batch executes correctly and increments version.
   - Verify Cases 3 & 4: worker resolving a cancelled or reassigned work order with valid evidence preserves evidence and generates a `dispatch_conflict_review` record with `status = 'pending'`.
   - Verify Case 5: peer race between two workers completing the same work order rejects the second with `conflict_already_completed` without creating a supervisor conflict.
   - Verify supervisor adjudication endpoint:
     - `accept_worker_evidence` sets work order to `completed` and incident to `resolved`.
     - `uphold_dispatcher_action` dismisses conflict and maintains dispatcher state.
   - Verify delta sync cursor: `since_cursor` returns only items modified after timestamp.

2. **Live Supabase Integration (`tests/test_live_supabase_phase9_sync.py`):**
   - Seed real organization, ward, department, field worker, incident, and work orders on live Supabase.
   - Test append-only constraint on `sync_mutation_log`: authenticated user can INSERT and SELECT, but UPDATE/DELETE are rejected by RLS/grants.
   - Test full conflict generation and adjudication flow with real seeded DB records.
   - Clean teardown in `finally` block.

3. **CI & Static Quality Gates:**
   - `ruff check`, `ruff format --check`, `mypy civicbrain` clean across all modules.
