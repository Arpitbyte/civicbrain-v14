# Graph Report - CivicBrain  (2026-09-19)

## Corpus Check
- 37 files · ~5,318 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 160 nodes · 171 edges · 30 communities (9 shown, 21 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c4c956d6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- models.py
- test_rls_organization.py
- main.py
- test_health.py
- config.py
- CivicBrain v14 — Operational Rules & Architecture Ground Truth
- 0001_phase0_init.sql
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md
- cases/__init__.py
- gis/__init__.py
- identity/__init__.py
- domain/__init__.py
- intake/__init__.py
- notifications/__init__.py
- priority/__init__.py
- infra/__init__.py
- civicbrain/__init__.py
- schemas/__init__.py
- workers/__init__.py
- CLAUDE.md
- GEMINI.md
- copilot-instructions.md
- integrations/__init__.py
- civicbrain
- CivicBrain v14
- test_live_supabase_rls.py

## God Nodes (most connected - your core abstractions)
1. `Organization` - 7 edges
2. `CivicBrain v14 — Operational Rules & Architecture Ground Truth` - 6 edges
3. `readiness_check()` - 5 edges
4. `ULBType` - 5 edges
5. `Settings` - 5 edges
6. `Base` - 5 edges
7. `HealthResponse` - 5 edges
8. `ReadinessResponse` - 5 edges
9. `CivicBrain v14` - 5 edges
10. `Phase 0: Foundations & Kickoff — Implementation Log` - 5 edges

## Surprising Connections (you probably didn't know these)
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `test_organization_schema_structure()` --uses--> `ULBType`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py
- `test_organization_schema_structure()` --uses--> `Organization`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py
- `health_check()` --uses--> `HealthResponse`  [INFERRED]
  civicbrain/api/v1/health.py → civicbrain/schemas/health.py

## Import Cycles
- None detected.

## Communities (30 total, 21 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.15
Nodes (17): BaseModel, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection() (+9 more)

### Community 1 - "models.py"
Cohesion: 0.15
Nodes (14): AsyncSession, Identity and Organization domain entities., Base, get_db(), Database engine, session management, and connectivity diagnostics., Base declarative class for all CivicBrain database entities., Dependency that provides an async session per request., collections_abc (+6 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.09
Nodes (23): Organization, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, ULBType, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Open TODOs & Prerequisites for Phase 1 (+15 more)

### Community 3 - "main.py"
Cohesion: 0.15
Nodes (12): civicbrain_api_v1, API v1 router registry., lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root() (+4 more)

### Community 4 - "test_health.py"
Cohesion: 0.22
Nodes (10): asyncio, httpx, pytest, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness() (+2 more)

### Community 5 - "config.py"
Cohesion: 0.20
Nodes (7): BaseSettings, Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env., Settings, field_validator, pydantic, pydantic_settings

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "test_live_supabase_rls.py"
Cohesion: 0.22
Nodes (8): skipif, supabase, is_live_supabase_configured(), Live Supabase RLS and Auth integration test. In strict accordance with Phase 0…, Check if real Supabase credentials are provided in settings., End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary(), uuid

## Knowledge Gaps
- **19 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 107 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `test_rls_organization.py` to `models.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Organization` (e.g. with `1. What Was Built` and `test_organization_schema_structure()`) actually correct?**
  _`Organization` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ULBType` (e.g. with `1. What Was Built` and `test_organization_schema_structure()`) actually correct?**
  _`ULBType` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)` to the rest of the system?**
  _19 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_rls_organization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08547008547008547 - nodes in this community are weakly interconnected._