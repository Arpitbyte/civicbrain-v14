-- CivicBrain v14 — Phase 5: NLP Pipeline & Multilingual Ingestion (§A11)
-- Migration 0006: Linguistic Metadata, Decoupled Urgency Scoring & Check Constraints

-- 1. Extend intake_report with linguistic and sentiment metadata
ALTER TABLE public.intake_report
    ADD COLUMN IF NOT EXISTS detected_language VARCHAR(20) DEFAULT 'en',
    ADD COLUMN IF NOT EXISTS detected_script VARCHAR(20) DEFAULT 'Latin',
    ADD COLUMN IF NOT EXISTS citizen_urgency_score DOUBLE PRECISION DEFAULT 0.0;

-- 2. Extend observation with extracted keywords and decoupled emotion metrics
ALTER TABLE public.observation
    ADD COLUMN IF NOT EXISTS extracted_keywords TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS text_severity_hint SMALLINT DEFAULT NULL;

-- 3. Validation Check Constraints
-- 3.1 Citizen urgency score must strictly lie between 0.0 and 1.0
ALTER TABLE public.intake_report
    DROP CONSTRAINT IF EXISTS chk_citizen_urgency_range;
ALTER TABLE public.intake_report
    ADD CONSTRAINT chk_citizen_urgency_range
    CHECK (citizen_urgency_score >= 0.0 AND citizen_urgency_score <= 1.0);

-- 3.2 Text severity hint (if provided) must strictly lie between 1 and 5
ALTER TABLE public.observation
    DROP CONSTRAINT IF EXISTS chk_text_severity_range;
ALTER TABLE public.observation
    ADD CONSTRAINT chk_text_severity_range
    CHECK (text_severity_hint IS NULL OR (text_severity_hint >= 1 AND text_severity_hint <= 5));
