-- CivicBrain v14 — Phase 12: Hardening, Red-Team Audit & Production Isolation
-- Migration 0013: RLS Policy Hardening & Privilege Alignment

-- 1. Add Authenticated INSERT Policy on dispatch_conflict_review (§A15)
-- Enables field workers to log concurrent-dispatch conflicts when resolving offline work orders
DROP POLICY IF EXISTS conflict_review_insert_policy ON public.dispatch_conflict_review;
CREATE POLICY conflict_review_insert_policy ON public.dispatch_conflict_review
    FOR INSERT TO authenticated
    WITH CHECK (
        worker_id = auth.uid()
        OR is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = dispatch_conflict_review.organization_id
              AND ura.role IN ('admin'::staff_role_enum, 'dispatcher'::staff_role_enum, 'zonal_supervisor'::staff_role_enum)
        )
    );

-- 2. Add Org Admin Management Policy on elected_representative
-- Enables municipal administrators in Control Room to manage corporator assignments
DROP POLICY IF EXISTS admin_manage_elected_reps ON public.elected_representative;
CREATE POLICY admin_manage_elected_reps ON public.elected_representative
    FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

GRANT INSERT, UPDATE, DELETE ON TABLE public.elected_representative TO authenticated;

-- 3. Enforce Strict SELECT-Only on nagar_pragati_city_snapshot for authenticated
REVOKE INSERT, UPDATE, DELETE ON TABLE public.nagar_pragati_city_snapshot FROM authenticated;
GRANT SELECT ON TABLE public.nagar_pragati_city_snapshot TO authenticated;

-- 4. Align Table Grants with Authenticated Admin RLS Policies
-- Grants operation privileges to 'authenticated' role so Postgres RLS policies (is_org_admin)
-- can properly evaluate and permit admin writes while blocking non-admin staff and citizens.
GRANT INSERT, UPDATE, DELETE ON TABLE public.zone TO authenticated;
GRANT INSERT, UPDATE, DELETE ON TABLE public.ward TO authenticated;
GRANT INSERT, UPDATE, DELETE ON TABLE public.department TO authenticated;
GRANT INSERT, UPDATE, DELETE ON TABLE public.incident TO authenticated;
GRANT INSERT, UPDATE, DELETE ON TABLE public.incident_causal_link TO authenticated;
GRANT INSERT, UPDATE, DELETE ON TABLE public.user_role_assignment TO authenticated;
GRANT DELETE ON TABLE public.ahp_matrix_config TO authenticated;
GRANT DELETE ON TABLE public.category_service_time_prior TO authenticated;
GRANT DELETE ON TABLE public.ward_equity_credibility TO authenticated;
GRANT DELETE ON TABLE public.ward_resolution_stat TO authenticated;
GRANT DELETE ON TABLE public.ward_report_card_snapshot TO authenticated;
