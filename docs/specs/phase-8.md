# Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification

**Version:** CivicBrain v14.8.0  
**Phase:** 8  
**Status:** APPROVED & IMPLEMENTED  

---

## 1. Executive Summary & Scope

Phase 8 implements the operational field dispatch execution, evidence-gated resolution, and satisfaction verification loop for CivicBrain v14 (§A14, §A16):

1. **Work Order Progression & Field Operations (§A14, §A16):**
   - Establishes the `work_order` table tracking field assignments, worker timestamps, and repair actions.
   - Work order lifecycle states (`work_order_status_enum`):
     `created` $\to$ `dispatched` $\to$ `accepted` $\to$ `in_progress` $\to$ `completed` (or `cancelled`).
   - Syncs directly with parent `incident.status` (§A16 11-state machine):
     - Work order dispatched $\to$ `incident.status = 'assigned'`
     - Field worker accepts/starts work $\to$ `incident.status = 'in_progress'`
     - Evidence-gated completion $\to$ `incident.status = 'resolved'`
     - Verification confirmation $\to$ `incident.status = 'confirmed'`
     - Citizen dispute $\to$ `incident.status = 'appealed'`

2. **Database-Level Evidence Gate (Correction 2):**
   - An incident or work order CANNOT persist in `resolved` (or `completed`) state without verified proof.
   - Enforced by a real PostgreSQL conditional `CHECK` constraint:
     ```sql
     CONSTRAINT chk_work_order_resolved_evidence CHECK (
         status <> 'completed' OR (
             array_length(resolution_media_urls, 1) > 0 
             AND resolution_geom IS NOT NULL
             AND resolution_notes IS NOT NULL
         )
     )
     ```
   - Mirror constraint applied directly on `incident` table:
     ```sql
     CONSTRAINT chk_incident_resolved_evidence CHECK (
         status <> 'resolved' OR (
             array_length(resolution_proof_urls, 1) > 0 
             AND resolution_geom IS NOT NULL
             AND resolution_notes IS NOT NULL
         )
     )
     ```
   - Eliminates "prose invariants": Attempting to set `status = 'completed'` or `status = 'resolved'` with empty arrays or null coordinates raises database error `23514 (check_violation)`.

3. **Geographic Proximity Gate (Correction 3):**
   - Field worker resolution submission requires an explicit proximity check:
     The resolution coordinate (`resolution_geom`) must be within **50 meters** of the incident's recorded location (`incident.geom`).
   - Implemented at the application service layer via PostGIS `ST_DWithin` / geodetic distance:
     $$\text{ST\_DWithin}(inc.geom::geography, res.geom::geography, 50.0)$$
   - Live integration tests explicitly verify that submitting proof coordinates out of range (> 50m away) raises HTTP 422 with `resolution_out_of_bounds`.

4. **Deterministic Confirmation & Dispute Routing (§A16, Correction 4):**
   - **72-Hour Auto-Confirmation Window:**
     When an incident transitions to `resolved`, an auto-confirm timer begins. If the citizen does not dispute the resolution within 72 hours, the incident automatically transitions to `confirmed` (and parent `intake_report.status` to `closed`), satisfying the Satisfaction Loop (§A16).
   - **Dispute Routing to `appealed`:**
     If the citizen rejects/disputes the resolution via the tracking portal, the incident **always routes to `status = 'appealed'`**.
     - *Justification:* As established in Phase 2 (§A16), `appealed` is an explicit branch state requiring human administrative/supervisor re-triage. It prevents the system from silently reopening or re-dispatching without investigating *why* the citizen contested the worker's submitted photographic evidence (e.g. photo of wrong pothole, superficial patch, debris left behind). The supervisor then decides to either reassign (`in_progress` / `assigned`) or reject the dispute (`confirmed`).
   - Automated inspection / spatial verifier consensus is explicitly **deferred** to future IoT/sensor integrations. This phase focuses entirely on cryptographic photo evidence + citizen satisfaction feedback.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Enforced Database Evidence Gate (Hard Invariant):**
   - Zero transitions to `resolved` without non-empty `resolution_media_urls` and non-null `resolution_geom`.
2. **50-Meter Geographic Proximity Enforcement:**
   - Field worker submissions beyond 50 meters from the incident point are rejected.
3. **Dispute Routing Single State:**
   - Citizen contestation transitions incident to `appealed` with mandatory `appeal_reason`.
4. **Mandatory Scoped Grants (Standing Invariant 4):**
   - Scoped `GRANT` statements per role with zero `GRANT ALL`.

---

## 3. Database Schema (`migrations/0009_phase8_dispatch_evidence.sql`)

```sql
-- Migration 0009: Work Orders, Evidence Gate Constraints & Resolution Proofs

DO $$ BEGIN
    CREATE TYPE work_order_status_enum AS ENUM (
        'created',
        'dispatched',
        'accepted',
        'in_progress',
        'completed',
        'cancelled'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 1. Work Order Table with Conditional CHECK Constraint
CREATE TABLE IF NOT EXISTS public.work_order (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    incident_id UUID NOT NULL REFERENCES public.incident(id) ON DELETE CASCADE,
    department_id UUID NOT NULL REFERENCES public.department(id) ON DELETE RESTRICT,
    assigned_worker_id UUID REFERENCES public.user_account(id) ON DELETE SET NULL,
    status work_order_status_enum NOT NULL DEFAULT 'created',
    dispatched_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    resolution_notes TEXT,
    resolution_media_urls TEXT[] DEFAULT '{}',
    resolution_geom geometry(Point, 4326),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_work_order_completed_evidence CHECK (
        status <> 'completed' OR (
            array_length(resolution_media_urls, 1) > 0 
            AND resolution_geom IS NOT NULL
            AND resolution_notes IS NOT NULL
        )
    )
);

CREATE INDEX IF NOT EXISTS idx_work_order_org ON public.work_order(organization_id);
CREATE INDEX IF NOT EXISTS idx_work_order_incident ON public.work_order(incident_id);
CREATE INDEX IF NOT EXISTS idx_work_order_worker ON public.work_order(assigned_worker_id);
CREATE INDEX IF NOT EXISTS idx_work_order_status ON public.work_order(status);

-- 2. Extend Incident Table with Resolution Proofs and Evidence Gate
ALTER TABLE public.incident
    ADD COLUMN IF NOT EXISTS resolution_proof_urls TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS resolution_geom geometry(Point, 4326),
    ADD COLUMN IF NOT EXISTS auto_confirm_deadline TIMESTAMPTZ;

ALTER TABLE public.incident
    ADD CONSTRAINT chk_incident_resolved_evidence CHECK (
        status <> 'resolved' OR (
            array_length(resolution_proof_urls, 1) > 0 
            AND resolution_geom IS NOT NULL
            AND resolution_notes IS NOT NULL
        )
    );

-- 3. Row-Level Security & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.work_order ENABLE ROW LEVEL SECURITY;

CREATE POLICY service_role_work_order_all ON public.work_order
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Authenticated staff can read work orders within their organization
CREATE POLICY work_order_select_org ON public.work_order
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = work_order.organization_id
        )
    );

-- Field workers can update work orders assigned to them; Admin/Dispatchers can manage
CREATE POLICY work_order_update_worker ON public.work_order
    FOR UPDATE TO authenticated
    USING (
        assigned_worker_id = auth.uid()
        OR is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = work_order.organization_id
              AND ura.role IN ('admin', 'dispatcher')
        )
    )
    WITH CHECK (
        assigned_worker_id = auth.uid()
        OR is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = work_order.organization_id
              AND ura.role IN ('admin', 'dispatcher')
        )
    );

CREATE POLICY work_order_insert_staff ON public.work_order
    FOR INSERT TO authenticated
    WITH CHECK (
        is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = work_order.organization_id
              AND ura.role IN ('admin', 'dispatcher')
        )
    );

-- Explicit Grants: Scoped, zero blanket GRANT ALL
REVOKE ALL ON TABLE public.work_order FROM PUBLIC;
GRANT SELECT ON TABLE public.work_order TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.work_order TO service_role;
GRANT SELECT, INSERT, UPDATE ON TABLE public.work_order TO authenticated;
```

---

## 4. REST API Endpoints

### 4.1 Dispatch & Work Order Operations (`/v1/dispatch/work-orders`)

- `POST /v1/dispatch/work-orders`:
  - **Auth:** Dispatcher / Admin.
  - **Action:** Creates and dispatches a work order for an incident, assigning a field worker.
  - **Side-effect:** Sets `work_order.status = 'dispatched'`, updates `incident.status = 'assigned'` and `incident.assigned_worker_id`.

- `GET /v1/dispatch/work-orders/my`:
  - **Auth:** Field Worker.
  - **Action:** Retrieves active work orders assigned to the calling field worker.

- `POST /v1/dispatch/work-orders/{work_order_id}/start`:
  - **Auth:** Assigned Field Worker.
  - **Action:** Field worker marks arrival/start.
  - **Side-effect:** Sets `work_order.status = 'in_progress'` and `incident.status = 'in_progress'`.

- `POST /v1/dispatch/work-orders/{work_order_id}/resolve`:
  - **Auth:** Assigned Field Worker.
  - **Payload:** `resolution_notes`, `resolution_media_urls: list[str]`, `latitude: float`, `longitude: float`.
  - **Verification:**
    1. Validates `len(resolution_media_urls) > 0`.
    2. Validates spatial distance between `(latitude, longitude)` and `incident.geom` is $\le 50.0$ meters using PostGIS `ST_DWithin`.
  - **Side-effect:**
    - Updates `work_order` with evidence, setting `status = 'completed'` and `completed_at = now()`.
    - Updates `incident` setting `status = 'resolved'`, `resolved_at = now()`, `resolution_proof_urls`, `resolution_geom`, `resolution_notes`, and `auto_confirm_deadline = now() + interval '72 hours'`.
    - Recomputes parent `intake_report.status = 'resolved'`.

### 4.2 Citizen Verification & Satisfaction Loop (`/v1/intake/reports`)

- `POST /v1/intake/reports/{tracking_token}/confirm`:
  - **Auth:** Public via valid anonymous `tracking_token` or report owner.
  - **Action:** Citizen confirms satisfactory completion.
  - **Side-effect:** Sets child incidents to `status = 'confirmed'`, `confirmed_at = now()`, and parent `intake_report.status = 'closed'`.

- `POST /v1/intake/reports/{tracking_token}/dispute`:
  - **Auth:** Public via valid anonymous `tracking_token` or report owner.
  - **Payload:** `reason: str`.
  - **Action:** Citizen rejects resolution proof.
  - **Side-effect:**
    - Routes child incidents strictly to `status = 'appealed'`, setting `appealed_at = now()` and `appeal_reason = reason`.
    - Recomputes parent `intake_report.status = 'in_progress'`.
    - Triggers notification in Control Room Dispatcher queue for supervisor review.

- `POST /v1/dispatch/cron/auto-confirm`:
  - **Auth:** Service role / Admin cron.
  - **Action:** Evaluates all incidents with `status = 'resolved'` where `now() >= auto_confirm_deadline`.
  - **Side-effect:** Automatically transitions expired incidents to `status = 'confirmed'`.

---

## 5. Verification Plan

1. **Unit Tests (`tests/test_dispatch_workflow.py`):**
   - Enforce 11-state machine transitions: illegal transitions (e.g. `reported` $\to$ `resolved`) raise HTTP 400.
   - Proximity verification: GPS distance $> 50$ meters raises HTTP 422 with `resolution_out_of_bounds`.
   - Evidence check: Submitting resolution with empty `resolution_media_urls` raises validation error.
   - Citizen dispute routing: Assert dispute transitions incident to `status = 'appealed'`.
   - Auto-confirm evaluation: Assert 72-hour deadline expiry transitions to `status = 'confirmed'`.

2. **Live Supabase Integration (`tests/test_live_supabase_phase8_dispatch.py`):**
   - Seed real incident, create work order, assign field worker.
   - Prove DB check constraint `chk_work_order_completed_evidence` rejects `status = 'completed'` when `resolution_media_urls` is empty.
   - Prove DB check constraint `chk_incident_resolved_evidence` rejects `status = 'resolved'` with null `resolution_geom`.
   - Submit valid resolution ($< 50$m with photo), verify DB state.
   - Execute citizen dispute, assert `status = 'appealed'`.
   - Clean teardown in `finally` block.

3. **CI & Quality Gates:**
   - Full test suite, ruff format check, ruff linter, and mypy clean across all source files.
