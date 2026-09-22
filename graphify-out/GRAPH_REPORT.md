# Graph Report - CivicBrain  (2026-09-22)

## Corpus Check
- 158 files · ~81,912 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 1203 nodes · 2315 edges · 100 communities (70 shown, 30 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 180 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f3253f5e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- jwt.py
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
- update_incident_status
- CausalGraphService
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- hierarchy.py
- intake/services.py
- identity/models.py
- schemas/intake.py
- transparency/services.py
- test_taxonomy_governance.py
- analytics/services.py
- test_vision_splitting.py
- list_staff_members
- supabase
- FastAPI
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis.py
- test_hierarchy_api.py
- main.py
- test_corporator_digest_authorized_ward_success
- public.jan_sunwai_ledger_entry
- StaffRole
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- submit_photo_intake
- test_health.py
- dispute_report_resolution
- get_ward_report_card
- AsyncSession
- DeterministicIndicRuleProcessor
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- TaxonomyCategoryApprove
- test_live_supabase_phase3_rls.py
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- config.py
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- test_live_supabase_phase5_nlp.py
- record_ledger_checkpoint
- test_live_supabase_rls.py
- os
- test_phase12_pii_scrubbing.py
- audit/__init__.py
- global_unhandled_exception_handler
- 0014_performance_indexes.sql
- list_categories
- adjudicate_dispatch_conflict
- prioritization.py
- get_active_ahp_matrix
- test_security_performance_hardening.py
- SecurityHeadersMiddleware
- list_dispatch_conflicts
- process_field_sync
- cache_get
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- logging.py
- test_nlp_analyze_api_auth_enforcement
- pytest
- citizen_confirm_report
- test_live_supabase_phase12_exhaustive_rls_matrix
- test_eta_department_backlog_load
- patch
- field_validator
- Request
- DetectedDefect
- test_splink_dedup.py

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 24 edges
2. `Incident` - 20 edges
3. `CurrentUserClaims` - 20 edges
4. `IncidentStatus` - 18 edges
5. `StaffRole` - 17 edges
6. `test_process_photo_intake_multi_department_splitting()` - 15 edges
7. `Organization` - 14 edges
8. `IntakeStatus` - 14 edges
9. `Base` - 14 edges
10. `CausalGraphService` - 14 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `1. What Was Built & Optimized` --references--> `SecurityHeadersMiddleware`  [INFERRED]
  docs/phase-log/phase-13.md → civicbrain/api/middleware.py
- `2. Verification & Test Evidence` --references--> `test_log_level_pii_scrubbing()`  [INFERRED]
  docs/phase-log/phase-13.md → tests/test_security_performance_hardening.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py

## Import Cycles
- None detected.

## Communities (100 total, 30 thin omitted)

### Community 0 - "jwt.py"
Cohesion: 0.14
Nodes (12): JWT claims extraction and RBAC security dependencies for Supabase Auth., NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, HealthResponse, BaseModel, Schemas for health and readiness probes., Liveness probe response model., Readiness probe response model., ReadinessResponse (+4 more)

### Community 1 - "CurrentUserClaims"
Cohesion: 0.11
Nodes (20): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, CurrentUserClaims, get_current_user_claims(), get_optional_user_claims() (+12 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.06
Nodes (32): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Urban Local Body classification under 74th Constitutional Amendment Act, 1992. (+24 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.12
Nodes (28): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+20 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.15
Nodes (16): Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, redis_asyncio, asyncio, Integration tests for citizen intake and operational incidents APIs. (+8 more)

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
Cohesion: 0.13
Nodes (29): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase, DepartmentCreate, DepartmentResponse (+21 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "update_incident_status"
Cohesion: 0.26
Nodes (13): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+5 more)

### Community 30 - "CausalGraphService"
Cohesion: 0.07
Nodes (37): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, CausalGraphService, CyclicCausalDependencyError (+29 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "hierarchy.py"
Cohesion: 0.15
Nodes (25): get_hierarchy(), Administrative hierarchy, department taxonomy, and representative discovery…, Retrieve complete tree of zones and wards for an organization., CitizenProfile, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Citizen identity record verifying phone number without collecting Aadhaar (§A8)., UserAccount (+17 more)

### Community 34 - "intake/services.py"
Cohesion: 0.10
Nodes (41): FastAPI Operational Incidents Endpoints., Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), calculate_jaro_winkler_similarity(), Deterministic Jaro-Winkler similarity calculation for cold-start text matching., Citizen intake & observation domain., DedupDecision, Incident (+33 more)

### Community 35 - "identity/models.py"
Cohesion: 0.12
Nodes (28): FastAPI Analytics and ETA Prediction Endpoints (§A21, §A23)., API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Living Taxonomy Governance REST Endpoints (§A11, Standing Invariant 1)., Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, CausalRelationType, Phase 7 Domain Models: IncidentCausalLink, CausalRelationType., Causal taxonomy classifying upstream failure modes., Identity and Organization domain entities. (+20 more)

### Community 36 - "schemas/intake.py"
Cohesion: 0.13
Nodes (21): IntakeChannel, IntakeStatus, Citizen reporting channels., Aggregate lifecycle status for parent citizen intake report., AnonymousTrackingResponse, BaseSchema, IncidentResponse, IncidentStatusUpdate (+13 more)

### Community 37 - "transparency/services.py"
Cohesion: 0.17
Nodes (11): FastAPI Ingestion and Anonymous Tracking Endpoints., Dispatch domain services (§A14, §A15, §A16)., civicbrain_domain_prioritization_models, civicbrain_domain_transparency_models, Citizen Transparency, Jan Sunwai Ledger, Differential Privacy & Civic Assistant…, Generalized IP-based rate limiting via Upstash Redis., civicbrain_schemas_dispatch, hashlib (+3 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.11
Nodes (25): CategoryStatus, create_default_rubric(), BaseModel, field_validator, Lifecycle status for a taxonomy category., Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories. (+17 more)

### Community 39 - "analytics/services.py"
Cohesion: 0.07
Nodes (44): Base, BaseModel, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, compute_csi() (+36 more)

### Community 40 - "test_vision_splitting.py"
Cohesion: 0.08
Nodes (39): Department, Organization, Administrative subdivision of a ULB., Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, Zone (+31 more)

### Community 41 - "list_staff_members"
Cohesion: 0.31
Nodes (9): get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, List staff accounts within the admin's tenant organization., List all active departments within the ULB. (+1 more)

### Community 42 - "supabase"
Cohesion: 0.25
Nodes (7): supabase, is_live_supabase_configured(), skipif, Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings., Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 43 - "FastAPI"
Cohesion: 0.11
Nodes (21): civicbrain_api_v1_dispatch, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), API v1 router registry. (+13 more)

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
Cohesion: 0.18
Nodes (10): civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Redirect or direct reference to API docs., root(), contextlib (+2 more)

### Community 48 - "test_corporator_digest_authorized_ward_success"
Cohesion: 0.29
Nodes (7): ElectedRepresentative, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives…, Verify Corporator querying their own assigned ward succeeds with alerts and…, test_corporator_digest_authorized_ward_success(), test_corporator_digest_ward_boundary_rejection(), mock_execute()

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.08
Nodes (36): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+28 more)

### Community 50 - "StaffRole"
Cohesion: 0.20
Nodes (9): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, Role-check dependency factory., require_roles(), Staff roles mapped to §A18 named workspaces., StaffRole, Verify staff_role_enum matches §A18 named workspaces. (+1 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "submit_photo_intake"
Cohesion: 0.17
Nodes (12): Any, get, Request, SupabaseClaims, UUID, Submit photo report with 10MB payload size limit and streaming RAM protection.…, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, submit_photo_intake() (+4 more)

### Community 53 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 54 - "dispute_report_resolution"
Cohesion: 0.25
Nodes (9): confirm_report_resolution(), dispute_report_resolution(), AsyncSession, ConfirmResponse, DisputeResponse, post, Citizen confirms satisfaction with resolved incident(s)., Citizen disputes resolution; strictly routes incident(s) to APPEALED for… (+1 more)

### Community 55 - "get_ward_report_card"
Cohesion: 0.14
Nodes (21): CategoryPriorCreate, CategoryPriorResponse, configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession (+13 more)

### Community 56 - "AsyncSession"
Cohesion: 0.19
Nodes (17): AutoConfirmResponse, create_work_order(), evaluate_auto_confirm_cron(), list_conflicts_for_worker(), AsyncSession, UUID, Field worker marks arrival/start; transitions work order and incident to…, Submits evidence-gated resolution. Enforces: 1. Non-empty photographic evidence… (+9 more)

### Community 57 - "DeterministicIndicRuleProcessor"
Cohesion: 0.06
Nodes (31): DeterministicIndicRuleProcessor, NLPProcessor, BaseModel, Protocol, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Standard protocol for multilingual civic grievance text analysis. (+23 more)

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - "TaxonomyCategoryApprove"
Cohesion: 0.25
Nodes (8): BaseSchema, BaseModel, Staff/Citizen payload proposing a new civic category., Admin payload approving a proposed category (§A11, Standing Invariant 1). Must…, Taxonomy category output., TaxonomyCategoryApprove, TaxonomyCategoryPropose, TaxonomyCategoryResponse

### Community 66 - "test_live_supabase_phase3_rls.py"
Cohesion: 0.25
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 3 Living Taxonomy RLS & Scoped Grants Test Suite. In strict…, Check if real Supabase credentials are provided in settings., Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

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

### Community 77 - "global_unhandled_exception_handler"
Cohesion: 0.33
Nodes (6): global_unhandled_exception_handler(), Request, Catches unhandled exceptions, logging internally without leaking stack traces…, Exception, exception_handler, JSONResponse

### Community 78 - "0014_performance_indexes.sql"
Cohesion: 0.10
Nodes (24): idx_causal_established_by, idx_conflict_review_incident_id, idx_conflict_review_reviewed_by, idx_conflict_review_worker_id, idx_js_ledger_cat_code, idx_js_ledger_dept_id, idx_sync_log_org_id, idx_taxonomy_category_dept_id (+16 more)

### Community 79 - "list_categories"
Cohesion: 0.15
Nodes (17): CategoryStatus, approve_category(), list_categories(), propose_category(), AsyncSession, CurrentUserClaims, get, post (+9 more)

### Community 80 - "adjudicate_dispatch_conflict"
Cohesion: 0.50
Nodes (4): adjudicate_dispatch_conflict(), Supervisory adjudication of concurrent dispatch conflict. -…, ConflictAdjudicationResponse, ConflictDecision

### Community 81 - "prioritization.py"
Cohesion: 0.20
Nodes (10): get_ward_equity(), get, UUID, API endpoints for Phase 6 AHP Prioritization, Equity Compensator & Confidence…, Retrieve ward equity stats, credibility factor, and equity boost., civicbrain_domain_prioritization_ahp, civicbrain_domain_prioritization_equity, civicbrain_domain_prioritization_gate (+2 more)

### Community 82 - "get_active_ahp_matrix"
Cohesion: 0.21
Nodes (13): AHPMatrixConfigRequest, AHPMatrixConfigResponse, evaluate_incident_priority(), get_active_ahp_matrix(), AsyncSession, CurrentUserClaims, post, Retrieve active AHP criteria weights for the caller's organization. (+5 more)

### Community 83 - "test_security_performance_hardening.py"
Cohesion: 0.15
Nodes (17): asyncio, 2. Verification & Test Evidence, Phase 13: Security & Performance Hardening — Implementation Log, io, Comprehensive verification tests for Security and Performance Hardening pass., 5. Verify generalized IP rate limiter protects POST /v1/intake/reports., 8. Verify Upstash Redis caching for hot public reads., 1. Verify standard defensive security headers injected on all HTTP responses. (+9 more)

### Community 84 - "SecurityHeadersMiddleware"
Cohesion: 0.17
Nodes (8): ASGIApp, Security and hardening ASGI middleware., Injects standard defensive security headers into all HTTP responses. Enforces:…, SecurityHeadersMiddleware, Receive, Scope, Send, starlette_types

### Community 85 - "list_dispatch_conflicts"
Cohesion: 0.50
Nodes (4): list_dispatch_conflicts(), Lists reviewable concurrent dispatch conflicts in the supervisor review queue., ConflictReviewStatus, DispatchConflictReview

### Community 86 - "process_field_sync"
Cohesion: 0.50
Nodes (4): process_field_sync(), Executes two-way delta sync for Karmi Sahayak with strict idempotency and…, FieldSyncPushRequest, FieldSyncResponse

### Community 87 - "cache_get"
Cohesion: 0.21
Nodes (11): cache_delete(), cache_get(), cache_set(), Any, Upstash Redis caching layer for hot, rarely-changing public reads., Retrieves JSON-deserialized value from Redis cache. Fails open on connection…, Stores JSON-serialized value into Redis cache with specified TTL. Fails open on…, Deletes cached key upon invalidation. Fails open on error. (+3 more)

### Community 88 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 89 - "logging.py"
Cohesion: 0.15
Nodes (12): PIIScrubbingFilter, Logging infrastructure and automated PII redaction filter., Replaces sensitive citizen PII and credentials with redact labels., Logging filter that scrubs sensitive citizen PII and credentials from all log…, scrub_log_message(), Request, RateLimiter, FastAPI dependency for sliding/fixed-window IP rate limiting via Upstash Redis. (+4 more)

### Community 90 - "test_nlp_analyze_api_auth_enforcement"
Cohesion: 0.67
Nodes (3): asyncio, Verify POST /v1/nlp/analyze requires authentication and rejects unauthenticated…, test_nlp_analyze_api_auth_enforcement()

### Community 91 - "pytest"
Cohesion: 0.22
Nodes (7): pytest, is_live_supabase_configured(), skipif, Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings., Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 94 - "citizen_confirm_report"
Cohesion: 0.22
Nodes (9): citizen_confirm_report(), citizen_dispute_report(), _get_incidents_for_report(), ConfirmResponse, DisputeResponse, Citizen confirms satisfaction with resolution; sets child incidents to…, Citizen disputes resolution proof; strictly routes child incidents to APPEALED…, Helper retrieving all child incidents associated with an intake report. (+1 more)

### Community 95 - "test_live_supabase_phase12_exhaustive_rls_matrix"
Cohesion: 0.33
Nodes (5): skipif, Systematically audits positive and negative paths across all application tables., test_live_supabase_phase12_exhaustive_rls_matrix(), Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 96 - "test_eta_department_backlog_load"
Cohesion: 0.22
Nodes (8): asyncio, Verify department load factor increases ETA when backlog spikes., Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot., Verify parametric ETA scales with severity and respects confidence intervals., test_eta_department_backlog_load(), test_eta_prediction_severity_scaling(), mock_execute_side_effect(), test_ward_report_card_computation_and_snapshot()

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 475 - "test_splink_dedup.py"
Cohesion: 0.17
Nodes (13): evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, math, Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation., Verify that co-located defect (<=15m) within 72h window and matching category…, Verify that far-away defect (>50m) or different category is marked distinct. (+5 more)

## Knowledge Gaps
- **80 isolated node(s):** `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton`, `4. Phase Roadmap (Summary)`, `5. Specific Invariant Rules (v14 Re-derivations)` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 592 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CausalGraphService` connect `CausalGraphService` to `identity/models.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `submit_photo_intake()` connect `submit_photo_intake` to `intake/services.py`, `schemas/intake.py`, `transparency/services.py`, `dispute_report_resolution`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `Incident` connect `intake/services.py` to `test_eta_department_backlog_load`, `v1/gis.py`, `identity/models.py`, `test_corporator_digest_authorized_ward_success`, `update_incident_status`, `CausalGraphService`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. The 17 Hard Rules`, `2. The Bootstrap Principle (Self-Calibrating Intelligence)`, `3. Directory & File Skeleton` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `jwt.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14166666666666666 - nodes in this community are weakly interconnected._