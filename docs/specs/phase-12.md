# Phase 12: System Hardening, Compliance Audit & Red-Team Verification — Technical Specification

**Version:** CivicBrain v14.12.0  
**Phase:** 12  
**Status:** SPECIFICATION SUBMITTED FOR REVIEW  

---

## 1. Executive Summary & Scope

Phase 12 constitutes the comprehensive system hardening, compliance verification, and red-team penetration audit of CivicBrain v14 across all preceding 11 phases, executed strictly under Part B's Prompt 8 pattern:

1. **Pillar 1: Deterministic-Only Rules & Zero Unauthorized External LLM Calls (§A3, §A11, §A23):**
   - AST-based and runtime network audit scanning every file across `civicbrain/`:
     - Verifies zero runtime calls or SDK imports to paid external proprietary LLMs (OpenAI, Anthropic, Gemini, Cohere) in production inference code.
     - Verifies all multilingual text triage adheres to Phase 5's IndicBERT / local heuristic pipeline.
     - Verifies defect detection adheres to Phase 3's local YOLO-World/ViT feature protocols.
     - Verifies prioritization adheres to Phase 6's Saaty AHP eigenvalue solver and Bühlmann empirical credibility.
     - Verifies causal root-cause analysis adheres to Phase 7's cycle-guarded BFS/DFS DAGs.
     - Verifies service-time ETA adheres to Phase 10's deterministic parametric percentiles.
     - Verifies Civic Assistant adheres to Phase 11's local multilingual template catalogue.
2. **Pillar 2: Exhaustive RLS Matrix & Real Client-SDK Test Coverage (Standing Invariants 4, 5):**
   - Live audit of all 20 RLS-bearing tables across migrations 0001 through 0012:
     `organization`, `zone`, `ward`, `department`, `user_account`, `user_role_assignment`, `citizen_profile`, `elected_representative`, `intake_report`, `observation`, `incident`, `category_severity_rubric`, `causal_link`, `work_order`, `sync_mutation_log`, `dispatch_conflict_review`, `category_service_time_prior`, `ward_report_card_snapshot`, `jan_sunwai_ledger_entry`, `nagar_pragati_city_snapshot`.
   - Client-SDK tests proving zero cross-tenant row leakage, anonymous read denial on non-public tables, strict role-scoped write boundaries, and zero blanket `GRANT ALL`.
3. **Pillar 3: Consent, PII Scrubbing & Redaction (DPDP Act 2023, §A8, §A23):**
   - Citizen phone numbers, OTP verification records, and WhatsApp identities must never be exposed across public API routes or serialized responses.
   - Public Jan Sunwai microdata ledger must maintain zero PII and verify single-draw 2D Laplace spatial perturbation ($\Delta \text{dist} \ge 30\text{m}$) and 1D Laplace temporal jitter.
4. **Pillar 4: Production Isolation & Zero Demo-Data Leakage:**
   - Audit all seed scripts, test fixtures, and mock factories to ensure demo or synthetic test data cannot leak into production environments.
   - All test runs must use isolated `run_id` namespaces and execute complete database teardown in `finally` blocks.
   - Automated CI environments must enforce clean separation between staging and production secrets.

---

## 2. Invariant Rules & Audit Standards

1. **Zero External LLM Dependency Invariant (Bootstrap Principle §A3):**
   - Core municipal workflows (triage, prioritization, causal analysis, dispatch, ETA, and public transparency) must operate completely offline / locally with deterministic fallback rules. No workflow may break if external cloud AI APIs are unreachable.
2. **Exhaustive RLS Coverage Invariant (Standing Invariant 4):**
   - Every single table in the database must have `ROW LEVEL SECURITY ENABLED` and explicit scoped grants (`SELECT`, `INSERT`, `UPDATE`). Blanket `GRANT ALL ON TABLE ... TO PUBLIC` is strictly prohibited.
3. **Digital Personal Data Protection (DPDP Act 2023 Compliance):**
   - Citizen consent and PII minimization must be provably enforced. Unauthenticated public access is strictly limited to differentially private aggregated snapshots (`ward_report_card_snapshot`, `nagar_pragati_city_snapshot`) and perturbed microdata (`jan_sunwai_ledger_entry`).
4. **Deterministic Red-Team Audit Execution:**
   - The hardening test suite must run automatically on every commit, asserting that any new PR or commit violating Pillars 1–4 fails CI immediately.

---

## 3. Hardening & Compliance Implementation Plan

### 3.1 Automated Deterministic & AST Compliance Scanner (`tests/test_audit_deterministic_compliance.py`)
- Python AST scanner traversing all modules under `civicbrain/`:
  - Asserts forbidden imports (`openai`, `anthropic`, `google.generativeai`, `langchain`, `cohere`) are absent from production code.
  - Inspects all HTTP requests to verify external cloud LLM endpoints are not invoked.
  - Verifies local deterministic algorithms are active across all 6 analytical pipelines.

### 3.2 Exhaustive Live RLS & Privilege Matrix Audit (`tests/test_live_supabase_phase12_hardening.py`)
- Executes live PostgREST queries against Supabase (`pg_tables`, `pg_policies`, `information_schema.table_privileges`):
  1. Verifies that 100% of user tables have `rowsecurity = true`.
  2. Verifies that 0 tables have `GRANT ALL TO PUBLIC` or `GRANT ALL TO anon`.
  3. Verifies that `anon` cannot write (`INSERT`, `UPDATE`, `DELETE`) to ANY table in the system.
  4. Tests cross-tenant isolation on live seeded data across two distinct organizations (Org Alpha vs Org Beta) across all sensitive tables (`incident`, `work_order`, `user_account`, `causal_link`).

### 3.3 PII Leakage & DPDP Redaction Verification
- Inspects all API schemas and endpoint responses for unhashed phone numbers, emails, and names.
- Proves Jan Sunwai ledger records zero citizen identifiers and verifies anti-composition coordinate reuse.

### 3.4 Production Isolation Verification
- Validates that all automated tests use ephemeral UUID prefixes and teardown all created entities in `finally` blocks.
- Scans git repository to verify zero `.env` or production secrets are committed.

---

## 4. Verification Plan

1. **Compliance Test Suites:**
   - `tests/test_audit_deterministic_compliance.py`: 100% clean AST and deterministic algorithm verification.
   - `tests/test_live_supabase_phase12_hardening.py`: Live Supabase RLS matrix query and cross-tenant red-team penetration test.
2. **CI & Static Quality Gates:**
   - Full test suite execution (P1 through P12), `ruff check`, `ruff format --check`, and `mypy civicbrain` green.
