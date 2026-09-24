# Graph Report - CivicBrain  (2026-09-24)

## Corpus Check
- 278 files · ~134,390 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 56 file(s) not represented in the graph (top: .css 42, .woff2 9, (none) 3)

## Summary
- 2354 nodes · 4838 edges · 137 communities (107 shown, 30 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 639 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `762b43ed`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- analyze_text
- typing
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
- CausalGraphService
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- IncidentDetailView.tsx
- submit_photo_intake
- test_dispatch_workflow.py
- analytics/services.py
- CivicBrain: Complete Reference Document for Frontend Engineers & Designers
- v1/taxonomy.py
- AuthContext.tsx
- package.json
- CivicShowcase.tsx
- StaffRole
- test_offline_sync.py
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_taxonomy_governance.py
- identity/services.py
- dispatch/services.py
- test_security_performance_hardening.py
- public.jan_sunwai_ledger_entry
- SharedQueueTable.tsx
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- identity/models.py
- httpx
- prioritization/models.py
- CurrentUserClaims
- v1/dispatch.py
- pydantic
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- BuhlmannEquityCompensator
- DESIGN.md — CivicBrain Canonical Design System
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- uuid
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- IncidentStatus
- transparency/services.py
- 2. Screen specifications
- os
- test_gis_wards_geojson_empty
- audit/__init__.py
- karmi-sahayak/package.json
- 0014_performance_indexes.sql
- nagrik-setu/package.json
- karmi-sahayak/src/App.tsx
- staff-console/package.json
- SecurityHeadersMiddleware
- cache_set
- main.py
- test_live_supabase_phase4_gis
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Implementation Log
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- README.md
- test_live_supabase_phase5_nlp
- v1/transparency.py
- PrimitivesShowcase.tsx
- public.dispatch_conflict_review
- test_live_supabase_rls_boundary
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log
- exports
- Audit categories & pass criteria
- UI_ARCHITECTURE.md — CivicBrain Frontend Architecture
- public.work_order
- 0011_phase10_analytics_eta.sql
- transparency-board/package.json
- FRONTEND_CONTEXT.md — CivicBrain Frontend Source of Truth
- 3. Hardening & Compliance Implementation Plan
- 0005_phase4_gis_core.sql
- 0007_phase6_ahp_credibility.sql
- ui/package.json
- Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification
- public.incident_causal_link
- Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification
- public.taxonomy_category
- public.staff_bulk_import_log
- api-client/package.json
- i18n/package.json
- get_incidents_geojson
- compilerOptions
- verify_cron_or_admin
- AHPMatrix
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- v1/health.py
- 2. The Six Corrected Design Pillars
- hierarchy.py
- shells/index.ts
- ref_react
- lucide-react
- public.incident
- Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification
- dependencies
- Phase 13: Security & Performance Hardening — Technical Specification
- Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Implementation Log
- test_live_supabase_rbac_rls
- test_live_supabase_phase2_rls
- test_live_supabase_phase7_causal_cycles_and_centrality
- test_live_supabase_phase9_sync_and_adjudication_flow
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- test_live_supabase_phase3_rls

## God Nodes (most connected - your core abstractions)
1. `CurrentUserClaims` - 51 edges
2. `IncidentStatus` - 48 edges
3. `StaffRole` - 45 edges
4. `Incident` - 42 edges
5. `Base` - 36 edges
6. `1. Shared component architecture (`packages/ui`)` - 30 edges
7. `lucide-react` - 29 edges
8. `Department` - 28 edges
9. `WorkOrderStatus` - 27 edges
10. `WorkOrder` - 26 edges

## Surprising Connections (you probably didn't know these)
- `1. What Was Built` --references--> `resolve_work_order()`  [INFERRED]
  docs/phase-log/phase-8.md → civicbrain/domain/dispatch/services.py
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `2. Verification & Test Evidence` --references--> `verify_incident_ledger_chain()`  [INFERRED]
  docs/phase-log/phase-11.md → civicbrain/domain/transparency/services.py
- `6. Verification Plan` --references--> `verify_incident_ledger_chain()`  [INFERRED]
  docs/specs/phase-11.md → civicbrain/domain/transparency/services.py

## Import Cycles
- 3-file cycle: `packages/ui/src/civic/SharedQueueTable.tsx -> packages/ui/src/index.ts -> packages/ui/src/civic/index.ts -> packages/ui/src/civic/SharedQueueTable.tsx`

## Communities (137 total, 30 thin omitted)

### Community 0 - "analyze_text"
Cohesion: 0.24
Nodes (9): analyze_text(), post, Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint., TextAnalysisRequest (+1 more)

### Community 1 - "typing"
Cohesion: 0.09
Nodes (28): DetectedDefect, FixtureVisionDetector, HonestColdStartDetector, BaseModel, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration. (+20 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.06
Nodes (31): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Urban Local Body classification under 74th Constitutional Amendment Act, 1992. (+23 more)

### Community 3 - "test_gis_core.py"
Cohesion: 0.26
Nodes (11): GeoJSONFeature, GeoJSONFeatureCollection, IncidentClusterResponse, BaseModel, Geospatial and GeoJSON schemas for GIS Core (§A14)., RFC 7946 GeoJSON Feature representation., RFC 7946 GeoJSON FeatureCollection representation., Detected defect density hotspot cluster (§A14). (+3 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.11
Nodes (22): fakeredis_aioredis, create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided., Verify /v1/auth/me decodes claims from authenticated token. (+14 more)

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
Cohesion: 0.11
Nodes (34): CitizenVerificationMethod, Citizen identity verification methods per §A8., BaseSchema, BulkImportResponse, BulkImportRowResult, CitizenProfileCreate, CitizenProfileResponse, DepartmentBase (+26 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (6): CivicBrain v14, Core Features, Getting Started, Overview, Phase Architecture, Running Tests & Quality Gates

### Community 29 - "update_incident_status"
Cohesion: 0.26
Nodes (13): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+5 more)

### Community 30 - "CausalGraphService"
Cohesion: 0.05
Nodes (46): create_causal_link(), get_downstream_symptoms(), AsyncSession, get, post, UUID, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff… (+38 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "IncidentDetailView.tsx"
Cohesion: 0.08
Nodes (33): MOCK_FIXTURES, ReportTrackData, TrackDetailView(), getValidNextStatuses(), STATUS_LABELS, VALID_NEXT_STATUS_TRANSITIONS, CausalLinkItem, IncidentDetailData (+25 more)

### Community 34 - "submit_photo_intake"
Cohesion: 0.15
Nodes (16): confirm_report_resolution(), dispute_report_resolution(), Any, AsyncSession, get, post, Request, SupabaseClaims (+8 more)

### Community 35 - "test_dispatch_workflow.py"
Cohesion: 0.11
Nodes (25): asyncio, Unit & Integration Tests for Phase 8 Evidence-Gated Dispatch & Satisfaction…, Verify resolve_work_order rejects whitespace-only notes with 422., Verify field worker attempting to resolve another worker's work order raises…, Verify unauthorized field worker cannot start another worker's work order., Verify resolve_work_order rejects coordinates > 50m away with…, Verify dispatching a work order without token returns 401., Verify citizen confirm returns 404 for invalid tracking token. (+17 more)

### Community 36 - "analytics/services.py"
Cohesion: 0.05
Nodes (70): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, date, get (+62 more)

### Community 37 - "CivicBrain: Complete Reference Document for Frontend Engineers & Designers"
Cohesion: 0.06
Nodes (31): 1. Project Theme & Pitch, 2.1 Workspace Naming Table (§A5, §A18), 2.2 Plain-English Domain Glossary, 2. Naming & Terminology Glossary, 3.1 Confidence is First-Class, Never Hidden, 3.2 Evidence (Photos & GPS) is Central, Not an Attachment, 3.3 Itemized Score Breakdowns Over Opaque Single Numbers, 3.4 Status is Per-Observation, Never Prematurely Collapsed (+23 more)

### Community 38 - "v1/taxonomy.py"
Cohesion: 0.10
Nodes (36): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+28 more)

### Community 39 - "AuthContext.tsx"
Cohesion: 0.15
Nodes (20): RoleSwitcher(), PROMPT 2 — Navigation & Role-Gated Routing, [2026-09-24] — PROMPT 2 — Navigation & Routing (staff-console & all deployables), AuthContext, AuthContextType, AuthProvider(), AuthProviderProps, useAuth() (+12 more)

### Community 40 - "package.json"
Cohesion: 0.08
Nodes (27): devDependencies, @fontsource/ibm-plex-mono, @fontsource/ibm-plex-sans, @fontsource/ibm-plex-sans-devanagari, @fontsource-variable/fraunces, tailwindcss, @tailwindcss/vite, typescript (+19 more)

### Community 41 - "CivicShowcase.tsx"
Cohesion: 0.05
Nodes (71): ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts, Implementation order, PROMPT 0 — Foundation: Tokens & Repo Scaffold, PROMPT 10 — Representative Screen: Control Room · AHP Weight Calibration, PROMPT 11 — Representative Screen: Transparency Board · Nagar Pragati, PROMPT 1 — Shared App Shells, PROMPT 34 — Responsive Refinement Pass, PROMPT 35 — Motion Pass (+63 more)

### Community 42 - "StaffRole"
Cohesion: 0.11
Nodes (32): Staff roles mapped to §A18 named workspaces., StaffRole, 6. Verification Plan & Test Strategy, fixture, io, random, admin_fixture(), create_jwt_token() (+24 more)

### Community 43 - "test_offline_sync.py"
Cohesion: 0.12
Nodes (41): Dispatch and Field Operations Domain Module (§A14, §A15, §A16)., ConflictReviewStatus, DispatchConflictReview, Dispatch and Field Operations Domain Models (§A14, §A15, §A16)., Append-only log of offline client mutations from Karmi Sahayak (§A15)., Supervisor review queue for concurrent dispatch conflicts (§A15)., Work order lifecycle status (§A14, §A16)., Offline mutation synchronization status (§A15). (+33 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "test_taxonomy_governance.py"
Cohesion: 0.13
Nodes (21): BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, RubricLevel, SeverityRubric, Unit tests for Living Taxonomy Governance (§A11, Standing Invariant 1).…, Verify create_default_rubric generates all 5 required tiers with valid criteria… (+13 more)

### Community 46 - "identity/services.py"
Cohesion: 0.10
Nodes (31): get_my_profile(), AsyncSession, get, Authentication and user session endpoints., Returns the authenticated identity, role assignments, and jurisdictional scopes…, CitizenProfile, Staff user account linked to Supabase Auth auth.users., Explicit role assignment for staff users with optional department, zone, or… (+23 more)

### Community 47 - "dispatch/services.py"
Cohesion: 0.13
Nodes (29): citizen_confirm_report(), citizen_dispute_report(), create_work_order(), evaluate_auto_confirm_cron(), _get_incidents_for_report(), list_conflicts_for_worker(), list_dispatch_conflicts(), AsyncSession (+21 more)

### Community 48 - "test_security_performance_hardening.py"
Cohesion: 0.10
Nodes (28): PIIScrubbingFilter, Logging infrastructure and automated PII redaction filter., Replaces sensitive citizen PII and credentials with redact labels., Logging filter that scrubs sensitive citizen PII and credentials from all log…, scrub_log_message(), Any, Overrides redis client (used for testing or dependency injection)., set_redis_client() (+20 more)

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.22
Nodes (14): idx_js_ledger_category, idx_js_ledger_created, idx_js_ledger_geom, idx_js_ledger_org, idx_js_ledger_ward, idx_nagar_pragati_date, idx_nagar_pragati_org, public.jan_sunwai_ledger_entry (+6 more)

### Community 50 - "SharedQueueTable.tsx"
Cohesion: 0.08
Nodes (30): TrackLookupView(), DepartmentQueueView(), MOCK_OPS_WORK_ORDERS, IncidentQueueView(), MOCK_CITY_INCIDENTS, [2026-09-24] — PROMPT 7 — Representative Screen: Ops Board · Department Queue (apps/staff-console), BaseQueueItem, SharedQueueTable() (+22 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "identity/models.py"
Cohesion: 0.10
Nodes (26): GIS Core and Spatial Analysis REST Endpoints (§A14)., Analytics and Service-Time Prediction Domain Module (§A21, §A23)., Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, Department, Identity and Organization domain entities., Administrative subdivision of a ULB. (+18 more)

### Community 53 - "httpx"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 54 - "prioritization/models.py"
Cohesion: 0.29
Nodes (6): Phase 6 Prioritization Domain Models: AHPMatrixConfig, WardEquityCredibility,…, Bühlmann credibility blending expected-vs-observed incident rates per ward., Ward operational SLA and historical resolution telemetry., WardEquityCredibility, WardResolutionStat, sqlalchemy_dialects_postgresql

### Community 55 - "CurrentUserClaims"
Cohesion: 0.08
Nodes (41): API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, API v1 router registry., NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., evaluate_incident_priority(), get_active_ahp_matrix(), get_ward_equity(), AsyncSession, get (+33 more)

### Community 56 - "v1/dispatch.py"
Cohesion: 0.08
Nodes (49): adjudicate_conflict(), create_new_work_order(), execute_field_sync(), get_worker_sync_conflicts(), list_my_work_orders(), list_supervisor_conflicts(), AsyncSession, get (+41 more)

### Community 57 - "pydantic"
Cohesion: 0.13
Nodes (16): DeterministicIndicRuleProcessor, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Deterministic, lightweight multilingual processor optimized for Render free-…, Schemas for health and readiness probes., pydantic, re, asyncio, Unit tests for Phase 5 NLP Pipeline & Emotion-Severity Decoupling (§A11). (+8 more)

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema & Migration (`migrations/0007_phase6_ahp_credibility.sql`), 4.2 REST API Surface (`civicbrain/api/v1/prioritization.py`), 4. Software Architecture & Implementation Design, 5. Verification Plan, Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - "BuhlmannEquityCompensator"
Cohesion: 0.12
Nodes (14): BuhlmannEquityCompensator, Self-calibrating actuarial equity engine., Initialize compensator with provisional parameters pending empirical…, Compute Bühlmann credibility factor Z_i = n_i / (n_i + K). Cold start: n_i = 0…, r"""Compute expected issue rate \hat{\mu}_i = Z_i * X_bar_i + (1 - Z_i) * \mu_0., r"""Compute the deficit Delta_i = max(0, \hat{\mu}_i - O_i)., Derive priority boost beta_i = min(beta_max, gamma * (Delta_i / (expected_rate…, Full evaluation pipeline for a ward's reporting equity. (+6 more)

### Community 66 - "DESIGN.md — CivicBrain Canonical Design System"
Cohesion: 0.10
Nodes (20): 10. Loading — honest, specific, never generic theater, 11. Responsive system, 12. Accessibility — part of the design, not QA, 13. Performance, 14. AI-slop pre-flight — permanent banned-pattern list, 15. Implementation contract — every future Antigravity prompt must include, 1. Art direction — The Benchmark, 2. Visual variation by workspace (+12 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "uuid"
Cohesion: 0.05
Nodes (47): Application configuration via pydantic-settings., Pydantic schemas for Phase 7 Causal Root-Cause Linking API., postgrest_exceptions, pydantic_settings, pytest, supabase, Unit tests for Phase 7 Causal Root-Cause Linking & Incident Graph Centrality…, is_live_supabase_configured() (+39 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "IncidentStatus"
Cohesion: 0.06
Nodes (73): FastAPI Operational Incidents Endpoints., FastAPI Ingestion and Anonymous Tracking Endpoints., Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), calculate_jaro_winkler_similarity(), evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.… (+65 more)

### Community 71 - "transparency/services.py"
Cohesion: 0.07
Nodes (44): Citizen Transparency, Jan Sunwai Public Ledger, Nagar Pragati & Civic Assistant…, JanSunwaiLedgerEntry, NagarPragatiCitySnapshot, Phase 11 Transparency Domain Models: JanSunwaiLedgerEntry,…, Public, tamper-evident civic grievance ledger entry with Differential Privacy…, City-wide municipal progress and transparency dashboard snapshot (§A21)., compute_entry_hash(), compute_nagar_pragati() (+36 more)

### Community 72 - "2. Screen specifications"
Cohesion: 0.07
Nodes (29): 0.1 `apps/nagrik-setu` (public, anon + Phone OTP), 0.2 `apps/staff-console` (authenticated, role-gated — Command Deck / Ops Board / City Pulse / Control Room), 0.3 `apps/karmi-sahayak` (field_worker, offline-first PWA), 0.4 `apps/transparency-board` (Astro, public + corporator auth), 0. Complete sitemap (4 deployables, per `UI_ARCHITECTURE.md` §1), 2.10 Department Queue, 2.11 Work Order Detail, 2.15 My Work Orders (+21 more)

### Community 74 - "test_gis_wards_geojson_empty"
Cohesion: 0.29
Nodes (7): asyncio, Verify GET /v1/gis/wards/geojson returns valid RFC 7946 FeatureCollection for…, Verify GET /v1/gis/incidents/geojson validates bounding-box arguments and…, Verify GET /v1/gis/clusters parameter validation and empty response for non-…, test_gis_clusters_empty_and_param_validation(), test_gis_incidents_geojson_empty_and_bbox_validation(), test_gis_wards_geojson_empty()

### Community 77 - "karmi-sahayak/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 78 - "0014_performance_indexes.sql"
Cohesion: 0.09
Nodes (26): idx_causal_established_by, idx_conflict_review_incident_id, idx_conflict_review_reviewed_by, idx_conflict_review_worker_id, idx_incident_worker_id, idx_js_ledger_cat_code, idx_js_ledger_dept_id, idx_sync_log_org_id (+18 more)

### Community 79 - "nagrik-setu/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 80 - "karmi-sahayak/src/App.tsx"
Cohesion: 0.11
Nodes (14): App(), apps_karmi_sahayak_src_index, root, MyOrdersView(), SyncStatusView(), WorkOrderActionView(), App(), apps_nagrik_setu_src_index (+6 more)

### Community 81 - "staff-console/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 82 - "SecurityHeadersMiddleware"
Cohesion: 0.17
Nodes (8): ASGIApp, Security and hardening ASGI middleware., Injects standard defensive security headers into all HTTP responses. Enforces:…, SecurityHeadersMiddleware, Receive, Scope, Send, starlette_types

### Community 83 - "cache_set"
Cohesion: 0.16
Nodes (13): cache_get(), cache_set(), Any, Upstash Redis caching layer for hot, rarely-changing public reads., Retrieves JSON-deserialized value from Redis cache. Fails open on connection…, Stores JSON-serialized value into Redis cache with specified TTL. Fails open on…, Request, get_redis_client() (+5 more)

### Community 84 - "main.py"
Cohesion: 0.12
Nodes (15): civicbrain_api_v1, global_unhandled_exception_handler(), lifespan(), get, Request, CivicBrain application entrypoint and ASGI factory., Application lifecycle management., Catches unhandled exceptions, logging internally without leaking stack traces… (+7 more)

### Community 85 - "test_live_supabase_phase4_gis"
Cohesion: 0.40
Nodes (4): asyncio, skipif, Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 86 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Implementation Log

### Community 87 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 88 - "README.md"
Cohesion: 0.13
Nodes (10): 1. What Was Built & Hardened, 2. Verification & Test Evidence, 3. Next Phase, Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log, 1. What Was Built, 2. Verification & Test Evidence, Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log, 1. What Was Built (+2 more)

### Community 89 - "test_live_supabase_phase5_nlp"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 90 - "v1/transparency.py"
Cohesion: 0.09
Nodes (38): ask_civic_assistant(), get_incident_chain(), get_nagar_pragati(), get_public_ledger(), AsyncSession, get, post, UUID (+30 more)

### Community 91 - "PrimitivesShowcase.tsx"
Cohesion: 0.04
Nodes (69): PROMPT 3 — Tier 0 Primitives, [2026-09-24] — PROMPT 3 — Tier 0 Primitives (packages/ui), Badge(), BadgeProps, BadgeSize, BadgeVariant, Chip, Checkbox() (+61 more)

### Community 92 - "public.dispatch_conflict_review"
Cohesion: 0.24
Nodes (13): idx_conflict_review_org, idx_conflict_review_status, idx_conflict_review_wo, idx_sync_log_created, idx_sync_log_entity, idx_sync_log_worker, public.dispatch_conflict_review, public.sync_mutation_log (+5 more)

### Community 93 - "test_live_supabase_rls_boundary"
Cohesion: 0.67
Nodes (3): skipif, End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 94 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log

### Community 96 - "exports"
Cohesion: 0.15
Nodes (12): exports, ./components/*, ./fonts, ./primitives, ./semantic, ./tailwind, ./themes/*, files (+4 more)

### Community 97 - "Audit categories & pass criteria"
Cohesion: 0.17
Nodes (11): 1. Design-system compliance, 2. Backend-truth compliance, 3. UX / lifecycle correctness, 4. Responsiveness, 5. Accessibility (WCAG 2.1 AA), 6. Performance, 7. Anti-AI-slop, Audit categories & pass criteria (+3 more)

### Community 98 - "UI_ARCHITECTURE.md — CivicBrain Frontend Architecture"
Cohesion: 0.17
Nodes (11): 10. What's confirmed vs. what needs verification, 1. Deployable apps (not one monolith), 2. Shared packages, 3. Styling implementation, 4. State & data, 5. Offline & sync (Karmi Sahayak + Nagrik Setu draft persistence), 6. Maps / GIS, 7. Accessibility baseline (non-negotiable, all apps) (+3 more)

### Community 99 - "public.work_order"
Cohesion: 0.25
Nodes (10): idx_work_order_incident, idx_work_order_org, idx_work_order_status, idx_work_order_worker, public.work_order, public, public.department, public.incident (+2 more)

### Community 100 - "0011_phase10_analytics_eta.sql"
Cohesion: 0.29
Nodes (10): idx_cat_prior_code, idx_cat_prior_org, idx_wrc_date, idx_wrc_org, idx_wrc_ward, public.category_service_time_prior, public.ward_report_card_snapshot, public (+2 more)

### Community 101 - "transparency-board/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 102 - "FRONTEND_CONTEXT.md — CivicBrain Frontend Source of Truth"
Cohesion: 0.20
Nodes (9): 1. What CivicBrain is, 2. The 7 workspaces (dual-named, distinct cohorts), 3. Entity model (condensed — 25 tables, see reference doc §4 for full ERD), 4. The 11-state incident lifecycle, 5. Roles (6 staff roles + citizen, RLS-enforced), 6. API surface — grouped by workspace, 7. Hard constraints — do not violate, 8. Status of this documentation set (+1 more)

### Community 103 - "3. Hardening & Compliance Implementation Plan"
Cohesion: 0.20
Nodes (9): 1. Executive Summary & Scope, 2. Invariant Rules & Audit Standards, 3.1 Automated Deterministic & AST Compliance Scanner (`tests/test_audit_deterministic_compliance.py`), 3.2 Exhaustive Live RLS & Privilege Matrix Audit (`tests/test_live_supabase_phase12_hardening.py`), 3.3 PII Leakage & DPDP Redaction Verification, 3.4 Production Isolation Verification, 3. Hardening & Compliance Implementation Plan, 4. Verification Plan (+1 more)

### Community 104 - "0005_phase4_gis_core.sql"
Cohesion: 0.20
Nodes (8): idx_incident_geom_gist, idx_intake_report_geom_gist, idx_ward_geom_gist, idx_zone_geom_gist, public.incident, public.intake_report, public.ward, public.zone

### Community 105 - "0007_phase6_ahp_credibility.sql"
Cohesion: 0.36
Nodes (9): idx_ahp_org_active, idx_ward_equity_org_ward, idx_ward_res_stat_ward_cat, public.ahp_matrix_config, public.ward_equity_credibility, public.ward_resolution_stat, public, public.organization (+1 more)

### Community 106 - "ui/package.json"
Cohesion: 0.10
Nodes (19): @civicbrain/design-tokens, react, react-dom, react-router-dom, @types/react, @types/react-dom, main, name (+11 more)

### Community 107 - "Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification"
Cohesion: 0.22
Nodes (8): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0009_phase8_dispatch_evidence.sql`), 4.1 Dispatch & Work Order Operations (`/v1/dispatch/work-orders`), 4.2 Citizen Verification & Satisfaction Loop (`/v1/intake/reports`), 4. REST API Endpoints, 5. Verification Plan, Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification

### Community 108 - "public.incident_causal_link"
Cohesion: 0.31
Nodes (7): idx_causal_org_id, idx_causal_root_id, idx_causal_symptom_id, public.incident_causal_link, public.incident, public.organization, public.user_account

### Community 110 - "Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification"
Cohesion: 0.29
Nodes (6): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0010_phase9_offline_sync.sql`), 4. Conflict Arbitration Matrix (§A15), 6. Verification Plan, Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification

### Community 111 - "public.taxonomy_category"
Cohesion: 0.38
Nodes (6): idx_taxonomy_category_org_dept, idx_taxonomy_category_status, public.taxonomy_category, public, public.department, public.organization

### Community 112 - "public.staff_bulk_import_log"
Cohesion: 0.43
Nodes (6): idx_import_log_admin, idx_import_log_org, public.staff_bulk_import_log, public.organization, public.user_account, uq_import_org_hash_live

### Community 113 - "api-client/package.json"
Cohesion: 0.29
Nodes (6): main, name, private, type, types, version

### Community 114 - "i18n/package.json"
Cohesion: 0.29
Nodes (6): main, name, private, type, types, version

### Community 117 - "get_incidents_geojson"
Cohesion: 0.33
Nodes (9): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, Serve active or filtered operational incidents as GeoJSON FeatureCollection.…, Execute PostGIS ST_ClusterDBSCAN density clustering for civic defect hotspot… (+1 more)

### Community 122 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+9 more)

### Community 123 - "verify_cron_or_admin"
Cohesion: 0.50
Nodes (4): Request, SupabaseClaims, Verifies caller is an automated cron task, service role, or system admin., verify_cron_or_admin()

### Community 124 - "AHPMatrix"
Cohesion: 0.09
Nodes (32): AHPMatrix, AHPResult, calculate_raw_priority(), CriteriaSubscores, Analytic Hierarchy Process (AHP) Engine over 5 Orthogonal Dimensions (§A12).…, Extract principal eigenvector via power iteration in pure Python. Enforces…, Calculate deterministic linear combination raw priority score in [0.0, 1.0].…, The 5 orthogonal incident evaluation sub-scores in [0.0, 1.0]. (+24 more)

### Community 125 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.09
Nodes (19): NLPProcessor, BaseModel, Protocol, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Standard protocol for multilingual civic grievance text analysis., Process incoming citizen grievance text into structured NLP metadata. (+11 more)

### Community 126 - "v1/health.py"
Cohesion: 0.18
Nodes (14): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+6 more)

### Community 127 - "2. The Six Corrected Design Pillars"
Cohesion: 0.12
Nodes (16): 1. Department Creation Endpoint, 1. Executive Summary & Core Requirements, 2. Staff Bulk Import Endpoint, 2. The Six Corrected Design Pillars, 3. Database Schema Changes (`migrations/0015_staff_bulk_import_audit.sql`), 4. API Surface & Schemas, 5. Security & Defensive Hardening, CSV Formula Injection Neutralization (+8 more)

### Community 128 - "hierarchy.py"
Cohesion: 0.07
Nodes (39): bulk_import_users(), create_department(), create_staff_member(), get_hierarchy(), get_representative(), list_departments(), list_staff_members(), normalize_indian_phone() (+31 more)

### Community 129 - "shells/index.ts"
Cohesion: 0.20
Nodes (5): CitizenShellProps, EditorialShellProps, FieldShellProps, StaffConsoleShellProps, StaffWorkspace

### Community 131 - "ref_react"
Cohesion: 0.05
Nodes (45): HomeReportView(), ReportCaptureView(), ReportCategoryView(), ReportLocationView(), ReportReviewView(), ResolutionConfirmView(), ResolutionDisputeView(), App() (+37 more)

### Community 132 - "lucide-react"
Cohesion: 0.11
Nodes (18): BeforeAfterPairProps, ConfidenceBadgeProps, ConfidenceBand, EvidencePhotoCard(), EvidencePhotoCardProps, OfflineSyncBadgeProps, ScoreBreakdownProps, ScoreSubscores (+10 more)

### Community 134 - "Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants, 3.4 Row-Level Security Policies, 3. Database Schema (`migrations/0004_phase3_vision_taxonomy.sql`), 5.1 Automated Unit Tests (+4 more)

### Community 137 - "dependencies"
Cohesion: 0.11
Nodes (17): dependencies, @civicbrain/design-tokens, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-radio-group, @radix-ui/react-select, @radix-ui/react-switch (+9 more)

### Community 138 - "Phase 13: Security & Performance Hardening — Technical Specification"
Cohesion: 0.50
Nodes (3): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Constraints, Phase 13: Security & Performance Hardening — Technical Specification

### Community 139 - "Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Implementation Log

### Community 140 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 141 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 142 - "test_live_supabase_phase7_causal_cycles_and_centrality"
Cohesion: 0.67
Nodes (3): skipif, Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 144 - "test_live_supabase_phase9_sync_and_adjudication_flow"
Cohesion: 0.67
Nodes (3): skipif, Verify live Supabase offline sync constraints, preserved evidence, and…, test_live_supabase_phase9_sync_and_adjudication_flow()

### Community 145 - "Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. Incident Table RLS Audit & Access-Control Regression Fix, 2. What Was Built in Phase 5, 3. Verification & Live Test Evidence, Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

### Community 156 - "test_live_supabase_phase3_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 3 taxonomy category RLS policies, staff proposal check, and admin…, test_live_supabase_phase3_rls()

## Knowledge Gaps
- **464 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+459 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1183 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PrioritizationEvaluationResponse` connect `CurrentUserClaims` to `CivicShowcase.tsx`, `IncidentStatus`?**
  _High betweenness centrality (0.207) - this node is a cross-community bridge._
- **Why does `[2026-09-24] — PROMPT 4 — Tier 1 Civic-Specific Components (packages/ui)` connect `CivicShowcase.tsx` to `IncidentDetailView.tsx`, `lucide-react`, `CurrentUserClaims`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `IncidentStatus` connect `IncidentStatus` to `analytics/services.py`, `transparency/services.py`, `test_offline_sync.py`, `dispatch/services.py`, `identity/models.py`, `get_incidents_geojson`, `CurrentUserClaims`, `AHPMatrix`, `update_incident_status`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `CurrentUserClaims` (e.g. with `configure_category_prior()` and `get_corporator_digest()`) actually correct?**
  _`CurrentUserClaims` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `StaffRole` (e.g. with `configure_category_prior()` and `create_causal_link()`) actually correct?**
  _`StaffRole` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 26 INFERRED edges - model-reasoned connections that need verification._