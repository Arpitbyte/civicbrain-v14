# Phase 4: GIS Core & Spatial Analysis Pipeline — Technical Specification

**Version:** CivicBrain v14.4.0  
**Phase:** 4  
**Status:** SPECIFICATION PENDING APPROVAL  

---

## 1. Executive Summary & Scope

Phase 4 establishes the Geographic Information System (GIS) Core for CivicBrain v14 (§A14):
1. **Spatial Indexing & Query Architecture (§A14):** High-performance PostGIS 2D indexing (`GIST`) across wards, zones, intake reports, and operational incidents. Zero proprietary third-party GIS APIs (e.g. Mapbox/Google Maps server backends); 100% open PostGIS spatial processing on the existing Supabase PostgreSQL instance.
2. **GeoJSON FeatureCollection Serving (§A14, §A18):** Low-latency geospatial serialization endpoints producing valid RFC 7946 GeoJSON FeatureCollections for:
   - Administrative boundaries (`Zone` and `Ward` polygons).
   - Real-time operational incident feeds for staff workspaces (Command Deck, Ops Board).
   - Public transparency layers for citizen tracking (Nagrik Setu).
3. **Spatial Defect Clustering & Hotspot Detection (§A14):**
   - In-database density clustering utilizing PostGIS `ST_ClusterDBSCAN` (density-based spatial clustering of applications with noise) for automated civic hotspot detection (e.g. chronic pothole corridors or localized waterlogging clusters).
   - Spatial bounding-box filtering (`ST_MakeEnvelope` and PostGIS `&&` operator) with strict zoom-level spatial decimation to ensure sub-50ms query latency under Render free-tier RAM limits.
4. **Jurisdictional Bounding & Geofencing Enforcement (§A10, §A14):**
   - Verifying incident coordinates against municipal boundary geometries (`ST_Within`, `ST_Contains`).
   - Ward-level spatial assignment validation preventing cross-boundary leakage.

---

## 2. Invariant Rules & Architectural Ground Truth

1. **Zero External GIS Dependencies (Hard Rule 1 & Free Tier Grounding):**
   - All spatial relationships (containment, clustering, distance calculations, envelope intersections) are computed natively inside PostgreSQL via PostGIS.
   - Vector geometries are returned directly as standard GeoJSON objects via PostGIS `ST_AsGeoJSON` or SQLAlchemy `GeoAlchemy2` serialization.
2. **Strict Spatial Indexing on Every Geometry Column (Performance Invariant):**
   - Every table carrying a `Geometry` column (`zone.geom`, `ward.geom`, `intake_report.geom`, `incident.geom`) must have an active `GIST` index.
3. **Transparent Public Geometry Scrubbing (Privacy Invariant):**
   - While operational incidents for municipal staff maintain exact coordinates, public-facing GeoJSON feeds (for unauthenticated citizens or general transparency) apply subtle coordinate fuzzing (e.g. PostGIS `ST_SnapToGrid` to ~50m precision) to protect citizen residential privacy while preserving cluster veracity.
4. **Mandatory Explicit Scoped Grants (Standing Invariant 4):**
   - Any new RPC functions or views created in Phase 4 get explicit per-role `GRANT` statements with zero blanket `GRANT ALL`.

---

## 3. Database Migration & Schema Design (`migrations/0005_phase4_gis_core.sql`)

### 3.1 Spatial Indexes & Cluster Analysis Functions
```sql
-- Ensure GIST spatial indexes exist on all core geometry columns
CREATE INDEX IF NOT EXISTS idx_zone_geom_gist ON public.zone USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_ward_geom_gist ON public.ward USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_intake_report_geom_gist ON public.intake_report USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_incident_geom_gist ON public.incident USING GIST (geom);

-- In-database Spatial Clustering RPC using ST_ClusterDBSCAN
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
SECURITY DEFINER
SET search_path = public
AS $$
    WITH candidate_incidents AS (
        SELECT 
            id,
            geom,
            ST_ClusterDBSCAN(
                geom::geometry, 
                eps := p_eps_meters / 111320.0, -- approximate degrees for PostGIS planar DBSCAN in 4326
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

-- Scoped Grants on Clustering Function
REVOKE ALL ON FUNCTION get_incident_clusters(UUID, UUID, DOUBLE PRECISION, INTEGER) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION get_incident_clusters(UUID, UUID, DOUBLE PRECISION, INTEGER) TO anon, authenticated, service_role;
```

---

## 4. REST API Endpoints (`civicbrain/api/v1/gis.py`)

1. **`GET /v1/gis/wards/geojson`:**
   - Query params: `organization_id: UUID`, `zone_id: UUID | None`
   - Returns GeoJSON `FeatureCollection` of ward boundaries with metadata (`ward_number`, `name`, `code`).
2. **`GET /v1/gis/incidents/geojson`:**
   - Query params: `organization_id: UUID`, `department_id: UUID | None`, `bbox: str | None` (min_lon, min_lat, max_lon, max_lat), `status: str | None`
   - Returns GeoJSON `FeatureCollection` of active or filtered operational incidents with bounding-box spatial clipping via PostGIS `ST_MakeEnvelope`.
3. **`GET /v1/gis/clusters`:**
   - Query params: `organization_id: UUID`, `department_id: UUID | None`, `eps_meters: float = 100.0`, `min_points: int = 3`
   - Returns detected physical defect hotspots with centroid coordinates and grouped incident counts.

---

## 5. Verification Plan

1. **Automated Unit & Spatial Query Tests (`tests/test_gis_core.py`):**
   - Point-in-polygon containment verification against synthetic ward geometries.
   - Bounding-box intersection filtering (`&&` operator) verifying that out-of-bounds incidents are omitted.
   - DBSCAN cluster generation asserting that proximate incidents (<100m) are grouped into single cluster IDs.
2. **Live Supabase GIS Tests (`tests/test_live_supabase_phase4_gis.py`):**
   - Execution of `get_incident_clusters` RPC on live PostGIS database with real seeded incidents.
   - Verification of GeoJSON serialization and coordinate precision.
   - Teardown of all seeded test rows in `finally` block.
3. **CI & Quality Gates:**
   - `python -m ruff check civicbrain tests`
   - `python -m ruff format --check civicbrain tests`
   - `python -m mypy civicbrain`
   - `python -m pytest`
