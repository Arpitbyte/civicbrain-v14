# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 47 files · ~11,832 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 319 nodes · 533 edges · 36 communities (12 shown, 24 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f298df6d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- services.py
- test_rls_organization.py
- create_staff_member
- main.py
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
- 0001_phase0_init.sql
- BaseModel
- asyncio
- skipif

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
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `test_staff_role_enum_values()` --uses--> `StaffRole`  [INFERRED]
  tests/test_identity_models.py → civicbrain/domain/identity/models.py
- `test_organization_schema_structure()` --uses--> `ULBType`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py
- `test_jwt_claims_parsing()` --uses--> `StaffRole`  [INFERRED]
  tests/test_identity_models.py → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (36 total, 24 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.16
Nodes (16): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+8 more)

### Community 1 - "services.py"
Cohesion: 0.08
Nodes (41): BaseModel, get_my_profile(), AsyncSession, get, Returns the authenticated identity, role assignments, and jurisdictional scopes…, CitizenProfile, Department, ElectedRepresentative (+33 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.08
Nodes (24): Organization, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, ULBType, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status (+16 more)

### Community 3 - "create_staff_member"
Cohesion: 0.23
Nodes (12): create_staff_member(), get_hierarchy(), get_representative(), list_departments(), AsyncSession, get, UUID, Retrieve complete tree of zones and wards for an organization. (+4 more)

### Community 4 - "main.py"
Cohesion: 0.07
Nodes (30): asyncio, civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root() (+22 more)

### Community 5 - "config.py"
Cohesion: 0.08
Nodes (22): BaseSettings, Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env., Settings, field_validator, pydantic, pydantic_settings, pytest (+14 more)

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 7 - "0002_phase1_identity_rbac.sql"
Cohesion: 0.20
Nodes (21): auth.users, citizen_profile, department, elected_representative, idx_department_organization_id, idx_elected_rep_org_id, idx_user_account_organization_id, idx_user_role_org_id (+13 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "hierarchy.py"
Cohesion: 0.08
Nodes (34): Any, Authentication and user session endpoints., list_staff_members(), Administrative hierarchy, department taxonomy, and representative discovery…, List staff accounts within the admin's tenant organization., API v1 router registry., CurrentUserClaims, get_current_user_claims() (+26 more)

### Community 30 - "identity.py"
Cohesion: 0.12
Nodes (29): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase, DepartmentCreate, DepartmentResponse (+21 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

## Knowledge Gaps
- **24 isolated node(s):** `1. What Was Built`, `2. Key Architectural Decisions`, `3. Deviations from Specification`, `4. Verification & CI Status`, `civicbrain` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 167 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `test_rls_organization.py` to `services.py`, `hierarchy.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `ULBType` connect `test_rls_organization.py` to `services.py`, `hierarchy.py`, `identity.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `StaffRole` (e.g. with `create_staff_member()` and `list_staff_members()`) actually correct?**
  _`StaffRole` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `create_staff_member()`) actually correct?**
  _`CurrentUserClaims` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_organization_hierarchy()` (e.g. with `Organization` and `Zone`) actually correct?**
  _`get_organization_hierarchy()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. What Was Built`, `2. Key Architectural Decisions`, `3. Deviations from Specification` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `services.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08362369337979095 - nodes in this community are weakly interconnected._