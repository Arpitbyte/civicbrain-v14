-- CivicBrain v14 — Phase 7: Causal Root-Cause Linking & Incident Graph Centrality (§A13)
-- Migration 0008: Causal Link Topology, Cycle Prevention Trigger, and Centrality Metadata

-- 1. Create Causal Relation Type Enum
DO $$ BEGIN
    CREATE TYPE causal_relation_type_enum AS ENUM (
        'infrastructure_failure',   -- e.g. burst water main causing surface pothole/cave-in
        'environmental_cascade',    -- e.g. clogged drainage causing roadway flooding
        'operational_blockage',     -- e.g. solid waste dump blocking culvert
        'structural_damage'         -- e.g. retaining wall failure or tree root heave
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Incident Causal Link Table
CREATE TABLE IF NOT EXISTS public.incident_causal_link (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    root_incident_id UUID NOT NULL REFERENCES public.incident(id) ON DELETE CASCADE,
    symptom_incident_id UUID NOT NULL REFERENCES public.incident(id) ON DELETE CASCADE,
    relation_type causal_relation_type_enum NOT NULL,
    confidence DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    established_by UUID REFERENCES public.user_account(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_causal_pair UNIQUE (root_incident_id, symptom_incident_id),
    CONSTRAINT chk_no_self_causation CHECK (root_incident_id <> symptom_incident_id),
    CONSTRAINT chk_causal_confidence CHECK (confidence >= 0.0 AND confidence <= 1.0)
);

CREATE INDEX IF NOT EXISTS idx_causal_org_id ON public.incident_causal_link(organization_id);
CREATE INDEX IF NOT EXISTS idx_causal_root_id ON public.incident_causal_link(root_incident_id);
CREATE INDEX IF NOT EXISTS idx_causal_symptom_id ON public.incident_causal_link(symptom_incident_id);

-- 3. Extend Incident Table with Causal Graph Metadata
ALTER TABLE public.incident
    ADD COLUMN IF NOT EXISTS is_root_cause BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS downstream_symptom_count INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS root_cause_priority_boost DOUBLE PRECISION NOT NULL DEFAULT 0.0;

-- 4. In-Database Recursive Cycle Prevention Trigger
-- Traverses downstream from the proposed symptom_incident_id to verify root_incident_id is not already downstream.
CREATE OR REPLACE FUNCTION check_causal_cycle_trigger()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_has_cycle BOOLEAN;
BEGIN
    -- Immediate self-causation check
    IF NEW.root_incident_id = NEW.symptom_incident_id THEN
        RAISE EXCEPTION 'Cyclic causal dependency detected: self-causation (root == symptom)'
            USING ERRCODE = '23514';
    END IF;

    -- Transitive multi-hop cycle check via recursive CTE
    WITH RECURSIVE downstream_path AS (
        SELECT symptom_incident_id AS node_id, 1 AS depth
        FROM public.incident_causal_link
        WHERE root_incident_id = NEW.symptom_incident_id

        UNION

        SELECT l.symptom_incident_id, p.depth + 1
        FROM public.incident_causal_link l
        JOIN downstream_path p ON l.root_incident_id = p.node_id
        WHERE p.depth < 50
    )
    SELECT EXISTS (
        SELECT 1 FROM downstream_path WHERE node_id = NEW.root_incident_id
    ) INTO v_has_cycle;

    IF v_has_cycle THEN
        RAISE EXCEPTION 'Cyclic causal dependency detected: incident % is already a downstream symptom of %',
            NEW.root_incident_id, NEW.symptom_incident_id
            USING ERRCODE = '23514';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_prevent_causal_cycles ON public.incident_causal_link;
CREATE TRIGGER trg_prevent_causal_cycles
    BEFORE INSERT OR UPDATE ON public.incident_causal_link
    FOR EACH ROW
    EXECUTE FUNCTION check_causal_cycle_trigger();

-- 5. Row-Level Security (RLS) & Narrowed Table Grants
ALTER TABLE public.incident_causal_link ENABLE ROW LEVEL SECURITY;

CREATE POLICY service_role_causal_link_all ON public.incident_causal_link
    FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY causal_link_select_org ON public.incident_causal_link
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = incident_causal_link.organization_id
        )
    );

CREATE POLICY causal_link_manage_staff ON public.incident_causal_link
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = incident_causal_link.organization_id
              AND ura.role IN ('admin', 'dispatcher', 'zonal_supervisor')
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = incident_causal_link.organization_id
              AND ura.role IN ('admin', 'dispatcher', 'zonal_supervisor')
        )
    );

-- Scoped Grants (Correction 2: authenticated gets SELECT only, zero blanket write grants)
REVOKE ALL ON TABLE public.incident_causal_link FROM PUBLIC;
GRANT SELECT ON TABLE public.incident_causal_link TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.incident_causal_link TO service_role;
GRANT SELECT ON TABLE public.incident_causal_link TO authenticated;
