# Phase 2: Domain Core & Incident Lifecycle — Implementation Log

**Date:** 2026-09-20  
**Status:** COMPLETED  
**Version:** CivicBrain v14.2.0  

---

## 1. What Was Built

- **Domain Core Entities & Split (§A7, §A16):**
  - Conformed 3-way domain separation decoupling citizen reports from physical municipal incidents:
    - `intake_report`: Citizen/channel ingress record (`channel` in `pwa`, `whatsapp`, `phone_ivr`, `staff_proxy`, `transparency_appeal`; `status` in `submitted`, `triaged`, `assigned`, `in_progress`, `resolved`, `rejected`, `closed`; `tracking_token` for unauthenticated lookup).
    - `observation`: Atomic departmental finding or photo analysis routed to a specific department (`detected`, `verified`, `dismissed`, `merged`).
    - `incident`: The canonical physical entity on the ground managed by municipal crews, scoped to an administrative ward and department.
    - `incident_dedup_link`: Fellegi-Sunter / Splink record linkage pair recording similarity scores, match probability, and dedup decision (`exact_match`, `probable_match`, `distinct`, `manual_review`).
- **Multi-Department Photo Routing (§A7):**
  - Modeled one-to-many relationship from `intake_report` to `observation`, allowing a single citizen report (or uploaded image) to generate multiple departmental observations routed to different service departments (e.g. ROADS for potholes, SWM for waste alongside the road).
- **Incident State Machine (§A16):**
  - Fully implemented the 11-state enum conforming to §A16:
    - Linear flow: `reported` -> `triaged` -> `verified` -> `prioritized` -> `assigned` -> `in_progress` -> `resolved` -> `confirmed`.
    - Branch states: `rejected`, `appealed`, `reopened`.
- **Least-Advanced Child Status Aggregation (§A7, Standing Invariant 3):**
  - Implemented deterministic aggregation mapping all 11 incident states to child observations and deriving the parent `intake_report.status`:
    - `reported` -> `submitted`
    - `triaged`, `verified`, `prioritized` -> `triaged`
    - `assigned` -> `assigned`
    - `in_progress`, `appealed`, `reopened` -> `in_progress`
    - `resolved` -> `resolved`
    - `confirmed` -> `closed`
    - `rejected` -> `rejected`
- **Splink Deduplication Integration (§A11, Bootstrap Principle §A3):**
  - Integrated `splink>=4.0.0` dependency.
  - Implemented spatial proximity comparisons (Euclidean/Haversine distance in meters) and deterministic Jaro-Winkler string similarity on category codes and descriptions.
  - Formulated cold-start provisional priors ($P(\text{Match}) = 0.05$, spatial $m/u$ ratio of 10.0, category match $m/u$ ratio of 5.0) explicitly labeled as cold-start defaults pending re-estimation via Expectation-Maximization as real municipal datasets accumulate.
  - Reconciled decision enum thresholds against `dedup_decision_enum`:
    - $P \ge 0.85$: `exact_match`
    - $0.50 \le P < 0.85$: `probable_match`
    - $P < 0.50$: `distinct`
    - `manual_review` reserved for flagged or operator-disputed linkage.
- **Anonymous Tracking & Upstash Redis Rate Limiting:**
  - Designed and deployed PostgreSQL `SECURITY DEFINER` function `get_anonymous_intake_report(p_tracking_token TEXT)` that safely looks up and sanitizes report and observation data by tracking token without exposing citizen PII.
  - Enforced Upstash Redis-backed rate limiting (`civicbrain/infra/redis.py`) on `GET /v1/intake/reports/track` (10 requests per minute per client IP via atomic `INCR` and `EXPIRE`, returning HTTP 429 when rate limit is exceeded), preventing state reset on Render free-tier cold starts.
  - Standing Invariant 4 compliance: Table `intake_report` grants `INSERT` to `anon` but strictly denies `SELECT` (raising PostgreSQL 42501 permission denied upon direct select), ensuring anonymous citizens can only inspect reports through the audited RPC function.
- **Database Migration (`migrations/0003_phase2_intake_incident_dedup.sql`):**
  - Applied cleanly to live Supabase (`isqepbxkzxfpvfdkcntw`).
  - Contains explicit per-role scoped grants (`service_role`, `authenticated`, `anon`) with zero blanket `GRANT ALL`.
  - Configured PostGIS `Geometry('POINT', 4326)` for `intake_report.geom` and `incident.geom`.
  - Created RLS policies for citizen self-access, staff tenant/jurisdiction filtering, and public sanitized incident feed read-only access.
- **REST API Endpoints:**
  - `POST /v1/intake/reports`: Ingress endpoint for citizen and channel reports.
  - `GET /v1/intake/reports/track`: Token tracking endpoint with Upstash Redis rate limiting and RPC execution.
  - `GET /v1/incidents`: Incident listing filtered by organization, department, ward, and status.
  - `GET /v1/incidents/{incident_id}`: Detailed incident retrieval.
  - `PATCH /v1/incidents/{incident_id}/status`: Operational status transition enforcing the 11-state machine.
  - `GET /v1/incidents/{incident_id}/observations`: Linked observations for an incident.

---

## 2. Key Architectural Decisions

1. **Security Definer RPC for Token-Based Anonymous Tracking:**
   Rather than granting anonymous roles direct SELECT permission on the `intake_report` or `observation` tables or relying on session variables that can be bypassed, anonymous tracking is mediated entirely through the `get_anonymous_intake_report` stored procedure. This procedure verifies the tracking token and returns a clean, PII-scrubbed JSON payload while the underlying tables maintain zero anonymous read access.
2. **Deterministic Status Resolution for Appealed & Reopened Incidents:**
   When an incident is appealed or reopened, it re-enters active operational processing. Mapping both `appealed` and `reopened` to `in_progress` for the parent intake report prevents premature closure and signals to the reporting citizen that the issue remains under active municipal scrutiny.
3. **Upstash Redis for Ingress Rate Limiting:**
   Switched from in-memory dictionary storage to Upstash Redis (`UPSTASH_REDIS_URL`) using an atomic key increment and 60-second TTL. This guarantees rate limits are respected across server worker restarts and Render free-tier container cold starts.

---

## 3. Deviations from Specification

1. **Omission of Direct `SELECT` Grant on `observation` for `anon`:**
   - **Rationale:** The approved specification text noted that citizens can track individual observation statuses. However, granting `anon` a direct `SELECT` grant on the `observation` table would allow any anonymous client to query `/rest/v1/observation` directly via PostgREST, bulk-scraping raw citizen reports, confidence scores, and unverified defect detections across the entire municipality.
   - **Design Choice:** In adherence to the principle of least privilege and Standing Invariant 4, `anon` was deliberately denied direct `SELECT` on `observation`. Instead, anonymous reading of observations is routed strictly through the `get_anonymous_intake_report(p_tracking_token)` `SECURITY DEFINER` RPC. This provides the reporting citizen complete visibility into all child observations linked to their specific report token, while preserving complete privacy against external scraping.
2. **Deduplication Decision Enum Reconciliation:**
   - Earlier working notes referenced conceptual labels (`duplicate_auto`, `duplicate_suspected`, `distinct`). The database migration (`dedup_decision_enum`) and Python domain models (`DedupDecision`) formally define: `exact_match`, `probable_match`, `distinct`, `manual_review`.
   - The decision logic in `civicbrain/domain/intake/dedup.py` maps $P \ge 0.85 \to$ `exact_match`, $0.50 \le P < 0.85 \to$ `probable_match`, and $P < 0.50 \to$ `distinct`, matching the database enum exactly.
3. **Pure Math Implementation of Cold-Start Linkage vs Full DuckDB Linker Batch:**
   - `civicbrain/domain/intake/dedup.py` implements the Fellegi-Sunter log-likelihood math with explicit cold-start weights directly rather than instantiating an in-memory DuckDB `splink.Linker` on every atomic single-record HTTP request. This achieves sub-millisecond evaluation latency per ingress report while adhering to the Bootstrap Principle (§A3) until bulk batch volume warrants empirical EM parameter estimation.

---

## 4. Verification & CI Status

- [x] **Live Supabase Schema Applied:** Migration `0003_phase2_intake_incident_dedup.sql` applied cleanly with PostGIS point geometry columns on live Supabase.
- [x] **Scoped Grants Verified:** All 4 tables in migration 0003 have explicit scoped grants (zero blanket `GRANT ALL`).
- [x] **Live Client SDK Tests:** `tests/test_live_supabase_phase2_rls.py` executed against live Supabase asserting real pre-seeded rows, real Supabase Auth logins/JWTs, anonymous direct SELECT denial (42501), anonymous RPC success, and teardown in `finally` blocks.
- [x] **Upstash Redis Rate Limiting:** Verified via `tests/test_intake_api.py` asserting requests 1–10 pass and requests 11–12 are rejected with HTTP 429.
- [x] **Local Test Suite:** All tests passing with zero lint errors (`ruff check`) and formatting verified (`ruff format`).
