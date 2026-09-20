# Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Implementation Log

**Date:** 2026-09-20  
**Status:** COMPLETED  
**Version:** CivicBrain v14.6.0  

---

## 1. What Was Built

- **Analytic Hierarchy Process (AHP) 5-Criteria Engine (§A12):**
  - Evaluates civic incidents across the exact 5 orthogonal dimensions from §A12:
    - $C_1$: **Severity** ($w_S$)
    - $C_2$: **Risk** ($w_R$)
    - $C_3$: **Exposure** ($w_E$)
    - $C_4$: **Criticality** ($w_C$)
    - $C_5$: **Urgency** ($w_U$, decoupled from emotion per §A11)
  - Pure CPU Saaty pairwise comparison matrix solver with principal eigenvector extraction ($\lambda_{\max}$) via NumPy.
  - Strict Consistency Ratio ($CR < 0.10$) validation gate.
  - Database-level `CHECK (consistency_ratio < 0.10)` on `ahp_matrix_config` ensuring invalid matrices can never persist regardless of write path.
  - Five separate stored sub-scores ($s_S, s_R, s_E, s_C, s_U \in [0.0, 1.0]$) and five separate weights per incident, producing raw priority score $P_{\text{raw}} = \sum w_k s_k$.

- **Bühlmann Credibility Equity Compensator (§A13, Bootstrap Principle §A3):**
  - Mitigates civic grievance underreporting in marginalized / digitally disconnected wards.
  - Computes credibility factor $Z_i = \frac{n_i}{n_i + K}$.
  - Blends city prior rate $\mu_0$ with ward historical verified incident rate $\bar{X}_i$ to compute expected issue rate $\hat{\mu}_i$.
  - Compares expected rate to observed report rate $O_i$ to calculate the equity gap $\Delta_i = \max(0, \hat{\mu}_i - O_i)$.
  - Derives equity boost $\beta_i = \min(\beta_{\max}, \gamma \cdot \frac{\Delta_i}{\hat{\mu}_i + \epsilon})$, where $\beta_{\max} = 0.25$ and $\gamma = 0.5$ are provisional defaults pending real empirical calibration.
  - Stores `verified_incident_count`, `historical_incident_rate`, `credibility_factor`, `expected_issue_rate`, `observed_issue_rate`, `equity_gap`, and `equity_boost` in `ward_equity_credibility`.

- **Confidence-Gating and Human Review Routing (§A12, §A13):**
  - When raw priority is high ($P_{\text{final}} \ge 70.0$) and confidence is low ($C < 0.50$):
    - Routes incident to human review queue (`requires_human_review = true`, `review_reason = 'high_priority_low_confidence'`, `status = 'triaged'`).
    - Prevents automated dispatch progression until human verification.
  - When confidence is adequate or priority is normal, auto-progresses to `status = 'prioritized'`.

- **Database Migration & Scoped RLS (`migrations/0007_phase6_ahp_credibility.sql`):**
  - Created `ahp_matrix_config`, `ward_equity_credibility`, `ward_resolution_stat`.
  - Added 5 sub-scores, priority scores, equity boost, and human review gating flags to `incident`.
  - Check constraints for all sub-scores ($[0.0, 1.0]$), priority score ($[0.0, 100.0]$), and confidence score ($[0.0, 1.0]$).
  - RLS policies use `is_org_admin(organization_id)` for admin mutations and explicit organization scoping for staff reads.
  - Strict operation-scoped grants with zero blanket `GRANT ALL`.

- **REST API Endpoints (`civicbrain/api/v1/prioritization.py`):**
  - `POST /v1/prioritization/ahp/matrix` (Admin only)
  - `GET /v1/prioritization/ahp/matrix/active`
  - `GET /v1/prioritization/equity/wards/{ward_id}`
  - `POST /v1/prioritization/evaluate`

---

## 2. Verification & Test Evidence

1. **Unit Test Suite (`tests/test_ahp_credibility.py`):**
   - Verified 5 AHP weights sum to $1.0 \pm 10^{-4}$ with $CR < 0.10$.
   - Verified rejection of inconsistent comparison matrices ($CR \ge 0.10$).
   - Verified glass-box determinism across 1,000 runs to 6 decimal places.
   - Verified decoupling test: `subscore_urgency` is unaffected by citizen emotional distress / `citizen_urgency_score`.
   - Verified Bühlmann equity compensator: cold-start ward relies 100% on prior ($Z=0$), mature ward relies on empirical history ($Z=0.90$), and underreported wards receive positive equity boost.
   - Verified confidence gate: High priority + low confidence holds back from auto-dispatch to `status = 'triaged'`, while high confidence advances to `status = 'prioritized'`.

2. **Live Supabase Integration (`tests/test_live_supabase_phase6_ahp.py`):**
   - Seeded real test organization, zone, ward, department on live Supabase.
   - Proved database check constraint `chk_ahp_cr` rejects matrices with $CR \ge 0.10$.
   - Proved check constraint `chk_subscore_severity` rejects subscores $> 1.0$.
   - Verified clean teardown in `finally` blocks.

3. **Full Suite & Static Quality Gates:**
   - 57 passing tests across the entire test suite.
   - `ruff check` and `ruff format --check` passed with 0 errors.
   - `mypy civicbrain` passed with 0 errors across 47 source files.
