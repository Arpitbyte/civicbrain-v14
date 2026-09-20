# Phase 6: AHP Multi-Criteria Prioritization Engine, Bühlmann Equity Compensator & Confidence-Gated Dispatch — Technical Specification

**Version:** CivicBrain v14.6.0  
**Phase:** 6  
**Status:** APPROVED & IMPLEMENTED  

---

## 1. Executive Summary & Scope

Phase 6 implements the authoritative, deterministic civic prioritization and credibility engine for CivicBrain v14 (§A12, §A13, Bootstrap Principle §A3):

1. **Analytic Hierarchy Process (AHP) Engine over 5 Orthogonal Dimensions (§A12):**
   - Implements pairwise-compared criteria weighting across the exact five dimensions from §A12:
     1. $C_1$: **Severity** ($w_S$): Physical magnitude and structural degradation of the defect (from structured 1–5 rubrics / inspection).
     2. $C_2$: **Risk** ($w_R$): Public safety hazard, potential for secondary accidents, structural collapse, or contagion.
     3. $C_3$: **Exposure** ($w_E$): Footfall volume, commuter density, school zones, hospital perimeters, arterial vs. residential thoroughfare.
     4. $C_4$: **Criticality** ($w_C$): Municipal infrastructure tier, vulnerability of downstream network, vital lifeline status.
     5. $C_5$: **Urgency** ($w_U$): Temporal aging, SLA breach proximity, and rate of decay (strictly decoupled from citizen emotional expression and citizen urgency score per §A11).
   - Saaty pairwise comparison matrix $A \in \mathbb{R}^{5 \times 5}$ solved via principal eigenvector extraction ($\lambda_{\max}$ and normalized vector $w$).
   - Strict Consistency Ratio verification:
     $$CI = \frac{\lambda_{\max} - n}{n - 1}, \quad CR = \frac{CI}{RI_5} < 0.10 \quad (\text{where } RI_5 = 1.12)$$
   - Rejection gate: Any matrix with $CR \ge 0.10$ raises validation error and cannot be activated or persisted (enforced by DB `CHECK` constraint).
   - Five separate stored sub-scores ($s_S, s_R, s_E, s_C, s_U \in [0.0, 1.0]$) and five separate weights per incident, producing the raw multi-criteria score:
     $$P_{\text{raw}} = \sum_{k \in \{S, R, E, C, U\}} w_k \cdot s_k \in [0.0, 1.0]$$

2. **Equity Compensator Mechanism via Bühlmann Credibility (§A13, Bootstrap Principle §A3):**
   - **The Civic Equity Problem:** In affluent or digitally literate wards, citizens submit complaints frequently. In underserved, marginalized, or digitally disconnected wards, complaints are severely underreported despite identical or higher real physical infrastructure degradation. Prioritizing solely on report volume or squeaky wheels systematically deprives low-reporting wards.
   - **Expected vs. Observed Issue Rate Formulation:**
     - For each ward $i$, compute an expected issue rate $\hat{\mu}_i$ by blending the city-wide prior issue rate $\mu_0$ with that ward's own verified historical incident record $\bar{X}_i$:
       $$\hat{\mu}_i = Z_i \bar{X}_i + (1 - Z_i) \mu_0$$
       where Bühlmann credibility factor $Z_i = \frac{n_i}{n_i + K}$, $n_i$ is the number of historical verified/resolved incidents in ward $i$, and $K$ is the structural actuarial variance parameter ($K = s^2 / a$, with cold-start provisional default $K = 10.0$).
     - Let $O_i$ be the observed reporting rate for ward $i$ over the active evaluation window (e.g. active complaints per 10,000 population or normalized ward area baseline).
     - Compute the **Equity Gap** ($\Delta_i$):
       $$\Delta_i = \max(0, \hat{\mu}_i - O_i)$$
     - If $\hat{\mu}_i > O_i$, the ward is demonstrably **underreported** relative to its actuarially expected infrastructure defect rate.
     - The **Equity Boost** $\beta_i \in [0.0, \beta_{\max}]$ is proportional to this expected-vs-observed gap:
       $$\beta_i = \min\left(\beta_{\max}, \gamma \cdot \frac{\Delta_i}{\hat{\mu}_i + \epsilon}\right)$$
       (with provisional cold-start defaults $\beta_{\max} = 0.25, \gamma = 0.5$, explicitly subject to re-estimation pending real empirical data tuning per Bootstrap Principle §A3).
     - Stored explicitly on the ward credibility table as `expected_issue_rate`, `observed_issue_rate`, `equity_gap`, and `equity_boost`.
     - Final Priority Score:
       $$P_{\text{final}} = \min(100.0, (P_{\text{raw}} + \beta_i) \times 100.0)$$

3. **Confidence-Gating and Human Review Routing (§A12, §A13):**
   - Confidence $C \in [0.0, 1.0]$ is computed based on data maturity and observation verification:
     $$Z_{\text{conf}} = \frac{n_{\text{obs}}}{n_{\text{obs}} + K_{\text{conf}}}$$
     incorporating inspector verification status and multi-source concordance.
   - **The Confidence Gate Rule:**
     - When raw priority score is high ($P_{\text{final}} \ge P_{\text{threshold}}$, default $70.0$) AND confidence is low ($C < C_{\text{threshold}}$, default $0.50$):
       - The incident **must not auto-proceed to dispatch** (`assigned` / dispatch queue).
       - Instead, the incident state is set to `status = 'triaged'` with flag `requires_human_review = true` and `review_reason = 'high_priority_low_confidence'`.
       - It routes to the Dispatcher / Control Room Human Review Queue.
     - When confidence is adequate ($C \ge C_{\text{threshold}}$) or raw priority is below threshold, normal automated workflow proceeds.

4. **Decoupling from Living Taxonomy (Standing Invariant 1):**
   - Approving a living taxonomy category in Phase 3 NEVER triggers an AHP re-estimation. AHP operates strictly on the 5 normalized dimension sub-scores.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Deterministic Glass-Box Reproducibility (Standing Invariant 2):**
   - Given identical incident sub-scores ($s_S, s_R, s_E, s_C, s_U$), identical ward stats ($n_i, \bar{X}_i, O_i$), and identical AHP matrix $A$, the resulting $P_{\text{final}}$ must be identical to 6 decimal places. Zero LLM hallucinations or hidden stochastic terms.
2. **Saaty Consistency Ratio Hard Gate ($CR < 0.10$):**
   - For $n=5$, Random Index $RI_5 = 1.12$. A matrix proposal with $CR \ge 0.10$ is rejected with an explicit HTTP 422 error and blocked by PostgreSQL table constraint `chk_ahp_cr`.
3. **Decoupled Urgency Subscore (§A11, §A12):**
   - `subscore_urgency` reflects temporal decay and SLA proximity; it must NEVER be derived from or correlated with `intake_report.citizen_urgency_score`.
4. **Pure CPU Computation with Zero External APIs (Hard Rule 1):**
   - NumPy / pure Python for power iteration / eigenvalue extraction and Bühlmann variance calculations. No external paid/black-box APIs.
5. **Mandatory Scoped Grants (Standing Invariant 4):**
   - Every new table and function in migration 0007 has explicit scoped grants (`service_role`, `authenticated`, `anon`), zero `GRANT ALL`.
6. **Real Seeded Tests with Clean Teardown (Standing Invariant 5):**
   - Live Supabase integration tests use real pre-seeded organizations, wards, incidents, and valid JWTs, completely cleaning up in `finally` blocks.

---

## 3. Database Schema & Migration (`migrations/0007_phase6_ahp_credibility.sql`)

```sql
-- Migration 0007: Phase 6 - AHP 5-Criteria Config, Ward Equity Credibility, Incident Priority & Confidence Gating

-- 1. AHP Matrix Configuration (5 Dimensions: Severity, Risk, Exposure, Criticality, Urgency)
CREATE TABLE IF NOT EXISTS public.ahp_matrix_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    matrix JSONB NOT NULL,            -- 5x5 pairwise comparison matrix
    weights JSONB NOT NULL,           -- {"severity": w_s, "risk": w_r, "exposure": w_e, "criticality": w_c, "urgency": w_u}
    lambda_max DOUBLE PRECISION NOT NULL,
    consistency_index DOUBLE PRECISION NOT NULL,
    consistency_ratio DOUBLE PRECISION NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ahp_org_active UNIQUE (organization_id, is_active),
    CONSTRAINT chk_ahp_cr CHECK (consistency_ratio < 0.10)
);

-- 2. Ward Equity Credibility Table (Bühlmann Expected vs. Observed Rates)
CREATE TABLE IF NOT EXISTS public.ward_equity_credibility (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    verified_incident_count INTEGER NOT NULL DEFAULT 0,
    historical_incident_rate DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    credibility_factor DOUBLE PRECISION NOT NULL DEFAULT 0.0,     -- Z_i = n_i / (n_i + K)
    expected_issue_rate DOUBLE PRECISION NOT NULL DEFAULT 0.0,    -- \hat{\mu}_i = Z_i * X_bar + (1 - Z_i) * \mu_0
    observed_issue_rate DOUBLE PRECISION NOT NULL DEFAULT 0.0,    -- O_i
    equity_gap DOUBLE PRECISION NOT NULL DEFAULT 0.0,             -- max(0, expected - observed)
    equity_boost DOUBLE PRECISION NOT NULL DEFAULT 0.0,           -- \beta_i added to priority
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ward_equity_org_ward UNIQUE (organization_id, ward_id)
);

-- Optional SLA / Resolution stats retained for operational telemetry & Phase 10 ETA
CREATE TABLE IF NOT EXISTS public.ward_resolution_stat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    category_code VARCHAR(50) NOT NULL,
    resolved_count INTEGER NOT NULL DEFAULT 0,
    mean_resolution_hours DOUBLE PRECISION NOT NULL DEFAULT 48.0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ward_res_stat UNIQUE (ward_id, category_code)
);

-- 3. Extend Incident Table with 5 Sub-Scores, Confidence, Equity Boost, and Human Review Gating
ALTER TABLE public.incident
    ADD COLUMN IF NOT EXISTS subscore_severity DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_risk DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_exposure DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_criticality DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS subscore_urgency DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS raw_priority_score DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS equity_boost DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS priority_score DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS confidence_score DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS requires_human_review BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS review_reason TEXT DEFAULT NULL;

-- 4. Check Constraints
ALTER TABLE public.incident
    ADD CONSTRAINT chk_subscore_severity CHECK (subscore_severity >= 0.0 AND subscore_severity <= 1.0),
    ADD CONSTRAINT chk_subscore_risk CHECK (subscore_risk >= 0.0 AND subscore_risk <= 1.0),
    ADD CONSTRAINT chk_subscore_exposure CHECK (subscore_exposure >= 0.0 AND subscore_exposure <= 1.0),
    ADD CONSTRAINT chk_subscore_criticality CHECK (subscore_criticality >= 0.0 AND subscore_criticality <= 1.0),
    ADD CONSTRAINT chk_subscore_urgency CHECK (subscore_urgency >= 0.0 AND subscore_urgency <= 1.0),
    ADD CONSTRAINT chk_priority_score CHECK (priority_score >= 0.0 AND priority_score <= 100.0),
    ADD CONSTRAINT chk_confidence_score CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0);

-- 5. Row-Level Security (RLS) & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.ahp_matrix_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ward_equity_credibility ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ward_resolution_stat ENABLE ROW LEVEL SECURITY;

-- Service Role full access
CREATE POLICY service_role_ahp_config_all ON public.ahp_matrix_config
    FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY service_role_ward_equity_all ON public.ward_equity_credibility
    FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY service_role_ward_res_all ON public.ward_resolution_stat
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Authenticated Staff: Select scoped by organization membership in user_role_assignment
CREATE POLICY ahp_config_select_org ON public.ahp_matrix_config
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = ahp_matrix_config.organization_id
        )
    );

-- Admin Manage Policy: Writes strictly gated by is_org_admin(organization_id)
CREATE POLICY ahp_config_admin_manage ON public.ahp_matrix_config
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

CREATE POLICY ward_equity_select_org ON public.ward_equity_credibility
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = ward_equity_credibility.organization_id
        )
    );

CREATE POLICY ward_equity_admin_manage ON public.ward_equity_credibility
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

CREATE POLICY ward_res_select_org ON public.ward_resolution_stat
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = ward_resolution_stat.organization_id
        )
    );

CREATE POLICY ward_res_admin_manage ON public.ward_resolution_stat
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- Scoped Grants (Zero GRANT ALL)
REVOKE ALL ON TABLE public.ahp_matrix_config FROM PUBLIC;
GRANT SELECT ON TABLE public.ahp_matrix_config TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ahp_matrix_config TO service_role;
GRANT INSERT, UPDATE ON TABLE public.ahp_matrix_config TO authenticated;

REVOKE ALL ON TABLE public.ward_equity_credibility FROM PUBLIC;
GRANT SELECT ON TABLE public.ward_equity_credibility TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ward_equity_credibility TO service_role;
GRANT INSERT, UPDATE ON TABLE public.ward_equity_credibility TO authenticated;

REVOKE ALL ON TABLE public.ward_resolution_stat FROM PUBLIC;
GRANT SELECT ON TABLE public.ward_resolution_stat TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.ward_resolution_stat TO service_role;
GRANT INSERT, UPDATE ON TABLE public.ward_resolution_stat TO authenticated;
```

---

## 4. Software Architecture & Implementation Design

### 4.1 Domain Modules (`civicbrain/domain/prioritization/`)

1. **`ahp.py`:**
   - Class `AHPMatrix`:
     - Accepts $5 \times 5$ positive reciprocal matrix ($A_{ji} = 1 / A_{ij}, A_{ii} = 1$).
     - Computes principal eigenvalue $\lambda_{\max}$ and principal eigenvector via power iteration / NumPy eigen solver.
     - Normalizes eigenvector to sum to $1.0$: $(w_S, w_R, w_E, w_C, w_U)$.
     - Verifies $CR = \frac{\lambda_{\max} - 5}{4 \times 1.12} < 0.10$.
     - Default §A12 calibrated 5-criteria Saaty matrix:
       - Pairwise importances: Severity (1.0), Risk (1.2), Exposure (0.9), Criticality (1.5), Urgency (0.8).
   - Dataclass `CriteriaSubscores`:
     - Holds 5 explicit floats in $[0.0, 1.0]$: `severity`, `risk`, `exposure`, `criticality`, `urgency`.
   - Function `calculate_raw_priority(subscores: CriteriaSubscores, weights: dict[str, float]) -> float`.

2. **`equity.py`:**
   - Class `BuhlmannEquityCompensator`:
     - Method `compute_credibility_factor(n_i: int, k_param: float = 10.0) -> float`:
       $$Z_i = \frac{n_i}{n_i + K}$$
     - Method `compute_expected_issue_rate(observed_ward_rate: float, city_prior_rate: float, z_i: float) -> float`:
       $$\hat{\mu}_i = Z_i \cdot \bar{X}_i + (1 - Z_i) \cdot \mu_0$$
     - Method `calculate_equity_gap(expected_rate: float, observed_report_rate: float) -> float`:
       $$\Delta_i = \max(0.0, \hat{\mu}_i - O_i)$$
     - Method `calculate_equity_boost(equity_gap: float, expected_rate: float, max_boost: float = 0.25, gamma: float = 0.5) -> float`:
       $$\beta_i = \min\left(\beta_{\max}, \gamma \cdot \frac{\Delta_i}{\hat{\mu}_i + 1e-6}\right)$$
       where $\beta_{\max} = 0.25$ and $\gamma = 0.5$ are provisional defaults pending real-data tuning.

3. **`gate.py`:**
   - Function `evaluate_confidence_gate(raw_priority: float, equity_boost: float, confidence: float, priority_threshold: float = 70.0, confidence_threshold: float = 0.50) -> PriorityEvaluationResult`:
     - Computes `final_priority = min(100.0, (raw_priority + equity_boost) * 100.0)`.
     - Checks:
       ```python
       if final_priority >= priority_threshold and confidence < confidence_threshold:
           requires_human_review = True
           review_reason = "high_priority_low_confidence"
           target_status = IncidentStatus.TRIAGED # holds back from automated dispatch
       else:
           requires_human_review = False
           review_reason = None
           target_status = IncidentStatus.PRIORITIZED
       ```

### 4.2 REST API Surface (`civicbrain/api/v1/prioritization.py`)

- `POST /v1/prioritization/ahp/matrix`: Admin-only endpoint to configure/update the 5x5 AHP comparison matrix for the organization. Validates $CR < 0.10$.
- `GET /v1/prioritization/ahp/matrix/active`: Fetches active 5-criteria matrix and weights.
- `GET /v1/prioritization/equity/wards/{ward_id}`: Retrieves ward equity credibility statistics, expected vs. observed issue rates, and active equity boost.
- `POST /v1/prioritization/evaluate`: Evaluates an incident's 5 sub-scores + ward equity + confidence, returning the itemized glass-box breakdown and dispatch gating determination.

---

## 5. Verification Plan

1. **Unit Tests (`tests/test_ahp_credibility.py`):**
   - **5-Criteria AHP:**
     - Saaty $5 \times 5$ matrix computes exact 5 weights summing to $1.0 \pm 10^{-6}$.
     - Consistency Ratio: Valid matrix yields $CR < 0.10$; inconsistent matrix ($CR \ge 0.10$) raises validation error.
     - Glass-box determinism: 1,000 evaluations yield identical float results to 6 decimal places.
   - **Decoupling Assertion:**
     - Explicit test verifying `subscore_urgency` is never derived from or correlated with `citizen_urgency_score`.
   - **Equity Compensator:**
     - Cold-start ward ($n_i = 0 \implies Z_i = 0$): Expected rate equals city prior $\mu_0$ exactly.
     - Underreported ward ($O_i \ll \hat{\mu}_i$): Produces positive $\Delta_i$ and positive equity boost $\beta_i$.
     - Well-reported / over-reported ward ($O_i \ge \hat{\mu}_i$): Gap is 0.0, boost is 0.0.
   - **Confidence-Gating:**
     - High priority ($P = 85.0$) + Low confidence ($C = 0.35$): Gated to `requires_human_review = True`, `target_status = 'triaged'`, does NOT auto-proceed to dispatch.
     - High priority ($P = 85.0$) + High confidence ($C = 0.85$): Passes gate to `requires_human_review = False`, `target_status = 'prioritized'`.
     - Low priority ($P = 40.0$) + Low confidence ($C = 0.30$): Passes gate (does not clog review queue for non-critical incidents).

2. **Live Supabase Integration (`tests/test_live_supabase_phase6_ahp.py`):**
   - Execute against live Supabase (`isqepbxkzxfpvfdkcntw`).
   - Insert 5x5 AHP matrix, assert check constraints on all 5 sub-scores ($[0.0, 1.0]$) and priority ($[0.0, 100.0]$).
   - Verify DB-level CHECK constraint rejects matrix with $CR \ge 0.10$.
   - Test RLS: Non-admin staff cannot insert/update AHP config (via `is_org_admin(organization_id)`); staff cannot read other org's equity tables.
   - Assert clean teardown in `finally` block (Standing Invariant 5).

3. **CI & Quality Gates:**
   - Full test suite execution (`pytest -v`), ruff format check, ruff linter, and mypy (strict type checking across all files).
   - Push to `origin main` and verify green GitHub Actions run.
