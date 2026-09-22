# Graph Report - CivicBrain  (2026-09-22)

## Corpus Check
- 156 files · ~80,332 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 1199 nodes · 2301 edges · 105 communities (75 shown, 30 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 169 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `51fc93dc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- auth.py
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
- update_incident_status
- CyclicCausalDependencyError
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- identity/services.py
- intake/services.py
- intake/models.py
- IncidentStatusUpdate
- identity/models.py
- test_taxonomy_governance.py
- generate_corporator_digest
- Phase 0: Foundations & Kickoff — Implementation Log
- hierarchy.py
- pytest
- v1/nlp.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- supabase
- test_hierarchy_api.py
- main.py
- test_corporator_digest_authorized_ward_success
- public.jan_sunwai_ledger_entry
- CurrentUserClaims
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- submit_intake_report
- test_health.py
- BaseModel
- get_ward_report_card
- AsyncSession
- test_nlp_pipeline.py
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- processor.py
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- config.py
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- test_live_supabase_phase5_nlp.py
- record_ledger_checkpoint
- test_live_supabase_rls.py
- os
- test_phase12_pii_scrubbing.py
- audit/__init__.py
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- 0014_performance_indexes.sql
- list_categories
- CategoryServiceTimePrior
- prioritization.py
- get_active_ahp_matrix
- test_security_performance_hardening.py
- SecurityHeadersMiddleware
- create_causal_link
- CausalGraphService
- cache_get
- test_identity_models.py
- logging.py
- cache.py
- test_live_supabase_rbac_rls.py
- graph.py
- CausalRelationType
- citizen_dispute_report
- test_live_supabase_phase12_exhaustive_rls_matrix
- test_eta_department_backlog_load
- configure_category_prior
- evaluate_incident_priority
- RateLimiter
- patch
- field_validator
- Request
- VisionDetector
- DedupDecision

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 24 edges
2. `CurrentUserClaims` - 20 edges
3. `Incident` - 20 edges
4. `IncidentStatus` - 18 edges
5. `StaffRole` - 17 edges
6. `test_process_photo_intake_multi_department_splitting()` - 15 edges
7. `CausalGraphService` - 14 edges
8. `Base` - 14 edges
9. `Organization` - 14 edges
10. `IntakeStatus` - 14 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py
- `1. What Was Built` --references--> `ULBType`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (105 total, 30 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.18
Nodes (14): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+6 more)

### Community 1 - "auth.py"
Cohesion: 0.20
Nodes (10): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, get_db(), AsyncSession, Dependency that provides an async session per request. (+2 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.08
Nodes (24): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Path (+16 more)

### Community 3 - "test_gis_core.py"
Cohesion: 0.12
Nodes (27): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, Serve active or filtered operational incidents as GeoJSON FeatureCollection.…, Execute PostGIS ST_ClusterDBSCAN density clustering for civic defect hotspot… (+19 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.18
Nodes (14): Any, Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, asyncio, Integration tests for citizen intake and operational incidents APIs., Verify tracking endpoint returns 404 for nonexistent token., Verify Redis-backed IP rate limiting on anonymous tracking token endpoint. (+6 more)

### Community 5 - "Settings"
Cohesion: 0.33
Nodes (4): BaseSettings, CivicBrain system settings loaded from environment or .env., Settings, field_validator

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

### Community 29 - "update_incident_status"
Cohesion: 0.23
Nodes (15): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+7 more)

### Community 30 - "CyclicCausalDependencyError"
Cohesion: 0.19
Nodes (12): CyclicCausalDependencyError, Raised when establishing a causal link would introduce a direct or indirect…, Unit tests for Phase 7 Causal Root-Cause Linking & Incident Graph Centrality…, Verify root cause priority multiplier scales with downstream blast radius…, Verify linking incident A -> A raises CyclicCausalDependencyError., Verify linking B -> A when A -> B exists raises CyclicCausalDependencyError., Verify 3-node cycle attempt (A -> B -> C -> A) is strictly rejected (Correction…, test_2_node_cycle_rejected() (+4 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "identity/services.py"
Cohesion: 0.14
Nodes (22): CitizenProfile, ElectedRepresentative, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserAccount, UserRoleAssignment (+14 more)

### Community 34 - "intake/services.py"
Cohesion: 0.07
Nodes (61): Department, Organization, Administrative subdivision of a ULB., Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, Zone (+53 more)

### Community 35 - "intake/models.py"
Cohesion: 0.16
Nodes (18): Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Phase 7 Domain Models: IncidentCausalLink, CausalRelationType., Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, Pydantic schemas for Phase 10 Analytics, Ward Report Card, Corporator Digest &…, Pydantic schemas for Phase 7 Causal Root-Cause Linking API., Schemas for health and readiness probes., Pydantic schemas for citizen intake, observation breakdown, and incident… (+10 more)

### Community 36 - "IncidentStatusUpdate"
Cohesion: 0.17
Nodes (12): AnonymousTrackingResponse, BaseSchema, IncidentStatusUpdate, IntakeReportCreate, IntakeReportResponse, ObservationCreate, BaseModel, Observation item provided during report ingestion. (+4 more)

### Community 37 - "identity/models.py"
Cohesion: 0.11
Nodes (32): FastAPI Analytics and ETA Prediction Endpoints (§A21, §A23)., API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, civicbrain_api_v1_dispatch, GIS Core and Spatial Analysis REST Endpoints (§A14)., FastAPI Operational Incidents Endpoints., API v1 router registry., FastAPI Ingestion and Anonymous Tracking Endpoints., Living Taxonomy Governance REST Endpoints (§A11, Standing Invariant 1). (+24 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.07
Nodes (37): create_default_rubric(), BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories., RubricLevel, SeverityRubric (+29 more)

### Community 39 - "generate_corporator_digest"
Cohesion: 0.15
Nodes (17): compute_csi(), compute_ward_report_card(), generate_corporator_digest(), predict_incident_eta(), AsyncSession, CurrentUserClaims, date, UUID (+9 more)

### Community 40 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 41 - "hierarchy.py"
Cohesion: 0.23
Nodes (14): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+6 more)

### Community 42 - "pytest"
Cohesion: 0.25
Nodes (7): pytest, is_live_supabase_configured(), skipif, Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings., Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 43 - "v1/nlp.py"
Cohesion: 0.24
Nodes (10): analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint. (+2 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "supabase"
Cohesion: 0.20
Nodes (8): supabase, is_live_supabase_configured(), asyncio, skipif, Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test…, Check if real Supabase credentials are provided in settings., Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 47 - "main.py"
Cohesion: 0.12
Nodes (15): civicbrain_api_v1, global_unhandled_exception_handler(), lifespan(), get, Request, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Catches unhandled exceptions, logging internally without leaking stack traces… (+7 more)

### Community 48 - "test_corporator_digest_authorized_ward_success"
Cohesion: 0.24
Nodes (8): asyncio, Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives…, Verify Corporator querying their own assigned ward succeeds with alerts and…, Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot., test_corporator_digest_authorized_ward_success(), test_corporator_digest_ward_boundary_rejection(), mock_execute(), test_ward_report_card_computation_and_snapshot()

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.08
Nodes (36): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+28 more)

### Community 50 - "CurrentUserClaims"
Cohesion: 0.12
Nodes (17): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, CurrentUserClaims, get_current_user_claims(), get_optional_user_claims(), Any, Dependency extracting Supabase JWT claims if present, returning None if… (+9 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "submit_intake_report"
Cohesion: 0.09
Nodes (29): confirm_report_resolution(), dispute_report_resolution(), Any, AsyncSession, ConfirmResponse, DisputeResponse, get, post (+21 more)

### Community 53 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 54 - "BaseModel"
Cohesion: 0.15
Nodes (13): BaseModel, CategoryPriorCreate, CategoryPriorResponse, ETAPredictionResponse, Payload to configure or initialize a category service-time prior., Category baseline service-time response., Ward-level municipal scorecard and transparent performance metrics (§A21)., Incident exceeding SLA threshold (> 72 hours). (+5 more)

### Community 55 - "get_ward_report_card"
Cohesion: 0.19
Nodes (16): get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, CurrentUserClaims, date, get (+8 more)

### Community 56 - "AsyncSession"
Cohesion: 0.11
Nodes (29): AutoConfirmResponse, adjudicate_dispatch_conflict(), create_work_order(), evaluate_auto_confirm_cron(), list_conflicts_for_worker(), list_dispatch_conflicts(), process_field_sync(), AsyncSession (+21 more)

### Community 57 - "test_nlp_pipeline.py"
Cohesion: 0.15
Nodes (14): DeterministicIndicRuleProcessor, Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Deterministic, lightweight multilingual processor optimized for Render free-…, asyncio, Unit tests for Phase 5 NLP Pipeline & Emotion-Severity Decoupling (§A11)., Verify citizen emotional intensity and anger NEVER inflate physical engineering…, Verify script detection and category resolution across Hindi, Kannada, Tamil,… (+6 more)

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
Cohesion: 0.18
Nodes (10): NLPProcessor, BaseModel, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Normalized analysis result returned by NLP processing pipeline (§A11)., Standard protocol for multilingual civic grievance text analysis., Process incoming citizen grievance text into structured NLP metadata., TextAnalysisResult (+2 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.13
Nodes (14): CorporatorDigestResponse, Executive operational digest tailored for Ward Elected Representatives (§A18,…, 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23) (+6 more)

### Community 68 - "config.py"
Cohesion: 0.18
Nodes (9): Application configuration via pydantic-settings., postgrest_exceptions, pydantic_settings, is_live_supabase_configured(), Live Supabase Phase 12 Exhaustive RLS & Privilege Matrix Audit Test Suite. In…, Check if real Supabase credentials are provided in settings., is_live_supabase_configured(), Live Supabase Phase 7 Causal Root-Cause Linking & In-Database Cycle Prevention… (+1 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "test_live_supabase_phase5_nlp.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 5 NLP Pipeline & Database Constraints Test Suite (§A11). In…, Check if real Supabase credentials are provided in settings., Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 71 - "record_ledger_checkpoint"
Cohesion: 0.10
Nodes (26): CivicAssistantQueryRequest, CivicAssistantQueryResponse, compute_entry_hash(), compute_nagar_pragati(), extract_coordinates(), generate_laplace_dp_perturbation(), get_incident_ledger_chain(), process_civic_assistant_query() (+18 more)

### Community 72 - "test_live_supabase_rls.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RLS and Auth integration test. In strict accordance with Phase 0…, Check if real Supabase credentials are provided in settings., End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 74 - "test_phase12_pii_scrubbing.py"
Cohesion: 0.22
Nodes (8): civicbrain_schemas_transparency, Tests for Pillar 3: DPDP Act 2023 Compliance, PII Scrubbing & Differential…, Verify that JanSunwaiLedgerResponse contains zero citizen PII fields., Verify that DP Laplace perturbation rigorously satisfies minimum privacy…, Verify that civic assistant queries with phone numbers do not echo raw PII., test_civic_assistant_scrubs_phone_numbers_in_responses(), test_dp_perturbation_guarantees_minimum_displacement(), test_public_ledger_response_schema_pii_absence()

### Community 77 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.22
Nodes (8): 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 6. Verification Plan, Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

### Community 78 - "0014_performance_indexes.sql"
Cohesion: 0.10
Nodes (24): idx_causal_established_by, idx_conflict_review_incident_id, idx_conflict_review_reviewed_by, idx_conflict_review_worker_id, idx_js_ledger_cat_code, idx_js_ledger_dept_id, idx_sync_log_org_id, idx_taxonomy_category_dept_id (+16 more)

### Community 79 - "list_categories"
Cohesion: 0.15
Nodes (17): CategoryStatus, approve_category(), list_categories(), propose_category(), AsyncSession, CurrentUserClaims, get, post (+9 more)

### Community 80 - "CategoryServiceTimePrior"
Cohesion: 0.33
Nodes (6): Base, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot

### Community 81 - "prioritization.py"
Cohesion: 0.33
Nodes (5): API endpoints for Phase 6 AHP Prioritization, Equity Compensator & Confidence…, civicbrain_domain_prioritization_ahp, civicbrain_domain_prioritization_equity, civicbrain_domain_prioritization_gate, civicbrain_schemas_prioritization

### Community 82 - "get_active_ahp_matrix"
Cohesion: 0.21
Nodes (13): AHPMatrixConfigRequest, AHPMatrixConfigResponse, get_active_ahp_matrix(), get_ward_equity(), AsyncSession, CurrentUserClaims, get, UUID (+5 more)

### Community 83 - "test_security_performance_hardening.py"
Cohesion: 0.17
Nodes (13): asyncio, io, Comprehensive verification tests for Security and Performance Hardening pass., 5. Verify generalized IP rate limiter protects POST /v1/intake/reports., 1. Verify standard defensive security headers injected on all HTTP responses., 2. Verify CORS allows only explicit origins and forbids wildcard '*'., 3. Verify unhandled exceptions return generic message without leaking trace or…, 4. Verify photo uploads exceeding 10MB are rejected with 413 Payload Too Large. (+5 more)

### Community 84 - "SecurityHeadersMiddleware"
Cohesion: 0.17
Nodes (8): ASGIApp, Security and hardening ASGI middleware., Injects standard defensive security headers into all HTTP responses. Enforces:…, SecurityHeadersMiddleware, Receive, Scope, Send, starlette_types

### Community 85 - "create_causal_link"
Cohesion: 0.20
Nodes (12): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, IncidentCausalLink, Base (+4 more)

### Community 86 - "CausalGraphService"
Cohesion: 0.20
Nodes (8): CausalGraphService, UUID, Scale root cause priority proportionally to downstream blast radius (§A13).…, Pure CPU directed graph service managing civic causal topology and acyclicity., Verify adding new_root_id -> new_symptom_id will NOT create any cycles in…, Collect all transitively reachable downstream symptom incidents from a root…, Verify valid acyclic DAG with branching and multi-tier downstream collection., test_valid_dag_branching_and_transitive_downstream_collection()

### Community 87 - "cache_get"
Cohesion: 0.21
Nodes (12): cache_delete(), cache_get(), cache_set(), Any, Retrieves JSON-deserialized value from Redis cache. Fails open on connection…, Stores JSON-serialized value into Redis cache with specified TTL. Fails open on…, Deletes cached key upon invalidation. Fails open on error., get_redis_client() (+4 more)

### Community 88 - "test_identity_models.py"
Cohesion: 0.23
Nodes (11): CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces., Verify citizen verification methods per §A8., Verify Pydantic request and response schemas. (+3 more)

### Community 89 - "logging.py"
Cohesion: 0.22
Nodes (9): PIIScrubbingFilter, Logging infrastructure and automated PII redaction filter., Replaces sensitive citizen PII and credentials with redact labels., Logging filter that scrubs sensitive citizen PII and credentials from all log…, scrub_log_message(), LogRecord, re, 7. Verify log-level filter scrubs Aadhaar, phone numbers, emails, and JWTs. (+1 more)

### Community 90 - "cache.py"
Cohesion: 0.25
Nodes (5): Upstash Redis caching layer for hot, rarely-changing public reads., Generalized IP-based rate limiting via Upstash Redis., Upstash Redis connection and rate limiting client., json, redis_asyncio

### Community 91 - "test_live_supabase_rbac_rls.py"
Cohesion: 0.25
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings., Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 92 - "graph.py"
Cohesion: 0.33
Nodes (5): Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13). Provides:…, Itemized breakdown of root-cause priority boost., RootCauseBoostResult, Domain models and logic for Phase 7 Causal Root-Cause Linking., dataclasses

### Community 93 - "CausalRelationType"
Cohesion: 0.33
Nodes (6): CausalRelationType, Causal taxonomy classifying upstream failure modes., CausalLinkResponse, CreateCausalLinkRequest, Payload to establish a directed causal link from root cause to child symptom., Causal link record response.

### Community 94 - "citizen_dispute_report"
Cohesion: 0.33
Nodes (6): citizen_dispute_report(), _get_incidents_for_report(), DisputeResponse, Citizen disputes resolution proof; strictly routes child incidents to APPEALED…, Helper retrieving all child incidents associated with an intake report., Incident

### Community 95 - "test_live_supabase_phase12_exhaustive_rls_matrix"
Cohesion: 0.33
Nodes (5): skipif, Systematically audits positive and negative paths across all application tables., test_live_supabase_phase12_exhaustive_rls_matrix(), Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 96 - "test_eta_department_backlog_load"
Cohesion: 0.33
Nodes (5): Verify department load factor increases ETA when backlog spikes., Verify parametric ETA scales with severity and respects confidence intervals., test_eta_department_backlog_load(), test_eta_prediction_severity_scaling(), mock_execute_side_effect()

### Community 97 - "configure_category_prior"
Cohesion: 0.40
Nodes (5): CategoryPriorCreate, CategoryPriorResponse, configure_category_prior(), post, Configures category baseline service-time priors.

### Community 98 - "evaluate_incident_priority"
Cohesion: 0.40
Nodes (5): evaluate_incident_priority(), post, Compute deterministic glass-box priority score across 5 dimensions and apply…, PrioritizationEvaluationRequest, PrioritizationEvaluationResponse

### Community 99 - "RateLimiter"
Cohesion: 0.40
Nodes (3): Request, RateLimiter, FastAPI dependency for sliding/fixed-window IP rate limiting via Upstash Redis.

### Community 134 - "VisionDetector"
Cohesion: 0.05
Nodes (39): DetectedDefect, FixtureVisionDetector, HonestColdStartDetector, BaseModel, Protocol, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration., Protocol for vision analysis backends. (+31 more)

### Community 475 - "DedupDecision"
Cohesion: 0.18
Nodes (15): evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, DedupDecision, Record linkage determination., math, Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation. (+7 more)

## Knowledge Gaps
- **80 isolated node(s):** `civicbrain`, `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)`, `3.2 Observation Table Alterations` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 591 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `1. Executive Summary & Scope` connect `VisionDetector` to `intake/services.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Observation` connect `intake/services.py` to `intake/models.py`, `identity/models.py`, `VisionDetector`, `submit_intake_report`, `update_incident_status`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `VisionDetector` connect `VisionDetector` to `intake/services.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `civicbrain`, `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_rls_organization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07741935483870968 - nodes in this community are weakly interconnected._