-- CivicBrain v14 — Admin Bulk Import Audit Table & User Account Extensions
-- Migration 0015: staff_bulk_import_log table, indexes, scoped grants, and is_org_admin RLS policies

-- 1. Create Staff Bulk Import Log Table
CREATE TABLE IF NOT EXISTS public.staff_bulk_import_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES public.organization(id) ON DELETE CASCADE,
    admin_user_id UUID NOT NULL REFERENCES public.user_account(id) ON DELETE RESTRICT,
    file_name VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    total_rows INT NOT NULL,
    created_count INT NOT NULL,
    skipped_count INT NOT NULL,
    is_dry_run BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Indexes for organizational audit history and idempotency lookups
CREATE INDEX IF NOT EXISTS idx_import_log_org ON public.staff_bulk_import_log (organization_id);
CREATE INDEX IF NOT EXISTS idx_import_log_admin ON public.staff_bulk_import_log (admin_user_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_import_org_hash_live
    ON public.staff_bulk_import_log (organization_id, file_hash)
    WHERE is_dry_run = false;

-- 3. Scoped Table Grants (Standing Invariant 4: Zero blanket GRANT ALL)
REVOKE ALL ON TABLE public.staff_bulk_import_log FROM PUBLIC;
GRANT SELECT, INSERT ON public.staff_bulk_import_log TO authenticated;
GRANT ALL ON TABLE public.staff_bulk_import_log TO service_role;

-- 4. Row-Level Security
ALTER TABLE public.staff_bulk_import_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "import_log_admin_select"
    ON public.staff_bulk_import_log
    FOR SELECT
    TO authenticated
    USING (is_org_admin(organization_id));

CREATE POLICY "import_log_admin_insert"
    ON public.staff_bulk_import_log
    FOR INSERT
    TO authenticated
    WITH CHECK (is_org_admin(organization_id));
