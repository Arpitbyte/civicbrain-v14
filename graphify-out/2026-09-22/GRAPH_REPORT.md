# Graph Report - CivicBrain  (2026-09-22)

## Corpus Check
- 151 files · ~78,551 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 997 nodes · 2007 edges · 77 communities (51 shown, 26 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c83d330a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/__init__.py
- auth.py
- compliance_scanner.py
- v1/gis.py
- test_intake_api.py
- config.py
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
- v1/causal.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- identity/services.py
- VisionDetector
- test_vision_splitting.py
- v1/intake.py
- identity/models.py
- v1/taxonomy.py
- analytics/services.py
- test_rls_organization.py
- hierarchy.py
- pytest
- jwt.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis.py
- test_hierarchy_api.py
- main.py
- test_analytics_eta.py
- public.jan_sunwai_ledger_entry
- CurrentUserClaims
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- track_anonymous_report
- test_health.py
- Phase 0: Foundations & Kickoff — Implementation Log
- v1/analytics.py
- intake/services.py
- uuid
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- test_live_supabase_phase12_rls_matrix.py
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- test_live_supabase_phase5_nlp.py
- IntakeStatus
- audit/__init__.py
- test_nlp_pipeline.py
- Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification
- intake/models.py

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `CurrentUserClaims` - 22 edges
3. `StaffRole` - 20 edges
4. `Incident` - 20 edges
5. `IncidentStatus` - 20 edges
6. `Organization` - 18 edges
7. `submit_intake_report()` - 18 edges
8. `IntakeStatus` - 16 edges
9. `Department` - 15 edges
10. `CategoryStatus` - 15 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `1. Executive Summary & Scope` --references--> `Zone`  [INFERRED]
  docs/specs/phase-4.md → civicbrain/domain/identity/models.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py

## Import Cycles
- None detected.

## Communities (77 total, 26 thin omitted)

### Community 0 - "v1/__init__.py"
Cohesion: 0.13
Nodes (17): civicbrain_api_v1_dispatch, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), API v1 router registry. (+9 more)

### Community 1 - "auth.py"
Cohesion: 0.20
Nodes (10): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, get_db(), AsyncSession, Dependency that provides an async session per request. (+2 more)

### Community 2 - "compliance_scanner.py"
Cohesion: 0.08
Nodes (22): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, civicbrain_domain_transparency_services (+14 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.11
Nodes (31): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+23 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.15
Nodes (16): Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, redis_asyncio, asyncio, Integration tests for citizen intake and operational incidents APIs. (+8 more)

### Community 5 - "config.py"
Cohesion: 0.22
Nodes (6): BaseSettings, field_validator, Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env., Settings, pydantic_settings

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 7 - "0003_phase2_intake_incident_dedup.sql"
Cohesion: 0.09
Nodes (45): auth.users, idx_organization_code, organization, citizen_profile, department, elected_representative, idx_department_organization_id, idx_elected_rep_org_id (+37 more)

### Community 15 - "identity.py"
Cohesion: 0.13
Nodes (29): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase, DepartmentCreate, DepartmentResponse (+21 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.14
Nodes (27): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+19 more)

### Community 30 - "v1/causal.py"
Cohesion: 0.06
Nodes (42): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, CausalGraphService (+34 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "identity/services.py"
Cohesion: 0.16
Nodes (21): ElectedRepresentative, Administrative subdivision of a ULB., Staff user account linked to Supabase Auth auth.users., Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., UserAccount, Zone, create_staff_user(), get_departments() (+13 more)

### Community 34 - "VisionDetector"
Cohesion: 0.13
Nodes (17): DetectedDefect, FixtureVisionDetector, HonestColdStartDetector, BaseModel, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration. (+9 more)

### Community 35 - "test_vision_splitting.py"
Cohesion: 0.16
Nodes (16): Department, Organization, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, asyncio, Unit & integration tests for Computer Vision protocol and Multi-Issue Photo-…, Verify photo splitting pipeline splits defects into atomic observations across…, Verify arbitrary photo in cold start creates an UNCLASSIFIED observation… (+8 more)

### Community 36 - "v1/intake.py"
Cohesion: 0.15
Nodes (21): AsyncSession, post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report() (+13 more)

### Community 37 - "identity/models.py"
Cohesion: 0.12
Nodes (18): asyncio, CitizenProfile, Identity and Organization domain entities., Administrative and electoral unit of a ULB representing a Corporator…, Explicit role assignment for staff users with optional department, zone, or…, Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserRoleAssignment, Ward (+10 more)

### Community 38 - "v1/taxonomy.py"
Cohesion: 0.05
Nodes (60): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+52 more)

### Community 39 - "analytics/services.py"
Cohesion: 0.12
Nodes (22): compute_csi(), compute_ward_report_card(), generate_corporator_digest(), AsyncSession, CurrentUserClaims, date, UUID, Analytical and Predictive Domain Services (§A21, §A23). (+14 more)

### Community 40 - "test_rls_organization.py"
Cohesion: 0.14
Nodes (13): sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT…, test_client_sdk_rls_anonymous_denial() (+5 more)

### Community 41 - "hierarchy.py"
Cohesion: 0.19
Nodes (16): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+8 more)

### Community 42 - "pytest"
Cohesion: 0.09
Nodes (20): pytest, supabase, is_live_supabase_configured(), skipif, Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings., Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls() (+12 more)

### Community 43 - "jwt.py"
Cohesion: 0.13
Nodes (17): analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, get_current_user_claims(), JWT claims extraction and RBAC security dependencies for Supabase Auth., Dependency verifying Supabase JWT and returning structured claims., BaseModel (+9 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis.py"
Cohesion: 0.20
Nodes (8): json, is_live_supabase_configured(), asyncio, skipif, Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test…, Check if real Supabase credentials are provided in settings., Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 47 - "main.py"
Cohesion: 0.20
Nodes (9): civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root(), contextlib (+1 more)

### Community 48 - "test_analytics_eta.py"
Cohesion: 0.10
Nodes (23): Base, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, civicbrain_domain_dispatch_models, asyncio (+15 more)

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.08
Nodes (35): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+27 more)

### Community 50 - "CurrentUserClaims"
Cohesion: 0.14
Nodes (14): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, CurrentUserClaims, Any, Role-check dependency factory., Parsed and validated claims from Supabase Auth JWT., require_roles() (+6 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "track_anonymous_report"
Cohesion: 0.22
Nodes (10): check_rate_limit(), Any, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client(), Returns singleton async Redis client connected to UPSTASH_REDIS_URL. (+2 more)

### Community 53 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 54 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.33
Nodes (5): 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 55 - "v1/analytics.py"
Cohesion: 0.16
Nodes (22): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, CurrentUserClaims, date (+14 more)

### Community 56 - "intake/services.py"
Cohesion: 0.14
Nodes (26): calculate_jaro_winkler_similarity(), Deterministic Jaro-Winkler similarity calculation for cold-start text matching., Citizen intake & observation domain., Incident, IncidentDedupLink, IntakeReport, Observation, Base (+18 more)

### Community 57 - "uuid"
Cohesion: 0.13
Nodes (18): BaseModel, Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, CausalRelationType, Causal taxonomy classifying upstream failure modes., CategoryPriorCreate, Pydantic schemas for Phase 10 Analytics, Ward Report Card, Corporator Digest &…, Payload to configure or initialize a category service-time prior., CausalLinkResponse (+10 more)

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - "Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. Incident Table RLS Audit & Access-Control Regression Fix, 2. What Was Built in Phase 5, 3. Verification & Live Test Evidence, Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

### Community 66 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.11
Nodes (15): BaseModel, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Process incoming citizen grievance text into structured NLP metadata., TextAnalysisResult, 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata (+7 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "test_live_supabase_phase12_rls_matrix.py"
Cohesion: 0.14
Nodes (12): postgrest_exceptions, skipif, is_live_supabase_configured(), Live Supabase Phase 12 Exhaustive RLS & Privilege Matrix Audit Test Suite. In…, Check if real Supabase credentials are provided in settings., Systematically audits positive and negative paths across all application tables., test_live_supabase_phase12_exhaustive_rls_matrix(), is_live_supabase_configured() (+4 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "test_live_supabase_phase5_nlp.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 5 NLP Pipeline & Database Constraints Test Suite (§A11). In…, Check if real Supabase credentials are provided in settings., Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 71 - "IntakeStatus"
Cohesion: 0.29
Nodes (7): IntakeStatus, Aggregate lifecycle status for parent citizen intake report., Unit tests for Phase 2 domain models, §A16 lifecycle, and least-advanced…, Verify incident_status_enum covers all 11 states per §A16., Verify §A7 & Standing Invariant 3 least-advanced aggregation logic., test_incident_status_enum_values(), test_least_advanced_child_status_aggregation()

### Community 78 - "test_nlp_pipeline.py"
Cohesion: 0.13
Nodes (17): DeterministicIndicRuleProcessor, NLPProcessor, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Standard protocol for multilingual civic grievance text analysis., Deterministic, lightweight multilingual processor optimized for Render free-…, 1. Executive Summary & Scope, asyncio (+9 more)

### Community 134 - "Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants, 3.4 Row-Level Security Policies, 3. Database Schema (`migrations/0004_phase3_vision_taxonomy.sql`), 5.1 Automated Unit Tests (+4 more)

### Community 475 - "intake/models.py"
Cohesion: 0.15
Nodes (18): evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, DedupDecision, Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Record linkage determination., geoalchemy2, logging (+10 more)

## Knowledge Gaps
- **80 isolated node(s):** `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)`, `3.2 Observation Table Alterations`, `3.3 Explicit Per-Role Scoped Grants` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 485 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `test_nlp_pipeline.py` to `Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log`, `Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification`, `jwt.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `CurrentUserClaims` connect `CurrentUserClaims` to `auth.py`, `v1/gis.py`, `v1/taxonomy.py`, `analytics/services.py`, `hierarchy.py`, `jwt.py`, `identity.py`, `test_analytics_eta.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `CorporatorDigestResponse` connect `analytics/services.py` to `uuid`, `Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification`, `v1/analytics.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `StaffRole` (e.g. with `get_incidents_geojson()` and `create_staff_member()`) actually correct?**
  _`StaffRole` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._