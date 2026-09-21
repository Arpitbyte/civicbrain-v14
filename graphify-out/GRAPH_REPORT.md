# Graph Report - CivicBrain  (2026-09-21)

## Corpus Check
- 133 files · ~67,527 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 946 nodes · 1927 edges · 84 communities (60 shown, 24 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `18b1d2b0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- CurrentUserClaims
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
- v1/causal.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- hierarchy.py
- DeterministicIndicRuleProcessor
- test_vision_splitting.py
- schemas/analytics.py
- intake/models.py
- test_taxonomy_governance.py
- analytics/services.py
- identity/models.py
- list_staff_members
- config.py
- v1/taxonomy.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis.py
- v1/intake.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_corporator_digest_authorized_ward_success
- public.incident_causal_link
- processor.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- v1/nlp.py
- StaffRole
- test_live_supabase_rbac_rls
- v1/analytics.py
- intake/services.py
- Phase 0: Foundations & Kickoff — Implementation Log
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- track_anonymous_report
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- generate_corporator_digest
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- TextAnalysisResult
- test_live_supabase_phase2_rls
- v1/__init__.py
- test_live_supabase_rls_boundary
- jwt.py
- test_hierarchy_api.py
- main.py
- test_health.py
- Organization
- test_live_supabase_phase7_causal.py
- test_live_supabase_phase3_rls
- DetectedDefect
- test_splink_dedup.py

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `CurrentUserClaims` - 22 edges
3. `Incident` - 20 edges
4. `StaffRole` - 20 edges
5. `IncidentStatus` - 20 edges
6. `Organization` - 18 edges
7. `submit_intake_report()` - 18 edges
8. `IntakeStatus` - 16 edges
9. `Department` - 15 edges
10. `CategoryStatus` - 15 edges

## Surprising Connections (you probably didn't know these)
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py
- `1. Executive Summary & Scope` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/specs/phase-5.md → civicbrain/domain/nlp/processor.py

## Import Cycles
- None detected.

## Communities (84 total, 24 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.18
Nodes (14): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+6 more)

### Community 1 - "CurrentUserClaims"
Cohesion: 0.12
Nodes (16): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, CurrentUserClaims, Any, Parsed and validated claims from Supabase Auth JWT. (+8 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.15
Nodes (12): pathlib, sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT…, test_client_sdk_rls_anonymous_denial() (+4 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.12
Nodes (28): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+20 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.14
Nodes (17): Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, logging, redis_asyncio, asyncio (+9 more)

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
Cohesion: 0.14
Nodes (28): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase, DepartmentCreate, DepartmentResponse (+20 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.14
Nodes (25): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+17 more)

### Community 30 - "v1/causal.py"
Cohesion: 0.06
Nodes (47): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, CausalGraphService (+39 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "hierarchy.py"
Cohesion: 0.15
Nodes (24): get_hierarchy(), Administrative hierarchy, department taxonomy, and representative discovery…, Retrieve complete tree of zones and wards for an organization., Administrative subdivision of a ULB., Staff user account linked to Supabase Auth auth.users., UserAccount, Zone, create_staff_user() (+16 more)

### Community 34 - "DeterministicIndicRuleProcessor"
Cohesion: 0.18
Nodes (10): DeterministicIndicRuleProcessor, Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Deterministic, lightweight multilingual processor optimized for Render free-…, Verify citizen emotional intensity and anger NEVER inflate physical engineering…, Verify script detection and category resolution across Hindi, Kannada, Tamil,…, Verify unrecognized text returns suggested_category = None and flags human…, test_cold_start_honesty_on_unrecognized_text() (+2 more)

### Community 35 - "test_vision_splitting.py"
Cohesion: 0.11
Nodes (29): Administrative and electoral unit of a ULB representing a Corporator…, Ward, ObservationStatus, Atomic observation state., FixtureVisionDetector, get_vision_detector(), HonestColdStartDetector, Protocol (+21 more)

### Community 36 - "schemas/analytics.py"
Cohesion: 0.21
Nodes (12): BaseModel, CategoryPriorCreate, CategoryPriorResponse, CorporatorDigestResponse, Pydantic schemas for Phase 10 Analytics, Ward Report Card, Corporator Digest &…, Payload to configure or initialize a category service-time prior., Category baseline service-time response., Ward-level municipal scorecard and transparent performance metrics (§A21). (+4 more)

### Community 37 - "intake/models.py"
Cohesion: 0.15
Nodes (17): Citizen intake & observation domain., DedupDecision, IncidentDedupLink, IntakeChannel, IntakeReport, Observation, Base, Phase 2 Domain Models: IntakeReport, Observation, Incident, and… (+9 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.12
Nodes (23): create_default_rubric(), BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories., RubricLevel, SeverityRubric (+15 more)

### Community 39 - "analytics/services.py"
Cohesion: 0.16
Nodes (16): Base, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, compute_csi() (+8 more)

### Community 40 - "identity/models.py"
Cohesion: 0.15
Nodes (16): CitizenProfile, ElectedRepresentative, Identity and Organization domain entities., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserRoleAssignment, Base (+8 more)

### Community 41 - "list_staff_members"
Cohesion: 0.31
Nodes (9): get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, List staff accounts within the admin's tenant organization., List all active departments within the ULB. (+1 more)

### Community 42 - "config.py"
Cohesion: 0.09
Nodes (23): Application configuration via pydantic-settings., postgrest_exceptions, pydantic_settings, pytest, supabase, is_live_supabase_configured(), Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings. (+15 more)

### Community 43 - "v1/taxonomy.py"
Cohesion: 0.12
Nodes (28): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+20 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis.py"
Cohesion: 0.20
Nodes (8): json, is_live_supabase_configured(), asyncio, skipif, Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test…, Check if real Supabase credentials are provided in settings., Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "v1/intake.py"
Cohesion: 0.14
Nodes (23): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+15 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_corporator_digest_authorized_ward_success"
Cohesion: 0.15
Nodes (13): asyncio, Verify department load factor increases ETA when backlog spikes., Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives…, Verify Corporator querying their own assigned ward succeeds with alerts and…, Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot., Verify parametric ETA scales with severity and respects confidence intervals., test_corporator_digest_authorized_ward_success(), test_corporator_digest_ward_boundary_rejection() (+5 more)

### Community 49 - "public.incident_causal_link"
Cohesion: 0.09
Nodes (26): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+18 more)

### Community 50 - "processor.py"
Cohesion: 0.29
Nodes (6): NLPProcessor, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Standard protocol for multilingual civic grievance text analysis., 1. Executive Summary & Scope, re

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "v1/nlp.py"
Cohesion: 0.24
Nodes (10): analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint. (+2 more)

### Community 53 - "StaffRole"
Cohesion: 0.20
Nodes (9): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, Role-check dependency factory., require_roles(), Staff roles mapped to §A18 named workspaces., StaffRole, Verify staff_role_enum matches §A18 named workspaces. (+1 more)

### Community 54 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 55 - "v1/analytics.py"
Cohesion: 0.19
Nodes (18): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, CurrentUserClaims, date (+10 more)

### Community 56 - "intake/services.py"
Cohesion: 0.18
Nodes (21): IncidentStatus, IntakeStatus, Aggregate lifecycle status for parent citizen intake report., Authoritative Incident Lifecycle (§A16 11-State Machine)., calculate_intake_status_from_children(), process_photo_intake(), AsyncSession, UUID (+13 more)

### Community 57 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.33
Nodes (5): 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 2D Planar Laplace Coordinate Perturbation, 4.2 Temporal Jittering, 4. Differential Privacy & Coordinate Perturbation (§A23), 5.1 Jan Sunwai Public Ledger (`/v1/transparency/ledger`), 5.2 Nagar Pragati City Progress (`/v1/transparency/pragati`) (+4 more)

### Community 65 - "track_anonymous_report"
Cohesion: 0.20
Nodes (11): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+3 more)

### Community 66 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.22
Nodes (8): 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 6. Verification Plan, Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "generate_corporator_digest"
Cohesion: 0.21
Nodes (13): compute_ward_report_card(), generate_corporator_digest(), predict_incident_eta(), AsyncSession, CurrentUserClaims, date, UUID, Generates an executive operational digest for an elected Corporator (§A18,… (+5 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. Incident Table RLS Audit & Access-Control Regression Fix, 2. What Was Built in Phase 5, 3. Verification & Live Test Evidence, Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

### Community 71 - "TextAnalysisResult"
Cohesion: 0.33
Nodes (5): BaseModel, Normalized analysis result returned by NLP processing pipeline (§A11)., Process incoming citizen grievance text into structured NLP metadata., TextAnalysisResult, 5. REST API Endpoints (`civicbrain/api/v1/nlp.py`)

### Community 72 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 73 - "v1/__init__.py"
Cohesion: 0.50
Nodes (3): civicbrain_api_v1_dispatch, API v1 router registry., civicbrain_api_v1_prioritization

### Community 74 - "test_live_supabase_rls_boundary"
Cohesion: 0.67
Nodes (3): skipif, End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 75 - "jwt.py"
Cohesion: 0.14
Nodes (14): JWT claims extraction and RBAC security dependencies for Supabase Auth., Schemas for health and readiness probes., datetime, FastAPI, fastapi_security, is_live_supabase_configured(), Live Supabase Phase 10 Analytics, Ward Report Card & Corporator Digest Test…, Check if real Supabase credentials are provided in settings. (+6 more)

### Community 76 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 77 - "main.py"
Cohesion: 0.20
Nodes (9): civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root(), contextlib (+1 more)

### Community 78 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 79 - "Organization"
Cohesion: 0.29
Nodes (7): Organization, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, ULBType, 1. What Was Built, Verify SQLAlchemy model reflects the required columns and ULBType enum., test_organization_schema_structure()

### Community 80 - "test_live_supabase_phase7_causal.py"
Cohesion: 0.29
Nodes (6): skipif, is_live_supabase_configured(), Live Supabase Phase 7 Causal Root-Cause Linking & In-Database Cycle Prevention…, Check if real Supabase credentials are provided in settings., Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 81 - "test_live_supabase_phase3_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 475 - "test_splink_dedup.py"
Cohesion: 0.16
Nodes (15): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., math, Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation. (+7 more)

## Knowledge Gaps
- **78 isolated node(s):** `1. Executive Summary & Scope`, `2. Invariant Rules & Architectural Ground Truth`, `3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`)`, `4.1 2D Planar Laplace Coordinate Perturbation`, `4.2 Temporal Jittering` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 465 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `DeterministicIndicRuleProcessor` to `processor.py`, `jwt.py`, `v1/nlp.py`, `Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `CurrentUserClaims` connect `CurrentUserClaims` to `hierarchy.py`, `v1/gis.py`, `generate_corporator_digest`, `list_staff_members`, `v1/taxonomy.py`, `jwt.py`, `identity.py`, `test_corporator_digest_authorized_ward_success`, `v1/nlp.py`, `StaffRole`, `incidents.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Observation` connect `intake/models.py` to `intake/services.py`, `test_vision_splitting.py`, `incidents.py`, `v1/intake.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `StaffRole` (e.g. with `get_incidents_geojson()` and `create_staff_member()`) actually correct?**
  _`StaffRole` has 12 INFERRED edges - model-reasoned connections that need verification._