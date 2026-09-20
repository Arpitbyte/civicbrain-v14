# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 71 files · ~27,418 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 631 nodes · 1260 edges · 68 communities (39 shown, 29 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 138 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0a49cd60`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- identity/services.py
- test_rls_organization.py
- incidents.py
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
- list_incidents
- intake/models.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- test_vision_splitting.py
- VisionDetector
- track_anonymous_report
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- intake/services.py
- test_hierarchy_api.py
- test_health.py
- v1/taxonomy.py
- hierarchy.py
- UUID
- test_taxonomy_governance.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- redis.py
- v1/intake.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_identity_models.py
- propose_category
- identity/models.py
- schemas/taxonomy.py
- CurrentUserClaims
- create_staff_member
- get_db
- AsyncSession
- get
- patch
- post
- SupabaseClaims
- UUID
- Any
- asyncio
- HonestColdStartDetector
- main.py
- route_and_deduplicate_observation
- public.taxonomy_category
- public.observation

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `Base` - 19 edges
3. `IncidentStatus` - 18 edges
4. `submit_intake_report()` - 18 edges
5. `Organization` - 16 edges
6. `IntakeStatus` - 16 edges
7. `route_and_deduplicate_observation()` - 15 edges
8. `test_process_photo_intake_multi_department_splitting()` - 15 edges
9. `CurrentUserClaims` - 14 edges
10. `Observation` - 14 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Observation`  [INFERRED]
  docs/phase-log/phase-3.md → civicbrain/domain/intake/models.py
- `1. Executive Summary & Scope` --references--> `Observation`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/models.py

## Import Cycles
- None detected.

## Communities (68 total, 29 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.16
Nodes (16): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+8 more)

### Community 1 - "identity/services.py"
Cohesion: 0.13
Nodes (23): Authentication and user session endpoints., CitizenProfile, ElectedRepresentative, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserAccount (+15 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.09
Nodes (22): Urban Local Body classification under 74th Constitutional Amendment Act, 1992., ULBType, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log (+14 more)

### Community 3 - "incidents.py"
Cohesion: 0.15
Nodes (21): patch, FastAPI Operational Incidents Endpoints., Progresses incident state across §A16 lifecycle and triggers least-advanced…, update_incident_status(), IncidentStatus, Authoritative Incident Lifecycle (§A16 11-State Machine)., AnonymousTrackingResponse, BaseSchema (+13 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.17
Nodes (14): asyncio, Any, Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, Integration tests for citizen intake and operational incidents APIs., Verify tracking endpoint returns 404 for nonexistent token., Verify Redis-backed IP rate limiting on anonymous tracking token endpoint. (+6 more)

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
Cohesion: 0.17
Nodes (21): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse, ElectedRepresentativeBase, ElectedRepresentativeCreate (+13 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "list_incidents"
Cohesion: 0.33
Nodes (10): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, SupabaseClaims, UUID, Lists all atomic citizen observations clustered into this operational incident. (+2 more)

### Community 30 - "intake/models.py"
Cohesion: 0.23
Nodes (10): Citizen intake & observation domain., Incident, IncidentDedupLink, Observation, ObservationStatus, Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Authoritative operational civic case tracked across §A16 lifecycle., Atomic localized defect extracted from citizen intake submission. (+2 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "test_vision_splitting.py"
Cohesion: 0.14
Nodes (22): Department, Organization, Administrative subdivision of a ULB., Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, Zone (+14 more)

### Community 34 - "VisionDetector"
Cohesion: 0.29
Nodes (7): get_vision_detector(), Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Dependency provider for FastAPI route handlers., Protocol for vision analysis backends., VisionDetector, 1. Executive Summary & Scope, Protocol

### Community 35 - "track_anonymous_report"
Cohesion: 0.29
Nodes (8): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), Request

### Community 36 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 37 - "intake/services.py"
Cohesion: 0.18
Nodes (19): IntakeReport, IntakeStatus, Aggregate lifecycle status for parent citizen intake report., Citizen submission provenance container., calculate_intake_status_from_children(), process_photo_intake(), AsyncSession, UUID (+11 more)

### Community 38 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 39 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 40 - "v1/taxonomy.py"
Cohesion: 0.16
Nodes (13): API v1 router registry., Living Taxonomy Governance REST Endpoints (§A11, Standing Invariant 1)., get_current_user_claims(), get_optional_user_claims(), JWT claims extraction and RBAC security dependencies for Supabase Auth., Dependency extracting Supabase JWT claims if present, returning None if…, Role-check dependency factory., Dependency verifying Supabase JWT and returning structured claims. (+5 more)

### Community 41 - "hierarchy.py"
Cohesion: 0.23
Nodes (15): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+7 more)

### Community 42 - "UUID"
Cohesion: 0.17
Nodes (10): Application configuration via pydantic-settings., pydantic, pydantic_settings, is_live_supabase_configured(), skipif, Live Supabase RLS and Auth integration test. In strict accordance with Phase 0…, Check if real Supabase credentials are provided in settings., End-to-end verification of RLS and Auth against a live Supabase project. (+2 more)

### Community 43 - "test_taxonomy_governance.py"
Cohesion: 0.05
Nodes (44): create_default_rubric(), BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories., RubricLevel, SeverityRubric (+36 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "redis.py"
Cohesion: 0.33
Nodes (5): get_redis_client(), Upstash Redis connection and rate limiting client., Returns singleton async Redis client connected to UPSTASH_REDIS_URL., Redis, redis_asyncio

### Community 46 - "v1/intake.py"
Cohesion: 0.18
Nodes (15): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+7 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_identity_models.py"
Cohesion: 0.17
Nodes (15): Staff roles mapped to §A18 named workspaces., StaffRole, CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces. (+7 more)

### Community 49 - "propose_category"
Cohesion: 0.16
Nodes (15): AsyncSession, CategoryStatus, approve_category(), list_categories(), propose_category(), Admin approves category (§A11, Standing Invariant 1). Approval strictly…, List taxonomy categories. Public/citizens see only approved active categories.…, Staff/Citizen proposes a new civic category in 'proposed' state. Strictly sets… (+7 more)

### Community 50 - "identity/models.py"
Cohesion: 0.23
Nodes (10): Identity and Organization domain entities., Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, Database engine, session management, and connectivity diagnostics., collections_abc, enum, geoalchemy2, sqlalchemy, sqlalchemy_dialects_postgresql (+2 more)

### Community 51 - "schemas/taxonomy.py"
Cohesion: 0.24
Nodes (10): BaseSchema, BaseModel, Pydantic schemas for Living Taxonomy Governance and Rubric validation., Staff/Citizen payload proposing a new civic category., Admin payload approving a proposed category (§A11, Standing Invariant 1). Must…, Taxonomy category output., TaxonomyCategoryApprove, TaxonomyCategoryPropose (+2 more)

### Community 52 - "CurrentUserClaims"
Cohesion: 0.25
Nodes (7): Any, get_my_profile(), AsyncSession, get, Returns the authenticated identity, role assignments, and jurisdictional scopes…, CurrentUserClaims, Parsed and validated claims from Supabase Auth JWT.

### Community 53 - "create_staff_member"
Cohesion: 0.50
Nodes (4): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, UserAccountCreate

### Community 54 - "get_db"
Cohesion: 0.67
Nodes (3): get_db(), AsyncSession, Dependency that provides an async session per request.

### Community 134 - "HonestColdStartDetector"
Cohesion: 0.06
Nodes (31): DetectedDefect, FixtureVisionDetector, HonestColdStartDetector, BaseModel, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., Production web detector under zero-GPU and 512MB RAM constraints (Render free… (+23 more)

### Community 326 - "main.py"
Cohesion: 0.20
Nodes (9): civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root(), contextlib (+1 more)

### Community 475 - "route_and_deduplicate_observation"
Cohesion: 0.16
Nodes (19): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., DedupDecision, Record linkage determination., Evaluates candidate open incidents in the same ward and department using… (+11 more)

### Community 1813 - "public.taxonomy_category"
Cohesion: 0.38
Nodes (6): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, public, public.department, public.organization

## Knowledge Gaps
- **43 isolated node(s):** `civicbrain`, `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)`, `3.2 Observation Table Alterations` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 312 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `test_vision_splitting.py` to `identity/services.py`, `test_rls_organization.py`, `intake/services.py`, `hierarchy.py`, `v1/intake.py`, `identity/models.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Observation` connect `intake/models.py` to `test_vision_splitting.py`, `VisionDetector`, `incidents.py`, `intake/services.py`, `v1/intake.py`, `route_and_deduplicate_observation`, `list_incidents`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `1. Executive Summary & Scope` connect `VisionDetector` to `HonestColdStartDetector`, `intake/models.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `IncidentStatus` (e.g. with `list_incidents()` and `update_incident_status()`) actually correct?**
  _`IncidentStatus` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `submit_intake_report()` (e.g. with `Department` and `Organization`) actually correct?**
  _`submit_intake_report()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `civicbrain`, `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._