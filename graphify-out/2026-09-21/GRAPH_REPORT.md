# Graph Report - CivicBrain  (2026-09-20)

## Corpus Check
- 86 files · ~35,533 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 747 nodes · 1500 edges · 68 communities (44 shown, 24 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 172 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8a2aff16`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- identity/services.py
- test_rls_organization.py
- test_gis_core.py
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
- main.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- v1/gis.py
- DeterministicIndicRuleProcessor
- test_vision_splitting.py
- test_taxonomy_governance.py
- v1/intake.py
- TaxonomyCategory
- test_health.py
- identity/models.py
- list_staff_members
- config.py
- v1/taxonomy.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis
- submit_intake_report
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_identity_models.py
- 0005_phase4_gis_core.sql
- intake/taxonomy.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- test_live_supabase_phase3_rls
- StaffRole
- test_live_supabase_rbac_rls
- intake/models.py
- test_live_supabase_rls_boundary
- Phase 0: Foundations & Kickoff — Implementation Log
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- test_live_supabase_phase5_nlp
- public.observation
- public.intake_report
- public.observation
- DetectedDefect
- DedupDecision
- public.taxonomy_category

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `StaffRole` - 20 edges
3. `IncidentStatus` - 20 edges
4. `CurrentUserClaims` - 19 edges
5. `Base` - 19 edges
6. `submit_intake_report()` - 18 edges
7. `Organization` - 18 edges
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
- `1. What Was Built` --references--> `Observation`  [INFERRED]
  docs/phase-log/phase-3.md → civicbrain/domain/intake/models.py
- `1. Executive Summary & Scope` --references--> `Observation`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/models.py

## Import Cycles
- None detected.

## Communities (68 total, 24 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.18
Nodes (14): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+6 more)

### Community 1 - "identity/services.py"
Cohesion: 0.14
Nodes (24): CitizenProfile, ElectedRepresentative, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserAccount, UserRoleAssignment (+16 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.13
Nodes (14): pathlib, sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT… (+6 more)

### Community 3 - "test_gis_core.py"
Cohesion: 0.16
Nodes (18): GeoJSONFeature, GeoJSONFeatureCollection, IncidentClusterResponse, BaseModel, Geospatial and GeoJSON schemas for GIS Core (§A14)., RFC 7946 GeoJSON Feature representation., RFC 7946 GeoJSON FeatureCollection representation., Detected defect density hotspot cluster (§A14). (+10 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.06
Nodes (39): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+31 more)

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
Cohesion: 0.18
Nodes (20): Urban Local Body classification under 74th Constitutional Amendment Act, 1992., ULBType, BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse, ElectedRepresentativeBase, ElectedRepresentativeCreate (+12 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.11
Nodes (33): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+25 more)

### Community 30 - "main.py"
Cohesion: 0.15
Nodes (11): civicbrain_api_v1, get, CivicBrain application entrypoint and ASGI factory., Redirect or direct reference to API docs., root(), contextlib, fastapi_middleware_cors, asyncio (+3 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "v1/gis.py"
Cohesion: 0.27
Nodes (11): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+3 more)

### Community 34 - "DeterministicIndicRuleProcessor"
Cohesion: 0.06
Nodes (31): DeterministicIndicRuleProcessor, NLPProcessor, BaseModel, Protocol, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Standard protocol for multilingual civic grievance text analysis. (+23 more)

### Community 35 - "test_vision_splitting.py"
Cohesion: 0.13
Nodes (24): Department, Organization, Administrative subdivision of a ULB., Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, Zone (+16 more)

### Community 36 - "test_taxonomy_governance.py"
Cohesion: 0.14
Nodes (21): create_default_rubric(), BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories., RubricLevel, SeverityRubric (+13 more)

### Community 37 - "v1/intake.py"
Cohesion: 0.17
Nodes (23): FastAPI Ingestion and Anonymous Tracking Endpoints., IntakeReport, IntakeStatus, Observation, Atomic localized defect extracted from citizen intake submission., Aggregate lifecycle status for parent citizen intake report., Citizen submission provenance container., calculate_intake_status_from_children() (+15 more)

### Community 38 - "TaxonomyCategory"
Cohesion: 0.17
Nodes (15): Categorical classification entity governed by living taxonomy rules., TaxonomyCategory, FixtureVisionDetector, get_vision_detector(), HonestColdStartDetector, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.… (+7 more)

### Community 39 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 40 - "identity/models.py"
Cohesion: 0.20
Nodes (12): Administrative hierarchy, department taxonomy, and representative discovery…, Identity and Organization domain entities., get_db(), AsyncSession, Database engine, session management, and connectivity diagnostics., Dependency that provides an async session per request., collections_abc, geoalchemy2 (+4 more)

### Community 41 - "list_staff_members"
Cohesion: 0.27
Nodes (11): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, List staff accounts within the admin's tenant organization. (+3 more)

### Community 42 - "config.py"
Cohesion: 0.09
Nodes (27): Application configuration via pydantic-settings., postgrest_exceptions, pydantic_settings, pytest, supabase, is_live_supabase_configured(), skipif, Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.… (+19 more)

### Community 43 - "v1/taxonomy.py"
Cohesion: 0.06
Nodes (50): API v1 router registry., analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, approve_category(), list_categories(), propose_category() (+42 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis"
Cohesion: 0.40
Nodes (4): asyncio, skipif, Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "submit_intake_report"
Cohesion: 0.19
Nodes (14): post, SupabaseClaims, UUID, Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake(), IntakeChannel (+6 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_identity_models.py"
Cohesion: 0.20
Nodes (13): CitizenVerificationMethod, Citizen identity verification methods per §A8., CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces. (+5 more)

### Community 49 - "0005_phase4_gis_core.sql"
Cohesion: 0.20
Nodes (8): idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report, public.incident, public.ward, public.zone

### Community 50 - "intake/taxonomy.py"
Cohesion: 0.22
Nodes (8): Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Schemas for health and readiness probes., enum, pydantic, re, sqlalchemy_dialects_postgresql, typing

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "test_live_supabase_phase3_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

### Community 53 - "StaffRole"
Cohesion: 0.13
Nodes (17): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's… (+9 more)

### Community 54 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 55 - "intake/models.py"
Cohesion: 0.32
Nodes (6): Citizen intake & observation domain., IncidentDedupLink, ObservationStatus, Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Splink probabilistic record linkage audit between observation and candidate…, Atomic observation state.

### Community 56 - "test_live_supabase_rls_boundary"
Cohesion: 0.67
Nodes (3): skipif, End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 57 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "test_live_supabase_phase5_nlp"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 475 - "DedupDecision"
Cohesion: 0.17
Nodes (17): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., DedupDecision, Record linkage determination., math (+9 more)

### Community 1813 - "public.taxonomy_category"
Cohesion: 0.38
Nodes (6): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, public, public.department, public.organization

## Knowledge Gaps
- **57 isolated node(s):** `civicbrain`, `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)` (+52 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 370 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `DeterministicIndicRuleProcessor` to `intake/taxonomy.py`, `v1/taxonomy.py`, `main.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `Organization` connect `test_vision_splitting.py` to `identity/services.py`, `test_rls_organization.py`, `v1/intake.py`, `identity/models.py`, `v1/taxonomy.py`, `submit_intake_report`, `Phase 0: Foundations & Kickoff — Implementation Log`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `Observation` connect `v1/intake.py` to `test_vision_splitting.py`, `TaxonomyCategory`, `submit_intake_report`, `intake/models.py`, `incidents.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `StaffRole` (e.g. with `get_incidents_geojson()` and `create_staff_member()`) actually correct?**
  _`StaffRole` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._