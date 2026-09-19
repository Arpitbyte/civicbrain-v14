# Graph Report - CivicBrain  (2026-09-19)

## Corpus Check
- 35 files · ~4,231 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 135 nodes · 141 edges · 28 communities (7 shown, 21 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `568af05d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- database.py
- Organization
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

## God Nodes (most connected - your core abstractions)
1. `Organization` - 7 edges
2. `readiness_check()` - 5 edges
3. `ULBType` - 5 edges
4. `Base` - 5 edges
5. `HealthResponse` - 5 edges
6. `ReadinessResponse` - 5 edges
7. `test_rls_anonymous_client_policy_boundary()` - 5 edges
8. `CivicBrain v14 — Operational Rules & Architecture Ground Truth` - 5 edges
9. `Phase 0: Foundations & Kickoff — Implementation Log` - 5 edges
10. `health_check()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `test_rls_anonymous_client_policy_boundary()` --uses--> `ULBType`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py
- `test_rls_anonymous_client_policy_boundary()` --uses--> `Organization`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py
- `health_check()` --uses--> `HealthResponse`  [INFERRED]
  civicbrain/api/v1/health.py → civicbrain/schemas/health.py

## Import Cycles
- None detected.

## Communities (28 total, 21 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.15
Nodes (17): BaseModel, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection() (+9 more)

### Community 1 - "database.py"
Cohesion: 0.14
Nodes (15): AsyncSession, Identity and Organization domain entities., Base, get_db(), Database engine, session management, and connectivity diagnostics., Base declarative class for all CivicBrain database entities., Dependency that provides an async session per request., collections_abc (+7 more)

### Community 2 - "Organization"
Cohesion: 0.12
Nodes (17): Organization, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, ULBType, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Open TODOs & Prerequisites for Phase 1 (+9 more)

### Community 3 - "main.py"
Cohesion: 0.15
Nodes (12): civicbrain_api_v1, API v1 router registry., lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root() (+4 more)

### Community 4 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 5 - "config.py"
Cohesion: 0.25
Nodes (6): BaseSettings, Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env., Settings, pydantic, pydantic_settings

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.33
Nodes (5): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), CivicBrain v14 — Operational Rules & Architecture Ground Truth

## Knowledge Gaps
- **14 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 93 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `Organization` to `database.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `ULBType` connect `Organization` to `database.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Organization` (e.g. with `1. What Was Built` and `test_rls_anonymous_client_policy_boundary()`) actually correct?**
  _`Organization` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ULBType` (e.g. with `1. What Was Built` and `test_rls_anonymous_client_policy_boundary()`) actually correct?**
  _`ULBType` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `database.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13970588235294118 - nodes in this community are weakly interconnected._
- **Should `Organization` be split into smaller, more focused modules?**
  _Cohesion score 0.11578947368421053 - nodes in this community are weakly interconnected._