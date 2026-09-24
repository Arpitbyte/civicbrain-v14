# Graph Report - CivicBrain  (2026-09-24)

## Corpus Check
- 284 files · ~141,874 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 56 file(s) not represented in the graph (top: .css 42, .woff2 9, (none) 3)

## Summary
- 2399 nodes · 4962 edges · 142 communities (109 shown, 33 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 648 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `650f140a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- analyze_text
- StatusTimeline
- test_rls_organization.py
- test_gis_core.py
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
- Incident
- CausalGraphService
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- IncidentDetailView.tsx
- v1/prioritization.py
- test_hierarchy_api.py
- create_causal_link
- CivicBrain: Complete Reference Document for Frontend Engineers & Designers
- test_taxonomy_governance.py
- AuthContext.tsx
- package.json
- CivicShowcase.tsx
- StaffRole
- ref_react
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- dependencies
- identity/services.py
- ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts
- test_security_performance_hardening.py
- public.jan_sunwai_ledger_entry
- is_live_supabase_configured
- Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log
- HeatmapClusterView.tsx
- test_health.py
- ref_react_router_dom
- CurrentUserClaims
- v1/dispatch.py
- DeterministicIndicRuleProcessor
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
- get_ward_report_card
- os
- civic/index.ts
- audit/__init__.py
- karmi-sahayak/package.json
- 0014_performance_indexes.sql
- nagrik-setu/package.json
- karmi-sahayak/src/main.tsx
- staff-console/package.json
- Tabs.tsx
- Phase 0: Foundations & Kickoff — Implementation Log
- main.py
- lucide-react
- README.md
- test_live_supabase_phase9_sync.py
- Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log
- create_department
- v1/health.py
- PrimitivesShowcase.tsx
- public.dispatch_conflict_review
- track_anonymous_report
- ConfidenceBadge
- cache_set
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
- VisionDetector
- Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification
- public.incident_causal_link
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification
- public.taxonomy_category
- public.staff_bulk_import_log
- api-client/package.json
- i18n/package.json
- test_nlp_pipeline.py
- get_supabase_admin_client
- 2. Screen specifications
- .__init__
- devDependencies
- Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log
- IMPLEMENTATION_LOG.md — CivicBrain Build History
- compilerOptions
- Badge.tsx
- AHPMatrix
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- 2. The Six Corrected Design Pillars
- hierarchy.py
- Radio.tsx
- Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log
- staff-console/src/App.tsx
- Toast.tsx
- public.incident
- Tooltip.tsx
- ui/package.json
- verify_cron_or_admin
- peerDependencies
- is_live_supabase_configured
- Phase 13: Security & Performance Hardening — Technical Specification

## God Nodes (most connected - your core abstractions)
1. `CurrentUserClaims` - 51 edges
2. `IncidentStatus` - 48 edges
3. `StaffRole` - 45 edges
4. `Incident` - 42 edges
5. `Base` - 36 edges
6. `lucide-react` - 35 edges
7. `1. Shared component architecture (`packages/ui`)` - 30 edges
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

## Communities (142 total, 33 thin omitted)

### Community 0 - "analyze_text"
Cohesion: 0.24
Nodes (9): analyze_text(), post, Analyze multilingual civic text. Authenticated-only endpoint (requires valid…, BaseModel, Pydantic schemas for NLP Analysis API (§A11)., Structured linguistic and defect triage result., Payload for text analysis endpoint., TextAnalysisRequest (+1 more)

### Community 1 - "StatusTimeline"
Cohesion: 0.18
Nodes (18): PROMPT 6 — Representative Screen: Command Deck · Incident Detail, 8. Component language, [2026-09-24] — PROMPT 6 — Representative Screen: Command Deck · Incident Detail (apps/staff-console), 2.1 Home / Report an Issue, 2.2 New Report Flow (`capture` → `location` → `category` → `review`), 2.3 Track Report (lookup + detail), 2.4 Resolution Confirm / Dispute, 2.5 Incident Queue (+10 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.08
Nodes (23): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Path (+15 more)

### Community 3 - "test_gis_core.py"
Cohesion: 0.12
Nodes (27): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, Serve active or filtered operational incidents as GeoJSON FeatureCollection.…, Execute PostGIS ST_ClusterDBSCAN density clustering for civic defect hotspot… (+19 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.15
Nodes (16): Any, Upstash Redis connection and rate limiting client., Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, redis_asyncio, asyncio, Integration tests for citizen intake and operational incidents APIs. (+8 more)

### Community 5 - "config.py"
Cohesion: 0.12
Nodes (12): BaseSettings, field_validator, Application configuration via pydantic-settings., CivicBrain system settings loaded from environment or .env., Settings, pydantic_settings, is_live_supabase_configured(), skipif (+4 more)

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 7 - "0003_phase2_intake_incident_dedup.sql"
Cohesion: 0.09
Nodes (45): auth.users, idx_organization_code, organization, citizen_profile, department, elected_representative, idx_department_organization_id, idx_elected_rep_org_id (+37 more)

### Community 15 - "identity.py"
Cohesion: 0.11
Nodes (35): CitizenVerificationMethod, Urban Local Body classification under 74th Constitutional Amendment Act, 1992., Citizen identity verification methods per §A8., ULBType, get_organization_hierarchy(), Fetch complete hierarchical tree of zones and wards for an organization., BaseSchema, CitizenProfileCreate (+27 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (6): CivicBrain v14, Core Features, Getting Started, Overview, Phase Architecture, Running Tests & Quality Gates

### Community 29 - "Incident"
Cohesion: 0.21
Nodes (18): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+10 more)

### Community 30 - "CausalGraphService"
Cohesion: 0.09
Nodes (27): CausalGraphService, CyclicCausalDependencyError, UUID, Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13). Provides:…, Scale root cause priority proportionally to downstream blast radius (§A13).…, Raised when establishing a causal link would introduce a direct or indirect…, Itemized breakdown of root-cause priority boost., Pure CPU directed graph service managing civic causal topology and acyclicity. (+19 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "IncidentDetailView.tsx"
Cohesion: 0.09
Nodes (28): MOCK_FIXTURES, ReportTrackData, TrackDetailView(), getValidNextStatuses(), STATUS_LABELS, VALID_NEXT_STATUS_TRANSITIONS, CausalLinkItem, IncidentDetailData (+20 more)

### Community 34 - "v1/prioritization.py"
Cohesion: 0.12
Nodes (29): evaluate_incident_priority(), get_active_ahp_matrix(), get_ward_equity(), AsyncSession, get, post, UUID, API endpoints for Phase 6 AHP Prioritization, Equity Compensator & Confidence… (+21 more)

### Community 35 - "test_hierarchy_api.py"
Cohesion: 0.19
Nodes (13): Verify non-dispatcher/admin role (e.g. field_worker) cannot create work orders., test_dispatch_work_orders_forbidden_role(), create_test_token(), asyncio, UUID, Integration tests for hierarchy, representative, and auth endpoints., Generate unsigned/signed HS256 JWT for API dependency testing., Verify /v1/auth/me returns 401 when no token is provided. (+5 more)

### Community 36 - "create_causal_link"
Cohesion: 0.14
Nodes (17): create_causal_link(), get_downstream_symptoms(), AsyncSession, get, post, UUID, Retrieve all downstream symptom incidents and priority boost breakdown., Create a causal link with strict multi-hop cycle prevention and staff… (+9 more)

### Community 37 - "CivicBrain: Complete Reference Document for Frontend Engineers & Designers"
Cohesion: 0.06
Nodes (31): 1. Project Theme & Pitch, 2.1 Workspace Naming Table (§A5, §A18), 2.2 Plain-English Domain Glossary, 2. Naming & Terminology Glossary, 3.1 Confidence is First-Class, Never Hidden, 3.2 Evidence (Photos & GPS) is Central, Not an Attachment, 3.3 Itemized Score Breakdowns Over Opaque Single Numbers, 3.4 Status is Per-Observation, Never Prematurely Collapsed (+23 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.07
Nodes (41): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+33 more)

### Community 39 - "AuthContext.tsx"
Cohesion: 0.13
Nodes (21): RoleSwitcher(), PROMPT 2 — Navigation & Role-Gated Routing, [2026-09-24] — PROMPT 2 — Navigation & Routing (staff-console & all deployables), AuthContext, AuthContextType, AuthProvider(), AuthProviderProps, useAuth() (+13 more)

### Community 40 - "package.json"
Cohesion: 0.07
Nodes (31): devDependencies, @fontsource/ibm-plex-mono, @fontsource/ibm-plex-sans, @fontsource/ibm-plex-sans-devanagari, @fontsource-variable/fraunces, tailwindcss, @tailwindcss/vite, typescript (+23 more)

### Community 41 - "CivicShowcase.tsx"
Cohesion: 0.10
Nodes (25): PROMPT 4 — Tier 1 Civic-Specific Components, [2026-09-24] — PROMPT 4 — Tier 1 Civic-Specific Components (packages/ui), BeforeAfterPair(), CivicShowcase(), WORKSPACES, packages_ui_src_civic_index_beforeafterpair, packages_ui_src_civic_index_clusterlayer, packages_ui_src_civic_index_confidencebadge (+17 more)

### Community 42 - "StaffRole"
Cohesion: 0.10
Nodes (33): Staff roles mapped to §A18 named workspaces., StaffRole, 6. Verification Plan & Test Strategy, io, random, create_jwt_token(), is_live_supabase_configured(), asyncio (+25 more)

### Community 43 - "ref_react"
Cohesion: 0.06
Nodes (25): ButtonProps, ButtonSize, ButtonVariant, IconButtonProps, CheckboxProps, DialogProps, DrawerProps, EmptyStateProps (+17 more)

### Community 44 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification"
Cohesion: 0.29
Nodes (6): 2. Invariant Rules & Architectural Ground Truth, 3.1 Spatial Indexes & Cluster Analysis Functions, 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`), 4. REST API Endpoints (`civicbrain/api/v1/gis.py`), 5. Verification Plan, Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

### Community 45 - "dependencies"
Cohesion: 0.17
Nodes (12): dependencies, @civicbrain/design-tokens, lucide-react, @radix-ui/react-checkbox, @radix-ui/react-dialog, @radix-ui/react-radio-group, @radix-ui/react-select, @radix-ui/react-switch (+4 more)

### Community 46 - "identity/services.py"
Cohesion: 0.12
Nodes (26): get_my_profile(), AsyncSession, get, Returns the authenticated identity, role assignments, and jurisdictional scopes…, create_staff_member(), Register staff account and assign role with jurisdictional scope within admin's…, CitizenProfile, Staff user account linked to Supabase Auth auth.users. (+18 more)

### Community 47 - "ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts"
Cohesion: 0.09
Nodes (23): ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts, Implementation order, PROMPT 0 — Foundation: Tokens & Repo Scaffold, PROMPT 10 — Representative Screen: Control Room · AHP Weight Calibration, PROMPT 11 — Representative Screen: Transparency Board · Nagar Pragati, PROMPT 34 — Responsive Refinement Pass, PROMPT 35 — Motion Pass, PROMPT 36 — Accessibility Pass (+15 more)

### Community 48 - "test_security_performance_hardening.py"
Cohesion: 0.11
Nodes (25): PIIScrubbingFilter, Logging infrastructure and automated PII redaction filter., Replaces sensitive citizen PII and credentials with redact labels., Logging filter that scrubs sensitive citizen PII and credentials from all log…, scrub_log_message(), 1. What Was Built & Optimized, 2. Verification & Test Evidence, Phase 13: Security & Performance Hardening — Implementation Log (+17 more)

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.22
Nodes (14): idx_js_ledger_category, idx_js_ledger_created, idx_js_ledger_geom, idx_js_ledger_org, idx_js_ledger_ward, idx_nagar_pragati_date, idx_nagar_pragati_org, public.jan_sunwai_ledger_entry (+6 more)

### Community 51 - "Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log

### Community 52 - "HeatmapClusterView.tsx"
Cohesion: 0.07
Nodes (39): TrackLookupView(), ClusterAccessibleListView(), ClusterAccessibleListViewProps, ClusterData, ClusterStatsPanel(), ClusterStatsPanelProps, CoordinateRulerFrame(), CoordinateRulerFrameProps (+31 more)

### Community 53 - "test_health.py"
Cohesion: 0.28
Nodes (8): asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema(), test_root_endpoint_metadata()

### Community 54 - "ref_react_router_dom"
Cohesion: 0.11
Nodes (17): HomeReportView(), ReportCaptureView(), ReportCategoryView(), ReportLocationView(), ReportReviewView(), ResolutionConfirmView(), ResolutionDisputeView(), CaseProvenanceChainView() (+9 more)

### Community 55 - "CurrentUserClaims"
Cohesion: 0.04
Nodes (107): FastAPI Analytics and ETA Prediction Endpoints (§A21, §A23)., Authentication and user session endpoints., API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, GIS Core and Spatial Analysis REST Endpoints (§A14)., API v1 router registry., NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)., Living Taxonomy Governance REST Endpoints (§A11, Standing Invariant 1)., Analytics and Service-Time Prediction Domain Module (§A21, §A23). (+99 more)

### Community 56 - "v1/dispatch.py"
Cohesion: 0.04
Nodes (136): adjudicate_conflict(), create_new_work_order(), execute_field_sync(), get_worker_sync_conflicts(), list_my_work_orders(), list_supervisor_conflicts(), AsyncSession, get (+128 more)

### Community 57 - "DeterministicIndicRuleProcessor"
Cohesion: 0.09
Nodes (21): DeterministicIndicRuleProcessor, NLPProcessor, BaseModel, Protocol, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics. (+13 more)

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
Cohesion: 0.10
Nodes (17): BuhlmannEquityCompensator, Self-calibrating actuarial equity engine., Initialize compensator with provisional parameters pending empirical…, Compute Bühlmann credibility factor Z_i = n_i / (n_i + K). Cold start: n_i = 0…, r"""Compute expected issue rate \hat{\mu}_i = Z_i * X_bar_i + (1 - Z_i) * \mu_0., r"""Compute the deficit Delta_i = max(0, \hat{\mu}_i - O_i)., Derive priority boost beta_i = min(beta_max, gamma * (Delta_i / (expected_rate…, Full evaluation pipeline for a ward's reporting equity. (+9 more)

### Community 66 - "DESIGN.md — CivicBrain Canonical Design System"
Cohesion: 0.10
Nodes (20): 10. Loading — honest, specific, never generic theater, 11. Responsive system, 12. Accessibility — part of the design, not QA, 13. Performance, 14. AI-slop pre-flight — permanent banned-pattern list, 15. Implementation contract — every future Antigravity prompt must include, 1. Art direction — The Benchmark, 2. Visual variation by workspace (+12 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "uuid"
Cohesion: 0.05
Nodes (46): postgrest_exceptions, pytest, supabase, is_live_supabase_configured(), skipif, Live Supabase Phase 12 Exhaustive RLS & Privilege Matrix Audit Test Suite. In…, Check if real Supabase credentials are provided in settings., Systematically audits positive and negative paths across all application tables. (+38 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "IncidentStatus"
Cohesion: 0.04
Nodes (107): confirm_report_resolution(), dispute_report_resolution(), AsyncSession, post, SupabaseClaims, UploadFile, UUID, FastAPI Ingestion and Anonymous Tracking Endpoints. (+99 more)

### Community 71 - "transparency/services.py"
Cohesion: 0.05
Nodes (81): ask_civic_assistant(), get_incident_chain(), get_nagar_pragati(), get_public_ledger(), AsyncSession, get, post, UUID (+73 more)

### Community 72 - "get_ward_report_card"
Cohesion: 0.18
Nodes (15): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, date, get (+7 more)

### Community 74 - "civic/index.ts"
Cohesion: 0.11
Nodes (12): BeforeAfterPairProps, ConfidenceBadgeProps, ConfidenceBand, EvidencePhotoCardProps, OfflineSyncBadgeProps, PriorityChipProps, PriorityLevel, ScoreBreakdownProps (+4 more)

### Community 77 - "karmi-sahayak/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 78 - "0014_performance_indexes.sql"
Cohesion: 0.09
Nodes (26): idx_causal_established_by, idx_conflict_review_incident_id, idx_conflict_review_reviewed_by, idx_conflict_review_worker_id, idx_incident_worker_id, idx_js_ledger_cat_code, idx_js_ledger_dept_id, idx_sync_log_org_id (+18 more)

### Community 79 - "nagrik-setu/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 80 - "karmi-sahayak/src/main.tsx"
Cohesion: 0.15
Nodes (10): App(), apps_karmi_sahayak_src_index, root, App(), apps_nagrik_setu_src_index, root, App(), apps_transparency_board_src_index (+2 more)

### Community 81 - "staff-console/package.json"
Cohesion: 0.07
Nodes (26): dependencies, @civicbrain/design-tokens, @civicbrain/ui, gsap, react, react-dom, react-router-dom, devDependencies (+18 more)

### Community 82 - "Tabs.tsx"
Cohesion: 0.25
Nodes (7): TabItem, TabsContent, TabsList, TabsProps, TabsRoot, TabsTrigger, @radix-ui/react-tabs

### Community 83 - "Phase 0: Foundations & Kickoff — Implementation Log"
Cohesion: 0.29
Nodes (6): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, 5. Prerequisites for Phase 1, Phase 0: Foundations & Kickoff — Implementation Log

### Community 84 - "main.py"
Cohesion: 0.07
Nodes (23): ASGIApp, Security and hardening ASGI middleware., Injects standard defensive security headers into all HTTP responses. Enforces:…, SecurityHeadersMiddleware, civicbrain_api_v1, global_unhandled_exception_handler(), lifespan(), get (+15 more)

### Community 85 - "lucide-react"
Cohesion: 0.15
Nodes (20): FieldLayout(), OfflineSyncContext, OfflineSyncContextValue, OfflineSyncProvider(), useOfflineSync(), getQueuedMutations(), QueuedMutation, removeMutation() (+12 more)

### Community 86 - "README.md"
Cohesion: 0.14
Nodes (9): 1. What Was Built, 2. Verification & Test Evidence, Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Implementation Log, 1. What Was Built, 2. Verification & Test Evidence, Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log, 1. What Was Built, 2. Verification & Test Evidence (+1 more)

### Community 87 - "test_live_supabase_phase9_sync.py"
Cohesion: 0.29
Nodes (6): is_live_supabase_configured(), skipif, Live Supabase Phase 9 Karmi Sahayak Offline Sync & Adjudication Test Suite…, Check if real Supabase credentials are provided in settings., Verify live Supabase offline sync constraints, preserved evidence, and…, test_live_supabase_phase9_sync_and_adjudication_flow()

### Community 88 - "Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built & Hardened, 2. Verification & Test Evidence, 3. Next Phase, Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log

### Community 89 - "create_department"
Cohesion: 0.21
Nodes (14): create_department(), get_hierarchy(), get_representative(), list_departments(), list_staff_members(), AsyncSession, get, post (+6 more)

### Community 90 - "v1/health.py"
Cohesion: 0.17
Nodes (15): health_check(), get, Health and readiness diagnostic endpoints., Liveness probe to confirm that the FastAPI process is running., Readiness probe checking database connectivity., readiness_check(), check_database_connection(), Verifies that the database is reachable and PostGIS is enabled. Returns:… (+7 more)

### Community 91 - "PrimitivesShowcase.tsx"
Cohesion: 0.09
Nodes (42): PROMPT 3 — Tier 0 Primitives, [2026-09-24] — PROMPT 3 — Tier 0 Primitives (packages/ui), 1. Shared component architecture (`packages/ui`), Badge(), Checkbox(), Dialog(), Drawer(), EmptyState() (+34 more)

### Community 92 - "public.dispatch_conflict_review"
Cohesion: 0.24
Nodes (13): idx_conflict_review_org, idx_conflict_review_status, idx_conflict_review_wo, idx_sync_log_created, idx_sync_log_entity, idx_sync_log_worker, public.dispatch_conflict_review, public.sync_mutation_log (+5 more)

### Community 93 - "track_anonymous_report"
Cohesion: 0.40
Nodes (5): Any, get, Request, Anonymous tracking lookup backed by the get_anonymous_intake_report SECURITY…, track_anonymous_report()

### Community 94 - "ConfidenceBadge"
Cohesion: 0.50
Nodes (5): 2.12 Heatmap / Cluster View, 2.13 Causal Graph View, 2.14 ETA / Confidence Panel, CITY PULSE, ConfidenceBadge()

### Community 95 - "cache_set"
Cohesion: 0.17
Nodes (13): cache_delete(), cache_get(), cache_set(), Any, Upstash Redis caching layer for hot, rarely-changing public reads., Retrieves JSON-deserialized value from Redis cache. Fails open on connection…, Stores JSON-serialized value into Redis cache with specified TTL. Fails open on…, Deletes cached key upon invalidation. Fails open on error. (+5 more)

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

### Community 106 - "VisionDetector"
Cohesion: 0.07
Nodes (28): DetectedDefect, FixtureVisionDetector, BaseModel, Protocol, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration., Protocol for vision analysis backends., Analyze image bytes and return list of detected defects. (+20 more)

### Community 107 - "Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification"
Cohesion: 0.22
Nodes (8): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0009_phase8_dispatch_evidence.sql`), 4.1 Dispatch & Work Order Operations (`/v1/dispatch/work-orders`), 4.2 Citizen Verification & Satisfaction Loop (`/v1/intake/reports`), 4. REST API Endpoints, 5. Verification Plan, Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification

### Community 108 - "public.incident_causal_link"
Cohesion: 0.31
Nodes (7): idx_causal_org_id, idx_causal_root_id, idx_causal_symptom_id, public.incident_causal_link, public.incident, public.organization, public.user_account

### Community 109 - "Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. Incident Table RLS Audit & Access-Control Regression Fix, 2. What Was Built in Phase 5, 3. Verification & Live Test Evidence, Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

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

### Community 115 - "test_nlp_pipeline.py"
Cohesion: 0.13
Nodes (12): httpx, is_live_supabase_configured(), asyncio, skipif, Live Supabase Phase 4 GIS Core, Spatial Clustering RPC & Cross-Tenant RLS Test…, Check if real Supabase credentials are provided in settings., Verify Phase 4 PostGIS spatial clustering, cross-tenant RLS isolation, and…, test_live_supabase_phase4_gis() (+4 more)

### Community 116 - "get_supabase_admin_client"
Cohesion: 0.25
Nodes (7): get_supabase_admin_client(), Supabase Admin Client provider., Returns initialized Supabase Admin Client using service role key., Client, fixture, admin_fixture(), Ensure a valid test organization and admin user exist in DB and Supabase.

### Community 117 - "2. Screen specifications"
Cohesion: 0.09
Nodes (22): 0.1 `apps/nagrik-setu` (public, anon + Phone OTP), 0.2 `apps/staff-console` (authenticated, role-gated — Command Deck / Ops Board / City Pulse / Control Room), 0.3 `apps/karmi-sahayak` (field_worker, offline-first PWA), 0.4 `apps/transparency-board` (Astro, public + corporator auth), 0. Complete sitemap (4 deployables, per `UI_ARCHITECTURE.md` §1), 2.10 Department Queue, 2.11 Work Order Detail, 2.15 My Work Orders (+14 more)

### Community 119 - "devDependencies"
Cohesion: 0.40
Nodes (5): devDependencies, react, react-dom, @types/react, @types/react-dom

### Community 120 - "Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log

### Community 121 - "IMPLEMENTATION_LOG.md — CivicBrain Build History"
Cohesion: 0.21
Nodes (12): PROMPT 1 — Shared App Shells, [2026-09-24] — PROMPT 0 — Foundation: Tokens & Repo Scaffold (none), [2026-09-24] — PROMPT 1 — Shared App Shells (all four deployables), [2026-09-24] — PROMPT 5 — Representative Screen: Nagrik Setu · Track Report (apps/nagrik-setu), [2026-09-24] — PROMPT 9 — Representative Screen: Karmi Sahayak · Work Order Action (apps/karmi-sahayak), Entry template (copy this for every new entry), IMPLEMENTATION_LOG.md — CivicBrain Build History, Log entries (+4 more)

### Community 122 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+9 more)

### Community 123 - "Badge.tsx"
Cohesion: 0.40
Nodes (4): BadgeProps, BadgeSize, BadgeVariant, Chip

### Community 124 - "AHPMatrix"
Cohesion: 0.09
Nodes (32): AHPMatrix, AHPResult, calculate_raw_priority(), CriteriaSubscores, Analytic Hierarchy Process (AHP) Engine over 5 Orthogonal Dimensions (§A12).…, Extract principal eigenvector via power iteration in pure Python. Enforces…, Calculate deterministic linear combination raw priority score in [0.0, 1.0].…, The 5 orthogonal incident evaluation sub-scores in [0.0, 1.0]. (+24 more)

### Community 125 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.22
Nodes (8): 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 6. Verification Plan, Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

### Community 126 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 127 - "2. The Six Corrected Design Pillars"
Cohesion: 0.12
Nodes (15): 1. Department Creation Endpoint, 1. Executive Summary & Core Requirements, 2. The Six Corrected Design Pillars, 3. Database Schema Changes (`migrations/0015_staff_bulk_import_audit.sql`), 4. API Surface & Schemas, 5. Security & Defensive Hardening, CSV Formula Injection Neutralization, PII & Secret Scrubbing in Application Logs (+7 more)

### Community 128 - "hierarchy.py"
Cohesion: 0.11
Nodes (21): bulk_import_users(), normalize_indian_phone(), UploadFile, Administrative hierarchy, department taxonomy, and representative discovery…, Bulk import staff users for non-admin operational roles from a CSV file.…, Validate and normalize Indian phone number to E.164 +91XXXXXXXXXX format., Audit record for administrative staff bulk-import events., StaffBulkImportLog (+13 more)

### Community 129 - "Radio.tsx"
Cohesion: 0.40
Nodes (4): RadioGroup(), RadioGroupProps, RadioOption, @radix-ui/react-radio-group

### Community 130 - "Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log

### Community 131 - "staff-console/src/App.tsx"
Cohesion: 0.06
Nodes (26): App(), apps_staff_console_src_index, root, AhpWeightCalibrationView(), BulkImportView(), CausalGraphView(), ConflictAdjudicationView(), CouncilorDigestView() (+18 more)

### Community 132 - "Toast.tsx"
Cohesion: 0.29
Nodes (6): ToastContext, ToastContextType, ToastItem, ToastProvider(), ToastVariant, @radix-ui/react-toast

### Community 134 - "Tooltip.tsx"
Cohesion: 0.50
Nodes (3): TooltipProps, TooltipProvider, @radix-ui/react-tooltip

### Community 137 - "ui/package.json"
Cohesion: 0.14
Nodes (13): @civicbrain/design-tokens, react, react-dom, react-router-dom, @types/react, @types/react-dom, main, name (+5 more)

### Community 138 - "verify_cron_or_admin"
Cohesion: 0.50
Nodes (4): Request, SupabaseClaims, Verifies caller is an automated cron task, service role, or system admin., verify_cron_or_admin()

### Community 139 - "peerDependencies"
Cohesion: 0.67
Nodes (3): peerDependencies, react, react-dom

### Community 142 - "Phase 13: Security & Performance Hardening — Technical Specification"
Cohesion: 0.50
Nodes (3): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Constraints, Phase 13: Security & Performance Hardening — Technical Specification

## Knowledge Gaps
- **480 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+475 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1203 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PrioritizationEvaluationResponse` connect `v1/prioritization.py` to `CivicShowcase.tsx`, `IncidentStatus`?**
  _High betweenness centrality (0.275) - this node is a cross-community bridge._
- **Why does `[2026-09-24] — PROMPT 4 — Tier 1 Civic-Specific Components (packages/ui)` connect `CivicShowcase.tsx` to `StatusTimeline`, `v1/prioritization.py`, `ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts`, `IMPLEMENTATION_LOG.md — CivicBrain Build History`, `ConfidenceBadge`?**
  _High betweenness centrality (0.275) - this node is a cross-community bridge._
- **Why does `IncidentStatus` connect `IncidentStatus` to `v1/prioritization.py`, `test_gis_core.py`, `transparency/services.py`, `CurrentUserClaims`, `v1/dispatch.py`, `AHPMatrix`, `Incident`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `CurrentUserClaims` (e.g. with `configure_category_prior()` and `get_corporator_digest()`) actually correct?**
  _`CurrentUserClaims` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `StaffRole` (e.g. with `configure_category_prior()` and `create_causal_link()`) actually correct?**
  _`StaffRole` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 26 INFERRED edges - model-reasoned connections that need verification._