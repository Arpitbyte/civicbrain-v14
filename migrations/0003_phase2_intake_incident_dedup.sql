-- =========================================================================
-- CivicBrain v14 — Phase 2: Domain Core (Intake, Incidents & Observations)
-- Migration 0003: Intake Report, Incident, Observation & Dedup Link Tables
-- =========================================================================

-- 1. Create Enums
DO $$ BEGIN
    CREATE TYPE intake_channel_enum AS ENUM (
        'pwa',
        'whatsapp',
        'ivr',
        'csc',
        'field_worker'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE intake_status_enum AS ENUM (
        'submitted',
        'processing',
        'triaged',
        'in_progress',
        'partially_resolved',
        'resolved',
        'closed',
        'rejected'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE observation_status_enum AS ENUM (
        'detected',
        'verified',
        'linked_to_incident',
        'rejected',
        'resolved'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE incident_status_enum AS ENUM (
        'reported',
        'triaged',
        'verified',
        'prioritized',
        'assigned',
        'in_progress',
        'resolved',
        'confirmed',
        'rejected',
        'appealed',
        'reopened'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE dedup_decision_enum AS ENUM (
        'exact_match',
        'probable_match',
        'distinct',
        'manual_review'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Intake Report Table
CREATE TABLE IF NOT EXISTS intake_report (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    citizen_id UUID REFERENCES citizen_profile(id) ON DELETE SET NULL,
    channel intake_channel_enum NOT NULL DEFAULT 'pwa',
    description TEXT,
    media_urls TEXT[] NOT NULL DEFAULT '{}',
    geom geometry(Point, 4326) NOT NULL,
    address_text TEXT,
    ward_id UUID REFERENCES ward(id) ON DELETE SET NULL,
    status intake_status_enum NOT NULL DEFAULT 'submitted',
    tracking_token VARCHAR(64) UNIQUE,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_intake_report_organization_id ON intake_report(organization_id);
CREATE INDEX IF NOT EXISTS idx_intake_report_citizen_id ON intake_report(citizen_id);
CREATE INDEX IF NOT EXISTS idx_intake_report_ward_id ON intake_report(ward_id);
CREATE INDEX IF NOT EXISTS idx_intake_report_geom ON intake_report USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_intake_report_status ON intake_report(status);
CREATE INDEX IF NOT EXISTS idx_intake_report_tracking_token ON intake_report(tracking_token);

-- 3. Incident Table (§A16 11-State Lifecycle)
CREATE TABLE IF NOT EXISTS incident (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    department_id UUID NOT NULL REFERENCES department(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES ward(id) ON DELETE CASCADE,
    category_code VARCHAR(50) NOT NULL,
    geom geometry(Point, 4326) NOT NULL,
    status incident_status_enum NOT NULL DEFAULT 'reported',
    severity SMALLINT NOT NULL DEFAULT 1 CHECK (severity BETWEEN 1 AND 5),
    assigned_worker_id UUID REFERENCES user_account(id) ON DELETE SET NULL,
    
    triaged_at TIMESTAMPTZ,
    verified_at TIMESTAMPTZ,
    prioritized_at TIMESTAMPTZ,
    assigned_at TIMESTAMPTZ,
    in_progress_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    confirmed_at TIMESTAMPTZ,
    rejected_at TIMESTAMPTZ,
    appealed_at TIMESTAMPTZ,
    reopened_at TIMESTAMPTZ,
    
    rejection_reason TEXT,
    appeal_reason TEXT,
    resolution_notes TEXT,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_incident_organization_id ON incident(organization_id);
CREATE INDEX IF NOT EXISTS idx_incident_dept_status ON incident(department_id, status);
CREATE INDEX IF NOT EXISTS idx_incident_ward_id ON incident(ward_id);
CREATE INDEX IF NOT EXISTS idx_incident_geom ON incident USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_incident_category ON incident(category_code);

-- 4. Observation Table
CREATE TABLE IF NOT EXISTS observation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    intake_report_id UUID NOT NULL REFERENCES intake_report(id) ON DELETE CASCADE,
    incident_id UUID REFERENCES incident(id) ON DELETE SET NULL,
    department_id UUID NOT NULL REFERENCES department(id) ON DELETE CASCADE,
    category_code VARCHAR(50) NOT NULL,
    source_media_url TEXT,
    bounding_box JSONB,
    confidence DOUBLE PRECISION NOT NULL DEFAULT 1.0 CHECK (confidence BETWEEN 0.0 AND 1.0),
    severity_score SMALLINT NOT NULL DEFAULT 1 CHECK (severity_score BETWEEN 1 AND 5),
    status observation_status_enum NOT NULL DEFAULT 'detected',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_observation_organization_id ON observation(organization_id);
CREATE INDEX IF NOT EXISTS idx_observation_intake_id ON observation(intake_report_id);
CREATE INDEX IF NOT EXISTS idx_observation_incident_id ON observation(incident_id);
CREATE INDEX IF NOT EXISTS idx_observation_dept_id ON observation(department_id);

-- 5. Incident Dedup Link Table
CREATE TABLE IF NOT EXISTS incident_dedup_link (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    observation_id UUID NOT NULL REFERENCES observation(id) ON DELETE CASCADE,
    candidate_incident_id UUID NOT NULL REFERENCES incident(id) ON DELETE CASCADE,
    spatial_distance_meters DOUBLE PRECISION NOT NULL,
    temporal_diff_seconds DOUBLE PRECISION NOT NULL,
    category_match BOOLEAN NOT NULL,
    text_similarity DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    match_weight DOUBLE PRECISION NOT NULL,
    match_probability DOUBLE PRECISION NOT NULL,
    decision dedup_decision_enum NOT NULL,
    model_version VARCHAR(50) NOT NULL DEFAULT 'splink_v4_cold_start',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_dedup_obs_candidate UNIQUE (observation_id, candidate_incident_id)
);

CREATE INDEX IF NOT EXISTS idx_dedup_organization_id ON incident_dedup_link(organization_id);
CREATE INDEX IF NOT EXISTS idx_dedup_obs_id ON incident_dedup_link(observation_id);
CREATE INDEX IF NOT EXISTS idx_dedup_candidate_id ON incident_dedup_link(candidate_incident_id);

-- =========================================================================
-- 6. Explicit Scoped Grants (Standing Invariant 4)
-- =========================================================================
-- intake_report
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE intake_report TO service_role;
GRANT SELECT, INSERT ON TABLE intake_report TO authenticated;
GRANT INSERT ON TABLE intake_report TO anon; -- For anonymous submissions (no broad SELECT)

-- incident
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE incident TO service_role;
GRANT SELECT, UPDATE ON TABLE incident TO authenticated;
GRANT SELECT ON TABLE incident TO anon; -- Public map & transparency

-- observation
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE observation TO service_role;
GRANT SELECT ON TABLE observation TO authenticated;
GRANT SELECT ON TABLE observation TO anon; -- Scoped via RLS

-- incident_dedup_link
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE incident_dedup_link TO service_role;
GRANT SELECT ON TABLE incident_dedup_link TO authenticated;
-- anon receives NO grants on incident_dedup_link

-- =========================================================================
-- 7. Security Definer RPC for Anonymous Tracking Token Lookup
-- =========================================================================
CREATE OR REPLACE FUNCTION get_anonymous_intake_report(p_tracking_token TEXT)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
DECLARE
    v_report_record RECORD;
    v_observations JSONB;
    v_result JSONB;
BEGIN
    SELECT 
        id, organization_id, channel, status, geom, address_text, 
        media_urls, created_at, updated_at
    INTO v_report_record
    FROM intake_report
    WHERE tracking_token = p_tracking_token;

    IF NOT FOUND THEN
        RETURN NULL;
    END IF;

    SELECT COALESCE(jsonb_agg(jsonb_build_object(
        'id', o.id,
        'category_code', o.category_code,
        'status', o.status,
        'severity_score', o.severity_score,
        'source_media_url', o.source_media_url,
        'created_at', o.created_at
    )), '[]'::jsonb)
    INTO v_observations
    FROM observation o
    WHERE o.intake_report_id = v_report_record.id;

    v_result := jsonb_build_object(
        'report_id', v_report_record.id,
        'organization_id', v_report_record.organization_id,
        'channel', v_report_record.channel,
        'status', v_report_record.status,
        'address_text', v_report_record.address_text,
        'media_urls', v_report_record.media_urls,
        'created_at', v_report_record.created_at,
        'updated_at', v_report_record.updated_at,
        'observations', v_observations
    );

    RETURN v_result;
END;
$$;

REVOKE ALL ON FUNCTION get_anonymous_intake_report(TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION get_anonymous_intake_report(TEXT) TO anon, authenticated, service_role;

-- =========================================================================
-- 8. Enable Row-Level Security
-- =========================================================================
ALTER TABLE intake_report ENABLE ROW LEVEL SECURITY;
ALTER TABLE incident ENABLE ROW LEVEL SECURITY;
ALTER TABLE observation ENABLE ROW LEVEL SECURITY;
ALTER TABLE incident_dedup_link ENABLE ROW LEVEL SECURITY;

-- 8.1 Service Role Policies
DROP POLICY IF EXISTS "service_role_intake_report_all" ON intake_report;
CREATE POLICY "service_role_intake_report_all" ON intake_report FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_incident_all" ON incident;
CREATE POLICY "service_role_incident_all" ON incident FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_observation_all" ON observation;
CREATE POLICY "service_role_observation_all" ON observation FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_dedup_link_all" ON incident_dedup_link;
CREATE POLICY "service_role_dedup_link_all" ON incident_dedup_link FOR ALL TO service_role USING (true) WITH CHECK (true);

-- 8.2 Citizen & Public Policies
-- Citizens can insert intake reports (both authenticated and anon)
DROP POLICY IF EXISTS "citizen_insert_intake_report" ON intake_report;
CREATE POLICY "citizen_insert_intake_report" ON intake_report FOR INSERT TO anon, authenticated WITH CHECK (true);

-- Authenticated citizens can view their own filed reports
DROP POLICY IF EXISTS "citizen_select_own_intake_report" ON intake_report;
CREATE POLICY "citizen_select_own_intake_report" ON intake_report FOR SELECT TO authenticated
    USING (citizen_id = auth.uid() OR is_org_admin(organization_id));

-- Public read on incident table (sanitized civic transparency)
DROP POLICY IF EXISTS "public_read_incidents" ON incident;
CREATE POLICY "public_read_incidents" ON incident FOR SELECT TO anon, authenticated USING (true);

-- Observations viewable if citizen owns parent report or is admin
DROP POLICY IF EXISTS "citizen_select_own_observations" ON observation;
CREATE POLICY "citizen_select_own_observations" ON observation FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM intake_report ir
            WHERE ir.id = observation.intake_report_id
              AND (ir.citizen_id = auth.uid() OR is_org_admin(ir.organization_id))
        )
    );

-- 8.3 Staff RBAC Policies for Incidents & Observations
-- Staff Admin full access on incidents within organization
DROP POLICY IF EXISTS "admin_manage_incidents" ON incident;
CREATE POLICY "admin_manage_incidents" ON incident FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- Department Staff: can update incidents within their own department
DROP POLICY IF EXISTS "dept_staff_update_incidents" ON incident;
CREATE POLICY "dept_staff_update_incidents" ON incident FOR UPDATE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = incident.organization_id
              AND ura.role = 'department_staff'
              AND ura.department_id = incident.department_id
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM user_role_assignment ura
            WHERE ura.user_id = auth.uid()
              AND ura.organization_id = incident.organization_id
              AND ura.role = 'department_staff'
              AND ura.department_id = incident.department_id
        )
    );

-- Dedup Link access for internal staff
DROP POLICY IF EXISTS "staff_view_dedup_links" ON incident_dedup_link;
CREATE POLICY "staff_view_dedup_links" ON incident_dedup_link FOR SELECT TO authenticated
    USING (is_org_admin(organization_id));
