-- CivicBrain v14 — Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction (§A21, §A23)
-- Migration 0011: Category Baseline Service-Time Priors & Ward Report Card Snapshots

-- 1. Category Baseline Service-Time Priors (§A23)
CREATE TABLE IF NOT EXISTS public.category_service_time_prior (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    category_code VARCHAR(50) NOT NULL,
    base_resolution_hours DOUBLE PRECISION NOT NULL DEFAULT 48.0,
    p25_hours DOUBLE PRECISION NOT NULL DEFAULT 24.0,
    p50_hours DOUBLE PRECISION NOT NULL DEFAULT 48.0,
    p90_hours DOUBLE PRECISION NOT NULL DEFAULT 96.0,
    min_hours DOUBLE PRECISION NOT NULL DEFAULT 6.0,
    sample_size INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_cat_org_prior UNIQUE (organization_id, category_code),
    CONSTRAINT chk_positive_hours CHECK (
        base_resolution_hours > 0 
        AND p25_hours > 0 
        AND p50_hours >= p25_hours 
        AND p90_hours >= p50_hours
        AND min_hours > 0
    )
);

CREATE INDEX IF NOT EXISTS idx_cat_prior_org ON public.category_service_time_prior(organization_id);
CREATE INDEX IF NOT EXISTS idx_cat_prior_code ON public.category_service_time_prior(category_code);

-- 2. Ward Report Card Snapshot Table (§A21)
CREATE TABLE IF NOT EXISTS public.ward_report_card_snapshot (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL DEFAULT 'weekly', -- 'daily', 'weekly', 'monthly'
    total_reported INT NOT NULL DEFAULT 0,
    total_active INT NOT NULL DEFAULT 0,
    total_resolved INT NOT NULL DEFAULT 0,
    total_confirmed INT NOT NULL DEFAULT 0,
    total_appealed INT NOT NULL DEFAULT 0,
    mean_resolution_hours DOUBLE PRECISION,
    median_resolution_hours DOUBLE PRECISION,
    citizen_satisfaction_index DOUBLE PRECISION, -- confirmed / (confirmed + appealed)
    sla_compliance_rate DOUBLE PRECISION,       -- % completed within SLA
    equity_observed_gap DOUBLE PRECISION,       -- observed vs expected report gap from equity compensator
    department_breakdown JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ward_snapshot_period UNIQUE (ward_id, snapshot_date, period_type)
);

CREATE INDEX IF NOT EXISTS idx_wrc_org ON public.ward_report_card_snapshot(organization_id);
CREATE INDEX IF NOT EXISTS idx_wrc_ward ON public.ward_report_card_snapshot(ward_id);
CREATE INDEX IF NOT EXISTS idx_wrc_date ON public.ward_report_card_snapshot(snapshot_date);

-- 3. Row-Level Security (Standing Invariant 4)
ALTER TABLE public.category_service_time_prior ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ward_report_card_snapshot ENABLE ROW LEVEL SECURITY;

-- Service role bypass
DROP POLICY IF EXISTS service_role_priors_all ON public.category_service_time_prior;
CREATE POLICY service_role_priors_all ON public.category_service_time_prior
    FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS service_role_snapshots_all ON public.ward_report_card_snapshot;
CREATE POLICY service_role_snapshots_all ON public.ward_report_card_snapshot
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Public / Anonymous can read ward report card snapshots (Transparency Principle §A21)
DROP POLICY IF EXISTS ward_report_card_public_read ON public.ward_report_card_snapshot;
CREATE POLICY ward_report_card_public_read ON public.ward_report_card_snapshot
    FOR SELECT TO anon, authenticated
    USING (true);

-- Admins and staff can write/manage report cards
DROP POLICY IF EXISTS ward_report_card_staff_write ON public.ward_report_card_snapshot;
CREATE POLICY ward_report_card_staff_write ON public.ward_report_card_snapshot
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- Authenticated and anon can read category service-time priors
DROP POLICY IF EXISTS category_priors_read ON public.category_service_time_prior;
CREATE POLICY category_priors_read ON public.category_service_time_prior
    FOR SELECT TO anon, authenticated
    USING (true);

-- Admins can update/insert priors
DROP POLICY IF EXISTS category_priors_admin_write ON public.category_service_time_prior;
CREATE POLICY category_priors_admin_write ON public.category_service_time_prior
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- 4. Scoped Grants (Zero blanket GRANT ALL)
REVOKE ALL ON TABLE public.category_service_time_prior FROM PUBLIC;
REVOKE ALL ON TABLE public.ward_report_card_snapshot FROM PUBLIC;

GRANT SELECT ON TABLE public.category_service_time_prior TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.category_service_time_prior TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.category_service_time_prior TO service_role;

GRANT SELECT ON TABLE public.ward_report_card_snapshot TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.ward_report_card_snapshot TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ward_report_card_snapshot TO service_role;
