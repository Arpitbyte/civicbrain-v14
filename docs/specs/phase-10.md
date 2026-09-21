# Phase 10: Analytics — Ward Report Card, Corporator Digest & Service-Time/ETA Prediction — Technical Specification

**Version:** CivicBrain v14.10.0  
**Phase:** 10  
**Status:** SPECIFICATION SUBMITTED FOR REVIEW  

---

## 1. Executive Summary & Scope

Phase 10 establishes the operational analytics, municipal transparency, and predictive service-time infrastructure for CivicBrain v14 (§A21, §A23):

1. **Ward Report Card (§A21):**
   - High-performance, transparent municipal performance scorecards aggregated at the ward level.
   - Core metrics:
     - Volume breakdown: Total reported, active, in-progress, resolved, confirmed, and appealed.
     - Mean Time to Resolution (MTTR) and Median Time to Resolution across categories and departments.
     - Citizen Satisfaction Index (CSI): Ratio of citizen-confirmed resolutions to total closed cases ($\frac{\text{confirmed}}{\text{confirmed} + \text{appealed}}$).
     - Ward Equity Credibility Gap: Historical expected report rate vs. observed intake rate from the Phase 6 Bühlmann Credibility model.
     - Periodic snapshots stored in `ward_report_card_snapshot` for historical trend analysis.
2. **Corporator Executive Digest (§A21):**
   - Specialized transparency briefings tailored for Ward Elected Representatives (Corporators, §A18).
   - Summarizes SLA breach alerts, long-standing unassigned/in-progress backlogs (> 48h and > 72h), department performance rankings, and citizen satisfaction ratings.
   - Structured for dashboard rendering and push distribution (WhatsApp/PDF digest generation).
3. **Service-Time / ETA Prediction Engine (§A23, Bootstrap Principle §A3):**
   - Empirically estimates expected resolution time ($\widehat{\text{ETA}}$) for any open incident based on:
     - Defect category baseline resolution hours.
     - Severity multiplier ($S_1 \dots S_5$).
     - Ward historical resolution efficiency (from `ward_resolution_stat`).
     - Real-time department active backlog load factor ($L_{\text{dept}} = 1.0 + \gamma \cdot \frac{\text{active\_work\_orders}}{\text{active\_workers}}$).
   - Pure, deterministic, zero-external-dependency calculation with fallback to city-wide empirical priors when sample size $N < 10$ (Bootstrap Principle §A3).
   - Generates confidence intervals: optimistic (P25), expected (P50), and SLA breach threshold (P90).

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Deterministic ETA Estimation (Bootstrap Principle §A3):**
   - ETA prediction MUST NOT rely on black-box external AI services. It must execute deterministically in sub-millisecond time using empirical parametric formulas and historical percentile distributions.
2. **Strict Jurisdictional Scoping for Corporators (Standing Invariant 4):**
   - Corporators can only generate and view digests for their own elected ward(s). Tenant isolation and role boundaries are strictly enforced via RLS and PostgreSQL table grants.
3. **Transparent Citizen Satisfaction Accounting:**
   - CSI explicitly distinguishes confirmed resolutions from citizen disputes (`appealed`), ensuring ground truth accountability cannot be masked by unverified contractor completions.
4. **Append-Only Snapshotting:**
   - Historical report card snapshots are immutable once generated.

---

## 3. Database Schema (`migrations/0011_phase10_analytics_eta.sql`)

```sql
-- Migration 0011: Ward Report Cards, Corporator Digests & Category Service-Time Priors (§A21, §A23)

-- 1. Category Baseline Service-Time Priors (§A23)
CREATE TABLE IF NOT EXISTS public.category_service_time_prior (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    category_code VARCHAR(50) NOT NULL,
    base_resolution_hours DOUBLE PRECISION NOT NULL DEFAULT 48.0,
    p25_hours DOUBLE PRECISION NOT NULL DEFAULT 24.0,
    p50_hours DOUBLE PRECISION NOT NULL DEFAULT 48.0,
    p90_hours DOUBLE PRECISION NOT NULL DEFAULT 96.0,
    min_hours DOUBLE PRECISION NOT NULL DEFAULT 6.0,
    sample_size INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_cat_org_prior UNIQUE (organization_id, category_code),
    CONSTRAINT chk_positive_hours CHECK (base_resolution_hours > 0 AND p25_hours > 0 AND p50_hours >= p25_hours AND p90_hours >= p50_hours)
);

-- 2. Ward Report Card Snapshot Table (§A21)
CREATE TABLE IF NOT EXISTS public.ward_report_card_snapshot (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL DEFAULT 'weekly', -- 'daily', 'weekly', 'monthly'
    total_reported INT NOT NULL DEFAULT 0,
    total_active INT NOT NULL DEFAULT 0,
    total_resolved INT NOT NULL DEFAULT 0,
    total_confirmed INT NOT NULL DEFAULT 0,
    total_appealed INT NOT NULL DEFAULT 0,
    mean_resolution_hours DOUBLE PRECISION,
    median_resolution_hours DOUBLE PRECISION,
    citizen_satisfaction_index DOUBLE PRECISION, -- confirmed / (confirmed + appealed)
    sla_compliance_rate DOUBLE PRECISION,       -- % completed within SLA
    equity_observed_gap DOUBLE PRECISION,       -- observed vs expected report gap
    department_breakdown JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ward_snapshot_period UNIQUE (ward_id, snapshot_date, period_type)
);

CREATE INDEX IF NOT EXISTS idx_wrc_org ON public.ward_report_card_snapshot(organization_id);
CREATE INDEX IF NOT EXISTS idx_wrc_ward ON public.ward_report_card_snapshot(ward_id);
CREATE INDEX IF NOT EXISTS idx_wrc_date ON public.ward_report_card_snapshot(snapshot_date);

-- 3. Row-Level Security & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.category_service_time_prior ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ward_report_card_snapshot ENABLE ROW LEVEL SECURITY;

-- Service role bypass
CREATE POLICY service_role_priors_all ON public.category_service_time_prior
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY service_role_snapshots_all ON public.ward_report_card_snapshot
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Public / Anonymous can read ward report card snapshots (Transparency Principle §A21)
CREATE POLICY ward_report_card_public_read ON public.ward_report_card_snapshot
    FOR SELECT TO anon, authenticated
    USING (true);

-- Authenticated staff can read category service-time priors
CREATE POLICY category_priors_read ON public.category_service_time_prior
    FOR SELECT TO authenticated
    USING (true);

-- Admins can update priors
CREATE POLICY category_priors_admin_write ON public.category_service_time_prior
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- Scoped Grants (Zero blanket GRANT ALL)
REVOKE ALL ON TABLE public.category_service_time_prior FROM PUBLIC;
REVOKE ALL ON TABLE public.ward_report_card_snapshot FROM PUBLIC;

GRANT SELECT ON TABLE public.category_service_time_prior TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.category_service_time_prior TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.category_service_time_prior TO service_role;

GRANT SELECT ON TABLE public.ward_report_card_snapshot TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.ward_report_card_snapshot TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ward_report_card_snapshot TO service_role;
```

---

## 4. Analytical & Predictive Mathematical Formulations (§A21, §A23)

### 4.1 Citizen Satisfaction Index (CSI)
$$\text{CSI} = \begin{cases} 
\frac{N_{\text{confirmed}}}{N_{\text{confirmed}} + N_{\text{appealed}}}, & \text{if } (N_{\text{confirmed}} + N_{\text{appealed}}) > 0 \\ 
1.0, & \text{if } N_{\text{resolved}} > 0 \text{ and } N_{\text{appealed}} = 0 \\
\text{None}, & \text{otherwise}
\end{cases}$$

### 4.2 Service-Time / ETA Prediction (§A23)
Given an incident $i$ with category $c$, severity $s \in [1, 5]$, ward $w$, and assigned department $d$:

1. **Category Base Time ($T_{\text{base}}$):**
   From `category_service_time_prior` ($P_{50}$) or cold-start fallback $48.0\text{ hours}$.
2. **Severity Scaling Multiplier ($M_{\text{sev}}$):**
   $$M_{\text{sev}}(s) = 0.6 + (s \times 0.2) \implies [0.8, 1.0, 1.2, 1.4, 1.6]$$
   *(Higher severity requires deeper engineering intervention and longer remediation).*
3. **Ward Efficiency Factor ($E_{\text{ward}}$):**
   $$E_{\text{ward}} = \frac{\text{mean\_resolution\_hours}_w}{\text{city\_mean\_resolution\_hours}}$$
   bounded to $[0.5, 2.0]$.
4. **Department Load Factor ($L_{\text{dept}}$):**
   $$L_{\text{dept}} = 1.0 + \min\left(1.5, \frac{\text{active\_work\_orders}_d}{20.0 \times \max(1, \text{active\_workers}_d)}\right)$$
5. **Expected Resolution Hours ($\widehat{T}$):**
   $$\widehat{T} = \max\left(4.0, T_{\text{base}} \times M_{\text{sev}}(s) \times E_{\text{ward}} \times L_{\text{dept}}\right)$$
6. **Target Predicted Completion Date:**
   $$\text{Predicted Completion} = \text{incident.created\_at} + \Delta t(\widehat{T})$$

---

## 5. REST API Endpoints

### 5.1 Ward Report Cards (`/v1/analytics/wards`)

- `GET /v1/analytics/wards/{ward_id}/report-card`:
  - **Auth:** Public / Anonymous (or Authenticated).
  - **Query Parameters:** `from_date: date | None`, `to_date: date | None`, `use_cache: bool = True`.
  - **Action:** Computes real-time or pulls snapshot scorecard:
    - Volume metrics (`total_reported`, `total_resolved`, `total_active`, `total_appealed`, `total_confirmed`).
    - MTTR & Median Resolution Time.
    - Citizen Satisfaction Index (CSI).
    - Department performance breakdown.

### 5.2 Corporator Executive Digest (`/v1/analytics/corporator/digest`)

- `GET /v1/analytics/corporator/digest`:
  - **Auth:** Authenticated Corporator (`StaffRole.CORPORATOR`) or Admin.
  - **Scope:** Enforced strictly to the calling Corporator's assigned `ward_id` (from JWT claims).
  - **Response (`CorporatorDigestResponse`):**
    - Executive summary: total active cases, newly reported this week, resolved this week.
    - SLA breach alerts: list of incidents exceeding SLA (> 72 hours).
    - Department backlog ranking (worst to best performing).
    - Satisfaction rating and citizen sentiment indicator.

### 5.3 ETA Prediction (`/v1/analytics/incidents/{incident_id}/eta`)

- `GET /v1/analytics/incidents/{incident_id}/eta`:
  - **Auth:** Public via valid tracking token OR Authenticated Staff.
  - **Action:** Computes parametric predicted ETA, confidence interval (P25, P50, P90), and estimated completion timestamp.

---

## 6. Verification Plan

1. **Unit Tests (`tests/test_analytics_eta.py`):**
   - CSI formula calculation correctness across edge cases (0 disputes, 100% disputes, no resolved).
   - Parametric ETA prediction scaling:
     - Verify higher severity yields proportionally longer expected ETA.
     - Verify higher department backlog increases load factor and extends completion timestamp.
     - Verify fallback to empirical priors when ward has zero historical records.
   - Corporator digest jurisdictional boundary enforcement: corporator for Ward 101 attempting to request Ward 102 receives 403 Forbidden.

2. **Live Supabase Integration (`tests/test_live_supabase_phase10_analytics.py`):**
   - Seed real organization, ward, corporator auth user, category priors, and incident history.
   - Test snapshot generation and persistence in `ward_report_card_snapshot`.
   - Test public read access to ward report cards via Supabase client.
   - Clean teardown in `finally` block.

3. **CI & Static Quality Gates:**
   - Full test suite, `ruff check`, `ruff format --check`, and `mypy civicbrain` clean.
