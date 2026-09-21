# Phase 11: Citizen Transparency Board, Jan Sunwai Ledger with Differential Privacy, Nagar Pragati & Civic Assistant — Implementation Log

**Date:** 2026-09-21  
**Status:** COMPLETED  
**Version:** CivicBrain v14.11.0  

---

## 1. What Was Built

- **Jan Sunwai Public Grievance Ledger Table (§A23):**
  - Migration `migrations/0012_phase11_transparency_ledger.sql` introducing `jan_sunwai_ledger_entry` and `nagar_pragati_city_snapshot`.
  - Composite uniqueness: `uq_ledger_incident_seq UNIQUE (incident_id, sequence_num)` and `uq_ledger_incident_status UNIQUE (incident_id, lifecycle_status)`.
  - Scoped table grants: Verified directly from live migration content. Zero literal `GRANT ALL` exists.
    - `jan_sunwai_ledger_entry`: `GRANT SELECT` to `anon, authenticated`; `GRANT SELECT, INSERT, UPDATE, DELETE` to `service_role`.
    - `nagar_pragati_city_snapshot`: `GRANT SELECT` to `anon, authenticated`; `GRANT SELECT, INSERT, UPDATE` to `authenticated`; `GRANT SELECT, INSERT, UPDATE, DELETE` to `service_role`. (RLS policy restricts public/authenticated to `SELECT` only).
  - Exact Table Name on Live Database: `nagar_pragati_city_snapshot`.
  - Genesis Hash Invariant: `prev_hash` genesis value is strictly `"0" * 64` (64 zeros) across schema comments, models, services, and tests (any prior conversational summary shorthand referencing "GENESIS" is clarified: the codebase and live DB strictly adhere to `"0" * 64`).

- **Differential Privacy Engine with Anti-Composition Guarantee (§A23, Correction 1 & 2):**
  - **Single-Draw Perturbation Rule:** Spatial perturbation (`dp_geom`) and temporal jitter offset ($\Delta t$) are drawn **once** per incident at sequence 0 (`REPORTED`). All subsequent lifecycle checkpoints (`ASSIGNED`, `RESOLVED`, `CONFIRMED`) reuse the exact same `dp_geom` and temporal offset $\Delta t$. This eliminates the composition flaw where averaging multiple lifecycle entries would erode noise variance and compromise complainant privacy.
  - **Per-Incident Budget:** Fixed at $\epsilon_{\text{incident}} = 1.0$ ($\epsilon_{\text{geom}} = 0.8$, $\epsilon_{\text{time}} = 0.2$). Zero additional privacy leakage over subsequent checkpoint rows.
  - **Consistent Laplace Mechanisms:**
    - 2D Planar Laplace spatial noise: $b = 125.0$m, clamped to $[-250\text{m}, +250\text{m}]$, guaranteed minimal displacement $\ge 30$m.
    - 1D Continuous Laplace temporal noise: $b = 75.0$ min, clamped to $[-120\text{ min}, +120\text{ min}]$, guaranteed minimal jitter $\ge 5$ min.
  - **PII Scrubbing:** Zero citizen names, phone numbers, WhatsApp JIDs, IP addresses, or user IDs are ever exposed or stored in the ledger view.

- **Cryptographic Per-Incident Hash Chain & Tamper Detection (§A23, Correction 4):**
  - Structured as an ordered linear hash chain per incident linking milestone checkpoints.
  - Sequence 0 uses genesis hash `"0"*64`. Subsequent checkpoints verify $\text{prev\_hash}_k == \text{entry\_hash}_{k-1}$.
  - Verification service: `verify_incident_ledger_chain(entries) -> tuple[bool, str | None]` verifies both hash pointer continuity and recomputed SHA-256 payload integrity.

- **Nagar Pragati City Progress Scorecards (§A21):**
  - Municipal-wide transparency dashboard aggregating City MTTR, City CSI, SLA compliance, department resolution rates, and Ward Equity Credibility distribution.
  - Publicly readable without authentication via `GET /v1/transparency/pragati`.

- **Multilingual Civic Assistant (§A23, Bootstrap Principle §A3):**
  - Pure, deterministic, zero-external-cost citizen service assistant.
  - Intent classification (`STATUS_INQUIRY`, `INTAKE_GUIDANCE`, `GENERAL_ASSISTANCE`).
  - Multilingual response generation across English, Hindi, and Kannada using local templates.

---

## 2. Verification & Test Evidence

1. **Unit Test Suite (`tests/test_transparency_ledger.py`):**
   - Verified 2D Laplace spatial bounds and 1D Laplace temporal jitter distributions across 50 iterations.
   - Verified anti-composition rule: sequence 0 and sequence 1 have strictly identical `dp_geom` coordinates and identical time offset $\Delta t$.
   - Verified cryptographic hash chain linking (`entry[k].prev_hash == entry[k-1].entry_hash`).
   - Verified tamper detection: mutating `lifecycle_status` in checkpoint 1 triggers failure in `verify_incident_ledger_chain` with `"Tamper detected at seq 1"`.
   - Verified multilingual assistance responses for English, Hindi, and Kannada.

2. **Live Supabase Integration (`tests/test_live_supabase_phase11_transparency.py`):**
   - Seeded real organization, zone, ward, department, and incident on live Supabase (`isqepbxkzxfpvfdkcntw`).
   - Published Checkpoint 0 (`reported`) and Checkpoint 1 (`assigned`) via domain services.
   - Confirmed anti-composition invariance: identical `dp_geom` coordinates across sequence 0 and sequence 1.
   - Confirmed cryptographic chain validity against live database records.
   - Confirmed live tamper detection: modifying a field causes verification failure.
   - Proved public anonymous `SELECT` succeeds on both `jan_sunwai_ledger_entry` and `nagar_pragati_city_snapshot`.
   - Proved anonymous `INSERT` is rejected by database table grants (`APIError`).
   - Clean teardown of seeded data in `finally` block.

3. **Static Quality Gates & Full Test Suite:**
   - 95 tests passing across entire project test suite.
   - `ruff check .` clean with 0 errors.
   - `ruff format --check .` clean (129 files formatted).
   - `mypy civicbrain` clean with 0 errors across 67 source files.
