# Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Implementation Log

**Date:** 2026-09-21  
**Status:** COMPLETED  
**Version:** CivicBrain v14.10.0  

---

## 1. What Was Built

- **Ward Report Card & Performance Snapshots (§A21):**
  - Schema migration `migrations/0011_phase10_analytics_eta.sql` introducing `ward_report_card_snapshot` and `category_service_time_prior`.
  - Metric calculations:
    - Volume metrics (`total_reported`, `total_active`, `total_resolved`, `total_confirmed`, `total_appealed`).
    - Mean Time to Resolution (MTTR) & Median Time to Resolution across categories.
    - Citizen Satisfaction Index (CSI): $N_{\text{confirmed}} / (N_{\text{confirmed}} + N_{\text{appealed}})$, defaulting to 1.0 on uncontested resolutions.
    - SLA compliance rate (% resolved within 72-hour threshold).
    - Ward Equity Credibility gap integration (from Phase 6 Bühlmann credibility model).
    - Department performance breakdown.
  - Periodic immutable snapshot persistence with composite unique constraint `uq_ward_snapshot_period`.
  - Scoped table grants and RLS: `anon, authenticated` have public `SELECT` on `ward_report_card_snapshot`; `authenticated` admins have write access. Zero blanket `GRANT ALL`.
  - **Privacy Confirmation & Justification:** Weekly snapshots aggregate macro totals across 30,000–80,000+ residents in municipal wards with zero individual coordinates, citizen IDs, or microdata timestamps; unconditional public `SELECT` presents zero small-count singling-out or linkage risk, leaving Differential Privacy ($\epsilon, \delta$-Laplace noise) for Phase 11's public microdata / Jan Sunwai ledger.

- **Corporator Executive Digest (§A18, §A21, Correction 1):**
  - Tailored briefing for Ward Elected Representatives (Corporators).
  - Explicit `ward_id: UUID` query parameter on `GET /v1/analytics/corporator/digest?ward_id=...`.
  - Strict database-backed ownership verification against `elected_representative` / `user_role_assignment`:
    - Corporators requesting unauthorized wards outside their jurisdiction receive HTTP 403 Forbidden (`detail="Corporator does not represent the requested ward"`).
    - Municipal administrators (`StaffRole.ADMIN`, `StaffRole.ZONAL_SUPERVISOR`) bypass ward restrictions to inspect any ward.
  - Summarizes total active cases, newly reported this week, resolved this week, CSI, aging SLA breaches (> 72 hours), and department backlog rankings.

- **Deterministic Service-Time / ETA Prediction Engine (§A23, Bootstrap Principle §A3):**
  - Pure, deterministic, zero-external-dependency parametric formula:
    $$\widehat{T} = \max\left(4.0, T_{\text{base}} \times M_{\text{sev}}(s) \times E_{\text{ward}} \times L_{\text{dept}}\right)$$
  - Baseline empirical priors stored in `category_service_time_prior` with cold-start fallbacks (48.0 hours).
  - Severity scaling: $M_{\text{sev}}(s) = 0.6 + (s \times 0.2) \implies [0.8, 1.0, 1.2, 1.4, 1.6]$.
  - Ward efficiency factor: $E_{\text{ward}} = \text{mean\_resolution\_hours}_w / T_{\text{base}}$ bounded to $[0.5, 2.0]$.
  - Department backlog load factor: $L_{\text{dept}} = 1.0 + \min\left(1.5, \frac{\text{active\_work\_orders}}{20.0 \times \max(1, \text{active\_workers})}\right)$.
  - Calculates confidence intervals: optimistic (P25), expected (P50), and breach threshold (P90).

- **FastAPI Analytics Endpoints (`civicbrain/api/v1/analytics.py`):**
  - `GET /v1/analytics/wards/{ward_id}/report-card`: Public/authenticated scorecard computation and snapshot retrieval.
  - `GET /v1/analytics/corporator/digest`: Corporator digest with jurisdictional ownership check.
  - `GET /v1/analytics/incidents/{incident_id}/eta`: Parametric ETA prediction and confidence bounds.
  - `POST /v1/analytics/priors` & `GET /v1/analytics/priors`: Category service-time prior configuration (Admin only).

---

## 2. Verification & Test Evidence

1. **Unit Test Suite (`tests/test_analytics_eta.py`):**
   - Verified CSI formula calculations across edge cases: 0 cases (None), uncontested resolutions (1.0), 50/50 splits (0.5), 80/20 splits (0.8).
   - Verified parametric ETA severity scaling ($S_1 \to 38.4$h, $S_5 \to 76.8$h) and confidence bound invariants ($P_{25} \le P_{50} \le P_{90}$).
   - Verified department backlog load scaling ($L_{\text{dept}} = 2.5 \to 72.0$h).
   - Verified Corporator ward boundary enforcement: unauthorized ward request returns HTTP 403 Forbidden with `"Corporator does not represent the requested ward"`.
   - Verified authorized Corporator request returns complete digest with SLA breach alerts and department backlog rankings.
   - Verified Ward Report Card calculation and snapshot persistence.

2. **Live Supabase Integration (`tests/test_live_supabase_phase10_analytics.py`):**
   - Seeded real organization, zone, two wards (Ward 101, Ward 102), department, real auth user, and `elected_representative` mapping to Ward 101 on live Supabase (`isqepbxkzxfpvfdkcntw`).
   - Verified live database ETA prediction using seeded `category_service_time_prior` ($T_{\text{base}}=24$h, $M_{\text{sev}}=1.4 \implies 33.6$h).
   - Verified ward report card computation and snapshot insertion.
   - Proved public anonymous `SELECT` on `ward_report_card_snapshot` via `anon_client`.
   - Proved live corporator boundary security: Corporator querying assigned Ward 101 succeeds (200 OK); querying unassigned Ward 102 is rejected with HTTP 403 Forbidden.
   - Clean teardown of all database entities and auth users in `finally` block.

3. **Static Quality Gates & Full Suite:**
   - 90 tests passing across entire project test suite.
   - `ruff check .` clean with 0 errors.
   - `ruff format --check .` clean (120 files formatted).
   - `mypy civicbrain` clean with 0 errors across 62 source files.
