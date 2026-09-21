-- CivicBrain v14 — Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant (§A21, §A23)
-- Migration 0012: Public Jan Sunwai Ledger Table & Nagar Pragati Snapshots

-- 1. Public Jan Sunwai Ledger Table (§A23)
CREATE TABLE IF NOT EXISTS public.jan_sunwai_ledger_entry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    incident_id UUID NOT NULL REFERENCES public.incident(id) ON DELETE CASCADE,
    sequence_num INT NOT NULL DEFAULT 0,       -- Monotonic checkpoint index per incident (0, 1, 2, ...)
    public_tracking_code VARCHAR(32) NOT NULL, -- Pseudonymous identifier
    category_code VARCHAR(50) NOT NULL,
    department_id UUID NOT NULL REFERENCES public.department(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    
    -- Differentially Private Perturbed Fields (Generated once at seq 0, reused on subsequent seq)
    dp_geom geometry(Point, 4326) NOT NULL,    -- 2D Laplace perturbed coordinates
    dp_timestamp TIMESTAMPTZ NOT NULL,         -- 1D Laplace jittered timestamp
    
    -- Public Status Telemetry
    lifecycle_status VARCHAR(50) NOT NULL,     -- 'reported', 'assigned', 'resolved', 'confirmed'
    sla_status VARCHAR(20) NOT NULL,           -- 'within_sla', 'breached'
    predicted_eta_hours DOUBLE PRECISION,      -- From Phase 10 ETA engine
    resolution_media_count INT NOT NULL DEFAULT 0,
    is_appealed BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Per-Incident Cryptographic Checkpoint Chain
    prev_hash VARCHAR(64) NOT NULL,            -- Genesis '000...0' on seq 0, else prior entry_hash
    entry_hash VARCHAR(64) NOT NULL,           -- SHA-256(prev_hash:incident_id:seq:status:dp_geom:dp_timestamp)
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ledger_incident_seq UNIQUE (incident_id, sequence_num),
    CONSTRAINT uq_ledger_incident_status UNIQUE (incident_id, lifecycle_status)
);

CREATE INDEX IF NOT EXISTS idx_js_ledger_org ON public.jan_sunwai_ledger_entry(organization_id);
CREATE INDEX IF NOT EXISTS idx_js_ledger_ward ON public.jan_sunwai_ledger_entry(ward_id);
CREATE INDEX IF NOT EXISTS idx_js_ledger_category ON public.jan_sunwai_ledger_entry(category_code);
CREATE INDEX IF NOT EXISTS idx_js_ledger_created ON public.jan_sunwai_ledger_entry(dp_timestamp);
CREATE INDEX IF NOT EXISTS idx_js_ledger_geom ON public.jan_sunwai_ledger_entry USING GIST(dp_geom);

-- 2. Nagar Pragati City Progress Aggregate View / Table (§A21)
CREATE TABLE IF NOT EXISTS public.nagar_pragati_city_snapshot (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL DEFAULT 'monthly', -- 'weekly', 'monthly', 'quarterly'
    city_mttr_hours DOUBLE PRECISION,
    city_csi DOUBLE PRECISION,
    city_sla_compliance_rate DOUBLE PRECISION,
    total_intake INT NOT NULL DEFAULT 0,
    total_resolved INT NOT NULL DEFAULT 0,
    department_rankings JSONB NOT NULL DEFAULT '[]'::jsonb,
    ward_equity_distribution JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_nagar_pragati_org_period UNIQUE (organization_id, snapshot_date, period_type)
);

CREATE INDEX IF NOT EXISTS idx_nagar_pragati_org ON public.nagar_pragati_city_snapshot(organization_id);
CREATE INDEX IF NOT EXISTS idx_nagar_pragati_date ON public.nagar_pragati_city_snapshot(snapshot_date);

-- 3. Row-Level Security & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.jan_sunwai_ledger_entry ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nagar_pragati_city_snapshot ENABLE ROW LEVEL SECURITY;

-- Service Role full access
DROP POLICY IF EXISTS service_role_ledger_all ON public.jan_sunwai_ledger_entry;
CREATE POLICY service_role_ledger_all ON public.jan_sunwai_ledger_entry
    FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS service_role_pragati_all ON public.nagar_pragati_city_snapshot;
CREATE POLICY service_role_pragati_all ON public.nagar_pragati_city_snapshot
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Public Anonymous & Authenticated Read
DROP POLICY IF EXISTS public_read_jan_sunwai_ledger ON public.jan_sunwai_ledger_entry;
CREATE POLICY public_read_jan_sunwai_ledger ON public.jan_sunwai_ledger_entry
    FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS public_read_nagar_pragati ON public.nagar_pragati_city_snapshot;
CREATE POLICY public_read_nagar_pragati ON public.nagar_pragati_city_snapshot
    FOR SELECT TO anon, authenticated USING (true);

-- Scoped Grants (Strict Invariant: authenticated gets SELECT only; zero blanket write grants)
REVOKE ALL ON TABLE public.jan_sunwai_ledger_entry FROM PUBLIC;
REVOKE ALL ON TABLE public.nagar_pragati_city_snapshot FROM PUBLIC;

GRANT SELECT ON TABLE public.jan_sunwai_ledger_entry TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.jan_sunwai_ledger_entry TO service_role;

GRANT SELECT ON TABLE public.nagar_pragati_city_snapshot TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.nagar_pragati_city_snapshot TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.nagar_pragati_city_snapshot TO service_role;
