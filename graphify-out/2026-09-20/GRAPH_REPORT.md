# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 59 files · ~18,869 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 463 nodes · 899 edges · 40 communities (20 shown, 20 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4a2fdc4f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- jwt.py
- hierarchy.py
- test_rls_organization.py
- v1/intake.py
- test_hierarchy_api.py
- uuid
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
- config.py
- test_health.py
- test_intake_api.py
- track_anonymous_report
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- test_live_supabase_rbac_rls
- test_live_supabase_phase2_rls
- test_live_supabase_rls_boundary

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
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `test_jwt_claims_parsing()` --calls--> `CurrentUserClaims`  [EXTRACTED]
  tests/test_identity_models.py → civicbrain/domain/identity/jwt.py
- `test_organization_schema_structure()` --uses--> `ULBType`  [INFERRED]
  tests/test_rls_organization.py → civicbrain/domain/identity/models.py
- `test_jwt_claims_parsing()` --uses--> `StaffRole`  [INFERRED]
  tests/test_identity_models.py → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (40 total, 20 thin omitted)

### Community 0 - "jwt.py"
Cohesion: 0.06
Nodes (35): civicbrain_api_v1, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), API v1 router registry. (+27 more)

### Community 1 - "hierarchy.py"
Cohesion: 0.05
Nodes (72): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, create_staff_member(), get_hierarchy(), get_representative() (+64 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.08
Nodes (24): Organization, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, ULBType, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status (+16 more)

### Community 3 - "v1/intake.py"
Cohesion: 0.07
Nodes (54): post, SupabaseClaims, FastAPI Ingestion and Anonymous Tracking Endpoints., Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), Administrative and electoral unit of a ULB representing a Corporator…, Ward, calculate_jaro_winkler_similarity() (+46 more)

### Community 4 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 5 - "uuid"
Cohesion: 0.17
Nodes (12): pytest, supabase, is_live_supabase_configured(), Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings., is_live_supabase_configured(), Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings. (+4 more)

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
Cohesion: 0.10
Nodes (35): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, SupabaseClaims, UUID, FastAPI Operational Incidents Endpoints. (+27 more)

### Community 30 - "identity.py"
Cohesion: 0.11
Nodes (32): CitizenVerificationMethod, Staff roles mapped to §A18 named workspaces., Citizen identity verification methods per §A8., StaffRole, BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase (+24 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 32 - "config.py"
Cohesion: 0.20
Nodes (7): BaseSettings, Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env., Settings, field_validator, pydantic, pydantic_settings

### Community 33 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 34 - "test_intake_api.py"
Cohesion: 0.28
Nodes (8): asyncio, Integration tests for citizen intake and operational incidents APIs., Verify tracking endpoint returns 404 for nonexistent token., Verify IP rate limiting on anonymous tracking token endpoint., Verify /v1/incidents returns empty list for empty or non-existent org., test_incidents_listing_nonexistent_org(), test_track_anonymous_report_not_found(), test_track_anonymous_report_rate_limit()

### Community 35 - "track_anonymous_report"
Cohesion: 0.29
Nodes (8): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address., track_anonymous_report(), Request

### Community 36 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 37 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 38 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 39 - "test_live_supabase_rls_boundary"
Cohesion: 0.67
Nodes (3): skipif, End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

## Knowledge Gaps
- **28 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 224 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `test_rls_organization.py` to `hierarchy.py`, `v1/intake.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
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
- **What connects `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._