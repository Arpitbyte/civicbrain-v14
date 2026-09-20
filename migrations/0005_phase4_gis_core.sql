-- CivicBrain v14 — Phase 4: GIS Core & Spatial Analysis Pipeline (§A14)
-- Migration 0005: Spatial Indexes, RLS Tenant Scoping, and In-Database Spatial Clustering

-- 1. Ensure GIST Spatial Indexes Exist on All Core Geometry Columns
CREATE INDEX IF NOT EXISTS idx_zone_geom_gist ON public.zone USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_ward_geom_gist ON public.ward USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_intake_report_geom_gist ON public.intake_report USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_incident_geom_gist ON public.incident USING GIST (geom);

-- 2. Refine RLS Policies on Incident Table for Tenant Isolation (§A10, §A14)
-- Public read on incident table strictly for anonymous transparency (with spatial scrubbing at API layer)
DROP POLICY IF EXISTS "public_read_incidents" ON public.incident;
CREATE POLICY "public_read_incidents" ON public.incident
    FOR SELECT TO anon
    USING (true);

-- Authenticated staff/admins can strictly only select incidents within their organization
DROP POLICY IF EXISTS "staff_read_incidents" ON public.incident;
CREATE POLICY "staff_read_incidents" ON public.incident
    FOR SELECT TO authenticated
    USING (
        is_org_admin(organization_id)
        OR EXISTS (
            SELECT 1 FROM public.user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = incident.organization_id
        )
    );

-- 3. In-Database Spatial Clustering RPC using ST_ClusterDBSCAN (§A14)
-- Note: SECURITY DEFINER is omitted so it runs as the calling role (SECURITY INVOKER)
-- and inherits table-level RLS on incident.
CREATE OR REPLACE FUNCTION get_incident_clusters(
    p_organization_id UUID,
    p_department_id UUID DEFAULT NULL,
    p_eps_meters DOUBLE PRECISION DEFAULT 100.0,
    p_min_points INTEGER DEFAULT 3
)
RETURNS TABLE (
    cluster_id INTEGER,
    incident_count BIGINT,
    centroid_geojson TEXT,
    incident_ids UUID[]
)
LANGUAGE sql
STABLE
SET search_path = public
AS $$
    WITH candidate_incidents AS (
        SELECT 
            id,
            geom,
            ST_ClusterDBSCAN(
                geom::geometry, 
                -- Planar degree approximation (1 deg ~ 111,320m) valid for single-city / fixed-latitude deployment; not latitude-corrected.
                eps := p_eps_meters / 111320.0,
                minpoints := p_min_points
            ) OVER () AS cid
        FROM incident
        WHERE organization_id = p_organization_id
          AND status NOT IN ('confirmed', 'rejected')
          AND (p_department_id IS NULL OR department_id = p_department_id)
    )
    SELECT 
        cid AS cluster_id,
        count(*) AS incident_count,
        ST_AsGeoJSON(ST_Centroid(ST_Collect(geom))) AS centroid_geojson,
        array_agg(id) AS incident_ids
    FROM candidate_incidents
    WHERE cid IS NOT NULL
    GROUP BY cid
    ORDER BY incident_count DESC;
$$;

-- 4. Scoped Grants on Clustering Function (Standing Invariant 4)
REVOKE ALL ON FUNCTION get_incident_clusters(UUID, UUID, DOUBLE PRECISION, INTEGER) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION get_incident_clusters(UUID, UUID, DOUBLE PRECISION, INTEGER) TO anon, authenticated, service_role;
