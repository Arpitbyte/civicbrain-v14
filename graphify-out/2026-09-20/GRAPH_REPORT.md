# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 60 files · ~19,321 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 475 nodes · 922 edges · 35 communities (14 shown, 21 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 86 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `38eeb258`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- hierarchy.py
- test_rls_organization.py
- v1/intake.py
- test_intake_api.py
- jwt.py
- CivicBrain v14 — Operational Rules & Architecture Ground Truth
- 0003_phase2_intake_incident_dedup.sql
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
- incidents.py
- identity.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- track_anonymous_report
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log

## God Nodes (most connected - your core abstractions)
1. `submit_intake_report()` - 18 edges
2. `Base` - 17 edges
3. `IncidentStatus` - 16 edges
4. `StaffRole` - 15 edges
5. `route_and_deduplicate_observation()` - 14 edges
6. `CurrentUserClaims` - 12 edges
7. `organization` - 12 edges
8. `update_incident_status()` - 11 edges
9. `Organization` - 11 edges
10. `get_organization_hierarchy()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `test_staff_role_enum_values()` --uses--> `StaffRole`  [INFERRED]
  tests/test_identity_models.py → civicbrain/domain/identity/models.py
- `test_organization_schema_structure()` --uses--> `ULBType`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (35 total, 21 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.09
Nodes (25): civicbrain_api_v1, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), API v1 router registry. (+17 more)

### Community 1 - "hierarchy.py"
Cohesion: 0.05
Nodes (76): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, create_staff_member(), get_hierarchy(), get_representative() (+68 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.08
Nodes (24): Organization, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, ULBType, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status (+16 more)

### Community 3 - "v1/intake.py"
Cohesion: 0.06
Nodes (68): post, SupabaseClaims, FastAPI Ingestion and Anonymous Tracking Endpoints., Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), Administrative and electoral unit of a ULB representing a Corporator…, Ward, calculate_jaro_winkler_similarity() (+60 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.07
Nodes (34): Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, httpx, redis_asyncio, asyncio (+26 more)

### Community 5 - "jwt.py"
Cohesion: 0.05
Nodes (34): BaseSettings, get_current_user_claims(), JWT claims extraction and RBAC security dependencies for Supabase Auth., Role-check dependency factory., Dependency verifying Supabase JWT and returning structured claims., require_roles(), Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env. (+26 more)

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 7 - "0003_phase2_intake_incident_dedup.sql"
Cohesion: 0.09
Nodes (45): auth.users, idx_organization_code, organization, citizen_profile, department, elected_representative, idx_department_organization_id, idx_elected_rep_org_id (+37 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.14
Nodes (26): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, SupabaseClaims, UUID, FastAPI Operational Incidents Endpoints. (+18 more)

### Community 30 - "identity.py"
Cohesion: 0.12
Nodes (28): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase, DepartmentCreate, DepartmentResponse (+20 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 35 - "track_anonymous_report"
Cohesion: 0.20
Nodes (11): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+3 more)

### Community 36 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

## Knowledge Gaps
- **27 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 231 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `test_rls_organization.py` to `hierarchy.py`, `v1/intake.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `DedupDecision` connect `v1/intake.py` to `Phase 2: Domain Core & Incident Lifecycle — Implementation Log`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Base` connect `hierarchy.py` to `test_rls_organization.py`, `v1/intake.py`, `incidents.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `submit_intake_report()` (e.g. with `Department` and `Organization`) actually correct?**
  _`submit_intake_report()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `IncidentStatus` (e.g. with `list_incidents()` and `update_incident_status()`) actually correct?**
  _`IncidentStatus` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `StaffRole` (e.g. with `create_staff_member()` and `list_staff_members()`) actually correct?**
  _`StaffRole` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `route_and_deduplicate_observation()` (e.g. with `DedupDecision` and `IncidentStatus`) actually correct?**
  _`route_and_deduplicate_observation()` has 4 INFERRED edges - model-reasoned connections that need verification._