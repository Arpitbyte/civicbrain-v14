# Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

**Version:** CivicBrain v14.7.0  
**Phase:** 7  
**Status:** SPECIFICATION PENDING APPROVAL  

---

## 1. Executive Summary & Scope

Phase 7 implements the Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13):
1. **Civic Causal Graph Topology:**
   - In municipal infrastructure, many visible surface symptoms (e.g. repeated potholes, road subsidence, surface flooding) are caused by common upstream root infrastructure failures (e.g. leaking underground water supply main, broken stormwater culvert, clogged underground trunk sewer).
   - Establishing the directed causal link table `incident_causal_link` connecting child symptoms to upstream parent root causes.
2. **Graph Centrality & Root-Cause Multipliers (§A13):**
   - In-database and Python graph algorithms to compute:
     - **Out-Degree Centrality / Downstream Blast Radius:** Number of downstream incidents causally spawned by an upstream failure.
     - **Root Cause Multiplier ($M_{\text{root}}$):** Scaling the parent incident's priority score proportionally to its downstream blast radius:
       $$P_{\text{root}} = \min\left(100.0, P_{\text{base}} \times \left(1.0 + \sum_{j \in \text{children}} \alpha_j \cdot P_j\right)\right)$$
       where $\alpha_j$ is a provisional coupling coefficient (e.g. $\alpha_j = 0.15$).
   - Resolving a root-cause incident automatically notifies dispatchers and triggers bulk progression / re-evaluation of downstream symptom incidents.
3. **Causal Candidate Discovery RPC:**
   - Spatial-temporal candidate pairing: Detects nearby incidents within radius $R$ (e.g. 50 meters) and time window $T$ (e.g. 14 days) sharing cross-departmental failure patterns (e.g. `WATER_SUPPLY` pipe leak $\to$ `POTHOLE` road sink).

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Acyclic Causal Graph (Hard Invariant):**
   - Causal links must form a Directed Acyclic Graph (DAG). Self-referential links ($A \to A$) and cyclic causal dependencies ($A \to B \to A$) are strictly forbidden and enforced by database check constraints and validation routines.
2. **Glass-Box Centrality Reproducibility (Standing Invariant 2):**
   - Root cause priority adjustments must be deterministic and fully itemized (listing all child incidents, coupling coefficients, and score increments).
3. **Pure CPU Graph Computation (Hard Rule 1):**
   - NetworkX / pure Python graph algorithms on CPU; zero external network/graph DB licensing.
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

-- Scoped Grants & RLS
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
GRANT INSERT, UPDATE, DELETE ON TABLE public.incident_causal_link TO authenticated;
```

---

## 4. Verification Plan

1. **Unit Tests (`tests/test_causal_graph.py`):**
   - DAG verification: Rejects cycles and self-referential links.
   - Centrality calculation: Root node blast radius correctly multiplies parent priority.
   - Cascade resolution: Resolving a root incident updates downstream symptoms.
2. **Live Supabase Tests (`tests/test_live_supabase_phase7_causal.py`):**
   - Real seeded incidents linked causally, RLS validation, and teardown in `finally`.
3. **CI & Quality Gates:**
   - Full test suite, ruff, and mypy clean.
