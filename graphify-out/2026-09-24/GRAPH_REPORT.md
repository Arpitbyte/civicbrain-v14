# Graph Report - CivicBrain  (2026-09-24)

## Corpus Check
- 289 files · ~150,616 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 57 file(s) not represented in the graph (top: .css 42, .woff2 9, (none) 3)

## Summary
- 2456 nodes · 5079 edges · 137 communities (106 shown, 31 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 662 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `99a4d496`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pydantic
- HomeReportView.tsx
- test_rls_organization.py
- test_gis_wards_geojson_empty
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
- IncidentDetailView.tsx
- v1/prioritization.py
- bulk_import_users
- test_identity_models.py
- CivicBrain: Complete Reference Document for Frontend Engineers & Designers
- test_taxonomy_governance.py
- AuthContext.tsx
- package.json
- CivicShowcase.tsx
- test_admin_bulk_import.py
- PrimitivesShowcase.tsx
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- get_db
- identity/services.py
- 2. Screen specifications
- v1/taxonomy.py
- public.jan_sunwai_ledger_entry
- v1/dispatch.py
- AhpWeightCalibrationView.tsx
- lucide-react
- uuid
- v1/health.py
- Toast.tsx
- test_nlp_pipeline.py
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- .evaluate_ward
- DESIGN.md — CivicBrain Canonical Design System
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- config.py
- README.md
- citizen_dispute_report
- transparency/services.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- os
- test_eta_department_backlog_load
- audit/__init__.py
- karmi-sahayak/package.json
- 0014_performance_indexes.sql
- nagrik-setu/package.json
- global_unhandled_exception_handler
- staff-console/package.json
- track_anonymous_report
- Phase 0: Foundations & Kickoff — Implementation Log
- main.py
- ui/src/index.ts
- test_live_supabase_phase5_nlp.py
- CurrentUserClaims
- Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log
- hierarchy.py
- IncidentQueueView.tsx
- RateLimiter
- public.dispatch_conflict_review
- test_live_supabase_phase7_causal.py
- test_live_supabase_phase8_dispatch.py
- test_live_supabase_phase9_sync.py
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
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification
- public.incident_causal_link
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log
- Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification
- public.taxonomy_category
- public.staff_bulk_import_log
- api-client/package.json
- i18n/package.json
- test_live_supabase_phase4_gis
- IncidentStatus
- test_live_supabase_admin_bulk_import_and_is_org_admin_rls
- is_live_supabase_configured
- postgrest_exceptions
- CitizenShell
- compilerOptions
- 2. The Six Corrected Design Pillars
- analytics/services.py
- test_live_supabase_rbac_rls.py
- Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log
- ref_react
- public.incident
- ui/package.json
- verify_cron_or_admin
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- .__call__
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- DetectedDefect
- Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Implementation Log

## God Nodes (most connected - your core abstractions)
1. `CurrentUserClaims` - 51 edges
2. `IncidentStatus` - 48 edges
3. `StaffRole` - 45 edges
4. `Incident` - 42 edges
5. `lucide-react` - 40 edges
6. `Base` - 36 edges
7. `1. Shared component architecture (`packages/ui`)` - 30 edges
8. `WorkOrderStatus` - 28 edges
9. `Department` - 28 edges
10. `WorkOrder` - 27 edges

## Surprising Connections (you probably didn't know these)
- `1. What Was Built` --references--> `resolve_work_order()`  [INFERRED]
  docs/phase-log/phase-8.md → civicbrain/domain/dispatch/services.py
- `1. Executive Summary & Scope` --references--> `Zone`  [INFERRED]
  docs/specs/phase-4.md → civicbrain/domain/identity/models.py
- `3. Deviations from Specification` --references--> `DedupDecision`  [INFERRED]
  docs/phase-log/phase-2.md → civicbrain/domain/intake/models.py
- `2. What Was Built in Phase 5` --references--> `DeterministicIndicRuleProcessor`  [INFERRED]
  docs/phase-log/phase-5.md → civicbrain/domain/nlp/processor.py
- `2. Verification & Test Evidence` --references--> `verify_incident_ledger_chain()`  [INFERRED]
  docs/phase-log/phase-11.md → civicbrain/domain/transparency/services.py

## Import Cycles
- 3-file cycle: `packages/ui/src/civic/SharedQueueTable.tsx -> packages/ui/src/index.ts -> packages/ui/src/civic/index.ts -> packages/ui/src/civic/SharedQueueTable.tsx`

## Communities (137 total, 31 thin omitted)

### Community 0 - "pydantic"
Cohesion: 0.22
Nodes (10): analyze_text(), post, Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint., TextAnalysisRequest (+2 more)

### Community 1 - "HomeReportView.tsx"
Cohesion: 0.18
Nodes (15): IntakeStepHeader(), IntakeStepHeaderProps, INITIAL_DRAFT, ReportDraft, ReportDraftContext, ReportDraftContextValue, ReportDraftProvider(), useReportDraft() (+7 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.08
Nodes (23): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Path (+15 more)

### Community 3 - "test_gis_wards_geojson_empty"
Cohesion: 0.29
Nodes (7): asyncio, Verify GET /v1/gis/wards/geojson returns valid RFC 7946 FeatureCollection for…, Verify GET /v1/gis/incidents/geojson validates bounding-box arguments and…, Verify GET /v1/gis/clusters parameter validation and empty response for non-…, test_gis_clusters_empty_and_param_validation(), test_gis_incidents_geojson_empty_and_bbox_validation(), test_gis_wards_geojson_empty()

### Community 4 - "test_intake_api.py"
Cohesion: 0.10
Nodes (25): Any, Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints. (+17 more)

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
Cohesion: 0.15
Nodes (24): CitizenVerificationMethod, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Citizen identity verification methods per §A8., ULBType, BaseSchema, BulkImportRowResult, CitizenProfileResponse, DepartmentBase (+16 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (6): CivicBrain v14, Core Features, Getting Started, Overview, Phase Architecture, Running Tests & Quality Gates

### Community 29 - "incidents.py"
Cohesion: 0.20
Nodes (18): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+10 more)

### Community 30 - "v1/causal.py"
Cohesion: 0.06
Nodes (49): create_causal_link(), get_downstream_symptoms(), AsyncSession, get, post, UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown. (+41 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "IncidentDetailView.tsx"
Cohesion: 0.11
Nodes (24): MOCK_FIXTURES, ReportTrackData, TrackDetailView(), getValidNextStatuses(), STATUS_LABELS, VALID_NEXT_STATUS_TRANSITIONS, CausalLinkItem, IncidentDetailData (+16 more)

### Community 34 - "v1/prioritization.py"
Cohesion: 0.05
Nodes (71): evaluate_incident_priority(), get_active_ahp_matrix(), get_ward_equity(), AsyncSession, get, post, UUID, API endpoints for Phase 6 AHP Prioritization, Equity Compensator & Confidence… (+63 more)

### Community 35 - "bulk_import_users"
Cohesion: 0.10
Nodes (20): bulk_import_users(), normalize_indian_phone(), UploadFile, Bulk import staff users for non-admin operational roles from a CSV file.…, Validate and normalize Indian phone number to E.164 +91XXXXXXXXXX format., Explicit role assignment for staff users with optional department, zone, or…, UserRoleAssignment, Security helpers: CSV formula injection defenses and sanitization. (+12 more)

### Community 36 - "test_identity_models.py"
Cohesion: 0.23
Nodes (11): CitizenProfileCreate, DepartmentCreate, WardCreate, ZoneCreate, Unit tests for Phase 1 identity, hierarchy models, schemas, and JWT parsing., Verify staff_role_enum matches §A18 named workspaces., Verify citizen verification methods per §A8., Verify Pydantic request and response schemas. (+3 more)

### Community 37 - "CivicBrain: Complete Reference Document for Frontend Engineers & Designers"
Cohesion: 0.06
Nodes (31): 1. Project Theme & Pitch, 2.1 Workspace Naming Table (§A5, §A18), 2.2 Plain-English Domain Glossary, 2. Naming & Terminology Glossary, 3.1 Confidence is First-Class, Never Hidden, 3.2 Evidence (Photos & GPS) is Central, Not an Attachment, 3.3 Itemized Score Breakdowns Over Opaque Single Numbers, 3.4 Status is Per-Observation, Never Prematurely Collapsed (+23 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.09
Nodes (29): create_default_rubric(), BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories., RubricLevel, SeverityRubric (+21 more)

### Community 39 - "AuthContext.tsx"
Cohesion: 0.13
Nodes (21): RoleSwitcher(), PROMPT 2 — Navigation & Role-Gated Routing, [2026-09-24] — PROMPT 2 — Navigation & Routing (staff-console & all deployables), AuthContext, AuthContextType, AuthProvider(), AuthProviderProps, useAuth() (+13 more)

### Community 40 - "package.json"
Cohesion: 0.07
Nodes (31): devDependencies, @fontsource/ibm-plex-mono, @fontsource/ibm-plex-sans, @fontsource/ibm-plex-sans-devanagari, @fontsource-variable/fraunces, tailwindcss, @tailwindcss/vite, typescript (+23 more)

### Community 41 - "CivicShowcase.tsx"
Cohesion: 0.05
Nodes (64): ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts, Implementation order, PROMPT 0 — Foundation: Tokens & Repo Scaffold, PROMPT 10 — Representative Screen: Control Room · AHP Weight Calibration, PROMPT 11 — Representative Screen: Transparency Board · Nagar Pragati, PROMPT 34 — Responsive Refinement Pass, PROMPT 35 — Motion Pass, PROMPT 36 — Accessibility Pass (+56 more)

### Community 42 - "test_admin_bulk_import.py"
Cohesion: 0.15
Nodes (22): 6. Verification Plan & Test Strategy, io, random, create_jwt_token(), asyncio, UUID, Tests for Admin Department Creation & Staff Bulk-Import System. Covers: -…, Admin can create a new department; non-admin receives 403; duplicate code… (+14 more)

### Community 43 - "PrimitivesShowcase.tsx"
Cohesion: 0.04
Nodes (65): PROMPT 3 — Tier 0 Primitives, [2026-09-24] — PROMPT 3 — Tier 0 Primitives (packages/ui), 1. Shared component architecture (`packages/ui`), OfflineSyncBadge(), PriorityChip(), Badge(), BadgeProps, BadgeSize (+57 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "get_db"
Cohesion: 0.09
Nodes (26): get_db(), AsyncSession, Dependency that provides an async session per request., PIIScrubbingFilter, Logging infrastructure and automated PII redaction filter., Replaces sensitive citizen PII and credentials with redact labels., Logging filter that scrubs sensitive citizen PII and credentials from all log…, scrub_log_message() (+18 more)

### Community 46 - "identity/services.py"
Cohesion: 0.11
Nodes (29): get_my_profile(), AsyncSession, get, Returns the authenticated identity, role assignments, and jurisdictional scopes…, CitizenProfile, ElectedRepresentative, Administrative subdivision of a ULB., Staff user account linked to Supabase Auth auth.users. (+21 more)

### Community 47 - "2. Screen specifications"
Cohesion: 0.07
Nodes (29): 0.1 `apps/nagrik-setu` (public, anon + Phone OTP), 0.2 `apps/staff-console` (authenticated, role-gated — Command Deck / Ops Board / City Pulse / Control Room), 0.3 `apps/karmi-sahayak` (field_worker, offline-first PWA), 0.4 `apps/transparency-board` (Astro, public + corporator auth), 0. Complete sitemap (4 deployables, per `UI_ARCHITECTURE.md` §1), 2.10 Department Queue, 2.11 Work Order Detail, 2.15 My Work Orders (+21 more)

### Community 48 - "v1/taxonomy.py"
Cohesion: 0.07
Nodes (43): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+35 more)

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.22
Nodes (14): idx_js_ledger_category, idx_js_ledger_created, idx_js_ledger_geom, idx_js_ledger_org, idx_js_ledger_ward, idx_nagar_pragati_date, idx_nagar_pragati_org, public.jan_sunwai_ledger_entry (+6 more)

### Community 50 - "v1/dispatch.py"
Cohesion: 0.04
Nodes (137): adjudicate_conflict(), create_new_work_order(), execute_field_sync(), get_worker_sync_conflicts(), list_my_work_orders(), list_supervisor_conflicts(), list_work_orders(), AsyncSession (+129 more)

### Community 51 - "AhpWeightCalibrationView.tsx"
Cohesion: 0.29
Nodes (9): AHPResult, CRITERIA_DEFINITIONS, CRITERIA_KEYS, CriteriaKey, CriteriaMeta, DEFAULT_AHP_MATRIX, SAATY_RI_5, solveAHPMatrix() (+1 more)

### Community 52 - "lucide-react"
Cohesion: 0.05
Nodes (48): ClusterAccessibleListView(), ClusterAccessibleListViewProps, ClusterData, ClusterStatsPanel(), ClusterStatsPanelProps, CoordinateRulerFrame(), CoordinateRulerFrameProps, IncidentCluster (+40 more)

### Community 53 - "uuid"
Cohesion: 0.14
Nodes (24): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+16 more)

### Community 54 - "v1/health.py"
Cohesion: 0.18
Nodes (14): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+6 more)

### Community 55 - "Toast.tsx"
Cohesion: 0.22
Nodes (7): TrackingTokenDisplayProps, ToastContext, ToastContextType, ToastItem, ToastProvider(), ToastVariant, @radix-ui/react-toast

### Community 56 - "test_nlp_pipeline.py"
Cohesion: 0.13
Nodes (17): DeterministicIndicRuleProcessor, NLPProcessor, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Standard protocol for multilingual civic grievance text analysis., Deterministic, lightweight multilingual processor optimized for Render free-…, 1. Executive Summary & Scope, asyncio (+9 more)

### Community 57 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.11
Nodes (15): BaseModel, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Process incoming citizen grievance text into structured NLP metadata., TextAnalysisResult, 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata (+7 more)

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema & Migration (`migrations/0007_phase6_ahp_credibility.sql`), 4.2 REST API Surface (`civicbrain/api/v1/prioritization.py`), 4. Software Architecture & Implementation Design, 5. Verification Plan, Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - ".evaluate_ward"
Cohesion: 0.20
Nodes (5): Compute Bühlmann credibility factor Z_i = n_i / (n_i + K). Cold start: n_i = 0…, r"""Compute expected issue rate \hat{\mu}_i = Z_i * X_bar_i + (1 - Z_i) * \mu_0., r"""Compute the deficit Delta_i = max(0, \hat{\mu}_i - O_i)., Derive priority boost beta_i = min(beta_max, gamma * (Delta_i / (expected_rate…, Full evaluation pipeline for a ward's reporting equity.

### Community 66 - "DESIGN.md — CivicBrain Canonical Design System"
Cohesion: 0.10
Nodes (20): 10. Loading — honest, specific, never generic theater, 11. Responsive system, 12. Accessibility — part of the design, not QA, 13. Performance, 14. AI-slop pre-flight — permanent banned-pattern list, 15. Implementation contract — every future Antigravity prompt must include, 1. Art direction — The Benchmark, 2. Visual variation by workspace (+12 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "config.py"
Cohesion: 0.07
Nodes (30): Application configuration via pydantic-settings., Supabase Admin Client provider., httpx, json, pydantic_settings, pytest, supabase, asyncio (+22 more)

### Community 69 - "README.md"
Cohesion: 0.14
Nodes (9): 1. What Was Built, 2. Verification & Test Evidence, Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Implementation Log, 1. What Was Built, 2. Verification & Test Evidence, Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log, 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Constraints (+1 more)

### Community 70 - "citizen_dispute_report"
Cohesion: 0.22
Nodes (10): confirm_report_resolution(), dispute_report_resolution(), AsyncSession, post, Citizen confirms satisfaction with resolved incident(s)., Citizen disputes resolution; strictly routes incident(s) to APPEALED for…, citizen_dispute_report(), Citizen disputes resolution proof; strictly routes child incidents to APPEALED… (+2 more)

### Community 71 - "transparency/services.py"
Cohesion: 0.05
Nodes (83): ask_civic_assistant(), get_incident_chain(), get_nagar_pragati(), get_public_ledger(), AsyncSession, get, post, UUID (+75 more)

### Community 72 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 74 - "test_eta_department_backlog_load"
Cohesion: 0.33
Nodes (6): asyncio, Verify department load factor increases ETA when backlog spikes., Verify parametric ETA scales with severity and respects confidence intervals., test_eta_department_backlog_load(), test_eta_prediction_severity_scaling(), mock_execute_side_effect()

### Community 77 - "karmi-sahayak/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 78 - "0014_performance_indexes.sql"
Cohesion: 0.09
Nodes (26): idx_causal_established_by, idx_conflict_review_incident_id, idx_conflict_review_reviewed_by, idx_conflict_review_worker_id, idx_incident_worker_id, idx_js_ledger_cat_code, idx_js_ledger_dept_id, idx_sync_log_org_id (+18 more)

### Community 79 - "nagrik-setu/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 80 - "global_unhandled_exception_handler"
Cohesion: 0.33
Nodes (6): global_unhandled_exception_handler(), Request, Catches unhandled exceptions, logging internally without leaking stack traces…, Exception, exception_handler, JSONResponse

### Community 81 - "staff-console/package.json"
Cohesion: 0.06
Nodes (32): dependencies, @civicbrain/design-tokens, @civicbrain/ui, gsap, leaflet, react, react-dom, react-router-dom (+24 more)

### Community 82 - "track_anonymous_report"
Cohesion: 0.40
Nodes (5): Any, get, Request, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, track_anonymous_report()

### Community 83 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.33
Nodes (5): 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 84 - "main.py"
Cohesion: 0.12
Nodes (14): ASGIApp, Security and hardening ASGI middleware., Injects standard defensive security headers into all HTTP responses. Enforces:…, SecurityHeadersMiddleware, civicbrain_api_v1, lifespan(), get, CivicBrain application entrypoint and ASGI factory. (+6 more)

### Community 85 - "ui/src/index.ts"
Cohesion: 0.16
Nodes (18): FieldLayout(), OfflineSyncContext, OfflineSyncContextValue, OfflineSyncProvider(), useOfflineSync(), getQueuedMutations(), QueuedMutation, removeMutation() (+10 more)

### Community 86 - "test_live_supabase_phase5_nlp.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 5 NLP Pipeline & Database Constraints Test Suite (§A11). In…, Check if real Supabase credentials are provided in settings., Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 87 - "CurrentUserClaims"
Cohesion: 0.06
Nodes (59): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, date, get (+51 more)

### Community 88 - "Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built & Hardened, 2. Verification & Test Evidence, 3. Next Phase, Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log

### Community 89 - "hierarchy.py"
Cohesion: 0.15
Nodes (22): create_department(), create_staff_member(), get_hierarchy(), get_representative(), list_departments(), list_organizations(), list_staff_members(), AsyncSession (+14 more)

### Community 90 - "IncidentQueueView.tsx"
Cohesion: 0.08
Nodes (26): TrackLookupView(), Department, DepartmentQueueView(), LiveWorkOrder, Organization, timeAgo(), CATEGORY_NAMES_HI, Department (+18 more)

### Community 91 - "RateLimiter"
Cohesion: 0.40
Nodes (3): Request, RateLimiter, FastAPI dependency for sliding/fixed-window IP rate limiting via Upstash Redis.

### Community 92 - "public.dispatch_conflict_review"
Cohesion: 0.24
Nodes (13): idx_conflict_review_org, idx_conflict_review_status, idx_conflict_review_wo, idx_sync_log_created, idx_sync_log_entity, idx_sync_log_worker, public.dispatch_conflict_review, public.sync_mutation_log (+5 more)

### Community 93 - "test_live_supabase_phase7_causal.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 7 Causal Root-Cause Linking & In-Database Cycle Prevention…, Check if real Supabase credentials are provided in settings., Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 94 - "test_live_supabase_phase8_dispatch.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 8 Evidence Gate & Dispatch Constraints Test Suite (§A14,…, Check if real Supabase credentials are provided in settings., Verify live Supabase database conditional CHECK constraints enforce evidence…, test_live_supabase_phase8_dispatch_evidence_gate()

### Community 95 - "test_live_supabase_phase9_sync.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 9 Karmi Sahayak Offline Sync & Adjudication Test Suite…, Check if real Supabase credentials are provided in settings., Verify live Supabase offline sync constraints, preserved evidence, and…, test_live_supabase_phase9_sync_and_adjudication_flow()

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
Cohesion: 0.07
Nodes (28): dependencies, @civicbrain/design-tokens, @civicbrain/ui, lenis, react, react-dom, react-router-dom, devDependencies (+20 more)

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

### Community 106 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 107 - "Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification"
Cohesion: 0.22
Nodes (8): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0009_phase8_dispatch_evidence.sql`), 4.1 Dispatch & Work Order Operations (`/v1/dispatch/work-orders`), 4.2 Citizen Verification & Satisfaction Loop (`/v1/intake/reports`), 4. REST API Endpoints, 5. Verification Plan, Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification

### Community 108 - "public.incident_causal_link"
Cohesion: 0.31
Nodes (7): idx_causal_org_id, idx_causal_root_id, idx_causal_symptom_id, public.incident_causal_link, public.incident, public.organization, public.user_account

### Community 109 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log

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

### Community 115 - "test_live_supabase_phase4_gis"
Cohesion: 0.40
Nodes (4): asyncio, skipif, Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis()

### Community 116 - "IncidentStatus"
Cohesion: 0.04
Nodes (118): SupabaseClaims, UploadFile, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints., Submit photo report with 10MB payload size limit and streaming RAM protection.…, Citizen or channel ingestion endpoint creating multi-issue reports.…, submit_intake_report(), submit_photo_intake() (+110 more)

### Community 117 - "test_live_supabase_admin_bulk_import_and_is_org_admin_rls"
Cohesion: 0.67
Nodes (3): skipif, Live Supabase integration test exercising dry_run=false with real admin JWT and…, test_live_supabase_admin_bulk_import_and_is_org_admin_rls()

### Community 119 - "postgrest_exceptions"
Cohesion: 0.22
Nodes (7): postgrest_exceptions, is_live_supabase_configured(), skipif, Live Supabase Phase 12 Exhaustive RLS & Privilege Matrix Audit Test Suite. In…, Check if real Supabase credentials are provided in settings., Systematically audits positive and negative paths across all application tables., test_live_supabase_phase12_exhaustive_rls_matrix()

### Community 121 - "CitizenShell"
Cohesion: 0.16
Nodes (12): PROMPT 1 — Shared App Shells, [2026-09-24] — PROMPT 1 — Shared App Shells (all four deployables), [2026-09-24] — PROMPT 9 — Representative Screen: Karmi Sahayak · Work Order Action (apps/karmi-sahayak), CitizenShell(), CitizenShellProps, EditorialShell(), EditorialShellProps, FieldShell() (+4 more)

### Community 122 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+9 more)

### Community 127 - "2. The Six Corrected Design Pillars"
Cohesion: 0.14
Nodes (13): 1. Executive Summary & Core Requirements, 2. The Six Corrected Design Pillars, 3. Database Schema Changes (`migrations/0015_staff_bulk_import_audit.sql`), 5. Security & Defensive Hardening, CSV Formula Injection Neutralization, PII & Secret Scrubbing in Application Logs, Pillar 1: Non-Admin Role Restriction, Pillar 2: Setup-Token & User-Sets-Own-Password Flow (Zero Admin-Visible Passwords) (+5 more)

### Community 128 - "analytics/services.py"
Cohesion: 0.07
Nodes (37): Analytics and Service-Time Prediction Domain Module (§A21, §A23)., Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, compute_csi(), compute_ward_report_card(), generate_corporator_digest(), AsyncSession (+29 more)

### Community 129 - "test_live_supabase_rbac_rls.py"
Cohesion: 0.25
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase RBAC & Multi-Tenant RLS Integration Test Suite. In strict…, Check if real Supabase credentials are provided in settings., Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 130 - "Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log

### Community 131 - "ref_react"
Cohesion: 0.05
Nodes (52): App(), apps_karmi_sahayak_src_index, root, App(), apps_nagrik_setu_src_index, root, ReportCaptureView(), ReportCategoryView() (+44 more)

### Community 137 - "ui/package.json"
Cohesion: 0.04
Nodes (45): dependencies, @civicbrain/design-tokens, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-radio-group, @radix-ui/react-select, @radix-ui/react-switch (+37 more)

### Community 138 - "verify_cron_or_admin"
Cohesion: 0.50
Nodes (4): Request, SupabaseClaims, Verifies caller is an automated cron task, service role, or system admin., verify_cron_or_admin()

### Community 141 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 142 - ".__call__"
Cohesion: 0.40
Nodes (3): Receive, Scope, Send

### Community 144 - "Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. Incident Table RLS Audit & Access-Control Regression Fix, 2. What Was Built in Phase 5, 3. Verification & Live Test Evidence, Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

### Community 147 - "DetectedDefect"
Cohesion: 0.09
Nodes (19): DetectedDefect, BaseModel, Atomic localized defect detected from photo analysis or citizen declaration., Analyze image bytes and return list of detected defects., 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants (+11 more)

### Community 150 - "Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Implementation Log

## Knowledge Gaps
- **500 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+495 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1230 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PrioritizationEvaluationResponse` connect `v1/prioritization.py` to `CivicShowcase.tsx`, `IncidentStatus`?**
  _High betweenness centrality (0.252) - this node is a cross-community bridge._
- **Why does `[2026-09-24] — PROMPT 4 — Tier 1 Civic-Specific Components (packages/ui)` connect `CivicShowcase.tsx` to `v1/prioritization.py`, `PrimitivesShowcase.tsx`, `lucide-react`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Why does `IncidentStatus` connect `IncidentStatus` to `analytics/services.py`, `v1/prioritization.py`, `citizen_dispute_report`, `transparency/services.py`, `v1/dispatch.py`, `uuid`, `incidents.py`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `CurrentUserClaims` (e.g. with `configure_category_prior()` and `get_corporator_digest()`) actually correct?**
  _`CurrentUserClaims` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `StaffRole` (e.g. with `configure_category_prior()` and `create_causal_link()`) actually correct?**
  _`StaffRole` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 26 INFERRED edges - model-reasoned connections that need verification._