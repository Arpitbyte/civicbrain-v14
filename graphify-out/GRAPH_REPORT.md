# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 71 files · ~27,418 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 619 nodes · 1282 edges · 54 communities (33 shown, 21 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 154 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c87cb62`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- identity/models.py
- test_rls_organization.py
- v1/intake.py
- test_intake_api.py
- Settings
- CivicBrain v14 — Operational Rules & Architecture Ground Truth
- 0003_phase2_intake_incident_dedup.sql
- AGENTS.md
- rules/graphify.md
- workflows/graphify.md
- cases/__init__.py
- gis/__init__.py
- identity/__init__.py
- domain/__init__.py
- identity.py
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
- update_incident_status
- intake/services.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- process_photo_intake
- test_vision_splitting.py
- track_anonymous_report
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- IncidentStatus
- test_hierarchy_api.py
- test_health.py
- uuid
- pytest
- test_live_supabase_rls.py
- test_taxonomy_governance.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- config.py
- test_live_supabase_phase3_rls.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- DetectedDefect
- main.py
- test_splink_dedup.py
- Phase 0: Foundations & Kickoff — Implementation Log
- public.taxonomy_category
- public.observation

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `Base` - 19 edges
3. `submit_intake_report()` - 18 edges
4. `StaffRole` - 18 edges
5. `Organization` - 18 edges
6. `IncidentStatus` - 18 edges
7. `IntakeStatus` - 16 edges
8. `CurrentUserClaims` - 15 edges
9. `route_and_deduplicate_observation()` - 15 edges
10. `CategoryStatus` - 15 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. Executive Summary & Scope` --references--> `Ward`  [INFERRED]
  docs/specs/phase-4.md → civicbrain/domain/identity/models.py
- `1. Executive Summary & Scope` --references--> `Observation`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/models.py

## Import Cycles
- None detected.

## Communities (54 total, 21 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.16
Nodes (16): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+8 more)

### Community 1 - "identity/models.py"
Cohesion: 0.05
Nodes (76): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, create_staff_member(), get_representative(), list_departments() (+68 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.13
Nodes (14): pathlib, sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT… (+6 more)

### Community 3 - "v1/intake.py"
Cohesion: 0.13
Nodes (27): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+19 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.18
Nodes (14): Any, Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, asyncio, Integration tests for citizen intake and operational incidents APIs., Verify tracking endpoint returns 404 for nonexistent token., Verify Redis-backed IP rate limiting on anonymous tracking token endpoint. (+6 more)

### Community 5 - "Settings"
Cohesion: 0.33
Nodes (4): BaseSettings, field_validator, CivicBrain system settings loaded from environment or .env., Settings

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 7 - "0003_phase2_intake_incident_dedup.sql"
Cohesion: 0.09
Nodes (45): auth.users, idx_organization_code, organization, citizen_profile, department, elected_representative, idx_department_organization_id, idx_elected_rep_org_id (+37 more)

### Community 15 - "identity.py"
Cohesion: 0.10
Nodes (39): get_hierarchy(), Retrieve complete tree of zones and wards for an organization., CitizenVerificationMethod, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Citizen identity verification methods per §A8., ULBType, get_organization_hierarchy(), Fetch complete hierarchical tree of zones and wards for an organization. (+31 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "update_incident_status"
Cohesion: 0.23
Nodes (15): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+7 more)

### Community 30 - "intake/services.py"
Cohesion: 0.14
Nodes (23): Administrative and electoral unit of a ULB representing a Corporator…, Ward, Citizen intake & observation domain., DedupDecision, Incident, IncidentDedupLink, IntakeReport, ObservationStatus (+15 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "process_photo_intake"
Cohesion: 0.13
Nodes (23): Department, Organization, Administrative subdivision of a ULB., Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Zone, Observation, Atomic localized defect extracted from citizen intake submission. (+15 more)

### Community 34 - "test_vision_splitting.py"
Cohesion: 0.13
Nodes (20): FixtureVisionDetector, get_vision_detector(), HonestColdStartDetector, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Dependency provider for FastAPI route handlers., Protocol for vision analysis backends., Production web detector under zero-GPU and 512MB RAM constraints (Render free… (+12 more)

### Community 35 - "track_anonymous_report"
Cohesion: 0.20
Nodes (11): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+3 more)

### Community 36 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 37 - "IncidentStatus"
Cohesion: 0.26
Nodes (11): IncidentStatus, IntakeStatus, Aggregate lifecycle status for parent citizen intake report., Authoritative Incident Lifecycle (§A16 11-State Machine)., calculate_intake_status_from_children(), Calculates parent intake_report.status based on the least-advanced active child…, Unit tests for Phase 2 domain models, §A16 lifecycle, and least-advanced…, Verify incident_status_enum covers all 11 states per §A16. (+3 more)

### Community 38 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 39 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 40 - "uuid"
Cohesion: 0.22
Nodes (7): is_live_supabase_configured(), skipif, Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings., Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls(), uuid

### Community 41 - "pytest"
Cohesion: 0.25
Nodes (7): pytest, is_live_supabase_configured(), skipif, Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings., Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 42 - "test_live_supabase_rls.py"
Cohesion: 0.25
Nodes (7): supabase, is_live_supabase_configured(), skipif, Live Supabase RLS and Auth integration test. In strict accordance with Phase 0…, Check if real Supabase credentials are provided in settings., End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 43 - "test_taxonomy_governance.py"
Cohesion: 0.06
Nodes (47): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+39 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "config.py"
Cohesion: 0.33
Nodes (4): Application configuration via pydantic-settings., Upstash Redis connection and rate limiting client., pydantic_settings, redis_asyncio

### Community 46 - "test_live_supabase_phase3_rls.py"
Cohesion: 0.40
Nodes (4): postgrest_exceptions, is_live_supabase_configured(), Live Supabase Phase 3 Living Taxonomy RLS & Scoped Grants Test Suite. In strict…, Check if real Supabase credentials are provided in settings.

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 326 - "main.py"
Cohesion: 0.20
Nodes (9): civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root(), contextlib (+1 more)

### Community 475 - "test_splink_dedup.py"
Cohesion: 0.16
Nodes (15): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., math, Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation. (+7 more)

### Community 1683 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 1813 - "public.taxonomy_category"
Cohesion: 0.38
Nodes (6): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, public, public.department, public.organization

## Knowledge Gaps
- **43 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 300 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `process_photo_intake` to `identity/models.py`, `test_rls_organization.py`, `v1/intake.py`, `test_vision_splitting.py`, `test_taxonomy_governance.py`, `identity.py`, `Phase 0: Foundations & Kickoff — Implementation Log`, `intake/services.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `Observation` connect `process_photo_intake` to `identity/models.py`, `test_vision_splitting.py`, `v1/intake.py`, `update_incident_status`, `intake/services.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `1. Executive Summary & Scope` connect `test_vision_splitting.py` to `process_photo_intake`, `DetectedDefect`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `submit_intake_report()` (e.g. with `Department` and `Organization`) actually correct?**
  _`submit_intake_report()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `StaffRole` (e.g. with `create_staff_member()` and `list_staff_members()`) actually correct?**
  _`StaffRole` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Organization` (e.g. with `submit_intake_report()` and `propose_category()`) actually correct?**
  _`Organization` has 8 INFERRED edges - model-reasoned connections that need verification._