# Graph Report - CivicBrain  (2026-09-21)

## Corpus Check
- 106 files · ~46,601 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 3, .mdc 1, .example 1)

## Summary
- 828 nodes · 1650 edges · 75 communities (51 shown, 24 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 185 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a24af4d6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- identity/services.py
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
- incidents.py
- CausalGraphService
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- Base
- test_nlp_pipeline.py
- test_vision_splitting.py
- v1/causal.py
- intake/services.py
- TaxonomyCategory
- test_health.py
- identity/models.py
- hierarchy.py
- pytest
- v1/taxonomy.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis.py
- v1/intake.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_identity_models.py
- public.incident_causal_link
- processor.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- v1/nlp.py
- jwt.py
- test_live_supabase_rbac_rls
- graph.py
- schemas/causal.py
- Phase 0: Foundations & Kickoff — Implementation Log
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification
- test_live_supabase_phase5_nlp.py
- public.observation
- public.intake_report
- public.observation
- track_anonymous_report
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- process_photo_intake
- test_live_supabase_phase7_causal.py
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- test_live_supabase_phase3_rls.py
- test_live_supabase_phase2_rls
- DetectedDefect
- test_splink_dedup.py

## God Nodes (most connected - your core abstractions)
1. `process_photo_intake()` - 25 edges
2. `IncidentStatus` - 20 edges
3. `StaffRole` - 20 edges
4. `CurrentUserClaims` - 19 edges
5. `Organization` - 18 edges
6. `submit_intake_report()` - 18 edges
7. `IntakeStatus` - 16 edges
8. `Incident` - 16 edges
9. `CategoryStatus` - 15 edges
10. `test_process_photo_intake_multi_department_splitting()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `1. What Was Built` --references--> `Observation`  [INFERRED]
  docs/phase-log/phase-3.md → civicbrain/domain/intake/models.py
- `1. Executive Summary & Scope` --references--> `Observation`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/models.py
- `4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)` --references--> `DetectedDefect`  [INFERRED]
  docs/specs/phase-3.md → civicbrain/domain/intake/vision.py

## Import Cycles
- None detected.

## Communities (75 total, 24 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.08
Nodes (27): civicbrain_api_v1, health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), API v1 router registry. (+19 more)

### Community 1 - "identity/services.py"
Cohesion: 0.17
Nodes (15): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, CitizenProfile, Citizen identity record verifying phone number without collecting Aadhaar (§A8)., Domain services for identity, administrative hierarchy, and role management. (+7 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.13
Nodes (14): pathlib, sqlalchemy_dialects, sqlalchemy_schema, RLS verification tests for the organization entity. In accordance with Hard…, Verify that migration DDL explicitly enables RLS on organization table., Verify SQLAlchemy model reflects the required columns and ULBType enum., Verify that querying organization via client SDK as anonymous user is denied.…, Verify that querying organization via client SDK with authenticated JWT… (+6 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.11
Nodes (31): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+23 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.10
Nodes (25): Any, Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints. (+17 more)

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
Cohesion: 0.16
Nodes (22): CitizenVerificationMethod, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Citizen identity verification methods per §A8., ULBType, BaseSchema, CitizenProfileResponse, DepartmentBase, DepartmentResponse (+14 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (5): CivicBrain v14, Core Features, Getting Started, Overview, Running Tests

### Community 29 - "incidents.py"
Cohesion: 0.12
Nodes (31): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+23 more)

### Community 30 - "CausalGraphService"
Cohesion: 0.15
Nodes (17): CausalGraphService, CyclicCausalDependencyError, Raised when establishing a causal link would introduce a direct or indirect…, Pure CPU directed graph service managing civic causal topology and acyclicity., Verify adding new_root_id -> new_symptom_id will NOT create any cycles in…, Unit tests for Phase 7 Causal Root-Cause Linking & Incident Graph Centrality…, Verify root cause priority multiplier scales with downstream blast radius…, Verify linking incident A -> A raises CyclicCausalDependencyError. (+9 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "Base"
Cohesion: 0.13
Nodes (16): create_staff_member(), post, Register staff account and assign role with jurisdictional scope within admin's…, ElectedRepresentative, Administrative subdivision of a ULB., Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or…, Corporator/Councillor record scoped to exactly one ward per 74th CAA, 1992. (+8 more)

### Community 34 - "test_nlp_pipeline.py"
Cohesion: 0.15
Nodes (14): DeterministicIndicRuleProcessor, Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Deterministic, lightweight multilingual processor optimized for Render free-…, asyncio, Unit tests for Phase 5 NLP Pipeline & Emotion-Severity Decoupling (§A11)., Verify citizen emotional intensity and anger NEVER inflate physical engineering…, Verify script detection and category resolution across Hindi, Kannada, Tamil,… (+6 more)

### Community 35 - "test_vision_splitting.py"
Cohesion: 0.14
Nodes (20): Department, Organization, Administrative and electoral unit of a ULB representing a Corporator…, Department matching DIGIT's PGR taxonomy (Roads, SWM, Water, Drains,…, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, Ward, ObservationStatus, Atomic observation state. (+12 more)

### Community 36 - "v1/causal.py"
Cohesion: 0.20
Nodes (13): AsyncSession, create_causal_link(), get_downstream_symptoms(), UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff…, IncidentCausalLink (+5 more)

### Community 37 - "intake/services.py"
Cohesion: 0.14
Nodes (24): Citizen intake & observation domain., DedupDecision, Incident, IncidentDedupLink, IntakeReport, IntakeStatus, Observation, Base (+16 more)

### Community 38 - "TaxonomyCategory"
Cohesion: 0.17
Nodes (15): Categorical classification entity governed by living taxonomy rules., TaxonomyCategory, FixtureVisionDetector, get_vision_detector(), HonestColdStartDetector, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.… (+7 more)

### Community 39 - "test_health.py"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 40 - "identity/models.py"
Cohesion: 0.22
Nodes (13): Phase 7 Domain Models: IncidentCausalLink, CausalRelationType., Identity and Organization domain entities., Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, Database engine, session management, and connectivity diagnostics., collections_abc, datetime, enum, geoalchemy2 (+5 more)

### Community 41 - "hierarchy.py"
Cohesion: 0.17
Nodes (21): get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, UUID, Administrative hierarchy, department taxonomy, and representative discovery… (+13 more)

### Community 42 - "pytest"
Cohesion: 0.13
Nodes (14): pytest, supabase, is_live_supabase_configured(), Live Supabase Phase 2 RLS, Anonymous Tracking RPC & Scoped Grants Test Suite.…, Check if real Supabase credentials are provided in settings., is_live_supabase_configured(), Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings. (+6 more)

### Community 43 - "v1/taxonomy.py"
Cohesion: 0.06
Nodes (51): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+43 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_live_supabase_phase4_gis.py"
Cohesion: 0.20
Nodes (8): json, is_live_supabase_configured(), asyncio, skipif, Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test…, Check if real Supabase credentials are provided in settings., Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 46 - "v1/intake.py"
Cohesion: 0.15
Nodes (18): post, SupabaseClaims, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report. 1. Executes spatial containment in ward boundary via…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+10 more)

### Community 47 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 48 - "test_identity_models.py"
Cohesion: 0.23
Nodes (11): CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces., Verify citizen verification methods per §A8., Verify Pydantic request and response schemas. (+3 more)

### Community 49 - "public.incident_causal_link"
Cohesion: 0.10
Nodes (19): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.intake_report (+11 more)

### Community 50 - "processor.py"
Cohesion: 0.17
Nodes (11): NLPProcessor, BaseModel, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Normalized analysis result returned by NLP processing pipeline (§A11)., Standard protocol for multilingual civic grievance text analysis., Process incoming citizen grievance text into structured NLP metadata., TextAnalysisResult (+3 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "v1/nlp.py"
Cohesion: 0.24
Nodes (10): analyze_text(), post, NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint. (+2 more)

### Community 53 - "jwt.py"
Cohesion: 0.14
Nodes (16): CurrentUserClaims, get_current_user_claims(), get_optional_user_claims(), Any, JWT claims extraction and RBAC security dependencies for Supabase Auth., Dependency extracting Supabase JWT claims if present, returning None if…, Role-check dependency factory., Parsed and validated claims from Supabase Auth JWT. (+8 more)

### Community 54 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 55 - "graph.py"
Cohesion: 0.20
Nodes (8): UUID, Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13). Provides:…, Scale root cause priority proportionally to downstream blast radius (§A13).…, Itemized breakdown of root-cause priority boost., Collect all transitively reachable downstream symptom incidents from a root…, RootCauseBoostResult, Domain models and logic for Phase 7 Causal Root-Cause Linking., dataclasses

### Community 56 - "schemas/causal.py"
Cohesion: 0.25
Nodes (10): BaseModel, CausalRelationType, Causal taxonomy classifying upstream failure modes., CausalLinkResponse, CreateCausalLinkRequest, DownstreamSymptomsResponse, Pydantic schemas for Phase 7 Causal Root-Cause Linking API., Payload to establish a directed causal link from root cause to child symptom. (+2 more)

### Community 57 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`), 4. Verification Plan, Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

### Community 60 - "test_live_supabase_phase5_nlp.py"
Cohesion: 0.25
Nodes (7): postgrest_exceptions, is_live_supabase_configured(), skipif, Live Supabase Phase 5 NLP Pipeline & Database Constraints Test Suite (§A11). In…, Check if real Supabase credentials are provided in settings., Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 65 - "track_anonymous_report"
Cohesion: 0.20
Nodes (11): check_rate_limit(), Any, AsyncSession, get, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, Enforces max 10 tracking requests per minute per IP address via Upstash Redis., track_anonymous_report(), get_redis_client() (+3 more)

### Community 66 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.22
Nodes (8): 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 6. Verification Plan, Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

### Community 67 - "process_photo_intake"
Cohesion: 0.39
Nodes (8): process_photo_intake(), AsyncSession, UUID, Evaluates candidate open incidents in the same ward and department using…, Multi-issue photo splitting pipeline (§A6, §A7). 1. Checks spatial containment…, Finds the containing ward for given GPS coordinates via PostGIS ST_Contains., resolve_ward_for_point(), route_and_deduplicate_observation()

### Community 68 - "test_live_supabase_phase7_causal.py"
Cohesion: 0.29
Nodes (6): skipif, is_live_supabase_configured(), Live Supabase Phase 7 Causal Root-Cause Linking & In-Database Cycle Prevention…, Check if real Supabase credentials are provided in settings., Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. Incident Table RLS Audit & Access-Control Regression Fix, 2. What Was Built in Phase 5, 3. Verification & Live Test Evidence, Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

### Community 71 - "test_live_supabase_phase3_rls.py"
Cohesion: 0.50
Nodes (3): is_live_supabase_configured(), Live Supabase Phase 3 Living Taxonomy RLS & Scoped Grants Test Suite. In strict…, Check if real Supabase credentials are provided in settings.

### Community 72 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 134 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 475 - "test_splink_dedup.py"
Cohesion: 0.16
Nodes (15): calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, Deterministic Jaro-Winkler similarity calculation for cold-start text matching., math, Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation. (+7 more)

## Knowledge Gaps
- **61 isolated node(s):** `1. Executive Summary & Scope`, `2. Invariant Rules & Architectural Ground Truth`, `3. Database Schema (`migrations/0008_phase7_causal_graph.sql`)`, `4. Verification Plan`, `Workflow: graphify` (+56 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 410 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DeterministicIndicRuleProcessor` connect `test_nlp_pipeline.py` to `processor.py`, `v1/nlp.py`, `Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `Organization` connect `test_vision_splitting.py` to `Base`, `identity/services.py`, `process_photo_intake`, `test_rls_organization.py`, `intake/services.py`, `identity/models.py`, `hierarchy.py`, `v1/taxonomy.py`, `v1/intake.py`, `Phase 0: Foundations & Kickoff — Implementation Log`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Observation` connect `intake/services.py` to `TaxonomyCategory`, `process_photo_intake`, `incidents.py`, `v1/intake.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `process_photo_intake()` (e.g. with `Department` and `Organization`) actually correct?**
  _`process_photo_intake()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `StaffRole` (e.g. with `get_incidents_geojson()` and `create_staff_member()`) actually correct?**
  _`StaffRole` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CurrentUserClaims` (e.g. with `get_my_profile()` and `get_incidents_geojson()`) actually correct?**
  _`CurrentUserClaims` has 7 INFERRED edges - model-reasoned connections that need verification._