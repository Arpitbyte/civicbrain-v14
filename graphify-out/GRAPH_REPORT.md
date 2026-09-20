# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 47 files · ~11,954 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 315 nodes · 533 edges · 32 communities (12 shown, 20 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f24f7195`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- models.py
- test_rls_organization.py
- main.py
- test_hierarchy_api.py
- config.py
- CivicBrain v14 — Operational Rules & Architecture Ground Truth
- 0002_phase1_identity_rbac.sql
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
- hierarchy.py
- identity.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

## God Nodes (most connected - your core abstractions)
1. `StaffRole` - 15 edges
2. `CurrentUserClaims` - 12 edges
3. `Base` - 12 edges
4. `get_organization_hierarchy()` - 11 edges
5. `BaseSchema` - 10 edges
6. `create_staff_member()` - 9 edges
7. `Organization` - 9 edges
8. `resolve_user_profile()` - 9 edges
9. `create_staff_user()` - 9 edges
10. `ward` - 9 edges

## Surprising Connections (you probably didn't know these)
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `test_staff_role_enum_values()` --uses--> `StaffRole`  [INFERRED]
  tests/test_identity_models.py → civicbrain/domain/identity/models.py
- `test_organization_schema_structure()` --uses--> `Organization`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py
- `test_organization_schema_structure()` --uses--> `ULBType`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (32 total, 20 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.15
Nodes (17): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+9 more)

### Community 1 - "models.py"
Cohesion: 0.07
Nodes (48): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, CitizenProfile, Department, ElectedRepresentative (+40 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.09
Nodes (22): Urban Local Body classification under 74th Constitutional Amendment Act, 1992., ULBType, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log (+14 more)

### Community 3 - "main.py"
Cohesion: 0.15
Nodes (12): civicbrain_api_v1, API v1 router registry., lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root() (+4 more)

### Community 4 - "test_hierarchy_api.py"
Cohesion: 0.12
Nodes (20): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+12 more)

### Community 5 - "config.py"
Cohesion: 0.08
Nodes (22): BaseSettings, Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env., Settings, field_validator, pydantic, pydantic_settings, pytest (+14 more)

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 7 - "0002_phase1_identity_rbac.sql"
Cohesion: 0.18
Nodes (22): auth.users, idx_organization_code, organization, citizen_profile, department, elected_representative, idx_department_organization_id, idx_elected_rep_org_id (+14 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "hierarchy.py"
Cohesion: 0.09
Nodes (35): Any, create_staff_member(), get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get (+27 more)

### Community 30 - "identity.py"
Cohesion: 0.12
Nodes (32): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase, DepartmentCreate, DepartmentResponse (+24 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

## Knowledge Gaps
- **24 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 164 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `models.py` to `test_rls_organization.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `ULBType` connect `test_rls_organization.py` to `models.py`, `identity.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `1. What Was Built` connect `test_rls_organization.py` to `models.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `StaffRole` (e.g. with `create_staff_member()` and `list_staff_members()`) actually correct?**
  _`StaffRole` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `create_staff_member()`) actually correct?**
  _`CurrentUserClaims` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_organization_hierarchy()` (e.g. with `Organization` and `Zone`) actually correct?**
  _`get_organization_hierarchy()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._