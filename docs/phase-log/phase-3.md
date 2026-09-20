# Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting — Implementation Log

**Date:** 2026-09-20  
**Status:** COMPLETED  
**Version:** CivicBrain v14.3.0  

---

## 1. What Was Built

- **Living Taxonomy Governance (§A11, Standing Invariant 1):**
  - Implemented `taxonomy_category` table and domain model (`civicbrain/domain/intake/taxonomy.py`) with strict `severity_rubric JSONB NOT NULL` containing 5-level structured criteria (`RubricLevel` tiers 1 through 5, criteria length $\ge 10$, baseline score in $[1.0, 5.0]$, and Bühlmann credibility factor defaulting to 10.0).
  - Standing Invariant 1 adherence: Category approval is strictly decoupled from static AHP criteria weights; approving a category verifies its 5-level rubric without triggering AHP re-estimation.
  - Lifecycle state machine governed via `category_status_enum`: `'proposed'`, `'approved'`, `'deprecated'`.
- **User Correction 2 Baked in Code:**
  - Row-Level Security policy on `taxonomy_category` enforces `WITH CHECK (status = 'proposed')` for the `authenticated` role (`taxonomy_category_insert_staff`).
  - Confirmed: Non-admin users cannot insert pre-approved categories regardless of request payload (attempting to insert `status = 'approved'` raises PostgreSQL RLS violation code `42501`). Only the admin-gated `UPDATE` path (`taxonomy_category_update_admin` checking `is_org_admin(organization_id)`) can transition status to `'approved'`.
- **Computer Vision Protocol & Honest Cold-Start Triage (Hard Rule 1):**
  - Protocol `VisionDetector` defined in `civicbrain/domain/intake/vision.py` specifying `detect(image_bytes, filename, citizen_categories) -> list[DetectedDefect]`.
  - Implemented `HonestColdStartDetector`: Under zero-GPU and 512MB RAM ceiling constraints (Render free tier), arbitrary photos are never assigned fabricated confidence scores or synthetic bounding boxes.
  - When no citizen categories are provided: Returns `category_code = "UNCLASSIFIED"`, `confidence = None`, `bbox = None`, `needs_manual_triage = True`, queueing the item for manual triage without automated incident creation.
  - **User Correction 1 Baked in Code:** When citizens declare issue categories, `confidence = None` (strictly `None`, never `1.0`; the `"or 1.0"` branch has been dropped entirely from `vision.py`).
- **Fixture Detector for Deterministic Testing:**
  - Implemented `FixtureVisionDetector` matching test assets (e.g. `multi_issue_road_swm.jpg`) to deterministic bounding boxes and category codes (`POTHOLE` with confidence `0.92` and `GARBAGE` with confidence `0.88`) solely for automated CI and pipeline validation.
- **Multi-Issue Photo Splitting Pipeline (`process_photo_intake`):**
  - Implemented in `civicbrain/domain/intake/services.py`:
    1. Validates organization and performs spatial containment via PostGIS `ST_Contains` against ward polygons.
    2. Runs `VisionDetector` protocol.
    3. Provisions parent `intake_report` with 256-bit entropy tracking token.
    4. Splits detected defects into atomic `Observation` records.
    5. Resolves departmental routing via approved `TaxonomyCategory` records (e.g. `POTHOLE` $\to$ ROADS, `GARBAGE` $\to$ SWM).
    6. Runs Fellegi-Sunter record linkage against active open incidents in the ward.
    7. Computes parent report status using the least-advanced child status invariant (§A7, Standing Invariant 3).
- **Database Migration (`migrations/0004_phase3_vision_taxonomy.sql`):**
  - Applied cleanly to live Supabase (`isqepbxkzxfpvfdkcntw`).
  - Created `taxonomy_category` table with `uq_taxonomy_org_code` unique constraint and performance indexes.
  - Extended `observation` table with `image_url`, `bbox JSONB`, `detection_source`, `needs_manual_triage`, and made `confidence` nullable (`DROP NOT NULL`).
  - Enforced Standing Invariant 4 scoped grants:
    - `anon`: `SELECT` on `taxonomy_category`.
    - `authenticated`: `SELECT`, `INSERT`, `UPDATE` on `taxonomy_category` (governed by RLS).
    - `service_role`: Full CRUD (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
    - Explicit `REVOKE ALL ON TABLE public.taxonomy_category FROM PUBLIC`.
- **REST API Endpoints:**
  - `GET /v1/taxonomy/categories`: Lists approved active categories for public/citizens; permits org admins to inspect proposed categories.
  - `POST /v1/taxonomy/categories`: Staff/citizen endpoint proposing categories with `status = 'proposed'`.
  - `PATCH /v1/taxonomy/categories/{category_id}/approve`: Admin-gated endpoint requiring validated 5-level severity rubric.
  - `POST /v1/intake/reports/photo`: Multipart image intake endpoint executing PostGIS ward lookup, vision detection, departmental splitting, and status aggregation.

---

## 2. Key Code References for Mandatory Corrections

1. **Correction 1: `citizen_declared` Confidence Strictly `None`:**
   - File: [`civicbrain/domain/intake/vision.py`](file:///e:/CivicBrain/civicbrain/domain/intake/vision.py#L69-L76)
   - Line 70: `confidence=None` (strictly `None`, zero `"or 1.0"` branch in the implementation).
2. **Correction 2: Strict `WITH CHECK (status = 'proposed')` on Authenticated Category Insertion:**
   - File: [`migrations/0004_phase3_vision_taxonomy.sql`](file:///e:/CivicBrain/migrations/0004_phase3_vision_taxonomy.sql#L77-L82)
   - Line 81: `CREATE POLICY "taxonomy_category_insert_staff" ON public.taxonomy_category FOR INSERT TO authenticated WITH CHECK (status = 'proposed');`

---

## 3. Verification & Live Test Evidence

- [x] **Live Supabase Schema Applied:** Migration `0004_phase3_vision_taxonomy.sql` applied cleanly via raw connection on live Supabase (`isqepbxkzxfpvfdkcntw`).
- [x] **Scoped Grants Verified:** Explicit per-role grants applied on `taxonomy_category` with zero blanket `GRANT ALL`.
- [x] **Live Supabase RLS Tests:** `tests/test_live_supabase_phase3_rls.py` executed with real Supabase Auth users and JWTs asserting:
  - Anon can read approved categories.
  - Anon cannot read proposed categories.
  - Authenticated staff cannot insert pre-approved categories (`WITH CHECK (status = 'proposed')` raises 42501).
  - Authenticated staff can insert with `status = 'proposed'`.
  - Authenticated non-admin cannot update category to approved.
  - Authenticated org admin can approve category with rubric.
  - Full teardown in `finally` block.
- [x] **Taxonomy Rubric Governance Tests:** `tests/test_taxonomy_governance.py` passes all 7 validation scenarios (rejection of missing tiers, duplicates, short criteria, out-of-bounds scores).
- [x] **Vision Splitting Tests:** `tests/test_vision_splitting.py` passes all 5 tests (honest cold-start triage, citizen declared confidence=None, fixture multi-issue splitting across ROADS and SWM, parent least-advanced status aggregation).
- [x] **Full Test Suite:** 39 passed in 57.37s across entire repository with zero regressions.
