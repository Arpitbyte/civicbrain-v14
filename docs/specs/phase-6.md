# Phase 6: AHP Prioritization & Bühlmann Credibility Engine — Technical Specification

**Version:** CivicBrain v14.6.0  
**Phase:** 6  
**Status:** SPECIFICATION PENDING APPROVAL  

---

## 1. Executive Summary & Scope

Phase 6 implements the core deterministic civic prioritization engine for CivicBrain v14 (§A12, §A13):
1. **Analytic Hierarchy Process (AHP) Engine (§A12):**
   - Multi-criteria decision engine evaluating civic incidents across 4 orthogonal dimensions:
     1. $C_1$: Severity & Structural Hazard ($w_1$).
     2. $C_2$: Population Density & Ward Vulnerability ($w_2$).
     3. $C_3$: SLA Breach Risk & Temporal Aging ($w_3$).
     4. $C_4$: Critical Infrastructure Proximity ($w_4$, hospitals, schools, transit corridors).
   - Pairwise comparison matrix $A \in \mathbb{R}^{4 \times 4}$ with principal eigenvector computation ($\lambda_{\max}$).
   - Strict Consistency Ratio ($CR = \frac{CI}{RI} < 0.10$) enforcement. If $CR \ge 0.10$, the weight matrix is rejected and falls back to deterministic equal weighting until human administrator re-triage.
2. **Bühlmann Credibility Self-Bootstrapping Engine (§A13, Bootstrap Principle §A3):**
   - Self-calibrating credibility formula:
     $$\hat{\mu}_i = Z_i \bar{X}_i + (1 - Z_i) \mu_0$$
     where credibility factor $Z_i = \frac{n_i}{n_i + K}$, $n_i$ is ward historical resolved volume, and $K$ is the Bühlmann structural parameter ($K = \frac{s^2}{a}$).
   - In cold-start ($n_i = 0 \implies Z_i = 0$), prioritization relies 100% on the city-wide collective prior $\mu_0$ (zero data requirement, zero IoT dependencies).
   - As localized operational history accumulates ($n_i \to \infty \implies Z_i \to 1$), the estimate smoothly transitions to ward-empirical performance without discontinuous step-function jumps.
3. **Decoupling from Living Taxonomy (Standing Invariant 1):**
   - Approving a category in the Living Taxonomy (§A11) NEVER triggers an AHP re-estimation. AHP weights operate on normalized category-independent criteria.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Deterministic Glass-Box Reproducibility (Standing Invariant 2):**
   - Given the identical incident attributes, ward volume, and AHP matrix, the priority score $P \in [0.0, 100.0]$ must be identical to 6 decimal places. Zero non-deterministic LLM scoring.
2. **Consistency Ratio Hard Gate ($CR < 0.10$):**
   - Any proposed AHP criteria matrix with $CR \ge 0.10$ raises a validation error.
3. **Zero Proprietary/External Math APIs (Hard Rule 1):**
   - Eigenvector calculation, power iteration, and Bühlmann variance decomposition run natively in pure Python/NumPy on CPU.

---

## 3. Database Migration & Schema Design (`migrations/0007_phase6_ahp_credibility.sql`)

```sql
-- Migration 0007: AHP Matrices, Ward Credibility Parameters & Priority Score

-- 1. AHP Configuration Table per Organization
CREATE TABLE IF NOT EXISTS public.ahp_matrix_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    matrix JSONB NOT NULL,
    weights JSONB NOT NULL,
    lambda_max DOUBLE PRECISION NOT NULL,
    consistency_ratio DOUBLE PRECISION NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ahp_org_active UNIQUE (organization_id, is_active)
);

-- 2. Extend Incident with Priority Score and Criteria Breakdown
ALTER TABLE public.incident
    ADD COLUMN IF NOT EXISTS priority_score DOUBLE PRECISION DEFAULT 0.0,
    ADD COLUMN IF NOT EXISTS criteria_breakdown JSONB DEFAULT '{}'::jsonb;

-- 3. Ward Historical Volume & Bühlmann Credibility Table
CREATE TABLE IF NOT EXISTS public.ward_credibility_stat (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    category_code VARCHAR(50) NOT NULL,
    resolved_count INTEGER NOT NULL DEFAULT 0,
    mean_resolution_hours DOUBLE PRECISION NOT NULL DEFAULT 48.0,
    credibility_factor DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ward_cred_cat UNIQUE (ward_id, category_code)
);

-- Scoped Grants
REVOKE ALL ON TABLE public.ahp_matrix_config FROM PUBLIC;
GRANT SELECT ON TABLE public.ahp_matrix_config TO anon, authenticated;
GRANT ALL ON TABLE public.ahp_matrix_config TO service_role;

REVOKE ALL ON TABLE public.ward_credibility_stat FROM PUBLIC;
GRANT SELECT ON TABLE public.ward_credibility_stat TO anon, authenticated;
GRANT ALL ON TABLE public.ward_credibility_stat TO service_role;
```

---

## 4. Verification Plan

1. **Unit Tests (`tests/test_ahp_credibility.py`):**
   - AHP matrix consistency: Valid Saaty matrix achieves $CR < 0.10$; inconsistent matrix is rejected.
   - Bühlmann asymptotic behavior: $n_i = 0 \implies Z_i = 0$; $n_i = 100 \implies Z_i > 0.85$.
   - Glass-box determinism: Repeated executions produce byte-for-byte identical priority rankings.
2. **Live Supabase Integration (`tests/test_live_supabase_phase6_ahp.py`):**
   - Seed matrix, compute priority score, verify RLS boundaries and clean teardown in `finally`.
3. **CI & Quality Gates:**
   - Full test suite, ruff, and mypy green.
