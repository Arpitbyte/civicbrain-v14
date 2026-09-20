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
    - `incident_dedup_link`: Fellegi-Sunter / Splink record linkage pair recording similarity scores, match probability, and dedup decision.
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
  - Integrated `splink>=4.0.0` with Fellegi-Sunter record linkage.
  - Implemented spatial proximity comparisons (Euclidean/Haversine distance in meters) and Jaro-Winkler string similarity on category codes and descriptions.
  - Formulated cold-start provisional priors ($P(\text{Match}) = 0.05$, spatial $m/u$ ratio of 10.0, category match $m/u$ ratio of 5.0) explicitly labeled as cold-start defaults pending re-estimation via Expectation-Maximization as real municipal datasets accumulate.
  - Automated triage categorization:
    - $P \ge 0.85$: `duplicate_auto`
    - $0.50 \le P < 0.85$: `duplicate_suspected`
    - $P < 0.50$: `distinct`
- **Anonymous Tracking & Token Security:**
  - Designed and deployed PostgreSQL `SECURITY DEFINER` function `get_anonymous_intake_report(p_tracking_token TEXT)` that safely looks up and sanitizes report and observation data by tracking token without exposing citizen PII.
  - Enforced IP-based rate limiting on `GET /v1/intake/reports/track` (10 requests per minute per client IP, returning HTTP 429 when rate limit is exceeded).
  - Standing Invariant 4 compliance: Table `intake_report` grants `INSERT` to `anon` but strictly denies `SELECT` (raising PostgreSQL 42501 permission denied upon direct select), ensuring anonymous citizens can only inspect reports through the audited RPC function.
- **Database Migration (`migrations/0003_phase2_intake_incident_dedup.sql`):**
  - Applied cleanly to live Supabase (`isqepbxkzxfpvfdkcntw`).
  - Contains explicit per-role scoped grants (`service_role`, `authenticated`, `anon`) with zero blanket `GRANT ALL`.
  - Configured PostGIS `Geometry('POINT', 4326)` for `intake_report.geom` and `incident.geom`.
  - Created RLS policies for citizen self-access, staff tenant/jurisdiction filtering, and public sanitized incident feed read-only access.
- **REST API Endpoints:**
  - `POST /v1/intake/reports`: Ingress endpoint for citizen and channel reports.
  - `GET /v1/intake/reports/track`: Token tracking endpoint with IP rate limiting and RPC execution.
  - `GET /v1/incidents`: Incident listing filtered by organization, department, ward, and status.
  - `GET /v1/incidents/{incident_id}`: Detailed incident retrieval.
  - `PATCH /v1/incidents/{incident_id}/status`: Operational status transition enforcing the 11-state machine.
  - `GET /v1/incidents/{incident_id}/observations`: Linked observations for an incident.

---

## 2. Key Architectural Decisions

1. **Security Definer RPC for Token-Based Anonymous Tracking:**
   Rather than granting anonymous roles direct SELECT permission on the `intake_report` table or relying on session variables that can be bypassed, anonymous tracking is mediated entirely through the `get_anonymous_intake_report` stored procedure. This procedure verifies the tracking token and returns a clean, PII-scrubbed JSON payload while the underlying table maintains zero anonymous read access.
2. **Deterministic Status Resolution for Appealed & Reopened Incidents:**
   When an incident is appealed or reopened, it re-enters active operational processing. Mapping both `appealed` and `reopened` to `in_progress` for the parent intake report prevents premature closure and signals to the reporting citizen that the issue remains under active municipal scrutiny.
3. **Splink Dual-Engine Support:**
   Engineered deduplication logic using standard Fellegi-Sunter log-likelihood updates with Jaro-Winkler string similarity and spatial distance, compatible with Splink 4's comparison library while providing deterministic cold-start execution prior to EM convergence.

---

## 3. Deviations from Specification

- None. All 11 incident states, multi-department routing, Splink integration, and rate limiting were built directly from §A7, §A11, and §A16 of the master specification.

---

## 4. Verification & CI Status

- [x] **Live Supabase Schema Applied:** Migration `0003_phase2_intake_incident_dedup.sql` applied cleanly with PostGIS point geometry columns on live Supabase.
- [x] **Scoped Grants Verified:** All 4 tables in migration 0003 have explicit scoped grants (zero blanket `GRANT ALL`).
- [x] **Live Client SDK Tests:** `tests/test_live_supabase_phase2_rls.py` executed against live Supabase asserting real pre-seeded rows, real Supabase Auth logins/JWTs, anonymous direct SELECT denial (42501), anonymous RPC success, and teardown in `finally` blocks.
- [x] **Local Test Suite:** 25 tests passing in 46.26s with zero lint errors (`ruff check`) and formatting verified (`ruff format`).
