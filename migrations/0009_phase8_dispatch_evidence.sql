-- CivicBrain v14 — Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus (§A14, §A16)
-- Migration 0009: Work Orders, Evidence Gate Constraints & Resolution Proofs

-- 1. Create Work Order Status Enum
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

-- 2. Work Order Table with Conditional CHECK Constraint
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

-- 3. Extend Incident Table with Resolution Proofs, Geometries, Auto-Confirm Deadline, and CHECK Constraint
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

-- 4. Row-Level Security & Scoped Grants (Standing Invariant 4)
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
