# Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

**Version:** CivicBrain v14.7.0  
**Phase:** 7  
**Status:** SPECIFICATION APPROVED FOR IMPLEMENTATION (Corrected per User Review)  

---

## 1. Executive Summary & Scope

Phase 7 implements the Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13):
1. **Civic Causal Graph Topology:**
   - In municipal infrastructure, many visible surface symptoms (e.g. repeated potholes, road subsidence, surface flooding) are caused by common upstream root infrastructure failures (e.g. leaking underground water supply main, broken stormwater culvert, clogged underground trunk sewer).
   - Directed causal link table `incident_causal_link` connecting child symptoms to upstream parent root causes.
2. **Real Multi-Hop Cycle Prevention (Correction 1):**
   - In addition to direct self-reference checks ($A \to A$), insertion of any link ($A \to B$) must traverse the existing graph from $B$ downstream. If $A$ is reachable from $B$, the insertion is strictly rejected to prevent multi-hop cycles ($A \to B \to C \to A$).
   - Implemented via a recursive CTE in PostgreSQL (`validate_causal_link_acyclic` trigger / RPC) and mirrored at the application service layer in pure Python.
3. **Graph Centrality & Root-Cause Multipliers (§A13):**
   - Out-degree centrality / downstream blast radius:
     - Counts transitive and direct downstream incidents causally spawned by an upstream failure.
     - Scales the parent incident's priority score proportionally:
       $$P_{\text{root}} = \min\left(100.0, P_{\text{base}} \times \left(1.0 + \sum_{j \in \text{children}} \alpha_j \cdot \frac{P_j}{100.0}\right)\right)$$
       where $\alpha_j = 0.15$ is the provisional coupling coefficient.
   - Downstream cascade management: Resolving an upstream root-cause incident enables automated status transitions and dispatcher notifications for downstream symptoms.
4. **Scoped Table Grants (Correction 2):**
   - Narrowed table grants: `authenticated` role receives `SELECT` only on `incident_causal_link` (matching every other table's pattern).
   - Operational mutating access (`INSERT, UPDATE, DELETE`) is executed via privileged background workers / service_role or scoped RPC endpoints, eliminating broad blanket write grants on `authenticated`.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Acyclic Causal Graph (Hard Invariant):**
   - Causal links must form a Directed Acyclic Graph (DAG). Self-referential links ($A \to A$) and indirect cycles of any length ($A \to B \to C \to A$) raise validation errors and cannot be persisted.
2. **Glass-Box Centrality Reproducibility (Standing Invariant 2):**
   - Priority multipliers must be deterministic and fully itemized (listing all child incidents, coupling coefficients, and score increments).
3. **Pure CPU Graph Computation (Hard Rule 1):**
   - Pure Python graph algorithms on CPU; zero external network/graph DB licensing.
4. **Mandatory Scoped Grants (Standing Invariant 4):**
   - Explicit `GRANT` statements per role with zero `GRANT ALL`.

---

## 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`)

```sql
-- Migration 0008: Causal Root-Cause Links & Centrality Metadata

DO $$ BEGIN
    CREATE TYPE causal_relation_type_enum AS ENUM (
        'infrastructure_failure',   -- e.g. burst pipe causing pothole/sinkhole
        'environmental_cascade',    -- e.g. clogged drain causing road flooding
        'operational_blockage',     -- e.g. illegal dumping blocking stormwater drain
        'structural_damage'         -- e.g. tree root heave cracking pavement
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

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
    CONSTRAINT chk_no_self_causation CHECK (root_incident_id <> symptom_incident_id)
);

CREATE INDEX IF NOT EXISTS idx_causal_org_id ON public.incident_causal_link(organization_id);
CREATE INDEX IF NOT EXISTS idx_causal_root_id ON public.incident_causal_link(root_incident_id);
CREATE INDEX IF NOT EXISTS idx_causal_symptom_id ON public.incident_causal_link(symptom_incident_id);

-- Extend Incident with Root Cause Centrality Metadata
ALTER TABLE public.incident
    ADD COLUMN IF NOT EXISTS is_root_cause BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS downstream_symptom_count INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS root_cause_priority_boost DOUBLE PRECISION NOT NULL DEFAULT 0.0;

-- Cycle Prevention Trigger Function via Recursive CTE
CREATE OR REPLACE FUNCTION check_causal_cycle_trigger()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_has_cycle BOOLEAN;
BEGIN
    -- Check if root_incident_id is reachable downstream from symptom_incident_id
    WITH RECURSIVE downstream_path AS (
        SELECT symptom_incident_id AS node_id, 1 AS depth
        FROM public.incident_causal_link
        WHERE root_incident_id = NEW.symptom_incident_id

        UNION

        SELECT l.symptom_incident_id, p.depth + 1
        FROM public.incident_causal_link l
        JOIN downstream_path p ON l.root_incident_id = p.node_id
        WHERE p.depth < 100 -- Guard against runaway execution
    )
    SELECT EXISTS (
        SELECT 1 FROM downstream_path WHERE node_id = NEW.root_incident_id
    ) INTO v_has_cycle;

    IF v_has_cycle OR NEW.root_incident_id = NEW.symptom_incident_id THEN
        RAISE EXCEPTION 'Cyclic causal dependency detected: incident % is already a downstream symptom of %',
            NEW.root_incident_id, NEW.symptom_incident_id
            USING ERRCODE = '23514'; -- check_violation
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_prevent_causal_cycles ON public.incident_causal_link;
CREATE TRIGGER trg_prevent_causal_cycles
    BEFORE INSERT OR UPDATE ON public.incident_causal_link
    FOR EACH ROW
    EXECUTE FUNCTION check_causal_cycle_trigger();

-- Scoped Grants & RLS (Correction 2: authenticated gets SELECT only)
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

REVOKE ALL ON TABLE public.incident_causal_link FROM PUBLIC;
GRANT SELECT ON TABLE public.incident_causal_link TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.incident_causal_link TO service_role;
GRANT SELECT ON TABLE public.incident_causal_link TO authenticated;
```

---

## 4. Verification Plan

1. **Unit Tests (`tests/test_causal_graph.py`):**
   - Direct self-reference check ($A \to A$) rejected.
   - 2-node cycle ($A \to B \to A$) rejected.
   - 3-node cycle ($A \to B \to C \to A$) rejected.
   - Centrality & blast radius priority boost computation verified.
2. **Live Supabase Tests (`tests/test_live_supabase_phase7_causal.py`):**
   - Seed incidents and causal links on live DB.
   - Assert in-database trigger rejects 3-node cycle ($A \to B \to C \to A$).
   - Assert RLS isolation and clean teardown in `finally`.
3. **CI & Quality Gates:**
   - Full test suite, ruff, and mypy clean.
