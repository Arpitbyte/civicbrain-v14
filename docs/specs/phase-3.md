# Phase 3: Multi-Issue Photo Splitting Pipeline, Living Taxonomy Governance & Computer Vision — Technical Specification

**Version:** CivicBrain v14.3.0  
**Phase:** 3  
**Status:** APPROVED & IMPLEMENTED  

---

## 1. Executive Summary & Scope

Phase 3 establishes the visual and categorical ingestion pipeline for CivicBrain v14:
1. **Multi-Issue Single Report Photo-Splitting Pipeline (§A6, §A7):** Ingesting citizen photos, handling multiple concurrent civic issues in a single submission, and splitting them into atomic child `Observation` records routed to distinct municipal departments.
2. **Living Taxonomy Governance (§A11, Standing Invariant 1):** Database schema, API endpoints, and validation for proposing, reviewing, and approving civic issue categories. In accordance with Standing Invariant 1, approving any category requires a structured 1–5 severity rubric (defaulting to a Bühlmann-blended baseline), strictly decoupled from static AHP criterion weights.
3. **Computer Vision Detector Interface & Honest Cold-Start Triage (Hard Rule 1):** Establishing the `VisionDetector` protocol. On resource-constrained environments (Render free tier with 512MB RAM ceiling) where full GPU-based neural models cannot run, arbitrary photos are **never** assigned fabricated bounding boxes or hallucinated confidence scores. Instead, the detector honestly marks unmodeled photos as `UNCLASSIFIED / needs_manual_triage` (or binds to citizen-selected categories), queuing them for dispatcher review on the Command Deck, while full YOLO-World-v2 detection is architected as an asynchronous worker backend.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **No Fabrication of Model Confidence or Bounding Boxes (Hard Rule 1 & Hard Rule 2):**
   - An image cannot be assigned an arbitrary confidence score (e.g. `0.88`) or fictitious bounding box coordinates without a real model executing inference.
   - When no computer vision model is active or when an arbitrary image is submitted in cold-start mode, the detector outputs:
     `category_code = "UNCLASSIFIED"`, `confidence = None`, `bbox = None`, `needs_manual_triage = True`.
   - Pre-annotated bounding boxes and category matches are restricted strictly to deterministic test fixtures (e.g. `test_multi_defect_pothole_garbage.jpg`) for pipeline verification, visibly labeled and isolated from production data.
2. **Living Taxonomy Governance Decoupled from AHP (Standing Invariant 1):**
   - Approving a category requires defining its severity rubric across all 5 levels (`level 1` through `level 5`), specifying concrete physical criteria and baseline scores.
   - A category cannot be approved with a blank rubric.
   - Baseline scores default to a city-wide average blended via Bühlmann credibility ($Z = \frac{n}{n+K}$) as verified inspection data accumulates.
   - Category approval **never** triggers re-computation of static AHP criteria weights (§A12).
3. **Multi-Issue Single Report State Aggregation (§A7, Standing Invariant 3):**
   - When an image or citizen report contains multiple observations routed to different departments (e.g. `ROADS` and `SWM`), parent `intake_report.status` is strictly the **least-advanced status** among all child observations/incidents.
   - Individual observation statuses remain independently visible to citizens.
4. **Mandatory Explicit Scoped Grants (Standing Invariant 4):**
   - Every table created in Phase 3 gets explicit, per-role `GRANT` statements in the migration with zero blanket `GRANT ALL`.

---

## 3. Database Schema (`migrations/0004_phase3_vision_taxonomy.sql`)

### 3.1 Taxonomy Category Table (`taxonomy_category`)
```sql
DO $$ BEGIN
    CREATE TYPE category_status_enum AS ENUM ('proposed', 'approved', 'deprecated');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE public.taxonomy_category (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    department_id UUID NOT NULL REFERENCES public.department(id) ON DELETE RESTRICT,
    code VARCHAR(64) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    severity_rubric JSONB NOT NULL,
    status category_status_enum NOT NULL DEFAULT 'proposed',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_taxonomy_org_code UNIQUE (organization_id, code)
);

CREATE INDEX idx_taxonomy_category_org_dept 
    ON public.taxonomy_category (organization_id, department_id);
CREATE INDEX idx_taxonomy_category_status 
    ON public.taxonomy_category (organization_id, status) 
    WHERE is_active = true;
```

### 3.2 Observation Table Alterations
Extend `observation` with computer vision metadata and provenance:
```sql
ALTER TABLE public.observation
    ADD COLUMN IF NOT EXISTS image_url TEXT,
    ADD COLUMN IF NOT EXISTS bbox JSONB,           -- {"x": float, "y": float, "w": float, "h": float} in [0, 1]
    ADD COLUMN IF NOT EXISTS detection_source TEXT NOT NULL DEFAULT 'citizen_declared', -- 'model_yolo_world', 'citizen_declared', 'dispatcher_manual', 'test_fixture'
    ADD COLUMN IF NOT EXISTS needs_manual_triage BOOLEAN NOT NULL DEFAULT false;

-- Allow confidence to be NULL when no model ran (avoiding fabricated numbers)
ALTER TABLE public.observation
    ALTER COLUMN confidence DROP NOT NULL;
```

### 3.3 Explicit Per-Role Scoped Grants
```sql
-- Scoped grants on taxonomy_category
GRANT SELECT ON public.taxonomy_category TO anon;
GRANT SELECT, INSERT ON public.taxonomy_category TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.taxonomy_category TO service_role;
```

### 3.4 Row-Level Security Policies
- **`anon`:** Can `SELECT` active categories where `status = 'approved'`.
- **`authenticated` (Staff/Citizen):** Can `SELECT` approved categories. Authenticated staff can `INSERT` new categories in `'proposed'` status.
- **Admin Only:** Only admins (verified via `is_org_admin(organization_id)`) can `UPDATE` category status (e.g. approve or deprecate) or update severity rubrics.

---

## 4. Software Architecture & Implementation Details

### 4.1 Living Taxonomy Governance (`civicbrain/domain/intake/taxonomy.py`)
- **Severity Rubric Schema:**
  ```python
  class RubricLevel(BaseModel):
      level: int = Field(ge=1, le=5)
      criteria: str = Field(min_length=10)
      baseline_score: float = Field(ge=1.0, le=5.0)


  class SeverityRubric(BaseModel):
      levels: list[RubricLevel] = Field(min_length=5, max_length=5)
      buhlmann_k: float = Field(default=10.0, ge=1.0)
  ```
- **Validation:** Approving a category requires all 5 levels to be fully defined. Reject approvals if rubric is missing or incomplete.

### 4.2 Computer Vision Protocol & Detection Pipeline (`civicbrain/domain/intake/vision.py`)
- **Data Contract:**
  ```python
  class DetectedDefect(BaseModel):
      category_code: str
      confidence: float | None = None  # None if no model evaluated
      bbox: dict[str, float] | None = None  # {"x": float, "y": float, "w": float, "h": float}
      severity_hint: int | None = None
      detection_source: (
          str  # "model_yolo_world", "citizen_declared", "dispatcher_manual", "test_fixture"
      )
      needs_manual_triage: bool = False
  ```
- **`VisionDetector` Protocol:**
  ```python
  class VisionDetector(Protocol):
      async def detect(
          self, image_bytes: bytes, filename: str, citizen_categories: list[str] | None = None
      ) -> list[DetectedDefect]: ...
  ```
- **Execution Modes:**
  1. **`HonestColdStartDetector` (Default for Web Process):**
     - When arbitrary images are uploaded:
       - If citizen explicitly selected categories (e.g. `["POTHOLE", "GARBAGE"]`): creates defects mapped to those categories with `detection_source="citizen_declared"`, `confidence=None`, `bbox=None`.
       - If no categories provided: returns a single defect with `category_code="UNCLASSIFIED"`, `confidence=None`, `bbox=None`, `needs_manual_triage=True`.
     - Zero fabricated confidence scores. Zero fabricated bounding box coordinates. Zero RAM overhead.
  2. **`FixtureVisionDetector` (Testing & CI Only):**
     - Matches deterministic filenames (e.g. `multi_issue_road_swm.jpg`) to pre-annotated ground-truth fixtures for testing the multi-department splitting pipeline and UI bounding box rendering.
  3. **`YOLOWorldDetector` (Worker Architecture Specification):**
     - Decoupled Celery task specification running zero-shot open-vocabulary prompts on dedicated worker instances with GPU/adequate RAM, updating observations asynchronously.

### 4.3 Photo Intake & Multi-Department Splitting (`civicbrain/domain/intake/services.py`)
- Ingestion flow for `POST /v1/intake/reports/photo`:
  1. Receives image upload + coordinates (`lat`, `lon`) + optional citizen category tags + channel.
  2. Resolves containing `ward_id` via PostGIS `ST_Contains`.
  3. Invokes detector $\to$ receives list of `DetectedDefect` items.
  4. Creates parent `intake_report`.
  5. For each detected defect:
     - Resolves the responsible `department_id` via `taxonomy_category`. If `UNCLASSIFIED`, routes to default General Administration / Triage queue.
     - Creates child `observation` with bounding box, image reference, confidence, and detection source.
     - Evaluates deduplication against existing incidents in the ward for that department via Fellegi-Sunter (`dedup.py`).
     - Links to matched incident or provisions new operational `incident`.
  6. Computes parent `intake_report.status` from all child observations using the least-advanced child status invariant.
  7. Returns aggregated response containing the parent report, tracking token, and array of child observations.

### 4.4 API Endpoints
- **Taxonomy:**
  - `GET /v1/taxonomy/categories?organization_id=...`: Publicly lists approved categories.
  - `POST /v1/taxonomy/categories`: Staff/Admin proposes new category.
  - `PATCH /v1/taxonomy/categories/{category_id}/approve`: Admin approves category with validated 5-level severity rubric.
- **Intake:**
  - `POST /v1/intake/reports/photo`: Multi-part image intake with GPS, channel, and category hints.

---

## 5. Verification Plan

### 5.1 Automated Unit Tests
- `tests/test_taxonomy_governance.py`:
  - Verify category proposal creation (`status = proposed`).
  - Verify admin approval rejects empty or incomplete severity rubrics.
  - Verify admin approval succeeds with complete 5-level rubric and sets `status = approved`.
- `tests/test_vision_splitting.py`:
  - Verify that an arbitrary photo with no citizen categories produces an `UNCLASSIFIED` observation with `confidence = None` and `needs_manual_triage = True` (zero fabrication).
  - Verify that a photo with multiple citizen-selected categories splits into distinct observations routed to different departments (e.g. `ROADS` and `SWM`).
  - Verify test fixture multi-defect detection correctly populates bounding boxes and routes to distinct departments.
  - Verify that parent report status reflects the least-advanced child status across the split.

### 5.2 Live Supabase Integration & RLS Tests
- `tests/test_live_supabase_phase3_rls.py`:
  - Seed organization, departments, and categories via `service_role`.
  - Verify anonymous client can `SELECT` approved categories, but cannot see proposed/deprecated categories.
  - Verify non-admin authenticated users cannot execute `UPDATE` to approve a category.
  - Verify admin user can approve category with rubric.
  - Full cleanup of all seeded rows in `finally` block.

### 5.3 CI & Quality Gates
- `python -m ruff check civicbrain tests`
- `python -m ruff format --check civicbrain tests`
- `python -m mypy civicbrain`
- `python -m pytest`
- GitHub Actions CI matrix verification across Python 3.11 and 3.12.
