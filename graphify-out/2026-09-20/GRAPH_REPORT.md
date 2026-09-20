# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 78 files · ~31,469 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 686 nodes · 1406 edges · 61 communities (40 shown, 21 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 165 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0a49cd60`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- database.py
- identity/models.py
- test_rls_organization.py
- v1/gis.py
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
- incidents.py
- intake/models.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- test_vision_splitting.py
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- track_anonymous_report
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- intake/services.py
- test_hierarchy_api.py
- test_health.py
- jwt.py
- hierarchy.py
- config.py
- v1/taxonomy.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis.py
- v1/intake.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_identity_models.py
- 0005_phase4_gis_core.sql
- Phase 0: Foundations & Kickoff — Implementation Log
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- test_live_supabase_phase3_rls
- StaffRole
- test_live_supabase_rbac_rls
- test_live_supabase_phase2_rls
- test_live_supabase_rls_boundary
- HonestColdStartDetector
- test_splink_dedup.py
- public.taxonomy_category
- public.observation

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `StaffRole` - 20 edges
3. `IncidentStatus` - 20 edges
4. `Base` - 19 edges
5. `submit_intake_report()` - 18 edges
6. `Organization` - 18 edges
7. `CurrentUserClaims` - 17 edges
8. `IntakeStatus` - 16 edges
9. `route_and_deduplicate_observation()` - 15 edges
10. `CategoryStatus` - 15 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `RubricLevel`  [INFERRED]
  docs/phase-log/phase-3.md → civicbrain/domain/intake/taxonomy.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py

## Import Cycles
- None detected.

## Communities (61 total, 21 thin omitted)

### Community 0 - "database.py"
Cohesion: 0.07
Nodes (32): civicbrain_api_v1, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), API v1 router registry. (+24 more)

### Community 1 - "identity/models.py"
Cohesion: 0.13
Nodes (24): CitizenProfile, ElectedRepresentative, Identity and Organization domain entities., Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserAccount (+16 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.13
Nodes (14): pathlib, sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT… (+6 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.12
Nodes (29): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+21 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.15
Nodes (16): Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, redis_asyncio, asyncio, Integration tests for citizen intake and operational incidents APIs. (+8 more)

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
Nodes (21): Urban Local Body classification under 74th Constitutional Amendment Act, 1992., ULBType, BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse, ElectedRepresentativeBase, ElectedRepresentativeCreate (+13 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.19
Nodes (20): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+12 more)

### Community 30 - "intake/models.py"
Cohesion: 0.18
Nodes (14): Citizen intake & observation domain., IncidentDedupLink, IncidentStatus, IntakeStatus, Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Splink probabilistic record linkage audit between observation and candidate…, Aggregate lifecycle status for parent citizen intake report., Authoritative Incident Lifecycle (§A16 11-State Machine). (+6 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "test_vision_splitting.py"
Cohesion: 0.18
Nodes (17): Department, Organization, Administrative subdivision of a ULB., Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, Zone (+9 more)

### Community 34 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.18
Nodes (10): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 5. REST API Endpoints (`civicbrain/api/v1/nlp.py`) (+2 more)

### Community 35 - "track_anonymous_report"
Cohesion: 0.20
Nodes (11): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+3 more)

### Community 36 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 37 - "intake/services.py"
Cohesion: 0.13
Nodes (28): DedupDecision, IntakeReport, Observation, Atomic localized defect extracted from citizen intake submission., Record linkage determination., Citizen submission provenance container., calculate_intake_status_from_children(), process_photo_intake() (+20 more)

### Community 38 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 39 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 40 - "jwt.py"
Cohesion: 0.13
Nodes (18): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, CurrentUserClaims, get_current_user_claims(), get_optional_user_claims() (+10 more)

### Community 41 - "hierarchy.py"
Cohesion: 0.23
Nodes (15): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+7 more)

### Community 42 - "config.py"
Cohesion: 0.12
Nodes (17): Application configuration via pydantic-settings., postgrest_exceptions, pydantic_settings, pytest, supabase, is_live_supabase_configured(), Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings. (+9 more)

### Community 43 - "v1/taxonomy.py"
Cohesion: 0.07
Nodes (52): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+44 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis.py"
Cohesion: 0.20
Nodes (8): json, is_live_supabase_configured(), asyncio, skipif, Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test…, Check if real Supabase credentials are provided in settings., Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "v1/intake.py"
Cohesion: 0.13
Nodes (27): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+19 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_identity_models.py"
Cohesion: 0.20
Nodes (13): CitizenVerificationMethod, Citizen identity verification methods per §A8., CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces. (+5 more)

### Community 49 - "0005_phase4_gis_core.sql"
Cohesion: 0.20
Nodes (8): idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.incident, public.intake_report, public.ward, public.zone

### Community 50 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "test_live_supabase_phase3_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

### Community 53 - "StaffRole"
Cohesion: 0.20
Nodes (9): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, Role-check dependency factory., require_roles(), Staff roles mapped to §A18 named workspaces., StaffRole, Verify CurrentUserClaims parses custom Supabase app_metadata. (+1 more)

### Community 54 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 55 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 56 - "test_live_supabase_rls_boundary"
Cohesion: 0.67
Nodes (3): skipif, End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 134 - "HonestColdStartDetector"
Cohesion: 0.06
Nodes (31): DetectedDefect, FixtureVisionDetector, HonestColdStartDetector, BaseModel, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., Production web detector under zero-GPU and 512MB RAM constraints (Render free… (+23 more)

### Community 475 - "test_splink_dedup.py"
Cohesion: 0.15
Nodes (16): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., logging, math, Unit tests for Splink deduplication integration under provisional cold-start… (+8 more)

### Community 1813 - "public.taxonomy_category"
Cohesion: 0.38
Nodes (6): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, public, public.department, public.organization

## Knowledge Gaps
- **53 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 336 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Organization` connect `test_vision_splitting.py` to `identity/models.py`, `test_rls_organization.py`, `intake/services.py`, `hierarchy.py`, `v1/taxonomy.py`, `v1/intake.py`, `Phase 0: Foundations & Kickoff — Implementation Log`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Observation` connect `intake/services.py` to `test_vision_splitting.py`, `incidents.py`, `v1/intake.py`, `intake/models.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `1. Executive Summary & Scope` connect `intake/services.py` to `HonestColdStartDetector`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `StaffRole` (e.g. with `get_incidents_geojson()` and `create_staff_member()`) actually correct?**
  _`StaffRole` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `submit_intake_report()` (e.g. with `Department` and `Organization`) actually correct?**
  _`submit_intake_report()` has 10 INFERRED edges - model-reasoned connections that need verification._