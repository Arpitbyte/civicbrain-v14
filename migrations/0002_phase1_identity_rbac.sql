-- CivicBrain Phase 1: Identity, Multi-Tenant Hierarchy & RBAC Migration
-- Sets up administrative hierarchy (zone, ward with PostGIS polygons, department),
-- user accounts, role assignments, elected representatives, citizen profiles,
-- and strict operation-scoped table grants and Row-Level Security (RLS) policies.

-- 1. Create Staff Role and Citizen Verification Enums
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'staff_role_enum') THEN
        CREATE TYPE staff_role_enum AS ENUM (
            'admin',
            'dispatcher',
            'department_staff',
            'zonal_supervisor',
            'field_worker',
            'corporator'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'citizen_verification_method_enum') THEN
        CREATE TYPE citizen_verification_method_enum AS ENUM (
            'phone_otp',
            'digilocker'
        );
    END IF;
END $$;

-- 2. Administrative Hierarchy: Zone Table
CREATE TABLE IF NOT EXISTS zone (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    geom geometry(Polygon, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_zone_org_code UNIQUE (organization_id, code)
);

CREATE INDEX IF NOT EXISTS idx_zone_organization_id ON zone(organization_id);
CREATE INDEX IF NOT EXISTS idx_zone_geom ON zone USING GIST(geom);

-- 3. Administrative & Electoral Hierarchy: Ward Table
CREATE TABLE IF NOT EXISTS ward (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    zone_id UUID NOT NULL REFERENCES zone(id) ON DELETE CASCADE,
    ward_number INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    geom geometry(Polygon, 4326) NOT NULL,
    centroid geometry(Point, 4326),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_ward_org_number UNIQUE (organization_id, ward_number),
    CONSTRAINT uq_ward_org_code UNIQUE (organization_id, code)
);

CREATE INDEX IF NOT EXISTS idx_ward_organization_id ON ward(organization_id);
CREATE INDEX IF NOT EXISTS idx_ward_zone_id ON ward(zone_id);
CREATE INDEX IF NOT EXISTS idx_ward_geom ON ward USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_ward_centroid ON ward USING GIST(centroid);

-- 4. Department Table (Matching DIGIT PGR Taxonomy)
CREATE TABLE IF NOT EXISTS department (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_department_org_code UNIQUE (organization_id, code)
);

CREATE INDEX IF NOT EXISTS idx_department_organization_id ON department(organization_id);

-- 5. User Account Table (Maps to Supabase Auth auth.users)
CREATE TABLE IF NOT EXISTS user_account (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    email VARCHAR(255),
    phone VARCHAR(20) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    mfa_enabled BOOLEAN NOT NULL DEFAULT false,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_account_organization_id ON user_account(organization_id);

-- 6. User Role Assignment Table
CREATE TABLE IF NOT EXISTS user_role_assignment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    role staff_role_enum NOT NULL,
    department_id UUID REFERENCES department(id) ON DELETE SET NULL,
    zone_id UUID REFERENCES zone(id) ON DELETE SET NULL,
    ward_id UUID REFERENCES ward(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_role_assignment UNIQUE (user_id, role, department_id, zone_id, ward_id)
);

CREATE INDEX IF NOT EXISTS idx_user_role_user_id ON user_role_assignment(user_id);
CREATE INDEX IF NOT EXISTS idx_user_role_organization_id ON user_role_assignment(organization_id);

-- 7. Elected Representative (Corporator / Councillor per 74th CAA, 1992)
CREATE TABLE IF NOT EXISTS elected_representative (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    ward_id UUID NOT NULL REFERENCES ward(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    party_affiliation VARCHAR(100),
    term_start DATE NOT NULL,
    term_end DATE NOT NULL,
    office_contact VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_elected_representative_ward UNIQUE (ward_id),
    CONSTRAINT uq_elected_representative_user UNIQUE (user_id)
);

CREATE INDEX IF NOT EXISTS idx_elected_rep_org_id ON elected_representative(organization_id);

-- 8. Citizen Profile Table (Phone OTP Primary, No Aadhaar per §A8)
CREATE TABLE IF NOT EXISTS citizen_profile (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    display_name VARCHAR(255),
    preferred_language VARCHAR(10) NOT NULL DEFAULT 'en',
    verification_method citizen_verification_method_enum NOT NULL DEFAULT 'phone_otp',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================================================================
-- 9. Explicit Operation-Scoped Table Grants (Standing Invariant 4)
-- Never blanket GRANT ALL. Scoped strictly per role.
-- =========================================================================

-- zone: public geographical boundaries
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE zone TO service_role;
GRANT SELECT ON TABLE zone TO authenticated;
GRANT SELECT ON TABLE zone TO anon;

-- ward: public geographical & electoral boundaries
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE ward TO service_role;
GRANT SELECT ON TABLE ward TO authenticated;
GRANT SELECT ON TABLE ward TO anon;

-- department: public intake taxonomy
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE department TO service_role;
GRANT SELECT ON TABLE department TO authenticated;
GRANT SELECT ON TABLE department TO anon;

-- elected_representative: public representative lookup
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE elected_representative TO service_role;
GRANT SELECT ON TABLE elected_representative TO authenticated;
GRANT SELECT ON TABLE elected_representative TO anon;

-- user_account & user_role_assignment: internal staff only (no anon)
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE user_account TO service_role;
GRANT SELECT, UPDATE ON TABLE user_account TO authenticated;

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE user_role_assignment TO service_role;
GRANT SELECT ON TABLE user_role_assignment TO authenticated;

-- citizen_profile: citizen self-service only (no anon)
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE citizen_profile TO service_role;
GRANT SELECT, INSERT, UPDATE ON TABLE citizen_profile TO authenticated;

-- =========================================================================
-- 10. Enable Row-Level Security
-- =========================================================================
ALTER TABLE zone ENABLE ROW LEVEL SECURITY;
ALTER TABLE ward ENABLE ROW LEVEL SECURITY;
ALTER TABLE department ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_account ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_role_assignment ENABLE ROW LEVEL SECURITY;
ALTER TABLE elected_representative ENABLE ROW LEVEL SECURITY;
ALTER TABLE citizen_profile ENABLE ROW LEVEL SECURITY;

-- =========================================================================
-- 11. Define RLS Policies
-- =========================================================================

-- 11.1 Service Role Policies (Trusted background workers)
DROP POLICY IF EXISTS "service_role_zone_all" ON zone;
CREATE POLICY "service_role_zone_all" ON zone FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_ward_all" ON ward;
CREATE POLICY "service_role_ward_all" ON ward FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_department_all" ON department;
CREATE POLICY "service_role_department_all" ON department FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_user_account_all" ON user_account;
CREATE POLICY "service_role_user_account_all" ON user_account FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_role_assignment_all" ON user_role_assignment;
CREATE POLICY "service_role_role_assignment_all" ON user_role_assignment FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_elected_rep_all" ON elected_representative;
CREATE POLICY "service_role_elected_rep_all" ON elected_representative FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_role_citizen_profile_all" ON citizen_profile;
CREATE POLICY "service_role_citizen_profile_all" ON citizen_profile FOR ALL TO service_role USING (true) WITH CHECK (true);

-- 11.2 Public Geographical & Department Boundaries Read Policies
DROP POLICY IF EXISTS "public_read_zones" ON zone;
CREATE POLICY "public_read_zones" ON zone FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "public_read_wards" ON ward;
CREATE POLICY "public_read_wards" ON ward FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "public_read_departments" ON department;
CREATE POLICY "public_read_departments" ON department FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "public_read_elected_reps" ON elected_representative;
CREATE POLICY "public_read_elected_reps" ON elected_representative FOR SELECT TO anon, authenticated USING (true);

-- Security Definer helper to check admin role without recursive RLS evaluation
CREATE OR REPLACE FUNCTION is_org_admin(p_org_id UUID)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
    SELECT EXISTS (
        SELECT 1 FROM user_role_assignment
        WHERE user_id = auth.uid()
          AND role = 'admin'
          AND organization_id = p_org_id
    );
$$;

GRANT EXECUTE ON FUNCTION is_org_admin(UUID) TO authenticated, service_role;

-- Staff Admin write policies on organization structure
DROP POLICY IF EXISTS "admin_manage_zones" ON zone;
CREATE POLICY "admin_manage_zones" ON zone FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

DROP POLICY IF EXISTS "admin_manage_wards" ON ward;
CREATE POLICY "admin_manage_wards" ON ward FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

DROP POLICY IF EXISTS "admin_manage_departments" ON department;
CREATE POLICY "admin_manage_departments" ON department FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- 11.3 User Account RLS Policies
-- Users can view their own profile; Admin can view staff within their organization
DROP POLICY IF EXISTS "user_account_read_policy" ON user_account;
CREATE POLICY "user_account_read_policy" ON user_account FOR SELECT TO authenticated
    USING (auth.uid() = id OR is_org_admin(organization_id));

-- Users can update their own profile; Admin can update staff within organization
DROP POLICY IF EXISTS "user_account_update_policy" ON user_account;
CREATE POLICY "user_account_update_policy" ON user_account FOR UPDATE TO authenticated
    USING (auth.uid() = id OR is_org_admin(organization_id))
    WITH CHECK (auth.uid() = id OR is_org_admin(organization_id));

-- 11.4 User Role Assignment RLS Policies
-- User can view own assignments; Admin can view and manage within their organization
DROP POLICY IF EXISTS "role_assignment_read_policy" ON user_role_assignment;
CREATE POLICY "role_assignment_read_policy" ON user_role_assignment FOR SELECT TO authenticated
    USING (user_id = auth.uid() OR is_org_admin(organization_id));

DROP POLICY IF EXISTS "admin_manage_role_assignments" ON user_role_assignment;
CREATE POLICY "admin_manage_role_assignments" ON user_role_assignment FOR ALL TO authenticated
    USING (is_org_admin(organization_id))
    WITH CHECK (is_org_admin(organization_id));

-- 11.5 Citizen Profile RLS Policies (Strict self-isolation)
DROP POLICY IF EXISTS "citizen_read_own_profile" ON citizen_profile;
CREATE POLICY "citizen_read_own_profile" ON citizen_profile FOR SELECT TO authenticated
    USING (auth.uid() = id);

DROP POLICY IF EXISTS "citizen_insert_own_profile" ON citizen_profile;
CREATE POLICY "citizen_insert_own_profile" ON citizen_profile FOR INSERT TO authenticated
    WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "citizen_update_own_profile" ON citizen_profile;
CREATE POLICY "citizen_update_own_profile" ON citizen_profile FOR UPDATE TO authenticated
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);
