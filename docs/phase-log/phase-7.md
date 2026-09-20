# Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Implementation Log

**Date:** 2026-09-21  
**Status:** COMPLETED  
**Version:** CivicBrain v14.7.0  

---

## 1. What Was Built

- **Causal Graph Topology & Domain Engine (§A13):**
  - Directed causal link table `incident_causal_link` connecting upstream root-cause infrastructure failures with downstream symptom incidents.
  - Multi-hop cycle prevention:
    - In-database PostgreSQL trigger `trg_prevent_causal_cycles` with recursive CTE verifying that adding edge $A \to B$ does not introduce a cycle ($A$ reachable from $B$ downstream).
    - Application-level graph traversal in `CausalGraphService.validate_acyclic_addition` in pure Python.
  - Out-degree centrality & downstream blast radius computation:
    - Transitive downstream symptom collection: `find_all_downstream_symptoms`.
    - Priority multiplier calculation:
      $$P_{\text{root}} = \min\left(100.0, P_{\text{base}} \times \left(1.0 + \sum_{j \in \text{children}} \alpha_j \cdot \frac{P_j}{100.0}\right)\right)$$
      with provisional coupling coefficient $\alpha = 0.15$.
  - Extended `incident` with `is_root_cause`, `downstream_symptom_count`, and `root_cause_priority_boost`.

- **Database Migration & Scoped Grants (`migrations/0008_phase7_causal_graph.sql`):**
  - Applied migration 0008 to live Supabase (`isqepbxkzxfpvfdkcntw`).
  - Strict table grants: `authenticated` receives `SELECT` only on `incident_causal_link` (no blanket write grant).
  - RLS policies restrict management of causal links strictly to `admin`, `dispatcher`, and `zonal_supervisor` roles.

- **REST API Endpoints (`civicbrain/api/v1/causal.py`):**
  - `POST /v1/causal/links`: Establishes directed causal link after cycle validation.
  - `GET /v1/causal/incidents/{incident_id}/downstream`: Returns itemized downstream symptoms and priority boost.

---

## 2. Verification & Test Evidence

1. **Unit Test Suite (`tests/test_causal_graph.py`):**
   - Self-causation check: $A \to A$ rejected with `CyclicCausalDependencyError`.
   - 2-node cycle: $B \to A$ when $A \to B$ exists rejected.
   - 3-node cycle: $C \to A$ when $A \to B \to C$ exists rejected.
   - Multi-tier DAG branching and blast radius collection verified.
   - Root-cause priority multiplier verified against mathematical expectation.

2. **Live Supabase Integration (`tests/test_live_supabase_phase7_causal.py`):**
   - Seeded real test organization, zone, ward, water & roads departments on live Supabase.
   - Seeded 3 incidents (water pipeline burst $\to$ road subsidence $\to$ surface crater).
   - Proved PostgreSQL trigger `trg_prevent_causal_cycles` rejects 3-node cycle ($C \to A$).
   - Clean teardown in `finally` block.

3. **Full Suite & Static Quality Gates:**
   - All 63 tests passing locally.
   - `ruff check` and `ruff format --check` clean with 0 errors.
   - `mypy civicbrain` clean with 0 errors across 52 source files.
