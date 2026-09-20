# Phase 5: NLP Pipeline & Multilingual Ingestion — Technical Specification

**Version:** CivicBrain v14.5.0  
**Phase:** 5  
**Status:** SPECIFICATION PENDING APPROVAL  

---

## 1. Executive Summary & Scope

Phase 5 establishes the Natural Language Processing (NLP) Pipeline for multilingual citizen grievance ingestion across Indian Urban Local Bodies (§A11):
1. **Multilingual Ingestion & Transliteration (§A11):**
   - Ingestion of citizen descriptions across major Indian languages and scripts (Devanagari, Kannada, Tamil, Telugu, Romanized Hinglish/Kanglish).
   - Transliteration normalization protocol for Romanized Indian scripts (e.g. `khadda` $\to$ pothole, `kachra` $\to$ garbage, `kasa` $\to$ solid waste).
2. **Emotion-Severity Decoupling Principle (§A11, Architectural Invariant):**
   - **Strict Decoupling:** Citizen emotional intensity, frustration, ALL-CAPS urgency, or angry sentiment must NEVER inflate the physical engineering severity score ($S \in \{1, 2, 3, 4, 5\}$).
   - Physical severity is strictly anchored to the approved 5-tier taxonomy rubric (`severity_rubric` from Phase 3).
   - Citizen sentiment/urgency is isolated into a separate metric: `citizen_urgency_score` ($U \in [0.0, 1.0]$) used solely for communication prioritization and dispatch notifications, never altering physical hazard triage.
3. **Hardware-Grounding & Honest Cold-Start Handling (Hard Rule 1):**
   - In adherence to Render free-tier RAM limits (512MB ceiling, zero GPU), heavy PyTorch/Transformer model weights (e.g. 500MB+ IndicBERT weights) are not loaded into memory in production.
   - Defines an abstract protocol `NLPProcessor` with an honest, lightweight cold-start heuristic implementation: `DeterministicIndicRuleProcessor`.
   - Uses localized lexicon matching, script detection, keyword extraction, and heuristic emotion markers without fabricating ML confidence scores or causing OOM container crashes.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Emotion-Severity Decoupling (Invariant Rule):**
   - Emotional markers (e.g. "SHAME ON BBMP!! THIS IS RIDICULOUS!! DANGEROUS EMERGENCY!!") evaluate to a high `citizen_urgency_score`, but physical severity ($S$) remains strictly derived from verifiable defect dimensions and hazards per the taxonomy rubric.
2. **Deterministic Cold-Start Transparency (Bootstrap Principle, §A3):**
   - Unrecognized colloquial phrases return `category_code = None` with `requires_human_triage = True` rather than hallucinating categories.
3. **Zero External Paid API Dependencies (Hard Rule 1):**
   - All text normalization, script detection, and category keyword extraction run locally on standard Python libraries with zero OpenAI/Google Gemini API billing calls.
4. **Mandatory Explicit Scoped Grants (Standing Invariant 4):**
   - All database columns and RPC procedures created in Phase 5 maintain explicit per-role grants with zero blanket `GRANT ALL`.

---

## 3. Database Migration & Schema Design (`migrations/0006_phase5_nlp_pipeline.sql`)

### 3.1 Extending Intake Report and Observation for NLP Metadata
```sql
-- Migration 0006: NLP Pipeline & Multilingual Metadata

-- 1. Extend intake_report with linguistic and sentiment metadata
ALTER TABLE public.intake_report
    ADD COLUMN IF NOT EXISTS detected_language VARCHAR(20) DEFAULT 'en',
    ADD COLUMN IF NOT EXISTS detected_script VARCHAR(20) DEFAULT 'Latin',
    ADD COLUMN IF NOT EXISTS citizen_urgency_score DOUBLE PRECISION DEFAULT 0.0;

-- 2. Extend observation with extracted keywords and decoupled emotion metrics
ALTER TABLE public.observation
    ADD COLUMN IF NOT EXISTS extracted_keywords TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS text_severity_hint SMALLINT DEFAULT NULL;

-- 3. Validation Check: Urgency score must strictly lie between 0.0 and 1.0
ALTER TABLE public.intake_report
    DROP CONSTRAINT IF EXISTS chk_citizen_urgency_range;
ALTER TABLE public.intake_report
    ADD CONSTRAINT chk_citizen_urgency_range
    CHECK (citizen_urgency_score >= 0.0 AND citizen_urgency_score <= 1.0);
```

---

## 4. Domain & Processor Architecture

### 4.1 Protocol Definition (`civicbrain/domain/nlp/processor.py`)
```python
class TextAnalysisResult(BaseModel):
    detected_language: str
    detected_script: str
    normalized_text: str
    suggested_category: str | None
    physical_severity_hint: int | None  # 1 to 5, or None if undetermined
    citizen_urgency_score: float        # 0.0 to 1.0 (decoupled from physical severity)
    extracted_keywords: list[str]
    requires_human_triage: bool

class NLPProcessor(Protocol):
    def process_text(self, text: str, citizen_category: str | None = None) -> TextAnalysisResult:
        ...
```

### 4.2 Decoupled Scoring Rules
- **Physical Severity Hint ($S \in \{1, \dots, 5\}$):**
  - Derived strictly from verifiable physical dimension descriptors (e.g. "deep crater", "broken main", "submerged road" $\to S \ge 4$; "minor crack", "small dip", "dim light" $\to S \le 2$).
- **Citizen Urgency Score ($U \in [0.0, 1.0]$):**
  - Computed from punctuation density (exclamations, multiple question marks), capitalization ratio, and emotional distress markers ("danger", "accident", "hospital", "urgent", "shame").

---

## 5. REST API Endpoints (`civicbrain/api/v1/nlp.py`)

1. **`POST /v1/nlp/analyze`:**
   - Request Body: `{ "text": str, "citizen_category": str | None }`
   - Response: `TextAnalysisResult`
   - Performs script identification, transliteration normalization, category keyword matching, physical severity hint inference, and decoupled citizen urgency scoring.

---

## 6. Verification Plan

1. **Unit Tests (`tests/test_nlp_pipeline.py`):**
   - Emotion-Severity Decoupling: Assert that identical physical descriptions with and without aggressive emotional language receive identical `physical_severity_hint` values while exhibiting distinct `citizen_urgency_score` values.
   - Multilingual & Romanized Ingestion: Assert accurate category extraction across Hindi, Kannada, Tamil, and Hinglish phrases.
   - Cold-Start Honesty: Assert that ambiguous descriptions trigger `requires_human_triage = True` with `suggested_category = None`.
2. **Live Supabase Schema & Constraint Verification (`tests/test_live_supabase_phase5_nlp.py`):**
   - Assert `chk_citizen_urgency_range` check constraint rejects invalid urgency scores ($<0.0$ or $>1.0$).
   - Assert persistence of linguistic metadata across `intake_report` and `observation`.
   - Teardown of all seeded entities in `finally` block.
3. **CI & Quality Gates:**
   - `ruff check`, `ruff format --check`, `mypy civicbrain`, and full `pytest` suite green.
