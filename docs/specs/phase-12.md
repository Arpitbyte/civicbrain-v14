# Phase 12: System Hardening, Compliance Audit & Red-Team Verification — Technical Specification

**Version:** CivicBrain v14.12.0  
**Phase:** 12  
**Status:** APPROVED & IMPLEMENTED  

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

Every application table created across migrations 0001–0012 has Row Level Security enabled. Below is the full 24-table matrix queried directly from `pg_tables` and `pg_policies` on the live database:

| # | Table Name | Policies on Live DB | Permitted Roles | Allowed Operations | Security Boundary & Condition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `ahp_matrix_config` | `ahp_config_admin_manage`<br>`ahp_config_select_org`<br>`service_role_ahp_config_all` | `authenticated`<br>`authenticated`<br>`service_role` | `ALL`<br>`SELECT`<br>`ALL` | Org Admin manage<br>Org member read<br>Service role bypass |
| 2 | `category_service_time_prior` | `category_priors_admin_write`<br>`category_priors_read`<br>`service_role_priors_all` | `authenticated`<br>`anon`, `authenticated`<br>`service_role` | `ALL`<br>`SELECT`<br>`ALL` | Org Admin manage<br>Public read category priors<br>Service role bypass |
| 3 | `citizen_profile` | `citizen_insert_own_profile`<br>`citizen_read_own_profile`<br>`citizen_update_own_profile`<br>`service_role_citizen_profile_all` | `authenticated`<br>`authenticated`<br>`authenticated`<br>`service_role` | `INSERT`<br>`SELECT`<br>`UPDATE`<br>`ALL` | Own profile only (`auth.uid() = id`)<br>Own profile only<br>Own profile only<br>Service role bypass |
| 4 | `department` | `admin_manage_departments`<br>`public_read_departments`<br>`service_role_department_all` | `authenticated`<br>`anon`, `authenticated`<br>`service_role` | `ALL`<br>`SELECT`<br>`ALL` | Org Admin manage<br>Public read departments<br>Service role bypass |
| 5 | `dispatch_conflict_review` | `conflict_review_select_policy`<br>`conflict_review_update_policy`<br>`service_role_conflict_review_all` | `authenticated`<br>`authenticated`<br>`service_role` | `SELECT`<br>`UPDATE`<br>`ALL` | Worker / Org Admin / Dispatcher / Supervisor<br>Org Admin / Dispatcher / Supervisor<br>Service role bypass |
| 6 | `elected_representative` | `public_read_elected_reps`<br>`service_role_elected_rep_all` | `anon`, `authenticated`<br>`service_role` | `SELECT`<br>`ALL` | Public read ward corporators<br>Service role bypass |
| 7 | `incident` | `admin_manage_incidents`<br>`corporator_select_incidents`<br>`dept_staff_select_incidents`<br>`dept_staff_update_incidents`<br>`dispatcher_select_incidents`<br>`field_worker_select_incidents`<br>`public_read_incidents`<br>`service_role_incident_all`<br>`zonal_supervisor_select_incidents` | `authenticated`<br>`authenticated`<br>`authenticated`<br>`authenticated`<br>`authenticated`<br>`authenticated`<br>`anon`<br>`service_role`<br>`authenticated` | `ALL`<br>`SELECT`<br>`SELECT`<br>`UPDATE`<br>`SELECT`<br>`SELECT`<br>`SELECT`<br>`ALL`<br>`SELECT` | Org Admin manage<br>Corporator ward incidents<br>Dept staff incidents<br>Dept staff status update<br>Dispatcher org incidents<br>Assigned worker / dept incidents<br>Public read active incidents<br>Service role bypass<br>Zonal supervisor zone incidents |
| 8 | `incident_causal_link` | `causal_link_manage_staff`<br>`causal_link_select_org`<br>`service_role_causal_link_all` | `authenticated`<br>`authenticated`<br>`service_role` | `ALL`<br>`SELECT`<br>`ALL` | Admin / Dispatcher / Supervisor manage<br>Org member read<br>Service role bypass |
| 9 | `incident_dedup_link` | `service_role_dedup_link_all`<br>`staff_view_dedup_links` | `service_role`<br>`authenticated` | `ALL`<br>`SELECT` | Service role bypass<br>Org Admin read |
| 10 | `intake_report` | `citizen_insert_intake_report`<br>`citizen_select_own_intake_report`<br>`service_role_intake_report_all` | `anon`, `authenticated`<br>`authenticated`<br>`service_role` | `INSERT`<br>`SELECT`<br>`ALL` | Public intake submission<br>Citizen own report / Org Admin read<br>Service role bypass |
| 11 | `jan_sunwai_ledger_entry` | `public_read_jan_sunwai_ledger`<br>`service_role_ledger_all` | `anon`, `authenticated`<br>`service_role` | `SELECT`<br>`ALL` | Public read DP-perturbed ledger<br>Service role bypass |
| 12 | `nagar_pragati_city_snapshot` | `public_read_nagar_pragati`<br>`service_role_pragati_all` | `anon`, `authenticated`<br>`service_role` | `SELECT`<br>`ALL` | Public read city progress metrics<br>Service role bypass |
| 13 | `observation` | `citizen_select_own_observations`<br>`service_role_observation_all` | `authenticated`<br>`service_role` | `SELECT`<br>`ALL` | Citizen own intake / Org Admin read<br>Service role bypass |
| 14 | `organization` | `authenticated_read_organizations`<br>`service_role_full_access` | `authenticated`<br>`service_role` | `SELECT`<br>`ALL` | Authenticated read organizations<br>Service role bypass |
| 15 | `sync_mutation_log` | `service_role_sync_log_all`<br>`sync_log_insert_policy`<br>`sync_log_select_policy` | `service_role`<br>`authenticated`<br>`authenticated` | `ALL`<br>`INSERT`<br>`SELECT` | Service role bypass<br>Worker own mutation / Org Admin<br>Worker / Org Admin / Dispatcher / Supervisor |
| 16 | `taxonomy_category` | `service_role_taxonomy_category_all`<br>`taxonomy_category_insert_staff`<br>`taxonomy_category_read_authenticated`<br>`taxonomy_category_read_public`<br>`taxonomy_category_update_admin` | `service_role`<br>`authenticated`<br>`authenticated`<br>`anon`<br>`authenticated` | `ALL`<br>`INSERT`<br>`SELECT`<br>`SELECT`<br>`UPDATE` | Service role bypass<br>Staff propose category<br>Staff read active/proposed<br>Public read approved categories<br>Org Admin manage |
| 17 | `user_account` | `service_role_user_account_all`<br>`user_account_read_policy`<br>`user_account_update_policy` | `service_role`<br>`authenticated`<br>`authenticated` | `ALL`<br>`SELECT`<br>`UPDATE` | Service role bypass<br>Self / Org Admin read<br>Self / Org Admin update |
| 18 | `user_role_assignment` | `admin_manage_role_assignments`<br>`role_assignment_read_policy`<br>`service_role_role_assignment_all` | `authenticated`<br>`authenticated`<br>`service_role` | `ALL`<br>`SELECT`<br>`ALL` | Org Admin manage staff roles<br>Self / Org Admin read<br>Service role bypass |
| 19 | `ward` | `admin_manage_wards`<br>`public_read_wards`<br>`service_role_ward_all` | `authenticated`<br>`anon`, `authenticated`<br>`service_role` | `ALL`<br>`SELECT`<br>`ALL` | Org Admin manage wards<br>Public read wards<br>Service role bypass |
| 20 | `ward_equity_credibility` | `service_role_ward_equity_all`<br>`ward_equity_admin_manage`<br>`ward_equity_select_org` | `service_role`<br>`authenticated`<br>`authenticated` | `ALL`<br>`ALL`<br>`SELECT` | Service role bypass<br>Org Admin manage equity multipliers<br>Org member read |
| 21 | `ward_report_card_snapshot` | `service_role_snapshots_all`<br>`ward_report_card_public_read`<br>`ward_report_card_staff_write` | `service_role`<br>`anon`, `authenticated`<br>`authenticated` | `ALL`<br>`SELECT`<br>`ALL` | Service role bypass<br>Public read weekly ward scorecards<br>Org Admin manage |
| 22 | `ward_resolution_stat` | `service_role_ward_res_all`<br>`ward_res_admin_manage`<br>`ward_res_select_org` | `service_role`<br>`authenticated`<br>`authenticated` | `ALL`<br>`ALL`<br>`SELECT` | Service role bypass<br>Org Admin manage stats<br>Org member read |
| 23 | `work_order` | `service_role_work_order_all`<br>`work_order_insert_staff`<br>`work_order_select_org`<br>`work_order_update_worker` | `service_role`<br>`authenticated`<br>`authenticated`<br>`authenticated` | `ALL`<br>`INSERT`<br>`SELECT`<br>`UPDATE` | Service role bypass<br>Admin / Dispatcher create work order<br>Org member read<br>Assigned worker / Dispatcher / Admin update |
| 24 | `zone` | `admin_manage_zones`<br>`public_read_zones`<br>`service_role_zone_all` | `authenticated`<br>`anon`, `authenticated`<br>`service_role` | `ALL`<br>`SELECT`<br>`ALL` | Org Admin manage zones<br>Public read zones<br>Service role bypass |

*(Note: PostGIS system table `spatial_ref_sys` is present in `pg_tables` but is a PostGIS internal dictionary table not managed by application migrations.)*

- Audit execution verifies:
  1. 100% of application tables (24/24) have `rowsecurity = true`.
  2. 0 tables have blanket `GRANT ALL TO PUBLIC` or `GRANT ALL TO anon`.
  3. `anon` write access (`INSERT`, `UPDATE`, `DELETE`) is rejected on all 24 tables except the deliberate public intake endpoint on `intake_report` (`citizen_insert_intake_report`).
  4. Cross-tenant isolation verification across Org Alpha vs Org Beta with real seeded test data.

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
