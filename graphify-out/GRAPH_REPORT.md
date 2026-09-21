# Graph Report - CivicBrain  (2026-09-21)

## Corpus Check
- 131 files · ~65,488 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 933 nodes · 1915 edges · 78 communities (54 shown, 24 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e83316da`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FastAPI
- auth.py
- test_rls_organization.py
- v1/gis.py
- main.py
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
- CausalGraphService
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- identity/services.py
- DeterministicIndicRuleProcessor
- test_vision_splitting.py
- v1/causal.py
- intake/services.py
- TaxonomyCategory
- analytics/services.py
- identity/models.py
- hierarchy.py
- jwt.py
- v1/taxonomy.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis
- v1/intake.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_identity_models.py
- public.incident_causal_link
- processor.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- v1/nlp.py
- CurrentUserClaims
- test_live_supabase_rbac_rls
- get_ward_report_card
- intake/models.py
- Phase 0: Foundations & Kickoff — Implementation Log
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- test_live_supabase_phase5_nlp
- public.observation
- public.intake_report
- public.observation
- track_anonymous_report
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- test_live_supabase_phase10_analytics_and_corporator_digest
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- TextAnalysisResult
- test_live_supabase_phase2_rls
- v1/__init__.py
- test_live_supabase_rls_boundary
- test_nlp_analyze_api_auth_enforcement
- DetectedDefect
- DedupDecision

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `CurrentUserClaims` - 22 edges
3. `IncidentStatus` - 20 edges
4. `Incident` - 20 edges
5. `StaffRole` - 20 edges
6. `Organization` - 18 edges
7. `submit_intake_report()` - 18 edges
8. `IntakeStatus` - 16 edges
9. `generate_corporator_digest()` - 15 edges
10. `Department` - 15 edges

## Surprising Connections (you probably didn't know these)
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (78 total, 24 thin omitted)

### Community 0 - "FastAPI"
Cohesion: 0.15
Nodes (17): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+9 more)

### Community 1 - "auth.py"
Cohesion: 0.25
Nodes (8): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, AuthMeResponse, Current authenticated user profile and resolved RBAC scopes., sqlalchemy_ext_asyncio

### Community 2 - "test_rls_organization.py"
Cohesion: 0.13
Nodes (14): pathlib, sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT… (+6 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.10
Nodes (32): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+24 more)

### Community 4 - "main.py"
Cohesion: 0.05
Nodes (46): civicbrain_api_v1, Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), lifespan(), get, CivicBrain application entrypoint and ASGI factory. (+38 more)

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
Cohesion: 0.16
Nodes (22): CitizenVerificationMethod, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Citizen identity verification methods per §A8., ULBType, BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse (+14 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.09
Nodes (33): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+25 more)

### Community 30 - "CausalGraphService"
Cohesion: 0.10
Nodes (25): CausalGraphService, CyclicCausalDependencyError, UUID, Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13). Provides:…, Scale root cause priority proportionally to downstream blast radius (§A13).…, Raised when establishing a causal link would introduce a direct or indirect…, Itemized breakdown of root-cause priority boost., Pure CPU directed graph service managing civic causal topology and acyclicity. (+17 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "identity/services.py"
Cohesion: 0.13
Nodes (26): CitizenProfile, ElectedRepresentative, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserAccount, UserRoleAssignment (+18 more)

### Community 34 - "DeterministicIndicRuleProcessor"
Cohesion: 0.18
Nodes (10): DeterministicIndicRuleProcessor, Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Deterministic, lightweight multilingual processor optimized for Render free-…, Verify citizen emotional intensity and anger NEVER inflate physical engineering…, Verify script detection and category resolution across Hindi, Kannada, Tamil,…, Verify unrecognized text returns suggested_category = None and flags human…, test_cold_start_honesty_on_unrecognized_text() (+2 more)

### Community 35 - "test_vision_splitting.py"
Cohesion: 0.14
Nodes (21): Department, Organization, Administrative subdivision of a ULB., Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, Zone (+13 more)

### Community 36 - "v1/causal.py"
Cohesion: 0.13
Nodes (23): AsyncSession, BaseModel, create_causal_link(), get_downstream_symptoms(), UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff… (+15 more)

### Community 37 - "intake/services.py"
Cohesion: 0.17
Nodes (21): calculate_jaro_winkler_similarity(), Deterministic Jaro-Winkler similarity calculation for cold-start text matching., Citizen intake & observation domain., IncidentDedupLink, IntakeReport, Observation, Base, Atomic localized defect extracted from citizen intake submission. (+13 more)

### Community 38 - "TaxonomyCategory"
Cohesion: 0.17
Nodes (15): Categorical classification entity governed by living taxonomy rules., TaxonomyCategory, FixtureVisionDetector, get_vision_detector(), HonestColdStartDetector, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.… (+7 more)

### Community 39 - "analytics/services.py"
Cohesion: 0.09
Nodes (39): Base, FastAPI Analytics and ETA Prediction Endpoints (§A21, §A23)., Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot (+31 more)

### Community 40 - "identity/models.py"
Cohesion: 0.25
Nodes (8): Identity and Organization domain entities., Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, Database engine, session management, and connectivity diagnostics., collections_abc, enum, sqlalchemy_dialects_postgresql, sqlalchemy_orm, sqlalchemy_pool

### Community 41 - "hierarchy.py"
Cohesion: 0.25
Nodes (13): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+5 more)

### Community 42 - "jwt.py"
Cohesion: 0.08
Nodes (33): JWT claims extraction and RBAC security dependencies for Supabase Auth., Application configuration via pydantic-settings., fastapi_security, postgrest_exceptions, pydantic_settings, pytest, supabase, is_live_supabase_configured() (+25 more)

### Community 43 - "v1/taxonomy.py"
Cohesion: 0.06
Nodes (55): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+47 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis"
Cohesion: 0.40
Nodes (4): asyncio, skipif, Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "v1/intake.py"
Cohesion: 0.13
Nodes (26): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+18 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_identity_models.py"
Cohesion: 0.23
Nodes (11): CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces., Verify citizen verification methods per §A8., Verify Pydantic request and response schemas. (+3 more)

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

### Community 53 - "CurrentUserClaims"
Cohesion: 0.16
Nodes (12): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, CurrentUserClaims, Any, Role-check dependency factory., Parsed and validated claims from Supabase Auth JWT., require_roles() (+4 more)

### Community 54 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 55 - "get_ward_report_card"
Cohesion: 0.16
Nodes (19): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, CurrentUserClaims, date (+11 more)

### Community 56 - "intake/models.py"
Cohesion: 0.21
Nodes (13): IncidentStatus, IntakeStatus, Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Aggregate lifecycle status for parent citizen intake report., Authoritative Incident Lifecycle (§A16 11-State Machine)., calculate_intake_status_from_children(), Calculates parent intake_report.status based on the least-advanced active child…, geoalchemy2 (+5 more)

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

### Community 65 - "track_anonymous_report"
Cohesion: 0.20
Nodes (11): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+3 more)

### Community 66 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.22
Nodes (8): 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 6. Verification Plan, Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "test_live_supabase_phase10_analytics_and_corporator_digest"
Cohesion: 0.33
Nodes (6): skipif, asyncio, Verify live Supabase report card snapshotting, public anon reads, and…, test_live_supabase_phase10_analytics_and_corporator_digest(), Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

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

### Community 75 - "test_nlp_analyze_api_auth_enforcement"
Cohesion: 0.67
Nodes (3): asyncio, Verify POST /v1/nlp/analyze requires authentication and rejects unauthenticated…, test_nlp_analyze_api_auth_enforcement()

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 475 - "DedupDecision"
Cohesion: 0.18
Nodes (15): evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, DedupDecision, Record linkage determination., math, Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation. (+7 more)

## Knowledge Gaps
- **69 isolated node(s):** `1. Executive Summary & Scope`, `2. Invariant Rules & Architectural Ground Truth`, `3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`)`, `4.1 Citizen Satisfaction Index (CSI)`, `4.2 Service-Time / ETA Prediction (§A23)` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 455 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `DeterministicIndicRuleProcessor` to `processor.py`, `v1/nlp.py`, `jwt.py`, `Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `CurrentUserClaims` connect `CurrentUserClaims` to `auth.py`, `v1/gis.py`, `test_live_supabase_phase10_analytics_and_corporator_digest`, `hierarchy.py`, `jwt.py`, `v1/taxonomy.py`, `test_identity_models.py`, `v1/nlp.py`, `incidents.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `Observation` connect `intake/services.py` to `intake/models.py`, `TaxonomyCategory`, `incidents.py`, `v1/intake.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 7 INFERRED edges - model-reasoned connections that need verification._