-- CivicBrain v14 — Phase 9: Karmi Sahayak Offline Sync & Conflict Adjudication Queue (§A15)
-- Migration 0010: Offline Sync Mutations, Revision Vectors & Supervisor Review Queue

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
