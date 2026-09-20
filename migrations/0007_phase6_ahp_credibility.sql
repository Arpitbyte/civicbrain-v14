-- CivicBrain v14 — Phase 6: AHP Prioritization & Bühlmann Equity Engine (§A12, §A13)
-- Migration 0007: AHP 5-Criteria Config, Ward Equity Credibility, Incident Priority & Confidence Gating

-- 1. AHP Matrix Configuration (5 Dimensions: Severity, Risk, Exposure, Criticality, Urgency)
CREATE TABLE IF NOT EXISTS public.ahp_matrix_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    matrix JSONB NOT NULL,            -- 5x5 pairwise comparison matrix
    weights JSONB NOT NULL,           -- {"severity": w_s, "risk": w_r, "exposure": w_e, "criticality": w_c, "urgency": w_u}
    lambda_max DOUBLE PRECISION NOT NULL,
    consistency_index DOUBLE PRECISION NOT NULL,
    consistency_ratio DOUBLE PRECISION NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ahp_org_active UNIQUE (organization_id, is_active),
    CONSTRAINT chk_ahp_cr CHECK (consistency_ratio < 0.10)
);

CREATE INDEX IF NOT EXISTS idx_ahp_org_active ON public.ahp_matrix_config(organization_id, is_active);

-- 2. Ward Equity Credibility Table (Bühlmann Expected vs. Observed Rates)
CREATE TABLE IF NOT EXISTS public.ward_equity_credibility (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    verified_incident_count INTEGER NOT NULL DEFAULT 0,
    historical_incident_rate DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    credibility_factor DOUBLE PRECISION NOT NULL DEFAULT 0.0,     -- Z_i = n_i / (n_i + K)
    expected_issue_rate DOUBLE PRECISION NOT NULL DEFAULT 0.0,    -- \hat{\mu}_i = Z_i * X_bar + (1 - Z_i) * \mu_0
    observed_issue_rate DOUBLE PRECISION NOT NULL DEFAULT 0.0,    -- O_i
    equity_gap DOUBLE PRECISION NOT NULL DEFAULT 0.0,             -- max(0, expected - observed)
    equity_boost DOUBLE PRECISION NOT NULL DEFAULT 0.0,           -- \beta_i added to priority
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ward_equity_org_ward UNIQUE (organization_id, ward_id)
);

CREATE INDEX IF NOT EXISTS idx_ward_equity_org_ward ON public.ward_equity_credibility(organization_id, ward_id);

-- Optional SLA / Resolution stats retained for operational telemetry & Phase 10 ETA
CREATE TABLE IF NOT EXISTS public.ward_resolution_stat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    category_code VARCHAR(50) NOT NULL,
    resolved_count INTEGER NOT NULL DEFAULT 0,
    mean_resolution_hours DOUBLE PRECISION NOT NULL DEFAULT 48.0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ward_res_stat UNIQUE (ward_id, category_code)
);

CREATE INDEX IF NOT EXISTS idx_ward_res_stat_ward_cat ON public.ward_resolution_stat(ward_id, category_code);

-- 3. Extend Incident Table with 5 Sub-Scores, Confidence, Equity Boost, and Human Review Gating
ALTER TABLE public.incident
    ADD COLUMN IF NOT EXISTS subscore_severity DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_risk DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_exposure DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_criticality DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_urgency DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS raw_priority_score DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS equity_boost DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS priority_score DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS confidence_score DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS requires_human_review BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS review_reason TEXT DEFAULT NULL;

-- 4. Check Constraints on Sub-scores and Priorities
ALTER TABLE public.incident
    ADD CONSTRAINT chk_subscore_severity CHECK (subscore_severity >= 0.0 AND subscore_severity <= 1.0),
    ADD CONSTRAINT chk_subscore_risk CHECK (subscore_risk >= 0.0 AND subscore_risk <= 1.0),
    ADD CONSTRAINT chk_subscore_exposure CHECK (subscore_exposure >= 0.0 AND subscore_exposure <= 1.0),
    ADD CONSTRAINT chk_subscore_criticality CHECK (subscore_criticality >= 0.0 AND subscore_criticality <= 1.0),
    ADD CONSTRAINT chk_subscore_urgency CHECK (subscore_urgency >= 0.0 AND subscore_urgency <= 1.0),
    ADD CONSTRAINT chk_priority_score CHECK (priority_score >= 0.0 AND priority_score <= 100.0),
    ADD CONSTRAINT chk_confidence_score CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0);

-- 5. Row-Level Security (RLS) & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.ahp_matrix_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ward_equity_credibility ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ward_resolution_stat ENABLE ROW LEVEL SECURITY;

-- 5.1 Service Role Policies
CREATE POLICY service_role_ahp_config_all ON public.ahp_matrix_config
    FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY service_role_ward_equity_all ON public.ward_equity_credibility
    FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY service_role_ward_res_all ON public.ward_resolution_stat
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- 5.2 Authenticated Staff Policies (Scoped by is_org_admin or organization membership)
CREATE POLICY ahp_config_select_org ON public.ahp_matrix_config
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = ahp_matrix_config.organization_id
        )
    );

CREATE POLICY ahp_config_admin_manage ON public.ahp_matrix_config
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

CREATE POLICY ward_equity_select_org ON public.ward_equity_credibility
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = ward_equity_credibility.organization_id
        )
    );

CREATE POLICY ward_equity_admin_manage ON public.ward_equity_credibility
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

CREATE POLICY ward_res_select_org ON public.ward_resolution_stat
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = ward_resolution_stat.organization_id
        )
    );

CREATE POLICY ward_res_admin_manage ON public.ward_resolution_stat
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- 5.3 Explicit Scoped Grants (Zero blanket GRANT ALL)
REVOKE ALL ON TABLE public.ahp_matrix_config FROM PUBLIC;
GRANT SELECT ON TABLE public.ahp_matrix_config TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ahp_matrix_config TO service_role;
GRANT INSERT, UPDATE ON TABLE public.ahp_matrix_config TO authenticated;

REVOKE ALL ON TABLE public.ward_equity_credibility FROM PUBLIC;
GRANT SELECT ON TABLE public.ward_equity_credibility TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ward_equity_credibility TO service_role;
GRANT INSERT, UPDATE ON TABLE public.ward_equity_credibility TO authenticated;

REVOKE ALL ON TABLE public.ward_resolution_stat FROM PUBLIC;
GRANT SELECT ON TABLE public.ward_resolution_stat TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ward_resolution_stat TO service_role;
GRANT INSERT, UPDATE ON TABLE public.ward_resolution_stat TO authenticated;
