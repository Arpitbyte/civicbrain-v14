# Graph Report - CivicBrain  (2026-09-22)

## Corpus Check
- 150 files · ~78,507 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 995 nodes · 2000 edges · 86 communities (58 shown, 28 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b6ea636a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- auth.py
- test_rls_organization.py
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
- update_incident_status
- v1/causal.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- identity/services.py
- test_vision_splitting.py
- identity/models.py
- v1/intake.py
- analytics/services.py
- v1/taxonomy.py
- generate_corporator_digest
- Phase 0: Foundations & Kickoff — Implementation Log
- list_staff_members
- pytest
- v1/nlp.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis.py
- test_hierarchy_api.py
- main.py
- test_corporator_digest_authorized_ward_success
- public.jan_sunwai_ledger_entry
- CurrentUserClaims
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- track_anonymous_report
- test_health.py
- schemas/analytics.py
- v1/analytics.py
- intake/services.py
- DeterministicIndicRuleProcessor
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- processor.py
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- test_live_supabase_phase12_rls_matrix.py
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- test_live_supabase_phase5_nlp.py
- IncidentStatus
- test_live_supabase_rls.py
- os
- test_phase12_pii_scrubbing.py
- audit/__init__.py
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- test_nlp_analyze_api_auth_enforcement
- process_photo_intake
- CategoryServiceTimePrior
- v1/__init__.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- asyncio
- DetectedDefect
- DedupDecision

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `CurrentUserClaims` - 22 edges
3. `Incident` - 20 edges
4. `IncidentStatus` - 20 edges
5. `StaffRole` - 20 edges
6. `Organization` - 18 edges
7. `submit_intake_report()` - 18 edges
8. `IntakeStatus` - 16 edges
9. `Department` - 15 edges
10. `CategoryStatus` - 15 edges

## Surprising Connections (you probably didn't know these)
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `1. Executive Summary & Scope` --references--> `Zone`  [INFERRED]
  docs/specs/phase-4.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (86 total, 28 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.17
Nodes (15): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+7 more)

### Community 1 - "auth.py"
Cohesion: 0.29
Nodes (7): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, AuthMeResponse, Current authenticated user profile and resolved RBAC scopes.

### Community 2 - "test_rls_organization.py"
Cohesion: 0.08
Nodes (24): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Path (+16 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.12
Nodes (28): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+20 more)

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
Cohesion: 0.12
Nodes (31): CitizenVerificationMethod, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Citizen identity verification methods per §A8., ULBType, BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase (+23 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "update_incident_status"
Cohesion: 0.26
Nodes (13): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+5 more)

### Community 30 - "v1/causal.py"
Cohesion: 0.06
Nodes (49): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, CausalGraphService (+41 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "identity/services.py"
Cohesion: 0.12
Nodes (29): CitizenProfile, ElectedRepresentative, Administrative subdivision of a ULB., Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserAccount (+21 more)

### Community 34 - "test_vision_splitting.py"
Cohesion: 0.09
Nodes (33): Department, Organization, Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, Categorical classification entity governed by living taxonomy rules., TaxonomyCategory (+25 more)

### Community 35 - "identity/models.py"
Cohesion: 0.20
Nodes (12): Administrative hierarchy, department taxonomy, and representative discovery…, Identity and Organization domain entities., get_db(), AsyncSession, Database engine, session management, and connectivity diagnostics., Dependency that provides an async session per request., collections_abc, geoalchemy2 (+4 more)

### Community 36 - "v1/intake.py"
Cohesion: 0.11
Nodes (31): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+23 more)

### Community 37 - "analytics/services.py"
Cohesion: 0.16
Nodes (16): Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Analytical and Predictive Domain Services (§A21, §A23)., civicbrain_domain_dispatch_models, JWT claims extraction and RBAC security dependencies for Supabase Auth., civicbrain_domain_prioritization_models, datetime, FastAPI, fastapi_security (+8 more)

### Community 38 - "v1/taxonomy.py"
Cohesion: 0.05
Nodes (60): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+52 more)

### Community 39 - "generate_corporator_digest"
Cohesion: 0.15
Nodes (17): compute_csi(), compute_ward_report_card(), generate_corporator_digest(), predict_incident_eta(), AsyncSession, CurrentUserClaims, date, UUID (+9 more)

### Community 40 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 41 - "list_staff_members"
Cohesion: 0.27
Nodes (11): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, List staff accounts within the admin's tenant organization. (+3 more)

### Community 42 - "pytest"
Cohesion: 0.12
Nodes (14): pytest, supabase, is_live_supabase_configured(), skipif, Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings., Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls() (+6 more)

### Community 43 - "v1/nlp.py"
Cohesion: 0.24
Nodes (10): analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint. (+2 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis.py"
Cohesion: 0.20
Nodes (8): json, is_live_supabase_configured(), asyncio, skipif, Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test…, Check if real Supabase credentials are provided in settings., Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 47 - "main.py"
Cohesion: 0.20
Nodes (9): civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root(), contextlib (+1 more)

### Community 48 - "test_corporator_digest_authorized_ward_success"
Cohesion: 0.15
Nodes (13): asyncio, Verify department load factor increases ETA when backlog spikes., Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives…, Verify Corporator querying their own assigned ward succeeds with alerts and…, Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot., Verify parametric ETA scales with severity and respects confidence intervals., test_corporator_digest_authorized_ward_success(), test_corporator_digest_ward_boundary_rejection() (+5 more)

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
Cohesion: 0.20
Nodes (11): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+3 more)

### Community 53 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 54 - "schemas/analytics.py"
Cohesion: 0.21
Nodes (12): BaseModel, CategoryPriorCreate, CategoryPriorResponse, ETAPredictionResponse, Pydantic schemas for Phase 10 Analytics, Ward Report Card, Corporator Digest &…, Payload to configure or initialize a category service-time prior., Category baseline service-time response., Ward-level municipal scorecard and transparent performance metrics (§A21). (+4 more)

### Community 55 - "v1/analytics.py"
Cohesion: 0.19
Nodes (18): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, CurrentUserClaims, date (+10 more)

### Community 56 - "intake/services.py"
Cohesion: 0.22
Nodes (15): FastAPI Operational Incidents Endpoints., Citizen intake & observation domain., Incident, IncidentDedupLink, IntakeReport, Observation, Base, Phase 2 Domain Models: IntakeReport, Observation, Incident, and… (+7 more)

### Community 57 - "DeterministicIndicRuleProcessor"
Cohesion: 0.18
Nodes (10): DeterministicIndicRuleProcessor, Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Deterministic, lightweight multilingual processor optimized for Render free-…, Verify citizen emotional intensity and anger NEVER inflate physical engineering…, Verify script detection and category resolution across Hindi, Kannada, Tamil,…, Verify unrecognized text returns suggested_category = None and flags human…, test_cold_start_honesty_on_unrecognized_text() (+2 more)

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

### Community 66 - "processor.py"
Cohesion: 0.17
Nodes (11): NLPProcessor, BaseModel, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Normalized analysis result returned by NLP processing pipeline (§A11)., Standard protocol for multilingual civic grievance text analysis., Process incoming citizen grievance text into structured NLP metadata., TextAnalysisResult (+3 more)

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

### Community 71 - "IncidentStatus"
Cohesion: 0.26
Nodes (11): IncidentStatus, IntakeStatus, Aggregate lifecycle status for parent citizen intake report., Authoritative Incident Lifecycle (§A16 11-State Machine)., calculate_intake_status_from_children(), Calculates parent intake_report.status based on the least-advanced active child…, Unit tests for Phase 2 domain models, §A16 lifecycle, and least-advanced…, Verify incident_status_enum covers all 11 states per §A16. (+3 more)

### Community 72 - "test_live_supabase_rls.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RLS and Auth integration test. In strict accordance with Phase 0…, Check if real Supabase credentials are provided in settings., End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 74 - "test_phase12_pii_scrubbing.py"
Cohesion: 0.20
Nodes (9): civicbrain_domain_transparency_services, civicbrain_schemas_transparency, Tests for Pillar 3: DPDP Act 2023 Compliance, PII Scrubbing & Differential…, Verify that JanSunwaiLedgerResponse contains zero citizen PII fields., Verify that DP Laplace perturbation rigorously satisfies minimum privacy…, Verify that civic assistant queries with phone numbers do not echo raw PII., test_civic_assistant_scrubs_phone_numbers_in_responses(), test_dp_perturbation_guarantees_minimum_displacement() (+1 more)

### Community 77 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.22
Nodes (8): 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 6. Verification Plan, Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

### Community 78 - "test_nlp_analyze_api_auth_enforcement"
Cohesion: 0.67
Nodes (3): asyncio, Verify POST /v1/nlp/analyze requires authentication and rejects unauthenticated…, test_nlp_analyze_api_auth_enforcement()

### Community 79 - "process_photo_intake"
Cohesion: 0.39
Nodes (8): process_photo_intake(), AsyncSession, UUID, Evaluates candidate open incidents in the same ward and department using…, Multi-issue photo splitting pipeline (§A6, §A7). 1. Checks spatial containment…, Finds the containing ward for given GPS coordinates via PostGIS ST_Contains., resolve_ward_for_point(), route_and_deduplicate_observation()

### Community 80 - "CategoryServiceTimePrior"
Cohesion: 0.33
Nodes (6): Base, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot

### Community 81 - "v1/__init__.py"
Cohesion: 0.50
Nodes (3): civicbrain_api_v1_dispatch, API v1 router registry., civicbrain_api_v1_prioritization

### Community 82 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 475 - "DedupDecision"
Cohesion: 0.17
Nodes (17): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., DedupDecision, Record linkage determination., math (+9 more)

## Knowledge Gaps
- **80 isolated node(s):** `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)`, `3.2 Observation Table Alterations`, `3.3 Explicit Per-Role Scoped Grants` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 484 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `DeterministicIndicRuleProcessor` to `Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log`, `processor.py`, `v1/nlp.py`, `analytics/services.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `Organization` connect `test_vision_splitting.py` to `identity/services.py`, `test_rls_organization.py`, `identity/models.py`, `v1/intake.py`, `v1/taxonomy.py`, `Phase 0: Foundations & Kickoff — Implementation Log`, `process_photo_intake`, `intake/services.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `CurrentUserClaims` connect `CurrentUserClaims` to `auth.py`, `v1/gis.py`, `identity/models.py`, `analytics/services.py`, `v1/taxonomy.py`, `generate_corporator_digest`, `list_staff_members`, `v1/nlp.py`, `identity.py`, `test_corporator_digest_authorized_ward_success`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._