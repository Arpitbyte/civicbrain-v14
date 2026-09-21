# Phase 9: Field Companion — Karmi Sahayak Offline Sync & Conflict Adjudication — Implementation Log

**Date:** 2026-09-21  
**Status:** COMPLETED  
**Version:** CivicBrain v14.9.0  

---

## 1. What Was Built

- **Karmi Sahayak Offline Sync Engine (§A15):**
  - Added monotonic revision counter `version INT NOT NULL DEFAULT 1` to `work_order` for optimistic concurrency.
  - Implemented append-only `sync_mutation_log` table tracking client mutations (`start`, `resolve`), idempotency vectors (`uq_worker_mutation_id`), and arbitration statuses (`applied`, `conflict`, `rejected`).
  - Strict append-only RLS and scoped grants: `authenticated` gets `SELECT, INSERT` only; `UPDATE` and `DELETE` are blocked.

- **Supervisor Conflict Adjudication Queue (§A15, Correction 1 & 2):**
  - Implemented `dispatch_conflict_review` table preserving full worker evidence (`submitted_media_urls`, `submitted_notes`, `submitted_geom`, `captured_at`) when offline resolution races against dispatcher cancellation or reassignment.
  - Surfaced conflicts to Control Room and Command Deck supervisors via:
    - `GET /v1/dispatch/conflicts`: Filterable queue of reviewable concurrent dispatch conflicts.
    - `POST /v1/dispatch/conflicts/{conflict_id}/adjudicate`: Supervisor adjudication endpoint allowing either:
      - `accept_worker_evidence`: Completes work order, resolves incident with 72h auto-confirm deadline, recomputes intake report.
      - `uphold_dispatcher_action`: Dismisses conflict review while upholding dispatcher cancellation/reassignment.

- **Deterministic Conflict Arbitration Matrix:**
  - Case 1 (Idempotent Retry): Cached outcome returned without duplicate DB writes.
  - Case 2 (Clean Progression): Version incremented, state transitioned to `in_progress` or `completed`.
  - Case 3 & 4 (Dispatcher Race with Valid Evidence): Evidence preserved in full in `dispatch_conflict_review` queue.
  - Case 5 (Peer Race): Already completed work orders return `conflict_already_completed` without supervisor queue.
  - Cases 6 & 7 (Proximity & Evidence Gates): Submissions $> 50$m or with empty evidence rejected with `resolution_out_of_bounds` or `missing_evidence`.

---

## 2. Verification & Test Evidence

1. **Unit Test Suite (`tests/test_offline_sync.py`):**
   - Idempotency deduplication verified.
   - Missing evidence and out-of-bounds GPS rejected with diagnostic codes.
   - Dispatcher cancellation with valid evidence preserves evidence in `dispatch_conflict_review` (`status = 'pending'`).
   - Peer race rejected with `conflict_already_completed`.
   - Supervisor adjudication `accept_worker_evidence` and `uphold_dispatcher_action` verified.

2. **Live Supabase Integration (`tests/test_live_supabase_phase9_sync.py`):**
   - Seeded real organization, ward, department, real auth users (field worker & supervisor), incident, and work order on live Supabase (`isqepbxkzxfpvfdkcntw`).
   - Proved append-only unique constraint `uq_worker_mutation_id` prevents duplicate client mutation insertion.
   - Proved cancelled work order race preserves evidence in `dispatch_conflict_review`.
   - Proved supervisor adjudication flow (`accept_worker_evidence`) updates work order to `completed` and incident to `resolved`.
   - Clean teardown of both database records and auth users in `finally` block.

3. **Static Quality Gates & Full Suite:**
   - 83 tests passing across full test suite.
   - `ruff check` and `ruff format --check` clean with 0 errors.
   - `mypy civicbrain` clean with 0 errors across 57 source files.
