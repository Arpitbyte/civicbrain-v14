-- =========================================================================
-- CivicBrain v14 — Phase 3: Vision Ingestion, Living Taxonomy & Photo Splitting
-- Migration 0004: Taxonomy Categories, Rubric Governance & Observation Extensions
-- =========================================================================

-- 1. Create Category Status Enum
DO $$ BEGIN
    CREATE TYPE category_status_enum AS ENUM (
        'proposed',
        'approved',
        'deprecated'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Taxonomy Category Table (§A11, Standing Invariant 1)
CREATE TABLE IF NOT EXISTS public.taxonomy_category (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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

CREATE INDEX IF NOT EXISTS idx_taxonomy_category_org_dept 
    ON public.taxonomy_category (organization_id, department_id);

CREATE INDEX IF NOT EXISTS idx_taxonomy_category_status 
    ON public.taxonomy_category (organization_id, status) 
    WHERE is_active = true;

-- 3. Extend Observation Table with Computer Vision Metadata & Provenance
ALTER TABLE public.observation
    ADD COLUMN IF NOT EXISTS image_url TEXT,
    ADD COLUMN IF NOT EXISTS bbox JSONB,
    ADD COLUMN IF NOT EXISTS detection_source TEXT NOT NULL DEFAULT 'citizen_declared',
    ADD COLUMN IF NOT EXISTS needs_manual_triage BOOLEAN NOT NULL DEFAULT false;

-- Allow confidence to be NULL when no model ran (avoiding fabricated numbers, Hard Rule 1)
ALTER TABLE public.observation
    ALTER COLUMN confidence DROP NOT NULL;

-- 4. Scoped Grants (Standing Invariant 4: Scoped table grants, zero blanket GRANT ALL)
REVOKE ALL ON TABLE public.taxonomy_category FROM PUBLIC;
GRANT SELECT ON public.taxonomy_category TO anon;
GRANT SELECT, INSERT, UPDATE ON public.taxonomy_category TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.taxonomy_category TO service_role;

-- 5. Enable Row-Level Security
ALTER TABLE public.taxonomy_category ENABLE ROW LEVEL SECURITY;

-- 5.1 Service Role Policy
DROP POLICY IF EXISTS "service_role_taxonomy_category_all" ON public.taxonomy_category;
CREATE POLICY "service_role_taxonomy_category_all" ON public.taxonomy_category
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- 5.2 Public Read on Approved Categories
DROP POLICY IF EXISTS "taxonomy_category_read_public" ON public.taxonomy_category;
CREATE POLICY "taxonomy_category_read_public" ON public.taxonomy_category
    FOR SELECT TO anon
    USING (status = 'approved' AND is_active = true);

-- 5.3 Authenticated Read (Approved and proposed categories visible to authenticated; deprecated visible to org admins)
DROP POLICY IF EXISTS "taxonomy_category_read_authenticated" ON public.taxonomy_category;
CREATE POLICY "taxonomy_category_read_authenticated" ON public.taxonomy_category
    FOR SELECT TO authenticated
    USING (
        (status IN ('approved', 'proposed') AND is_active = true)
        OR is_org_admin(organization_id)
    );

-- 5.4 Authenticated Staff Insertion (Phase 3 Correction 2: Strict WITH CHECK status = 'proposed')
-- Non-admin cannot insert a pre-approved category regardless of what the request sends.
DROP POLICY IF EXISTS "taxonomy_category_insert_staff" ON public.taxonomy_category;
CREATE POLICY "taxonomy_category_insert_staff" ON public.taxonomy_category
    FOR INSERT TO authenticated
    WITH CHECK (status = 'proposed');

-- 5.5 Admin Update Policy (Only org admins can update, e.g. approve or update rubric)
DROP POLICY IF EXISTS "taxonomy_category_update_admin" ON public.taxonomy_category;
CREATE POLICY "taxonomy_category_update_admin" ON public.taxonomy_category
    FOR UPDATE TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));
