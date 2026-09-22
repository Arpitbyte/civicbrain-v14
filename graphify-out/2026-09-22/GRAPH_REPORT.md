# Graph Report - CivicBrain  (2026-09-21)

## Corpus Check
- 137 files · ~69,252 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 958 nodes · 1952 edges · 75 communities (51 shown, 24 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c495fc99`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/health.py
- auth.py
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
- identity/models.py
- RubricLevel
- test_vision_splitting.py
- schemas/analytics.py
- uuid
- test_taxonomy_governance.py
- analytics/services.py
- StaffRole
- hierarchy.py
- config.py
- v1/taxonomy.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis
- v1/intake.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_eta_department_backlog_load
- public.jan_sunwai_ledger_entry
- generate_corporator_digest
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- process_photo_intake
- test_live_supabase_rls.py
- test_live_supabase_rbac_rls.py
- v1/analytics.py
- intake/services.py
- Phase 0: Foundations & Kickoff — Implementation Log
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- create_staff_member
- DeterministicIndicRuleProcessor
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- compute_ward_report_card
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- test_live_supabase_phase5_nlp
- main.py
- test_live_supabase_phase3_rls
- DetectedDefect
- DedupDecision

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `CurrentUserClaims` - 22 edges
3. `IncidentStatus` - 20 edges
4. `StaffRole` - 20 edges
5. `Incident` - 20 edges
6. `Organization` - 18 edges
7. `submit_intake_report()` - 18 edges
8. `IntakeStatus` - 16 edges
9. `Department` - 15 edges
10. `CategoryStatus` - 15 edges

## Surprising Connections (you probably didn't know these)
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py
- `1. Executive Summary & Scope` --references--> `Zone`  [INFERRED]
  docs/specs/phase-4.md → civicbrain/domain/identity/models.py
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py

## Import Cycles
- None detected.

## Communities (75 total, 24 thin omitted)

### Community 0 - "v1/health.py"
Cohesion: 0.18
Nodes (14): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+6 more)

### Community 1 - "auth.py"
Cohesion: 0.24
Nodes (10): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, Resolve full profile, role assignments, and active scopes for authenticated…, resolve_user_profile(), AuthMeResponse (+2 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.13
Nodes (14): pathlib, sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT… (+6 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.11
Nodes (29): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+21 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.06
Nodes (38): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+30 more)

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
Nodes (23): CitizenVerificationMethod, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Citizen identity verification methods per §A8., ULBType, BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse (+15 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.15
Nodes (23): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+15 more)

### Community 30 - "v1/causal.py"
Cohesion: 0.07
Nodes (38): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, CausalGraphService (+30 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "identity/models.py"
Cohesion: 0.15
Nodes (19): CitizenProfile, ElectedRepresentative, Identity and Organization domain entities., Administrative subdivision of a ULB., Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992., Citizen identity record verifying phone number without collecting Aadhaar (§A8). (+11 more)

### Community 34 - "RubricLevel"
Cohesion: 0.17
Nodes (15): Concrete physical criteria and baseline severity score for a single rubric tier., RubricLevel, FixtureVisionDetector, get_vision_detector(), HonestColdStartDetector, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.… (+7 more)

### Community 35 - "test_vision_splitting.py"
Cohesion: 0.12
Nodes (22): Organization, Administrative and electoral unit of a ULB representing a Corporator…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, CategoryStatus, create_default_rubric(), Categorical classification entity governed by living taxonomy rules., Lifecycle status for a taxonomy category. (+14 more)

### Community 36 - "schemas/analytics.py"
Cohesion: 0.21
Nodes (12): BaseModel, CategoryPriorCreate, CategoryPriorResponse, CorporatorDigestResponse, Pydantic schemas for Phase 10 Analytics, Ward Report Card, Corporator Digest &…, Payload to configure or initialize a category service-time prior., Category baseline service-time response., Ward-level municipal scorecard and transparent performance metrics (§A21). (+4 more)

### Community 37 - "uuid"
Cohesion: 0.12
Nodes (24): Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Domain models and logic for Phase 7 Causal Root-Cause Linking., CausalRelationType, Phase 7 Domain Models: IncidentCausalLink, CausalRelationType., Causal taxonomy classifying upstream failure modes., Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, Database engine, session management, and connectivity diagnostics., CausalLinkResponse (+16 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.11
Nodes (19): BaseModel, field_validator, Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, SeverityRubric, Unit tests for Living Taxonomy Governance (§A11, Standing Invariant 1).…, Verify create_default_rubric generates all 5 required tiers with valid criteria…, Verify valid 5-level rubric passes schema validation., Verify rubric with fewer than 5 levels is strictly rejected. (+11 more)

### Community 39 - "analytics/services.py"
Cohesion: 0.16
Nodes (15): Base, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, compute_csi(), Analytical and Predictive Domain Services (§A21, §A23). (+7 more)

### Community 40 - "StaffRole"
Cohesion: 0.17
Nodes (15): Staff roles mapped to §A18 named workspaces., StaffRole, CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces. (+7 more)

### Community 41 - "hierarchy.py"
Cohesion: 0.17
Nodes (21): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+13 more)

### Community 42 - "config.py"
Cohesion: 0.09
Nodes (26): Application configuration via pydantic-settings., postgrest_exceptions, pydantic_settings, pytest, supabase, is_live_supabase_configured(), Live Supabase Phase 10 Analytics, Ward Report Card & Corporator Digest Test…, Check if real Supabase credentials are provided in settings. (+18 more)

### Community 43 - "v1/taxonomy.py"
Cohesion: 0.06
Nodes (50): civicbrain_api_v1_dispatch, API v1 router registry., analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, civicbrain_api_v1_prioritization, approve_category() (+42 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis"
Cohesion: 0.40
Nodes (4): asyncio, skipif, Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "v1/intake.py"
Cohesion: 0.12
Nodes (29): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+21 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_eta_department_backlog_load"
Cohesion: 0.22
Nodes (8): asyncio, Verify department load factor increases ETA when backlog spikes., Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot., Verify parametric ETA scales with severity and respects confidence intervals., test_eta_department_backlog_load(), test_eta_prediction_severity_scaling(), mock_execute_side_effect(), test_ward_report_card_computation_and_snapshot()

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.08
Nodes (35): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+27 more)

### Community 50 - "generate_corporator_digest"
Cohesion: 0.25
Nodes (8): generate_corporator_digest(), CurrentUserClaims, Generates an executive operational digest for an elected Corporator (§A18,…, Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives…, Verify Corporator querying their own assigned ward succeeds with alerts and…, test_corporator_digest_authorized_ward_success(), test_corporator_digest_ward_boundary_rejection(), mock_execute()

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "process_photo_intake"
Cohesion: 0.39
Nodes (8): process_photo_intake(), AsyncSession, UUID, Evaluates candidate open incidents in the same ward and department using…, Multi-issue photo splitting pipeline (§A6, §A7). 1. Checks spatial containment…, Finds the containing ward for given GPS coordinates via PostGIS ST_Contains., resolve_ward_for_point(), route_and_deduplicate_observation()

### Community 53 - "test_live_supabase_rls.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RLS and Auth integration test. In strict accordance with Phase 0…, Check if real Supabase credentials are provided in settings., End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 54 - "test_live_supabase_rbac_rls.py"
Cohesion: 0.25
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings., Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 55 - "v1/analytics.py"
Cohesion: 0.19
Nodes (18): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, CurrentUserClaims, date (+10 more)

### Community 56 - "intake/services.py"
Cohesion: 0.16
Nodes (22): Citizen intake & observation domain., IncidentDedupLink, IncidentStatus, IntakeReport, IntakeStatus, Observation, Base, Phase 2 Domain Models: IntakeReport, Observation, Incident, and… (+14 more)

### Community 57 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - "create_staff_member"
Cohesion: 0.67
Nodes (3): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…

### Community 66 - "DeterministicIndicRuleProcessor"
Cohesion: 0.06
Nodes (33): DeterministicIndicRuleProcessor, NLPProcessor, BaseModel, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics. (+25 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "compute_ward_report_card"
Cohesion: 0.18
Nodes (13): compute_ward_report_card(), predict_incident_eta(), AsyncSession, date, UUID, Predicts deterministic empirical resolution hours (ETA) and confidence bounds…, Calculates ward performance scorecard and optionally persists snapshot (§A21)., skipif (+5 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "test_live_supabase_phase5_nlp"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 78 - "main.py"
Cohesion: 0.10
Nodes (20): civicbrain_api_v1, get, CivicBrain application entrypoint and ASGI factory., Redirect or direct reference to API docs., root(), contextlib, fastapi_middleware_cors, httpx (+12 more)

### Community 81 - "test_live_supabase_phase3_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 475 - "DedupDecision"
Cohesion: 0.17
Nodes (17): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., DedupDecision, Record linkage determination., math (+9 more)

## Knowledge Gaps
- **80 isolated node(s):** `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)`, `3.2 Observation Table Alterations`, `3.3 Explicit Per-Role Scoped Grants` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 466 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `DeterministicIndicRuleProcessor` to `v1/taxonomy.py`, `main.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `CurrentUserClaims` connect `v1/taxonomy.py` to `create_staff_member`, `auth.py`, `v1/gis.py`, `compute_ward_report_card`, `StaffRole`, `hierarchy.py`, `generate_corporator_digest`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Observation` connect `intake/services.py` to `RubricLevel`, `process_photo_intake`, `incidents.py`, `v1/intake.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `StaffRole` (e.g. with `get_incidents_geojson()` and `create_staff_member()`) actually correct?**
  _`StaffRole` has 12 INFERRED edges - model-reasoned connections that need verification._