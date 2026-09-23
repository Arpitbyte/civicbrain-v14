# Graph Report - CivicBrain  (2026-09-23)

## Corpus Check
- 165 files · ~90,317 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 1235 nodes · 2346 edges · 94 communities (63 shown, 31 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 180 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cbc9c403`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- identity/models.py
- compliance_scanner.py
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
- v1/causal.py
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- identity/services.py
- intake/services.py
- intake/models.py
- schemas/intake.py
- CivicBrain: Complete Reference Document for Frontend Engineers & Designers
- test_taxonomy_governance.py
- analytics/services.py
- test_vision_splitting.py
- create_staff_member
- test_live_supabase_phase2_rls
- analyze_text
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis
- test_hierarchy_api.py
- main.py
- test_rls_organization.py
- public.jan_sunwai_ledger_entry
- test_identity_models.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- submit_photo_intake
- test_health.py
- ULBType
- prioritization.py
- AsyncSession
- DeterministicIndicRuleProcessor
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- compute_nagar_pragati
- test_live_supabase_phase3_rls
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- uuid
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- test_live_supabase_phase5_nlp
- transparency/services.py
- test_live_supabase_rls.py
- os
- test_phase12_pii_scrubbing.py
- audit/__init__.py
- AuthMeResponse
- 0014_performance_indexes.sql
- list_categories
- generate_laplace_dp_perturbation
- is_live_supabase_configured
- test_security_performance_hardening.py
- SecurityHeadersMiddleware
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- logging.py
- test_live_supabase_rbac_rls.py
- test_live_supabase_phase10_analytics_and_corporator_digest
- test_corporator_digest_authorized_ward_success
- patch
- field_validator
- Request
- HonestColdStartDetector
- DedupDecision

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 24 edges
2. `CurrentUserClaims` - 20 edges
3. `Incident` - 20 edges
4. `IncidentStatus` - 18 edges
5. `StaffRole` - 17 edges
6. `test_process_photo_intake_multi_department_splitting()` - 15 edges
7. `CausalGraphService` - 14 edges
8. `IntakeStatus` - 14 edges
9. `Organization` - 14 edges
10. `Base` - 14 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py
- `1. What Was Built` --references--> `RubricLevel`  [INFERRED]
  docs/phase-log/phase-3.md → civicbrain/domain/intake/taxonomy.py
- `1. What Was Built` --references--> `Organization`  [INFERRED]
  docs/phase-log/phase-0.md → civicbrain/domain/identity/models.py

## Import Cycles
- None detected.

## Communities (94 total, 31 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.18
Nodes (14): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+6 more)

### Community 1 - "identity/models.py"
Cohesion: 0.08
Nodes (42): Authentication and user session endpoints., civicbrain_api_v1_dispatch, GIS Core and Spatial Analysis REST Endpoints (§A14)., Administrative hierarchy, department taxonomy, and representative discovery…, FastAPI Operational Incidents Endpoints., API v1 router registry., FastAPI Ingestion and Anonymous Tracking Endpoints., NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11). (+34 more)

### Community 2 - "compliance_scanner.py"
Cohesion: 0.17
Nodes (11): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Path (+3 more)

### Community 3 - "test_gis_core.py"
Cohesion: 0.12
Nodes (27): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, Serve active or filtered operational incidents as GeoJSON FeatureCollection.…, Execute PostGIS ST_ClusterDBSCAN density clustering for civic defect hotspot… (+19 more)

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
Cohesion: 0.20
Nodes (18): BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse, ElectedRepresentativeBase, ElectedRepresentativeCreate, ElectedRepresentativeResponse, OrganizationResponse (+10 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "update_incident_status"
Cohesion: 0.26
Nodes (13): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+5 more)

### Community 30 - "v1/causal.py"
Cohesion: 0.06
Nodes (47): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, CausalGraphService (+39 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "identity/services.py"
Cohesion: 0.16
Nodes (21): ElectedRepresentative, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., UserAccount, UserRoleAssignment, create_staff_user(), get_departments() (+13 more)

### Community 34 - "intake/services.py"
Cohesion: 0.08
Nodes (48): Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), calculate_jaro_winkler_similarity(), Deterministic Jaro-Winkler similarity calculation for cold-start text matching., Citizen intake & observation domain., Incident, IncidentDedupLink, IncidentStatus (+40 more)

### Community 35 - "intake/models.py"
Cohesion: 0.32
Nodes (6): Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, enum, geoalchemy2, sqlalchemy_dialects_postgresql, sqlalchemy_orm

### Community 36 - "schemas/intake.py"
Cohesion: 0.13
Nodes (21): IntakeChannel, ObservationStatus, Citizen reporting channels., Atomic observation state., AnonymousTrackingResponse, BaseSchema, IncidentResponse, IncidentStatusUpdate (+13 more)

### Community 37 - "CivicBrain: Complete Reference Document for Frontend Engineers & Designers"
Cohesion: 0.06
Nodes (31): 1. Project Theme & Pitch, 2.1 Workspace Naming Table (§A5, §A18), 2.2 Plain-English Domain Glossary, 2. Naming & Terminology Glossary, 3.1 Confidence is First-Class, Never Hidden, 3.2 Evidence (Photos & GPS) is Central, Not an Attachment, 3.3 Itemized Score Breakdowns Over Opaque Single Numbers, 3.4 Status is Per-Observation, Never Prematurely Collapsed (+23 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.09
Nodes (29): BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, RubricLevel, SeverityRubric, BaseSchema, BaseModel (+21 more)

### Community 39 - "analytics/services.py"
Cohesion: 0.08
Nodes (39): Base, BaseModel, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot (+31 more)

### Community 40 - "test_vision_splitting.py"
Cohesion: 0.14
Nodes (21): CitizenProfile, Department, Organization, Administrative subdivision of a ULB., Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Citizen identity record verifying phone number without collecting Aadhaar (§A8)., Root tenant representing an Urban Local Body (ULB) or multi-ULB state… (+13 more)

### Community 41 - "create_staff_member"
Cohesion: 0.20
Nodes (14): create_staff_member(), get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, post (+6 more)

### Community 42 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 43 - "analyze_text"
Cohesion: 0.24
Nodes (9): analyze_text(), post, Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint., TextAnalysisRequest (+1 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis"
Cohesion: 0.40
Nodes (4): asyncio, skipif, Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "test_hierarchy_api.py"
Cohesion: 0.23
Nodes (11): create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token., Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization. (+3 more)

### Community 47 - "main.py"
Cohesion: 0.12
Nodes (15): civicbrain_api_v1, global_unhandled_exception_handler(), lifespan(), get, Request, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Catches unhandled exceptions, logging internally without leaking stack traces… (+7 more)

### Community 48 - "test_rls_organization.py"
Cohesion: 0.14
Nodes (13): sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT…, test_client_sdk_rls_anonymous_denial() (+5 more)

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.08
Nodes (36): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+28 more)

### Community 50 - "test_identity_models.py"
Cohesion: 0.17
Nodes (15): CitizenVerificationMethod, Citizen identity verification methods per §A8., CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces. (+7 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "submit_photo_intake"
Cohesion: 0.11
Nodes (21): confirm_report_resolution(), dispute_report_resolution(), Any, AsyncSession, ConfirmResponse, DisputeResponse, get, post (+13 more)

### Community 53 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 54 - "ULBType"
Cohesion: 0.20
Nodes (9): Urban Local Body classification under 74th Constitutional Amendment Act, 1992., ULBType, HierarchyTreeResponse, 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1 (+1 more)

### Community 55 - "prioritization.py"
Cohesion: 0.05
Nodes (57): AHPMatrixConfigRequest, AHPMatrixConfigResponse, CategoryPriorCreate, CategoryPriorResponse, configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card() (+49 more)

### Community 56 - "AsyncSession"
Cohesion: 0.09
Nodes (35): AutoConfirmResponse, adjudicate_dispatch_conflict(), citizen_confirm_report(), create_work_order(), evaluate_auto_confirm_cron(), _get_incidents_for_report(), list_conflicts_for_worker(), list_dispatch_conflicts() (+27 more)

### Community 57 - "DeterministicIndicRuleProcessor"
Cohesion: 0.06
Nodes (32): DeterministicIndicRuleProcessor, NLPProcessor, BaseModel, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics. (+24 more)

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - "compute_nagar_pragati"
Cohesion: 0.22
Nodes (9): CivicAssistantQueryRequest, CivicAssistantQueryResponse, compute_nagar_pragati(), process_civic_assistant_query(), AsyncSession, date, Computes city-wide municipal progress and macro performance scorecard (§A21)., Processes natural language citizen inquiries with deterministic multilingual… (+1 more)

### Community 66 - "test_live_supabase_phase3_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "uuid"
Cohesion: 0.07
Nodes (34): Application configuration via pydantic-settings., Schemas for health and readiness probes., Pydantic schemas for Living Taxonomy Governance and Rubric validation., datetime, postgrest_exceptions, pydantic, pydantic_settings, pytest (+26 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "test_live_supabase_phase5_nlp"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 71 - "transparency/services.py"
Cohesion: 0.15
Nodes (19): civicbrain_domain_transparency_models, compute_entry_hash(), extract_coordinates(), get_incident_ledger_chain(), Any, UUID, Citizen Transparency, Jan Sunwai Ledger, Differential Privacy & Civic Assistant…, Computes deterministic SHA-256 checkpoint hash for per-incident ledger chain… (+11 more)

### Community 72 - "test_live_supabase_rls.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RLS and Auth integration test. In strict accordance with Phase 0…, Check if real Supabase credentials are provided in settings., End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 74 - "test_phase12_pii_scrubbing.py"
Cohesion: 0.20
Nodes (9): civicbrain_schemas_transparency, re, Tests for Pillar 3: DPDP Act 2023 Compliance, PII Scrubbing & Differential…, Verify that JanSunwaiLedgerResponse contains zero citizen PII fields., Verify that DP Laplace perturbation rigorously satisfies minimum privacy…, Verify that civic assistant queries with phone numbers do not echo raw PII., test_civic_assistant_scrubs_phone_numbers_in_responses(), test_dp_perturbation_guarantees_minimum_displacement() (+1 more)

### Community 77 - "AuthMeResponse"
Cohesion: 0.33
Nodes (6): get_my_profile(), AsyncSession, get, Returns the authenticated identity, role assignments, and jurisdictional scopes…, AuthMeResponse, Current authenticated user profile and resolved RBAC scopes.

### Community 78 - "0014_performance_indexes.sql"
Cohesion: 0.10
Nodes (24): idx_causal_established_by, idx_conflict_review_incident_id, idx_conflict_review_reviewed_by, idx_conflict_review_worker_id, idx_js_ledger_cat_code, idx_js_ledger_dept_id, idx_sync_log_org_id, idx_taxonomy_category_dept_id (+16 more)

### Community 79 - "list_categories"
Cohesion: 0.15
Nodes (17): CategoryStatus, approve_category(), list_categories(), propose_category(), AsyncSession, CurrentUserClaims, get, post (+9 more)

### Community 80 - "generate_laplace_dp_perturbation"
Cohesion: 0.67
Nodes (3): generate_laplace_dp_perturbation(), Generates 2D planar Laplace spatial noise and 1D continuous Laplace temporal…, timedelta

### Community 83 - "test_security_performance_hardening.py"
Cohesion: 0.13
Nodes (20): asyncio, cache_delete(), Upstash Redis caching layer for hot, rarely-changing public reads., Deletes cached key upon invalidation. Fails open on error., 2. Verification & Test Evidence, io, json, Comprehensive verification tests for Security and Performance Hardening pass. (+12 more)

### Community 84 - "SecurityHeadersMiddleware"
Cohesion: 0.17
Nodes (8): ASGIApp, Security and hardening ASGI middleware., Injects standard defensive security headers into all HTTP responses. Enforces:…, SecurityHeadersMiddleware, Receive, Scope, Send, starlette_types

### Community 88 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 89 - "logging.py"
Cohesion: 0.19
Nodes (10): PIIScrubbingFilter, Logging infrastructure and automated PII redaction filter., Replaces sensitive citizen PII and credentials with redact labels., Logging filter that scrubs sensitive citizen PII and credentials from all log…, scrub_log_message(), 1. What Was Built & Optimized, Phase 13: Security & Performance Hardening — Implementation Log, LogRecord (+2 more)

### Community 91 - "test_live_supabase_rbac_rls.py"
Cohesion: 0.25
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings., Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 95 - "test_live_supabase_phase10_analytics_and_corporator_digest"
Cohesion: 0.22
Nodes (8): skipif, asyncio, Verify live Supabase report card snapshotting, public anon reads, and…, test_live_supabase_phase10_analytics_and_corporator_digest(), Systematically audits positive and negative paths across all application tables., test_live_supabase_phase12_exhaustive_rls_matrix(), Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 96 - "test_corporator_digest_authorized_ward_success"
Cohesion: 0.15
Nodes (13): asyncio, Verify department load factor increases ETA when backlog spikes., Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives…, Verify Corporator querying their own assigned ward succeeds with alerts and…, Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot., Verify parametric ETA scales with severity and respects confidence intervals., test_corporator_digest_authorized_ward_success(), test_corporator_digest_ward_boundary_rejection() (+5 more)

### Community 134 - "HonestColdStartDetector"
Cohesion: 0.06
Nodes (31): DetectedDefect, FixtureVisionDetector, HonestColdStartDetector, BaseModel, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., Production web detector under zero-GPU and 512MB RAM constraints (Render free… (+23 more)

### Community 475 - "DedupDecision"
Cohesion: 0.20
Nodes (14): evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, DedupDecision, Record linkage determination., Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation., Verify that co-located defect (<=15m) within 72h window and matching category… (+6 more)

## Knowledge Gaps
- **104 isolated node(s):** `1. Project Theme & Pitch`, `2.1 Workspace Naming Table (§A5, §A18)`, `2.2 Plain-English Domain Glossary`, `3.1 Confidence is First-Class, Never Hidden`, `3.2 Evidence (Photos & GPS) is Central, Not an Attachment` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 617 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CorporatorDigestResponse` connect `analytics/services.py` to `Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` connect `Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification` to `analytics/services.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. Project Theme & Pitch`, `2.1 Workspace Naming Table (§A5, §A18)`, `2.2 Plain-English Domain Glossary` to the rest of the system?**
  _104 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `identity/models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08145363408521303 - nodes in this community are weakly interconnected._
- **Should `test_gis_core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11576354679802955 - nodes in this community are weakly interconnected._