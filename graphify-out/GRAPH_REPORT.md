# Graph Report - CivicBrain  (2026-09-22)

## Corpus Check
- 149 files · ~77,624 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 994 nodes · 2002 edges · 81 communities (55 shown, 26 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `490ef23a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- get_my_profile
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
- VisionDetector
- test_vision_splitting.py
- v1/intake.py
- identity/models.py
- CategoryStatus
- analytics/services.py
- test_identity_models.py
- hierarchy.py
- uuid
- v1/__init__.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis
- schemas/intake.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_eta_department_backlog_load
- public.jan_sunwai_ledger_entry
- CurrentUserClaims
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- propose_category
- test_live_supabase_rls_boundary
- test_live_supabase_rbac_rls
- v1/analytics.py
- intake/services.py
- pydantic
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- typing
- DeterministicIndicRuleProcessor
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- test_live_supabase_phase12_exhaustive_rls_matrix
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- test_live_supabase_phase5_nlp
- submit_intake_report
- IncidentStatus
- get_db
- test_live_supabase_phase2_rls
- audit/__init__.py
- test_nlp_analyze_api_auth_enforcement
- test_live_supabase_phase3_rls
- Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification
- DedupDecision

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `CurrentUserClaims` - 22 edges
3. `Incident` - 20 edges
4. `StaffRole` - 20 edges
5. `IncidentStatus` - 20 edges
6. `Organization` - 18 edges
7. `submit_intake_report()` - 18 edges
8. `IntakeStatus` - 16 edges
9. `CategoryStatus` - 15 edges
10. `Department` - 15 edges

## Surprising Connections (you probably didn't know these)
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py
- `5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)` --references--> `CorporatorDigestResponse`  [INFERRED]
  docs/specs/phase-10.md → civicbrain/schemas/analytics.py
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `1. Executive Summary & Scope` --references--> `Zone`  [INFERRED]
  docs/specs/phase-4.md → civicbrain/domain/identity/models.py
- `1. What Was Built` --references--> `RubricLevel`  [INFERRED]
  docs/phase-log/phase-3.md → civicbrain/domain/intake/taxonomy.py

## Import Cycles
- None detected.

## Communities (81 total, 26 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.16
Nodes (16): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+8 more)

### Community 1 - "get_my_profile"
Cohesion: 0.50
Nodes (4): get_my_profile(), AsyncSession, get, Returns the authenticated identity, role assignments, and jurisdictional scopes…

### Community 2 - "test_rls_organization.py"
Cohesion: 0.06
Nodes (33): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Urban Local Body classification under 74th Constitutional Amendment Act, 1992. (+25 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.10
Nodes (32): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+24 more)

### Community 4 - "main.py"
Cohesion: 0.05
Nodes (45): civicbrain_api_v1, Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), lifespan(), get, CivicBrain application entrypoint and ASGI factory. (+37 more)

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
Nodes (21): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse, ElectedRepresentativeBase, ElectedRepresentativeCreate (+13 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.25
Nodes (14): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+6 more)

### Community 30 - "CausalGraphService"
Cohesion: 0.10
Nodes (25): CausalGraphService, CyclicCausalDependencyError, UUID, Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13). Provides:…, Scale root cause priority proportionally to downstream blast radius (§A13).…, Raised when establishing a causal link would introduce a direct or indirect…, Itemized breakdown of root-cause priority boost., Pure CPU directed graph service managing civic causal topology and acyclicity. (+17 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "identity/services.py"
Cohesion: 0.10
Nodes (31): Authentication and user session endpoints., CitizenProfile, Department, ElectedRepresentative, Administrative subdivision of a ULB., Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or… (+23 more)

### Community 34 - "VisionDetector"
Cohesion: 0.13
Nodes (16): DetectedDefect, FixtureVisionDetector, get_vision_detector(), HonestColdStartDetector, BaseModel, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.… (+8 more)

### Community 35 - "test_vision_splitting.py"
Cohesion: 0.16
Nodes (16): Organization, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, IntakeChannel, Citizen reporting channels., asyncio, Unit & integration tests for Computer Vision protocol and Multi-Issue Photo-…, Verify photo splitting pipeline splits defects into atomic observations across…, Verify arbitrary photo in cold start creates an UNCLASSIFIED observation… (+8 more)

### Community 36 - "v1/intake.py"
Cohesion: 0.13
Nodes (19): check_rate_limit(), Any, AsyncSession, get, post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints. (+11 more)

### Community 37 - "identity/models.py"
Cohesion: 0.18
Nodes (14): API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Living Taxonomy Governance REST Endpoints (§A11, Standing Invariant 1)., Phase 7 Domain Models: IncidentCausalLink, CausalRelationType., JWT claims extraction and RBAC security dependencies for Supabase Auth., Identity and Organization domain entities., Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, Database engine, session management, and connectivity diagnostics., collections_abc (+6 more)

### Community 38 - "CategoryStatus"
Cohesion: 0.11
Nodes (25): CategoryStatus, create_default_rubric(), BaseModel, field_validator, Lifecycle status for a taxonomy category., Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories. (+17 more)

### Community 39 - "analytics/services.py"
Cohesion: 0.10
Nodes (30): Base, Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, compute_csi() (+22 more)

### Community 40 - "test_identity_models.py"
Cohesion: 0.23
Nodes (11): CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces., Verify citizen verification methods per §A8., Verify Pydantic request and response schemas. (+3 more)

### Community 41 - "hierarchy.py"
Cohesion: 0.23
Nodes (15): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+7 more)

### Community 42 - "uuid"
Cohesion: 0.08
Nodes (31): Application configuration via pydantic-settings., postgrest_exceptions, pydantic_settings, pytest, supabase, is_live_supabase_configured(), Live Supabase Phase 12 Exhaustive RLS & Privilege Matrix Audit Test Suite. In…, Check if real Supabase credentials are provided in settings. (+23 more)

### Community 43 - "v1/__init__.py"
Cohesion: 0.13
Nodes (16): civicbrain_api_v1_dispatch, API v1 router registry., analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, civicbrain_api_v1_prioritization, get_current_user_claims() (+8 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis"
Cohesion: 0.40
Nodes (4): asyncio, skipif, Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "schemas/intake.py"
Cohesion: 0.16
Nodes (17): AnonymousTrackingResponse, BaseSchema, IncidentResponse, IncidentStatusUpdate, IntakeReportCreate, IntakeReportResponse, ObservationCreate, ObservationResponse (+9 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_eta_department_backlog_load"
Cohesion: 0.18
Nodes (11): asyncio, Verify department load factor increases ETA when backlog spikes., Verify Corporator assigned to Ward 101 attempting to request Ward 102 receives…, Verify Ward Report Card calculates totals, MTTR, CSI, and creates snapshot., Verify parametric ETA scales with severity and respects confidence intervals., test_corporator_digest_ward_boundary_rejection(), mock_execute(), test_eta_department_backlog_load() (+3 more)

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.08
Nodes (35): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+27 more)

### Community 50 - "CurrentUserClaims"
Cohesion: 0.13
Nodes (14): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, CurrentUserClaims, Any, Role-check dependency factory., Parsed and validated claims from Supabase Auth JWT., require_roles() (+6 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "propose_category"
Cohesion: 0.20
Nodes (12): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+4 more)

### Community 53 - "test_live_supabase_rls_boundary"
Cohesion: 0.67
Nodes (3): skipif, End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 54 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 55 - "v1/analytics.py"
Cohesion: 0.08
Nodes (44): AsyncSession, BaseModel, configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession (+36 more)

### Community 56 - "intake/services.py"
Cohesion: 0.14
Nodes (29): Administrative and electoral unit of a ULB representing a Corporator…, Ward, Citizen intake & observation domain., Incident, IncidentDedupLink, IntakeReport, Observation, ObservationStatus (+21 more)

### Community 57 - "pydantic"
Cohesion: 0.22
Nodes (10): CausalRelationType, Causal taxonomy classifying upstream failure modes., CausalLinkResponse, CreateCausalLinkRequest, DownstreamSymptomsResponse, Pydantic schemas for Phase 7 Causal Root-Cause Linking API., Payload to establish a directed causal link from root cause to child symptom., Causal link record response. (+2 more)

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - "typing"
Cohesion: 0.24
Nodes (10): BaseSchema, BaseModel, Pydantic schemas for Living Taxonomy Governance and Rubric validation., Staff/Citizen payload proposing a new civic category., Admin payload approving a proposed category (§A11, Standing Invariant 1). Must…, Taxonomy category output., TaxonomyCategoryApprove, TaxonomyCategoryPropose (+2 more)

### Community 66 - "DeterministicIndicRuleProcessor"
Cohesion: 0.05
Nodes (42): DeterministicIndicRuleProcessor, NLPProcessor, BaseModel, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics. (+34 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "test_live_supabase_phase12_exhaustive_rls_matrix"
Cohesion: 0.33
Nodes (5): skipif, Systematically audits positive and negative paths across all application tables., test_live_supabase_phase12_exhaustive_rls_matrix(), Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "test_live_supabase_phase5_nlp"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 71 - "submit_intake_report"
Cohesion: 0.29
Nodes (9): Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), IntakeStatus, Aggregate lifecycle status for parent citizen intake report., calculate_intake_status_from_children(), Calculates parent intake_report.status based on the least-advanced active child…, Unit tests for Phase 2 domain models, §A16 lifecycle, and least-advanced…, Verify §A7 & Standing Invariant 3 least-advanced aggregation logic. (+1 more)

### Community 72 - "IncidentStatus"
Cohesion: 0.50
Nodes (4): IncidentStatus, Authoritative Incident Lifecycle (§A16 11-State Machine)., Verify incident_status_enum covers all 11 states per §A16., test_incident_status_enum_values()

### Community 73 - "get_db"
Cohesion: 0.67
Nodes (3): get_db(), AsyncSession, Dependency that provides an async session per request.

### Community 74 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 78 - "test_nlp_analyze_api_auth_enforcement"
Cohesion: 0.67
Nodes (3): asyncio, Verify POST /v1/nlp/analyze requires authentication and rejects unauthenticated…, test_nlp_analyze_api_auth_enforcement()

### Community 81 - "test_live_supabase_phase3_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

### Community 134 - "Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification"
Cohesion: 0.12
Nodes (15): 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants, 3.4 Row-Level Security Policies, 3. Database Schema (`migrations/0004_phase3_vision_taxonomy.sql`), 4.1 Living Taxonomy Governance (`civicbrain/domain/intake/taxonomy.py`), 4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`) (+7 more)

### Community 475 - "DedupDecision"
Cohesion: 0.17
Nodes (17): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., DedupDecision, Record linkage determination., math (+9 more)

## Knowledge Gaps
- **80 isolated node(s):** `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)`, `3.2 Observation Table Alterations`, `3.3 Explicit Per-Role Scoped Grants` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 483 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `DeterministicIndicRuleProcessor` to `uuid`, `v1/__init__.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `CurrentUserClaims` connect `CurrentUserClaims` to `identity/services.py`, `get_my_profile`, `v1/gis.py`, `identity/models.py`, `analytics/services.py`, `test_identity_models.py`, `hierarchy.py`, `v1/__init__.py`, `test_eta_department_backlog_load`, `propose_category`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `CorporatorDigestResponse` connect `v1/analytics.py` to `Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification`, `analytics/services.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Workflow: graphify`, `2. Invariant Rules & Architectural Ground Truth`, `3.1 Taxonomy Category Table (`taxonomy_category`)` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._