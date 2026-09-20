# Phase 5: NLP Pipeline, Multilingual Ingestion & Emotion-Severity Decoupling — Implementation Log

**Date:** 2026-09-20  
**Status:** COMPLETED  
**Version:** CivicBrain v14.5.0  

---

## 1. Incident Table RLS Audit & Access-Control Regression Fix

- **pg_policies Audit:**
  - Audited live Supabase `incident` policies. Confirmed that earlier `staff_read_incidents` policy combined via PostgreSQL OR-logic with other policies, which would allow any staff member within an organization to read all incidents across all departments.
- **Access-Control Regression Fixed:**
  - Completely dropped `staff_read_incidents`.
  - Enacted granular, role-scoped SELECT policies in `migrations/0005_phase4_gis_core.sql`:
    1. `dept_staff_select_incidents`: Strictly scoped to `ura.department_id = incident.department_id`.
    2. `zonal_supervisor_select_incidents`: Scoped to wards within supervised zones (`ura.zone_id = ward.zone_id`).
    3. `corporator_select_incidents`: Scoped to representative's ward (`ura.ward_id = incident.ward_id`).
    4. `field_worker_select_incidents`: Scoped to assigned incidents (`assigned_worker_id = auth.uid()`) or same department.
    5. `dispatcher_select_incidents`: Scoped to emergency triage across organization.
  - Verified via live test [`tests/test_live_supabase_phase4_gis.py`](file:///e:/CivicBrain/tests/test_live_supabase_phase4_gis.py): Roads department staff user with real JWT reads Roads incident, but receives 0 rows when selecting Sanitation incident.

---

## 2. What Was Built in Phase 5

- **Emotion-Severity Decoupling Principle (§A11):**
  - Architecture strictly decouples citizen emotional intensity from physical defect engineering severity.
  - Punctuation density (`!`, `?`), capitalization ratios, and distress keywords evaluate exclusively to `citizen_urgency_score` ($U \in [0.0, 1.0]$).
  - Physical severity hint ($S \in \{1, 2, 3, 4, 5\}$) is derived purely from physical dimension and hazard keywords (e.g. "deep", "crater", "burst main", "flooding"), remaining completely unaffected by citizen anger or all-caps shouting.
- **Multilingual Ingestion & Script Detection (§A11):**
  - Implemented `DeterministicIndicRuleProcessor` in [`civicbrain/domain/nlp/processor.py`](file:///e:/CivicBrain/civicbrain/domain/nlp/processor.py) supporting Unicode script detection (Devanagari, Kannada, Tamil, Telugu, Latin) and Romanized colloquial Indian dialects (Hinglish/Kanglish).
  - Normalizes civic terms across Indian languages (e.g. `khadda`/`gundi`/`kuzhi` $\to$ `POTHOLE`, `kachra`/`kasa`/`kuppa` $\to$ `GARBAGE`, `nala`/`kaluve` $\to$ `DRAINAGE`).
- **Bootstrap Principle & Cold-Start Honesty (Hard Rule 1, §A3):**
  - Lightweight CPU-only rule engine operating under 512MB RAM ceiling (zero heavy PyTorch weights in production).
  - Ambiguous or non-civic input returns `suggested_category = None`, `physical_severity_hint = None`, and `requires_human_triage = True`.
- **Database Migration (`migrations/0006_phase5_nlp_pipeline.sql`):**
  - Extended `intake_report` with `detected_language`, `detected_script`, and `citizen_urgency_score`.
  - Added check constraint `chk_citizen_urgency_range` enforcing `0.0 <= citizen_urgency_score <= 1.0`.
  - Extended `observation` with `extracted_keywords TEXT[]` and `text_severity_hint SMALLINT`.
  - Added check constraint `chk_text_severity_range` enforcing `text_severity_hint BETWEEN 1 AND 5`.
  - Applied cleanly to live Supabase instance (`isqepbxkzxfpvfdkcntw`).
- **REST Endpoints (`civicbrain/api/v1/nlp.py`):**
  - `POST /v1/nlp/analyze`: Authenticated-only operational endpoint (`claims: CurrentUserClaims = Depends(get_current_user_claims)`) for staff, dispatchers, and triage operators. Public grievances flow through `/v1/intake/reports`.

---

## 3. Verification & Live Test Evidence

- [x] **Live Supabase Schema & Constraints:** Migration 0006 applied cleanly. `tests/test_live_supabase_phase5_nlp.py` confirms `chk_citizen_urgency_range` rejects $>1.0$ and `chk_text_severity_range` rejects $>5$.
- [x] **Decoupling Unit Tests:** `tests/test_nlp_pipeline.py` confirms calm and angry reports of the same physical defect yield identical physical severity ($S=4$) while reflecting distinct urgency scores ($0.08$ vs $0.78$).
- [x] **Multilingual Processing:** Confirmed script and category extraction for Hindi, Kannada, Tamil, and Hinglish phrases.
- [x] **Department Isolation Live Test:** Confirmed Roads staff cannot read Sanitation incident via real Supabase JWT.
- [x] **Full Test Suite:** 50 passed in 74.89s across all project phases with zero regressions.
