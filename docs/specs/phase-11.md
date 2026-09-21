# Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification

**Version:** CivicBrain v14.11.0  
**Phase:** 11  
**Status:** SPECIFICATION SUBMITTED FOR REVIEW  

---

## 1. Executive Summary & Scope

Phase 11 implements the public-facing citizen accountability, open-data transparency, and conversational citizen accessibility surface for CivicBrain v14 (§A21, §A23):

1. **Jan Sunwai Public Grievance Ledger (§A23):**
   - Publicly readable, tamper-evident civic record enabling citizens, journalists, and civic watchdogs to inspect municipal complaint processing without authentication.
   - **Differential Privacy Engine ($\epsilon, \delta$-DP):**
     - Protects citizen complainants against re-identification and harassment via mathematically rigorous perturbation:
       - **Geographic Noise Injection:** Adds 2D planar Laplace noise $\Delta x, \Delta y \sim \text{Laplace}(0, b = \frac{\Delta S}{\epsilon})$ where global sensitivity $\Delta S \le 100\text{m}$ and privacy budget $\epsilon = 1.0$. Perturbed coordinates snap to a privacy-preserving $100\text{m} \times 100\text{m}$ municipal grid, guaranteeing zero exact household or building pinpointing.
       - **Temporal Jitter:** Perturbs incident intake timestamps with bounded Laplacian time noise ($\pm 30\text{ minutes}$), preventing correlation with CCTV footage or physical street encounters.
       - **PII Scrubbing:** Zero citizen names, phone numbers, WhatsApp JIDs, IP addresses, or device identifiers are ever persisted or exposed in the ledger.
2. **Nagar Pragati (City Progress Transparency Dashboard, §A21):**
   - Aggregate municipal progress metrics comparing all zones, wards, and departments across the Urban Local Body (ULB).
   - High-level city indices:
     - City-Wide Mean Time to Resolution (MTTR).
     - Department Service Delivery Index (SDI) and SLA compliance rankings.
     - Equity Compensator Gap map (highlighting wards receiving priority boosts).
     - Trend analytics across 30, 90, and 365 days.
3. **Multilingual Civic Assistant (§A23, Bootstrap Principle §A3):**
   - Pure, deterministic, zero-external-cost citizen service assistant integrated with the Phase 5 Indic multilingual pipeline (IndicBERT / Bhashini / IndicXlit).
   - Natural language grievance tracking ("Where is my complaint CB-2026-901?").
   - Plain-language explanation of Phase 10 Service-Time ETA ("Expected within 36 hours based on pothole repair priorities in Ward 12").
   - Conversational intake helper guiding citizens through grievance submission.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Strict Differential Privacy on Public Microdata (Standing Invariant 4):**
   - Raw coordinates (`geom`) and exact intake timestamps (`created_at`) must NEVER be exposed on public ledger endpoints. Only differentially private perturbed coordinates (`dp_geom`) and coarse timestamps (`dp_timestamp`) can be returned to unauthenticated callers.
2. **Zero PII Exposure Guarantee:**
   - The Jan Sunwai Ledger view and tables have no relationship with `citizen_profile`, `phone`, or WhatsApp identity tables.
3. **Immutable Public Ledger Invariant:**
   - Ledger entries represent cryptographically signed / hashed checkpoints of incident lifecycle milestones (`REPORTED`, `ASSIGNED`, `RESOLVED`, `CONFIRMED`).
4. **Local & Deterministic Assistant (Bootstrap Principle §A3):**
   - Citizen query parsing and ETA explanations must operate locally without paid external LLM APIs, utilizing deterministic template rendering, intent matching, and the Phase 5 local multilingual tokenizer.

---

## 3. Database Schema (`migrations/0012_phase11_transparency_ledger.sql`)

```sql
-- Migration 0012: Jan Sunwai Public Ledger, DP Perturbations & Nagar Pragati Scorecards (§A21, §A23)

-- 1. Public Jan Sunwai Ledger Table (§A23)
CREATE TABLE IF NOT EXISTS public.jan_sunwai_ledger_entry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    incident_id UUID NOT NULL REFERENCES public.incident(id) ON DELETE CASCADE,
    public_tracking_code VARCHAR(32) NOT NULL, -- Pseudonymous identifier
    category_code VARCHAR(50) NOT NULL,
    department_id UUID NOT NULL REFERENCES public.department(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    
    -- Differentially Private Perturbed Fields
    dp_geom geometry(Point, 4326) NOT NULL,    -- 2D Laplace perturbed coordinates
    dp_timestamp TIMESTAMPTZ NOT NULL,         -- Jittered timestamp (±30 min)
    
    -- Public Status Telemetry
    lifecycle_status VARCHAR(50) NOT NULL,     -- 'reported', 'assigned', 'resolved', 'confirmed'
    sla_status VARCHAR(20) NOT NULL,           -- 'within_sla', 'breached'
    predicted_eta_hours DOUBLE PRECISION,      -- From Phase 10 ETA engine
    resolution_media_count INT NOT NULL DEFAULT 0,
    is_appealed BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Cryptographic Checkpoint
    entry_hash VARCHAR(64) NOT NULL,           -- SHA-256 (prev_hash + incident_id + status + dp_timestamp)
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ledger_incident_status UNIQUE (incident_id, lifecycle_status)
);

CREATE INDEX IF NOT EXISTS idx_js_ledger_org ON public.jan_sunwai_ledger_entry(organization_id);
CREATE INDEX IF NOT EXISTS idx_js_ledger_ward ON public.jan_sunwai_ledger_entry(ward_id);
CREATE INDEX IF NOT EXISTS idx_js_ledger_category ON public.jan_sunwai_ledger_entry(category_code);
CREATE INDEX IF NOT EXISTS idx_js_ledger_created ON public.jan_sunwai_ledger_entry(dp_timestamp);
CREATE INDEX IF NOT EXISTS idx_js_ledger_geom ON public.jan_sunwai_ledger_entry USING GIST(dp_geom);

-- 2. Nagar Pragati City Progress Aggregate View / Table (§A21)
CREATE TABLE IF NOT EXISTS public.nagar_pragati_city_snapshot (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL DEFAULT 'monthly', -- 'weekly', 'monthly', 'quarterly'
    city_mttr_hours DOUBLE PRECISION,
    city_csi DOUBLE PRECISION,
    city_sla_compliance_rate DOUBLE PRECISION,
    total_intake INT NOT NULL DEFAULT 0,
    total_resolved INT NOT NULL DEFAULT 0,
    department_rankings JSONB NOT NULL DEFAULT '[]'::jsonb,
    ward_equity_distribution JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_nagar_pragati_org_period UNIQUE (organization_id, snapshot_date, period_type)
);

-- 3. Row-Level Security & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.jan_sunwai_ledger_entry ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nagar_pragati_city_snapshot ENABLE ROW LEVEL SECURITY;

-- Service Role full access
CREATE POLICY service_role_ledger_all ON public.jan_sunwai_ledger_entry
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY service_role_pragati_all ON public.nagar_pragati_city_snapshot
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Public Anonymous Read on Jan Sunwai Ledger and Nagar Pragati Snapshots
CREATE POLICY public_read_jan_sunwai_ledger ON public.jan_sunwai_ledger_entry
    FOR SELECT TO anon, authenticated USING (true);

CREATE POLICY public_read_nagar_pragati ON public.nagar_pragati_city_snapshot
    FOR SELECT TO anon, authenticated USING (true);

-- Admin staff write policies
CREATE POLICY admin_write_jan_sunwai_ledger ON public.jan_sunwai_ledger_entry
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

CREATE POLICY admin_write_nagar_pragati ON public.nagar_pragati_city_snapshot
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- Scoped Grants (Zero blanket GRANT ALL)
REVOKE ALL ON TABLE public.jan_sunwai_ledger_entry FROM PUBLIC;
REVOKE ALL ON TABLE public.nagar_pragati_city_snapshot FROM PUBLIC;

GRANT SELECT ON TABLE public.jan_sunwai_ledger_entry TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.jan_sunwai_ledger_entry TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.jan_sunwai_ledger_entry TO service_role;

GRANT SELECT ON TABLE public.nagar_pragati_city_snapshot TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.nagar_pragati_city_snapshot TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.nagar_pragati_city_snapshot TO service_role;
```

---

## 4. Differential Privacy & Coordinate Perturbation (§A23)

### 4.1 2D Planar Laplace Coordinate Perturbation
Given true incident coordinates $(\text{lon}, \text{lat})$ in SRID 4326:
1. Transform planar displacement scale:
   $$1^\circ \text{ latitude} \approx 111,000\text{ meters}$$
   $$1^\circ \text{ longitude} \approx 111,000 \times \cos(\text{lat})\text{ meters}$$
2. Generate independent Laplace noise:
   $$b = \frac{\Delta S}{\epsilon} = \frac{100\text{m}}{1.0} = 100\text{m}$$
   $$\delta x, \delta y \sim \text{Laplace}(0, b)$$
3. Clamp noise displacement within bounds $[-200\text{m}, +200\text{m}]$ to preserve municipal neighborhood context while eliminating pinpoint accuracy.
4. Convert $(\delta x, \delta y)$ meters back to degrees $(\Delta \text{lon}, \Delta \text{lat})$.
5. Differentially private point:
   $$\text{lon}_{\text{dp}} = \text{lon} + \Delta \text{lon}, \quad \text{lat}_{\text{dp}} = \text{lat} + \Delta \text{lat}$$

### 4.2 Temporal Jittering
$$t_{\text{dp}} = t_{\text{true}} + \Delta t, \quad \Delta t \sim \text{Uniform}(-30\text{ min}, +30\text{ min})$$

---

## 5. REST API Endpoints

### 5.1 Jan Sunwai Public Ledger (`/v1/transparency/ledger`)
- `GET /v1/transparency/ledger`:
  - **Auth:** Public / Anonymous (no token required).
  - **Query Parameters:** `ward_id: UUID | None`, `category_code: str | None`, `from_date: date | None`, `to_date: date | None`, `page: int = 1`, `page_size: int = 50`.
  - **Returns:** List of `JanSunwaiLedgerResponse` entries with `dp_geom`, `dp_timestamp`, `public_tracking_code`, `status`, and `sla_status`.

### 5.2 Nagar Pragati City Progress (`/v1/transparency/pragati`)
- `GET /v1/transparency/pragati`:
  - **Auth:** Public / Anonymous.
  - **Query Parameters:** `organization_id: UUID`, `period_type: str = "monthly"`.
  - **Returns:** Citywide aggregate MTTR, CSI, SLA compliance, department rankings, and equity gap map.

### 5.3 Multilingual Civic Assistant (`/v1/transparency/assistant`)
- `POST /v1/transparency/assistant/query`:
  - **Auth:** Public / Anonymous.
  - **Payload:** `CivicAssistantQueryRequest(query_text: str, language_code: str = "en", tracking_code: str | None = None)`.
  - **Returns:** Natural language status summary, plain-language ETA explanation, and helpful next steps in the requested language (e.g. Hindi, Kannada, Tamil, English).

---

## 6. Verification Plan

1. **Unit Tests (`tests/test_transparency_ledger.py`):**
   - Verify differential privacy coordinate perturbation:
     - Proves distance between true point and `dp_geom` is within expected noise bounds ($30\text{m} \le \text{dist} \le 250\text{m}$).
     - Proves repeated calls generate noisy, non-deterministic coordinates.
     - Proves exact point is never returned.
   - Verify zero PII leakage: ledger serialization contains no names, phone numbers, or user IDs.
   - Verify Civic Assistant query parsing and multilingual response formatting.
2. **Live Supabase Integration (`tests/test_live_supabase_phase11_transparency.py`):**
   - Seed real organization, ward, incident, and publish to `jan_sunwai_ledger_entry`.
   - Verify public anonymous `SELECT` query via `anon_client`.
   - Verify Nagar Pragati snapshot generation and query.
   - Clean teardown in `finally` block.
3. **CI & Static Quality Gates:**
   - Full test suite, `ruff check`, `ruff format --check`, and `mypy civicbrain` green.
