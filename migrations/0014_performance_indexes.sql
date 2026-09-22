-- CivicBrain v14 — Performance Optimization Pass
-- Migration 0014: Foreign Key and Query Path Indexing
-- Eliminates sequential scans on joins and filters identified in database audit

-- 1. Identity & RBAC Foreign Keys
CREATE INDEX IF NOT EXISTS idx_user_role_dept_id ON public.user_role_assignment (department_id);
CREATE INDEX IF NOT EXISTS idx_user_role_ward_id ON public.user_role_assignment (ward_id);
CREATE INDEX IF NOT EXISTS idx_user_role_zone_id ON public.user_role_assignment (zone_id);

-- 2. Incident Worker Assignment
CREATE INDEX IF NOT EXISTS idx_incident_worker_id ON public.incident (assigned_worker_id);

-- 3. Taxonomy Department Foreign Key
CREATE INDEX IF NOT EXISTS idx_taxonomy_category_dept_id ON public.taxonomy_category (department_id);

-- 4. Analytics & Equity Models Foreign Keys
CREATE INDEX IF NOT EXISTS idx_ward_equity_ward_id ON public.ward_equity_credibility (ward_id);
CREATE INDEX IF NOT EXISTS idx_ward_res_stat_org_id ON public.ward_resolution_stat (organization_id);

-- 5. Causal Graph Established By Foreign Key
CREATE INDEX IF NOT EXISTS idx_causal_established_by ON public.incident_causal_link (established_by);

-- 6. Dispatch & Work Orders Foreign Keys and Composite Filtering
CREATE INDEX IF NOT EXISTS idx_work_order_dept_id ON public.work_order (department_id);
CREATE INDEX IF NOT EXISTS idx_work_order_worker_status ON public.work_order (assigned_worker_id, status);

-- 7. Offline Sync Mutation Log Organization
CREATE INDEX IF NOT EXISTS idx_sync_log_org_id ON public.sync_mutation_log (organization_id);

-- 8. Dispatch Conflict Review Foreign Keys & Worker Lookup
CREATE INDEX IF NOT EXISTS idx_conflict_review_incident_id ON public.dispatch_conflict_review (incident_id);
CREATE INDEX IF NOT EXISTS idx_conflict_review_reviewed_by ON public.dispatch_conflict_review (reviewed_by);
CREATE INDEX IF NOT EXISTS idx_conflict_review_worker_id ON public.dispatch_conflict_review (worker_id);

-- 9. Jan Sunwai Transparency Ledger Filter Columns
CREATE INDEX IF NOT EXISTS idx_js_ledger_dept_id ON public.jan_sunwai_ledger_entry (department_id);
CREATE INDEX IF NOT EXISTS idx_js_ledger_cat_code ON public.jan_sunwai_ledger_entry (category_code);
