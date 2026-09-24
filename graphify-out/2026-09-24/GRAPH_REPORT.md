# Graph Report - CivicBrain  (2026-09-24)

## Corpus Check
- 244 files · ~114,753 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 56 file(s) not represented in the graph (top: .css 42, .woff2 9, (none) 3)

## Summary
- 2134 nodes · 4284 edges · 143 communities (113 shown, 30 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 501 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `040903f3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CurrentUserClaims
- identity/models.py
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
- hierarchy.py
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
- IncidentStatus
- CausalGraphService
- Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log
- time
- BuhlmannEquityCompensator
- intake/services.py
- 2. Screen specifications
- schemas/intake.py
- CivicBrain: Complete Reference Document for Frontend Engineers & Designers
- test_taxonomy_governance.py
- AuthContext.tsx
- package.json
- RateLimiter
- create_jwt_token
- analyze_text
- Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification
- test_live_supabase_phase4_gis
- test_hierarchy_api.py
- nagrik-setu/src/App.tsx
- WorkOrderStatus
- public.jan_sunwai_ledger_entry
- VisionDetector
- README.md
- v1/intake.py
- httpx
- transparency-board/src/App.tsx
- v1/prioritization.py
- test_offline_sync.py
- DeterministicIndicRuleProcessor
- Phase 2: Domain Core & Incident Lifecycle — Implementation Log
- Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification
- public.observation
- public.intake_report
- public.observation
- v1/taxonomy.py
- DESIGN.md — CivicBrain Canonical Design System
- Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification
- config.py
- Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification
- intake/models.py
- test_transparency_ledger.py
- test_live_supabase_rls_boundary
- os
- test_vision_splitting.py
- audit/__init__.py
- karmi-sahayak/package.json
- 0014_performance_indexes.sql
- nagrik-setu/package.json
- transparency/services.py
- staff-console/package.json
- ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts
- get_db
- main.py
- v1/dispatch.py
- test_nlp_analyze_api_auth_enforcement
- dispatch/services.py
- Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log
- test_security_performance_hardening.py
- v1/transparency.py
- test_live_supabase_rbac_rls
- public.dispatch_conflict_review
- v1/causal.py
- Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log
- test_live_supabase_phase12_exhaustive_rls_matrix
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
- test_phase12_pii_scrubbing.py
- Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Resolution — Technical Specification
- public.taxonomy_category
- public.staff_bulk_import_log
- api-client/package.json
- i18n/package.json
- AHPMatrix
- analytics/services.py
- test_live_supabase_phase8_dispatch_evidence_gate
- test_live_supabase_phase9_sync_and_adjudication_flow
- ref_react_router_dom
- karmi-sahayak/src/main.tsx
- Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log
- compilerOptions
- verify_cron_or_admin
- test_ahp_credibility.py
- Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification
- AHPResult
- intake/__init__.py
- compute_nagar_pragati
- CitizenShell
- Phase 13: Security & Performance Hardening — Technical Specification
- staff-console/src/App.tsx
- test_live_supabase_admin_bulk_import_and_is_org_admin_rls
- public.incident
- Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification
- test_live_supabase_phase2_rls
- test_live_supabase_phase5_nlp
- test_live_supabase_phase7_causal_cycles_and_centrality
- Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log
- Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log
- Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log

## God Nodes (most connected - your core abstractions)
1. `CurrentUserClaims` - 51 edges
2. `IncidentStatus` - 48 edges
3. `StaffRole` - 45 edges
4. `Incident` - 42 edges
5. `Base` - 36 edges
6. `Department` - 28 edges
7. `WorkOrderStatus` - 27 edges
8. `WorkOrder` - 26 edges
9. `process_field_sync()` - 25 edges
10. `process_photo_intake()` - 25 edges

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
- None detected.

## Communities (143 total, 30 thin omitted)

### Community 0 - "CurrentUserClaims"
Cohesion: 0.06
Nodes (53): configure_category_prior(), get_corporator_digest(), get_incident_eta_prediction(), get_ward_report_card(), list_category_priors(), AsyncSession, date, get (+45 more)

### Community 1 - "identity/models.py"
Cohesion: 0.10
Nodes (30): Phase 10 Analytics Domain Models: CategoryServiceTimePrior,…, CausalRelationType, Phase 7 Domain Models: IncidentCausalLink, CausalRelationType., Causal taxonomy classifying upstream failure modes., Identity and Organization domain entities., Living Taxonomy Governance (§A11, Standing Invariant 1). Decoupled from static…, NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling (§A11). In…, Phase 6 Prioritization Domain Models: AHPMatrixConfig, WardEquityCredibility,… (+22 more)

### Community 2 - "test_rls_organization.py"
Cohesion: 0.06
Nodes (31): ast, ComplianceReport, DeterministicComplianceScanner, CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner. Part B…, AST-based scanner verifying strict adherence to deterministic algorithmic…, run_cli_scan(), ScanViolation, Urban Local Body classification under 74th Constitutional Amendment Act, 1992. (+23 more)

### Community 3 - "v1/gis.py"
Cohesion: 0.11
Nodes (29): get_clusters(), get_incidents_geojson(), get_wards_geojson(), AsyncSession, get, UUID, GIS Core and Spatial Analysis REST Endpoints (§A14)., Serve active or filtered operational incidents as GeoJSON FeatureCollection.… (+21 more)

### Community 4 - "test_intake_api.py"
Cohesion: 0.18
Nodes (14): Any, Overrides redis client (used for testing or dependency injection)., set_redis_client(), fakeredis_aioredis, asyncio, Integration tests for citizen intake and operational incidents APIs., Verify tracking endpoint returns 404 for nonexistent token., Verify Redis-backed IP rate limiting on anonymous tracking token endpoint. (+6 more)

### Community 5 - "Settings"
Cohesion: 0.33
Nodes (4): BaseSettings, field_validator, CivicBrain system settings loaded from environment or .env., Settings

### Community 6 - "CivicBrain v14 — Operational Rules & Architecture Ground Truth"
Cohesion: 0.29
Nodes (6): 1. The 17 Hard Rules, 2. The Bootstrap Principle (Self-Calibrating Intelligence), 3. Directory & File Skeleton, 4. Phase Roadmap (Summary), 5. Specific Invariant Rules (v14 Re-derivations), CivicBrain v14 — Operational Rules & Architecture Ground Truth

### Community 7 - "0003_phase2_intake_incident_dedup.sql"
Cohesion: 0.09
Nodes (45): auth.users, idx_organization_code, organization, citizen_profile, department, elected_representative, idx_department_organization_id, idx_elected_rep_org_id (+37 more)

### Community 15 - "hierarchy.py"
Cohesion: 0.05
Nodes (91): bulk_import_users(), create_department(), create_staff_member(), get_hierarchy(), get_representative(), list_departments(), list_staff_members(), normalize_indian_phone() (+83 more)

### Community 28 - "CivicBrain v14"
Cohesion: 0.33
Nodes (6): CivicBrain v14, Core Features, Getting Started, Overview, Phase Architecture, Running Tests & Quality Gates

### Community 29 - "IncidentStatus"
Cohesion: 0.16
Nodes (24): get_incident(), get_incident_observations(), list_incidents(), AsyncSession, get, patch, SupabaseClaims, UUID (+16 more)

### Community 30 - "CausalGraphService"
Cohesion: 0.09
Nodes (27): CausalGraphService, CyclicCausalDependencyError, UUID, Causal Root-Cause Linking & Incident Graph Centrality Engine (§A13). Provides:…, Scale root cause priority proportionally to downstream blast radius (§A13).…, Raised when establishing a causal link would introduce a direct or indirect…, Itemized breakdown of root-cause priority boost., Pure CPU directed graph service managing civic causal topology and acyclicity. (+19 more)

### Community 31 - "Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 1: Identity, Multi-Tenant Hierarchy & RBAC — Implementation Log

### Community 33 - "BuhlmannEquityCompensator"
Cohesion: 0.15
Nodes (11): BuhlmannEquityCompensator, Self-calibrating actuarial equity engine., Initialize compensator with provisional parameters pending empirical…, Compute Bühlmann credibility factor Z_i = n_i / (n_i + K). Cold start: n_i = 0…, r"""Compute expected issue rate \hat{\mu}_i = Z_i * X_bar_i + (1 - Z_i) * \mu_0., r"""Compute the deficit Delta_i = max(0, \hat{\mu}_i - O_i)., Derive priority boost beta_i = min(beta_max, gamma * (Delta_i / (expected_rate…, Full evaluation pipeline for a ward's reporting equity. (+3 more)

### Community 34 - "intake/services.py"
Cohesion: 0.14
Nodes (23): calculate_jaro_winkler_similarity(), Deterministic Jaro-Winkler similarity calculation for cold-start text matching., IncidentDedupLink, IntakeReport, Splink probabilistic record linkage audit between observation and candidate…, Citizen submission provenance container., calculate_intake_status_from_children(), process_photo_intake() (+15 more)

### Community 35 - "2. Screen specifications"
Cohesion: 0.04
Nodes (44): 0.1 `apps/nagrik-setu` (public, anon + Phone OTP), 0.2 `apps/staff-console` (authenticated, role-gated — Command Deck / Ops Board / City Pulse / Control Room), 0.3 `apps/karmi-sahayak` (field_worker, offline-first PWA), 0.4 `apps/transparency-board` (Astro, public + corporator auth), 0. Complete sitemap (4 deployables, per `UI_ARCHITECTURE.md` §1), 2.10 Department Queue, 2.11 Work Order Detail, 2.12 Heatmap / Cluster View (+36 more)

### Community 36 - "schemas/intake.py"
Cohesion: 0.16
Nodes (17): IntakeChannel, IntakeStatus, Citizen reporting channels., Aggregate lifecycle status for parent citizen intake report., AnonymousTrackingResponse, BaseSchema, IntakeReportCreate, IntakeReportResponse (+9 more)

### Community 37 - "CivicBrain: Complete Reference Document for Frontend Engineers & Designers"
Cohesion: 0.06
Nodes (31): 1. Project Theme & Pitch, 2.1 Workspace Naming Table (§A5, §A18), 2.2 Plain-English Domain Glossary, 2. Naming & Terminology Glossary, 3.1 Confidence is First-Class, Never Hidden, 3.2 Evidence (Photos & GPS) is Central, Not an Attachment, 3.3 Itemized Score Breakdowns Over Opaque Single Numbers, 3.4 Status is Per-Observation, Never Prematurely Collapsed (+23 more)

### Community 38 - "test_taxonomy_governance.py"
Cohesion: 0.10
Nodes (26): create_default_rubric(), BaseModel, field_validator, Concrete physical criteria and baseline severity score for a single rubric tier., Complete 5-level severity rubric (§A11, Standing Invariant 1). Approval of a…, Generate a standard calibrated 5-level rubric for seed categories., RubricLevel, SeverityRubric (+18 more)

### Community 39 - "AuthContext.tsx"
Cohesion: 0.12
Nodes (21): RoleSwitcher(), PROMPT 2 — Navigation & Role-Gated Routing, AuthContext, AuthContextType, AuthProvider(), AuthProviderProps, useAuth(), UserProfile (+13 more)

### Community 40 - "package.json"
Cohesion: 0.08
Nodes (27): devDependencies, @fontsource/ibm-plex-mono, @fontsource/ibm-plex-sans, @fontsource/ibm-plex-sans-devanagari, @fontsource-variable/fraunces, tailwindcss, @tailwindcss/vite, typescript (+19 more)

### Community 41 - "RateLimiter"
Cohesion: 0.25
Nodes (5): Request, RateLimiter, FastAPI dependency for sliding/fixed-window IP rate limiting via Upstash Redis., 1. What Was Built & Optimized, Phase 13: Security & Performance Hardening — Implementation Log

### Community 42 - "create_jwt_token"
Cohesion: 0.07
Nodes (35): 1. Department Creation Endpoint, 1. Executive Summary & Core Requirements, 2. Staff Bulk Import Endpoint, 2. The Six Corrected Design Pillars, 3. Database Schema Changes (`migrations/0015_staff_bulk_import_audit.sql`), 4. API Surface & Schemas, 5. Security & Defensive Hardening, 6. Verification Plan & Test Strategy (+27 more)

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

### Community 47 - "nagrik-setu/src/App.tsx"
Cohesion: 0.11
Nodes (14): App(), apps_nagrik_setu_src_index, root, HomeReportView(), ReportCaptureView(), ReportCategoryView(), ReportLocationView(), ReportReviewView() (+6 more)

### Community 48 - "WorkOrderStatus"
Cohesion: 0.11
Nodes (29): Work order lifecycle status (§A14, §A16)., Work order tracking field dispatch and evidence-gated resolution., WorkOrder, WorkOrderStatus, asyncio, Unit & Integration Tests for Phase 8 Evidence-Gated Dispatch & Satisfaction…, Verify resolve_work_order rejects whitespace-only notes with 422., Verify field worker attempting to resolve another worker's work order raises… (+21 more)

### Community 49 - "public.jan_sunwai_ledger_entry"
Cohesion: 0.22
Nodes (14): idx_js_ledger_category, idx_js_ledger_created, idx_js_ledger_geom, idx_js_ledger_org, idx_js_ledger_ward, idx_nagar_pragati_date, idx_nagar_pragati_org, public.jan_sunwai_ledger_entry (+6 more)

### Community 50 - "VisionDetector"
Cohesion: 0.13
Nodes (17): DetectedDefect, FixtureVisionDetector, HonestColdStartDetector, BaseModel, Protocol, Computer Vision Protocol, Honest Cold-Start Triage & Fixture Detectors. In…, Deterministic fixture detector for multi-defect pipeline testing and CI.…, Atomic localized defect detected from photo analysis or citizen declaration. (+9 more)

### Community 51 - "README.md"
Cohesion: 0.14
Nodes (10): 1. What Was Built, 2. Verification & Test Evidence, Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Implementation Log, 1. What Was Built, 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 4: GIS Core & Spatial Analysis Pipeline — Implementation Log, 1. What Was Built (+2 more)

### Community 52 - "v1/intake.py"
Cohesion: 0.13
Nodes (22): confirm_report_resolution(), dispute_report_resolution(), Any, AsyncSession, get, post, Request, SupabaseClaims (+14 more)

### Community 53 - "httpx"
Cohesion: 0.24
Nodes (9): httpx, asyncio, Smoke and integration tests for health and readiness endpoints., Verify that /v1/health returns HTTP 200 and expected liveness schema., Verify that /v1/ready returns valid readiness response format., Verify that root endpoint provides documentation links., test_health_endpoint_liveness(), test_ready_endpoint_schema() (+1 more)

### Community 54 - "transparency-board/src/App.tsx"
Cohesion: 0.15
Nodes (10): App(), apps_transparency_board_src_index, root, CaseProvenanceChainView(), CityFeedView(), CivicAssistantView(), CouncilorDigestView(), PublicLedgerView() (+2 more)

### Community 55 - "v1/prioritization.py"
Cohesion: 0.12
Nodes (29): evaluate_incident_priority(), get_active_ahp_matrix(), get_ward_equity(), AsyncSession, get, post, UUID, API endpoints for Phase 6 AHP Prioritization, Equity Compensator & Confidence… (+21 more)

### Community 56 - "test_offline_sync.py"
Cohesion: 0.13
Nodes (32): Dispatch and Field Operations Domain Module (§A14, §A15, §A16)., DispatchConflictReview, Dispatch and Field Operations Domain Models (§A14, §A15, §A16)., Append-only log of offline client mutations from Karmi Sahayak (§A15)., Supervisor review queue for concurrent dispatch conflicts (§A15)., Offline mutation synchronization status (§A15)., SyncMutationLog, SyncMutationStatus (+24 more)

### Community 57 - "DeterministicIndicRuleProcessor"
Cohesion: 0.10
Nodes (19): DeterministicIndicRuleProcessor, NLPProcessor, BaseModel, Protocol, Normalized analysis result returned by NLP processing pipeline (§A11)., Detect script and primary language using Unicode block ranges., Analyze grievance text extracting category hints and decoupled emotion metrics., Standard protocol for multilingual civic grievance text analysis. (+11 more)

### Community 58 - "Phase 2: Domain Core & Incident Lifecycle — Implementation Log"
Cohesion: 0.33
Nodes (5): 1. What Was Built, 2. Key Architectural Decisions, 3. Deviations from Specification, 4. Verification & CI Status, Phase 2: Domain Core & Incident Lifecycle — Implementation Log

### Community 59 - "Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification"
Cohesion: 0.25
Nodes (7): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema & Migration (`migrations/0007_phase6_ahp_credibility.sql`), 4.2 REST API Surface (`civicbrain/api/v1/prioritization.py`), 4. Software Architecture & Implementation Design, 5. Verification Plan, Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification

### Community 60 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification"
Cohesion: 0.13
Nodes (14): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`), 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace), 4.2 Differential Privacy: Temporal Jittering (1D Laplace), 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee, 4.4 Per-Incident Cryptographic Hash Chain, 4. Mathematical Specifications (+6 more)

### Community 65 - "v1/taxonomy.py"
Cohesion: 0.14
Nodes (24): approve_category(), list_categories(), propose_category(), AsyncSession, get, patch, post, SupabaseClaims (+16 more)

### Community 66 - "DESIGN.md — CivicBrain Canonical Design System"
Cohesion: 0.09
Nodes (21): 10. Loading — honest, specific, never generic theater, 11. Responsive system, 12. Accessibility — part of the design, not QA, 13. Performance, 14. AI-slop pre-flight — permanent banned-pattern list, 15. Implementation contract — every future Antigravity prompt must include, 1. Art direction — The Benchmark, 2. Visual variation by workspace (+13 more)

### Community 67 - "Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification"
Cohesion: 0.15
Nodes (12): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`), 4.1 Citizen Satisfaction Index (CSI), 4.2 Service-Time / ETA Prediction (§A23), 4. Analytical & Predictive Mathematical Formulations (§A21, §A23), 5.1 Ward Report Cards (`/v1/analytics/wards`), 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`) (+4 more)

### Community 68 - "config.py"
Cohesion: 0.05
Nodes (45): Notifications domain service: multi-channel staff onboarding and citizen alerts., Application configuration via pydantic-settings., get_supabase_admin_client(), Supabase Admin Client provider., Returns initialized Supabase Admin Client using service role key., Client, fixture, io (+37 more)

### Community 69 - "Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification"
Cohesion: 0.33
Nodes (5): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0008_phase7_causal_graph.sql`), 4. Verification Plan, Phase 7: Causal Root-Cause Linking & Incident Graph Centrality — Technical Specification

### Community 70 - "intake/models.py"
Cohesion: 0.18
Nodes (15): evaluate_splink_record_linkage(), Direct Fellegi-Sunter implementation using provisional cold-start weights…, Evaluates pairwise record linkage using direct Fellegi-Sunter cold-start math.…, DedupDecision, Phase 2 Domain Models: IntakeReport, Observation, Incident, and…, Record linkage determination., Unit tests for Splink deduplication integration under provisional cold-start…, Verify deterministic string similarity calculation. (+7 more)

### Community 71 - "test_transparency_ledger.py"
Cohesion: 0.10
Nodes (28): JanSunwaiLedgerEntry, Public, tamper-evident civic grievance ledger entry with Differential Privacy…, compute_entry_hash(), extract_coordinates(), generate_laplace_dp_perturbation(), Any, Computes deterministic SHA-256 checkpoint hash for per-incident ledger chain…, Publishes an immutable milestone checkpoint to the Jan Sunwai Ledger (§A23).… (+20 more)

### Community 72 - "test_live_supabase_rls_boundary"
Cohesion: 0.67
Nodes (3): skipif, End-to-end verification of RLS and Auth against a live Supabase project., test_live_supabase_rls_boundary()

### Community 74 - "test_vision_splitting.py"
Cohesion: 0.16
Nodes (16): Organization, Root tenant representing an Urban Local Body (ULB) or multi-ULB state…, ObservationStatus, Atomic observation state., asyncio, Unit & integration tests for Computer Vision protocol and Multi-Issue Photo-…, Verify photo splitting pipeline splits defects into atomic observations across…, Verify arbitrary photo in cold start creates an UNCLASSIFIED observation… (+8 more)

### Community 77 - "karmi-sahayak/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 78 - "0014_performance_indexes.sql"
Cohesion: 0.09
Nodes (26): idx_causal_established_by, idx_conflict_review_incident_id, idx_conflict_review_reviewed_by, idx_conflict_review_worker_id, idx_incident_worker_id, idx_js_ledger_cat_code, idx_js_ledger_dept_id, idx_sync_log_org_id (+18 more)

### Community 79 - "nagrik-setu/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 80 - "transparency/services.py"
Cohesion: 0.18
Nodes (14): Citizen Transparency, Jan Sunwai Ledger, Differential Privacy & Civic Assistant…, CivicAssistantQueryResponse, IncidentLedgerChainResponse, JanSunwaiLedgerResponse, NagarPragatiResponse, BaseModel, Pydantic schemas for Phase 11 Transparency, Jan Sunwai Ledger & Civic Assistant…, Publicly accessible, differentially private civic ledger milestone entry (§A23). (+6 more)

### Community 81 - "staff-console/package.json"
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, @civicbrain/ui, react, react-dom, react-router-dom, devDependencies, @types/react (+16 more)

### Community 82 - "ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts"
Cohesion: 0.11
Nodes (18): ANTIGRAVITY_PROMPTS.md — CivicBrain Implementation Prompts, Implementation order, PROMPT 0 — Foundation: Tokens & Repo Scaffold, PROMPT 10 — Representative Screen: Control Room · AHP Weight Calibration, PROMPT 11 — Representative Screen: Transparency Board · Nagar Pragati, PROMPT 34 — Responsive Refinement Pass, PROMPT 35 — Motion Pass, PROMPT 36 — Accessibility Pass (+10 more)

### Community 83 - "get_db"
Cohesion: 0.15
Nodes (15): get_db(), AsyncSession, Dependency that provides an async session per request., 2. Verification & Test Evidence, asyncio, 5. Verify generalized IP rate limiter protects POST /v1/intake/reports., 1. Verify standard defensive security headers injected on all HTTP responses., 2. Verify CORS allows only explicit origins and forbids wildcard '*'. (+7 more)

### Community 84 - "main.py"
Cohesion: 0.07
Nodes (24): ASGIApp, Security and hardening ASGI middleware., Injects standard defensive security headers into all HTTP responses. Enforces:…, SecurityHeadersMiddleware, civicbrain_api_v1, global_unhandled_exception_handler(), lifespan(), get (+16 more)

### Community 85 - "v1/dispatch.py"
Cohesion: 0.08
Nodes (50): adjudicate_conflict(), create_new_work_order(), execute_field_sync(), get_worker_sync_conflicts(), list_my_work_orders(), list_supervisor_conflicts(), AsyncSession, get (+42 more)

### Community 86 - "test_nlp_analyze_api_auth_enforcement"
Cohesion: 0.67
Nodes (3): asyncio, Verify POST /v1/nlp/analyze requires authentication and rejects unauthenticated…, test_nlp_analyze_api_auth_enforcement()

### Community 87 - "dispatch/services.py"
Cohesion: 0.14
Nodes (27): adjudicate_dispatch_conflict(), citizen_confirm_report(), citizen_dispute_report(), create_work_order(), evaluate_auto_confirm_cron(), _get_incidents_for_report(), list_conflicts_for_worker(), AsyncSession (+19 more)

### Community 88 - "Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log"
Cohesion: 0.50
Nodes (3): 2. Key Code References for Mandatory Corrections, 3. Verification & Live Test Evidence, Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

### Community 89 - "test_security_performance_hardening.py"
Cohesion: 0.11
Nodes (26): cache_delete(), cache_get(), cache_set(), Any, Upstash Redis caching layer for hot, rarely-changing public reads., Retrieves JSON-deserialized value from Redis cache. Fails open on connection…, Stores JSON-serialized value into Redis cache with specified TTL. Fails open on…, Deletes cached key upon invalidation. Fails open on error. (+18 more)

### Community 90 - "v1/transparency.py"
Cohesion: 0.23
Nodes (13): ask_civic_assistant(), get_incident_chain(), get_nagar_pragati(), get_public_ledger(), AsyncSession, get, post, UUID (+5 more)

### Community 91 - "test_live_supabase_rbac_rls"
Cohesion: 0.50
Nodes (3): skipif, Verify Phase 1 RBAC, tenant isolation, and RLS policies on live Supabase., test_live_supabase_rbac_rls()

### Community 92 - "public.dispatch_conflict_review"
Cohesion: 0.24
Nodes (13): idx_conflict_review_org, idx_conflict_review_status, idx_conflict_review_wo, idx_sync_log_created, idx_sync_log_entity, idx_sync_log_worker, public.dispatch_conflict_review, public.sync_mutation_log (+5 more)

### Community 93 - "v1/causal.py"
Cohesion: 0.15
Nodes (19): create_causal_link(), get_downstream_symptoms(), AsyncSession, get, post, UUID, API endpoints for Phase 7 Causal Root-Cause Linking & Incident Centrality…, Retrieve all downstream symptom incidents and priority boost breakdown. (+11 more)

### Community 94 - "Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log

### Community 95 - "test_live_supabase_phase12_exhaustive_rls_matrix"
Cohesion: 0.50
Nodes (3): skipif, Systematically audits positive and negative paths across all application tables., test_live_supabase_phase12_exhaustive_rls_matrix()

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
Cohesion: 0.08
Nodes (24): dependencies, @civicbrain/design-tokens, lucide-react, react-router-dom, devDependencies, react, react-dom, @types/react (+16 more)

### Community 107 - "Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification"
Cohesion: 0.22
Nodes (8): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Ground Truth, 3. Database Schema (`migrations/0009_phase8_dispatch_evidence.sql`), 4.1 Dispatch & Work Order Operations (`/v1/dispatch/work-orders`), 4.2 Citizen Verification & Satisfaction Loop (`/v1/intake/reports`), 4. REST API Endpoints, 5. Verification Plan, Phase 8: Evidence-Gated Dispatch, Work-Order Progression & Verifier Consensus — Technical Specification

### Community 108 - "public.incident_causal_link"
Cohesion: 0.31
Nodes (7): idx_causal_org_id, idx_causal_root_id, idx_causal_symptom_id, public.incident_causal_link, public.incident, public.organization, public.user_account

### Community 109 - "test_phase12_pii_scrubbing.py"
Cohesion: 0.13
Nodes (16): process_civic_assistant_query(), Processes natural language citizen inquiries with deterministic multilingual…, CivicAssistantQueryRequest, Citizen multilingual query request payload., re, asyncio, Tests for Pillar 3: DPDP Act 2023 Compliance, PII Scrubbing & Differential…, Verify that JanSunwaiLedgerResponse contains zero citizen PII fields. (+8 more)

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

### Community 115 - "AHPMatrix"
Cohesion: 0.14
Nodes (13): AHPMatrix, 5x5 Saaty Pairwise Comparison Matrix solver with strict CR < 0.10 validation., Verify matrix is positive and reciprocal: A[i, j] * A[j, i] == 1, A[i, i] == 1., Verify Saaty 5x5 matrix solves exact 5 criteria weights summing to 1.0 with CR…, Verify an inconsistent 5x5 matrix (CR >= 0.10) is flagged as inconsistent., test_ahp_5_criteria_weights_and_consistency(), test_ahp_inconsistent_matrix_rejection(), is_live_supabase_configured() (+5 more)

### Community 116 - "analytics/services.py"
Cohesion: 0.05
Nodes (65): Analytics and Service-Time Prediction Domain Module (§A21, §A23)., CategoryServiceTimePrior, Category baseline service-time priors (§A23, Bootstrap Principle §A3)., Periodic municipal performance scorecard aggregated at the ward level (§A21)., WardReportCardSnapshot, compute_csi(), compute_ward_report_card(), generate_corporator_digest() (+57 more)

### Community 117 - "test_live_supabase_phase8_dispatch_evidence_gate"
Cohesion: 0.67
Nodes (3): skipif, Verify live Supabase database conditional CHECK constraints enforce evidence…, test_live_supabase_phase8_dispatch_evidence_gate()

### Community 118 - "test_live_supabase_phase9_sync_and_adjudication_flow"
Cohesion: 0.67
Nodes (3): skipif, Verify live Supabase offline sync constraints, preserved evidence, and…, test_live_supabase_phase9_sync_and_adjudication_flow()

### Community 119 - "ref_react_router_dom"
Cohesion: 0.33
Nodes (5): MyOrdersView(), SyncStatusView(), WorkOrderActionView(), packages_ui_src_index_fieldshell, ref_react_router_dom

### Community 120 - "karmi-sahayak/src/main.tsx"
Cohesion: 0.22
Nodes (7): App(), apps_karmi_sahayak_src_index, root, App(), apps_staff_console_src_index, root, ref_react_dom

### Community 121 - "Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. What Was Built & Hardened, 2. Verification & Test Evidence, 3. Next Phase, Phase 12: Hardening, Red-Team Audit & Production Isolation — Implementation Log

### Community 122 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+9 more)

### Community 123 - "verify_cron_or_admin"
Cohesion: 0.50
Nodes (4): Request, SupabaseClaims, Verifies caller is an automated cron task, service role, or system admin., verify_cron_or_admin()

### Community 124 - "test_ahp_credibility.py"
Cohesion: 0.13
Nodes (22): calculate_raw_priority(), CriteriaSubscores, Analytic Hierarchy Process (AHP) Engine over 5 Orthogonal Dimensions (§A12).…, Calculate deterministic linear combination raw priority score in [0.0, 1.0].…, The 5 orthogonal incident evaluation sub-scores in [0.0, 1.0]., r"""Bühlmann Credibility Equity Compensator (§A13, Bootstrap Principle §A3).…, Computed Bühlmann credibility and equity gap evaluation., WardEquityResult (+14 more)

### Community 125 - "Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification"
Cohesion: 0.22
Nodes (8): 2. Invariant Rules & Architectural Ground Truth, 3.1 Extending Intake Report and Observation for NLP Metadata, 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`), 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`), 4.2 Decoupled Scoring Rules, 4. Domain & Processor Architecture, 6. Verification Plan, Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

### Community 126 - "AHPResult"
Cohesion: 0.50
Nodes (3): AHPResult, Extract principal eigenvector via power iteration in pure Python. Enforces…, Computed AHP weights and consistency verification statistics.

### Community 127 - "intake/__init__.py"
Cohesion: 0.29
Nodes (7): Citizen intake & observation domain., Observation, Atomic localized defect extracted from citizen intake submission., Categorical classification entity governed by living taxonomy rules., TaxonomyCategory, 1. What Was Built, 1. Executive Summary & Scope

### Community 128 - "compute_nagar_pragati"
Cohesion: 0.33
Nodes (7): compute_nagar_pragati(), get_incident_ledger_chain(), AsyncSession, date, UUID, Retrieves full milestone chain and cryptographic validity status for an…, Computes city-wide municipal progress and macro performance scorecard (§A21).

### Community 129 - "CitizenShell"
Cohesion: 0.14
Nodes (15): PROMPT 1 — Shared App Shells, [2026-09-24] — PROMPT 0 — Foundation: Tokens & Repo Scaffold (none), [2026-09-24] — PROMPT 1 — Shared App Shells (all four deployables), Entry template (copy this for every new entry), IMPLEMENTATION_LOG.md — CivicBrain Build History, Log entries, 1. Shared component architecture (`packages/ui`), CitizenShell() (+7 more)

### Community 130 - "Phase 13: Security & Performance Hardening — Technical Specification"
Cohesion: 0.50
Nodes (3): 1. Executive Summary & Scope, 2. Invariant Rules & Architectural Constraints, Phase 13: Security & Performance Hardening — Technical Specification

### Community 131 - "staff-console/src/App.tsx"
Cohesion: 0.07
Nodes (27): AhpWeightCalibrationView(), BulkImportView(), CausalGraphView(), ConflictAdjudicationView(), CouncilorDigestView(), DepartmentQueueView(), EtaConfidenceView(), HeatmapClusterView() (+19 more)

### Community 132 - "test_live_supabase_admin_bulk_import_and_is_org_admin_rls"
Cohesion: 0.67
Nodes (3): skipif, Live Supabase integration test exercising dry_run=false with real admin JWT and…, test_live_supabase_admin_bulk_import_and_is_org_admin_rls()

### Community 134 - "Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification"
Cohesion: 0.17
Nodes (11): 2. Invariant Rules & Architectural Ground Truth, 3.1 Taxonomy Category Table (`taxonomy_category`), 3.2 Observation Table Alterations, 3.3 Explicit Per-Role Scoped Grants, 3.4 Row-Level Security Policies, 3. Database Schema (`migrations/0004_phase3_vision_taxonomy.sql`), 5.1 Automated Unit Tests, 5.2 Live Supabase Integration & RLS Tests (+3 more)

### Community 137 - "test_live_supabase_phase2_rls"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 2 intake, observations, anonymous tracking RPC and RLS policies., test_live_supabase_phase2_rls()

### Community 138 - "test_live_supabase_phase5_nlp"
Cohesion: 0.67
Nodes (3): skipif, Verify Phase 5 database columns, check constraints, and metadata persistence on…, test_live_supabase_phase5_nlp()

### Community 139 - "test_live_supabase_phase7_causal_cycles_and_centrality"
Cohesion: 0.67
Nodes (3): skipif, Verify live Supabase database trigger rejects 3-node cycle and updates incident…, test_live_supabase_phase7_causal_cycles_and_centrality()

### Community 145 - "Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log"
Cohesion: 0.40
Nodes (4): 1. Incident Table RLS Audit & Access-Control Regression Fix, 2. What Was Built in Phase 5, 3. Verification & Live Test Evidence, Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

### Community 146 - "Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log

### Community 147 - "Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log"
Cohesion: 0.50
Nodes (3): 1. What Was Built, 2. Verification & Test Evidence, Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log

## Knowledge Gaps
- **419 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+414 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1095 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CurrentUserClaims` connect `CurrentUserClaims` to `v1/taxonomy.py`, `v1/gis.py`, `analyze_text`, `hierarchy.py`, `analytics/services.py`, `v1/dispatch.py`, `v1/prioritization.py`, `v1/causal.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `StaffRole` connect `hierarchy.py` to `CurrentUserClaims`, `v1/taxonomy.py`, `identity/models.py`, `v1/gis.py`, `config.py`, `create_jwt_token`, `analytics/services.py`, `v1/dispatch.py`, `v1/prioritization.py`, `verify_cron_or_admin`, `v1/causal.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `IncidentStatus` connect `IncidentStatus` to `compute_nagar_pragati`, `intake/services.py`, `v1/gis.py`, `schemas/intake.py`, `intake/models.py`, `test_transparency_ledger.py`, `transparency/services.py`, `analytics/services.py`, `v1/intake.py`, `v1/prioritization.py`, `dispatch/services.py`, `test_offline_sync.py`, `test_ahp_credibility.py`, `intake/__init__.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `CurrentUserClaims` (e.g. with `configure_category_prior()` and `get_corporator_digest()`) actually correct?**
  _`CurrentUserClaims` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `IncidentStatus` (e.g. with `get_incidents_geojson()` and `list_incidents()`) actually correct?**
  _`IncidentStatus` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `StaffRole` (e.g. with `configure_category_prior()` and `create_causal_link()`) actually correct?**
  _`StaffRole` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `Incident` (e.g. with `create_causal_link()` and `get_downstream_symptoms()`) actually correct?**
  _`Incident` has 26 INFERRED edges - model-reasoned connections that need verification._