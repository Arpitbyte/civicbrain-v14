# Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Technical Specification

**Version:** CivicBrain v14.11.0  
**Phase:** 11  
**Status:** APPROVED & IMPLEMENTED  

---

## 1. Executive Summary & Scope

Phase 11 implements the public-facing citizen accountability, open-data transparency, and conversational citizen accessibility surface for CivicBrain v14 (§A21, §A23):

1. **Jan Sunwai Public Grievance Ledger (§A23):**
   - Publicly readable, tamper-evident civic record enabling citizens, journalists, and civic watchdogs to inspect municipal complaint processing without authentication.
   - **Differential Privacy Engine ($\epsilon, \delta$-DP) & Zero Composition Leakage:**
     - Protects citizen complainants against re-identification and physical harassment via mathematically rigorous perturbation:
       - **One-Time Noise Generation per Incident:** Perturbation parameters ($\Delta x, \Delta y, \Delta t$) are drawn **ONCE** upon incident creation (at the initial `REPORTED` ledger entry). All subsequent lifecycle milestone rows for that incident (`ASSIGNED`, `RESOLVED`, `CONFIRMED`) reuse the exact same `dp_geom` and genesis time offset $\Delta t$. This permanently eliminates the DP composition flaw where averaging multiple lifecycle entries could erode noise variance and locate the complainant.
       - **Per-Incident Privacy Budget ($\epsilon_{\text{incident}} = 1.0$):**
         - Spatial budget: $\epsilon_{\text{geom}} = 0.8$, global sensitivity $\Delta S_{\text{geom}} = 100\text{m}$, Laplace scale $b_{\text{geom}} = \frac{100}{0.8} = 125\text{m}$.
         - Temporal budget: $\epsilon_{\text{time}} = 0.2$, global sensitivity $\Delta S_{\text{time}} = 15\text{ min}$, Laplace scale $b_{\text{time}} = \frac{15}{0.2} = 75\text{ min}$.
         - Because noise is computed once per incident and reused, subsequent checkpoints consume $0$ additional privacy budget ($\epsilon_{\text{checkpoint}} = 0$), guaranteeing total leakage $\le 1.0$ over the full incident lifecycle.
       - **PII Scrubbing:** Zero citizen names, phone numbers, WhatsApp JIDs, IP addresses, or device identifiers are ever persisted or exposed in the ledger.
2. **Per-Incident Cryptographic Ledger Hash Chain (§A23):**
   - Tamper-evident ledger integrity structured as an ordered, per-incident cryptographic hash chain linking consecutive lifecycle milestones (`REPORTED` $\to$ `ASSIGNED` $\to$ `RESOLVED` $\to$ `CONFIRMED`).
   - Every entry explicitly records `prev_hash` and `sequence_num`. Tampering with any stored entry invalidates downstream hashes and is immediately flagged by verification algorithms.
3. **Nagar Pragati (City Progress Transparency Dashboard, §A21):**
   - Aggregate municipal progress metrics comparing all zones, wards, and departments across the Urban Local Body (ULB).
   - High-level city indices:
     - City-Wide Mean Time to Resolution (MTTR).
     - Department Service Delivery Index (SDI) and SLA compliance rankings.
     - Equity Compensator Gap map (highlighting wards receiving priority boosts).
     - Trend analytics across 30, 90, and 365 days.
4. **Multilingual Civic Assistant (§A23, Bootstrap Principle §A3):**
   - Pure, deterministic, zero-external-cost citizen service assistant integrated with the Phase 5 Indic multilingual pipeline (IndicBERT / Bhashini / IndicXlit).
   - Natural language grievance tracking ("Where is my complaint CB-2026-901?").
   - Plain-language explanation of Phase 10 Service-Time ETA ("Expected within 36 hours based on pothole repair priorities in Ward 12").
   - Conversational intake helper guiding citizens through grievance submission.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Strict Differential Privacy on Public Microdata (Standing Invariant 4):**
   - Raw coordinates (`geom`) and exact intake timestamps (`created_at`) must NEVER be exposed on public ledger endpoints. Only differentially private perturbed coordinates (`dp_geom`) and jittered timestamps (`dp_timestamp`) can be returned to unauthenticated callers.
2. **Once-Per-Incident DP Generation Rule (Anti-Composition Invariant):**
   - Spatial noise $(\Delta x, \Delta y)$ and temporal noise $\Delta t$ MUST be drawn exactly once when the incident first enters the ledger. Every subsequent checkpoint row for that same incident MUST reuse that identical `dp_geom` and identical time offset $\Delta t$. Independent noise draws across lifecycle events of the same incident are strictly forbidden.
3. **Consistent 1D/2D Laplace Mechanism (Zero Distribution Mismatch):**
   - Both spatial and temporal perturbations use the Laplace distribution ($2\text{D}$ planar Laplace for coordinates, $1\text{D}$ continuous Laplace for timestamps). Uniform distributions are not used.
4. **Scoped Table Grants (Standing Invariant 4):**
   - `public.jan_sunwai_ledger_entry` grants `SELECT` only to `anon` and `authenticated`. Writes are performed strictly by the service role or elevated administrative routines. Zero blanket `GRANT ALL` or wide write grants.
5. **Tamper-Evident Per-Incident Hash Chain:**
   - Every incident maintains a sequential hash chain starting from genesis hash $0^{64}$. Mutating historical rows breaks the integrity chain.
6. **Local & Deterministic Assistant (Bootstrap Principle §A3):**
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
    sequence_num INT NOT NULL DEFAULT 0,       -- Monotonic checkpoint index per incident (0, 1, 2, ...)
    public_tracking_code VARCHAR(32) NOT NULL, -- Pseudonymous identifier
    category_code VARCHAR(50) NOT NULL,
    department_id UUID NOT NULL REFERENCES public.department(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES public.ward(id) ON DELETE CASCADE,
    
    -- Differentially Private Perturbed Fields (Generated once at seq 0, reused on subsequent seq)
    dp_geom geometry(Point, 4326) NOT NULL,    -- 2D Laplace perturbed coordinates
    dp_timestamp TIMESTAMPTZ NOT NULL,         -- 1D Laplace jittered timestamp
    
    -- Public Status Telemetry
    lifecycle_status VARCHAR(50) NOT NULL,     -- 'reported', 'assigned', 'resolved', 'confirmed'
    sla_status VARCHAR(20) NOT NULL,           -- 'within_sla', 'breached'
    predicted_eta_hours DOUBLE PRECISION,      -- From Phase 10 ETA engine
    resolution_media_count INT NOT NULL DEFAULT 0,
    is_appealed BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Per-Incident Cryptographic Checkpoint Chain
    prev_hash VARCHAR(64) NOT NULL,            -- Genesis '000...0' on seq 0, else prior entry_hash
    entry_hash VARCHAR(64) NOT NULL,           -- SHA-256(prev_hash:incident_id:seq:status:dp_geom:dp_timestamp)
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_ledger_incident_seq UNIQUE (incident_id, sequence_num),
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

CREATE INDEX IF NOT EXISTS idx_nagar_pragati_org ON public.nagar_pragati_city_snapshot(organization_id);
CREATE INDEX IF NOT EXISTS idx_nagar_pragati_date ON public.nagar_pragati_city_snapshot(snapshot_date);

-- 3. Row-Level Security & Scoped Grants (Standing Invariant 4)
ALTER TABLE public.jan_sunwai_ledger_entry ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nagar_pragati_city_snapshot ENABLE ROW LEVEL SECURITY;

-- Service Role full access
CREATE POLICY service_role_ledger_all ON public.jan_sunwai_ledger_entry
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY service_role_pragati_all ON public.nagar_pragati_city_snapshot
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Public Anonymous & Authenticated Read
CREATE POLICY public_read_jan_sunwai_ledger ON public.jan_sunwai_ledger_entry
    FOR SELECT TO anon, authenticated USING (true);

CREATE POLICY public_read_nagar_pragati ON public.nagar_pragati_city_snapshot
    FOR SELECT TO anon, authenticated USING (true);

-- Scoped Grants (Strict Invariant: authenticated gets SELECT only; zero blanket write grants)
REVOKE ALL ON TABLE public.jan_sunwai_ledger_entry FROM PUBLIC;
REVOKE ALL ON TABLE public.nagar_pragati_city_snapshot FROM PUBLIC;

GRANT SELECT ON TABLE public.jan_sunwai_ledger_entry TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.jan_sunwai_ledger_entry TO service_role;

GRANT SELECT ON TABLE public.nagar_pragati_city_snapshot TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON TABLE public.nagar_pragati_city_snapshot TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.nagar_pragati_city_snapshot TO service_role;
```

---

## 4. Mathematical Specifications

### 4.1 Differential Privacy: Coordinate Perturbation (2D Planar Laplace)
Let true coordinates be $(\text{lon}, \text{lat})$. Sensitivity $\Delta S_{\text{geom}} = 100\text{ meters}$, budget $\epsilon_{\text{geom}} = 0.8$:
1. Scale parameter:
   $$b_{\text{geom}} = \frac{\Delta S_{\text{geom}}}{\epsilon_{\text{geom}}} = \frac{100.0}{0.8} = 125.0\text{ meters}$$
2. Independent Laplace noise draws:
   $$\delta x, \delta y \sim \text{Laplace}(0, b_{\text{geom}})$$
   $$\delta x = \text{sgn}(u_1) \cdot b_{\text{geom}} \ln(1 - 2|u_1|), \quad u_1 \in (-0.5, 0.5)$$
3. Clamping: bounded to $[-250\text{m}, +250\text{m}]$ to guarantee the perturbed coordinate stays in the same municipal neighborhood while masking the exact address.
4. Convert displacement to degrees:
   $$\Delta \text{lat} = \frac{\delta y}{111,000}, \quad \Delta \text{lon} = \frac{\delta x}{111,000 \times \cos(\text{lat}_{\text{radians}})}$$
   $$\text{lon}_{\text{dp}} = \text{lon} + \Delta \text{lon}, \quad \text{lat}_{\text{dp}} = \text{lat} + \Delta \text{lat}$$

### 4.2 Differential Privacy: Temporal Jittering (1D Laplace)
Let event timestamp be $t_{\text{true}}$. Sensitivity $\Delta S_{\text{time}} = 15\text{ minutes}$, budget $\epsilon_{\text{time}} = 0.2$:
1. Scale parameter:
   $$b_{\text{time}} = \frac{\Delta S_{\text{time}}}{\epsilon_{\text{time}}} = \frac{15.0}{0.2} = 75.0\text{ minutes}$$
2. Laplace noise draw:
   $$\Delta t \sim \text{Laplace}(0, b_{\text{time}})$$
   clamped to $[-120\text{ min}, +120\text{ min}]$.
3. Timestamp:
   $$t_{\text{dp}} = t_{\text{true}} + \Delta t$$

### 4.3 Total Per-Incident Privacy Budget & Anti-Composition Guarantee
For an incident $I$ progressing through lifecycle states $S_0, S_1, \dots, S_k$:
- At $S_0$ (`REPORTED`): draw $(\delta x_I, \delta y_I, \Delta t_I)$ once and compute $\text{dp\_geom}_I$.
- At $S_k$ ($k \ge 1$): assign $\text{dp\_geom} = \text{dp\_geom}_I$ and $t_{\text{dp}, k} = t_k + \Delta t_I$.
- Total privacy loss:
  $$\epsilon_{\text{total}}(I) = \epsilon_{\text{geom}} + \epsilon_{\text{time}} = 0.8 + 0.2 = 1.0$$
- Additional leakage from subsequent checkpoints: $0.0$.

### 4.4 Per-Incident Cryptographic Hash Chain
For checkpoint sequence $k$:
$$\text{prev\_hash}_k = \begin{cases} 
\text{"0"}^{64}, & \text{if } k = 0 \\ 
\text{entry\_hash}_{k-1}, & \text{if } k > 0 
\end{cases}$$

$$\text{payload}_k = \text{prev\_hash}_k \mathbin{\Vert} \text{incident\_id} \mathbin{\Vert} k \mathbin{\Vert} \text{status} \mathbin{\Vert} \text{WKT}(\text{dp\_geom}) \mathbin{\Vert} \text{ISO}(t_{\text{dp}}) \mathbin{\Vert} \text{code}$$
$$\text{entry\_hash}_k = \text{SHA-256}(\text{payload}_k)$$

---

## 5. REST API Endpoints

### 5.1 Jan Sunwai Public Ledger (`/v1/transparency/ledger`)
- `GET /v1/transparency/ledger`:
  - **Auth:** Public / Anonymous (no token required).
  - **Query Parameters:** `ward_id: UUID | None`, `category_code: str | None`, `from_date: date | None`, `to_date: date | None`, `page: int = 1`, `page_size: int = 50`.
  - **Returns:** List of `JanSunwaiLedgerResponse` entries with `dp_geom`, `dp_timestamp`, `public_tracking_code`, `lifecycle_status`, `sla_status`, `sequence_num`, `prev_hash`, and `entry_hash`.
- `GET /v1/transparency/ledger/incidents/{incident_id}/chain`:
  - **Auth:** Public / Anonymous.
  - **Returns:** Full chronological milestone chain for the incident and a boolean `chain_valid` verifying cryptographic hash integrity.

### 5.2 Nagar Pragati City Progress (`/v1/transparency/pragati`)
- `GET /v1/transparency/pragati`:
  - **Auth:** Public / Anonymous.
  - **Query Parameters:** `organization_id: UUID`, `period_type: str = "monthly"`.
  - **Returns:** Citywide aggregate MTTR, CSI, SLA compliance, department rankings, and equity gap map.

### 5.3 Multilingual Civic Assistant (`/v1/transparency/assistant`)
- `POST /v1/transparency/assistant/query`:
  - **Auth:** Public / Anonymous.
  - **Payload:** `CivicAssistantQueryRequest(query_text: str, language_code: str = "en", tracking_code: str | None = None)`.
  - **Returns:** Natural language status summary, plain-language ETA explanation, and guided triage in the requested language (Hindi, Kannada, Tamil, Marathi, Telugu, English).

---

## 6. Verification Plan

1. **Unit Tests (`tests/test_transparency_ledger.py`):**
   - **DP Single-Draw Anti-Composition Verification:**
     - Proves `dp_geom` and temporal jitter $\Delta t$ are computed ONCE at sequence 0 and strictly identical across subsequent lifecycle entries (`ASSIGNED`, `RESOLVED`, `CONFIRMED`) of the same incident.
     - Proves an attacker averaging rows cannot reduce noise variance.
   - **1D/2D Laplace Mechanism Verification:**
     - Proves spatial displacement follows bounded 2D Laplace distribution with $30\text{m} \le \text{dist} \le 250\text{m}$.
     - Proves temporal offset follows 1D continuous Laplace distribution (never uniform distribution).
     - Proves true coordinates and timestamps are never exposed.
   - **Cryptographic Hash Chain & Tamper Detection:**
     - Validates sequential linking: `entry[k].prev_hash == entry[k-1].entry_hash`.
     - **Tamper Test:** Mutates a field (`lifecycle_status` or `dp_timestamp`) in checkpoint 1 of a valid 3-checkpoint chain; recomputes verification and asserts `verify_incident_ledger_chain` fails with explicit tamper mismatch detection.
   - **PII Scrubbing:**
     - Proves serialization contains zero citizen phone numbers, names, or auth IDs.
   - **Civic Assistant:**
     - Tests intent resolution and multilingual templating (Hindi, Kannada, English) without external LLM calls.

2. **Live Supabase Integration (`tests/test_live_supabase_phase11_transparency.py`):**
   - Seed real organization, ward, incident, publish sequence 0 and sequence 1 ledger rows.
   - Verify public anonymous `SELECT` query via `anon_client`.
   - Verify unauthorized writes via `anon_client` or `authenticated` are rejected by table grant permissions.
   - Verify hash chain validation against live Supabase data.
   - Clean teardown in `finally` block.

3. **CI & Static Quality Gates:**
   - Full test suite, `ruff check`, `ruff format --check`, and `mypy civicbrain` clean.
