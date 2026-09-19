-- CivicBrain Phase 0: Foundations Migration
-- Sets up PostGIS, Organization tenant table, and enables Row-Level Security (RLS)

-- 1. Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Create ULB Type Enum (74th Constitutional Amendment Act, 1992)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ulb_type_enum') THEN
        CREATE TYPE ulb_type_enum AS ENUM (
            'municipal_corporation',
            'municipal_council',
            'nagar_panchayat'
        );
    END IF;
END $$;

-- 3. Create Root Tenant Organization Table
CREATE TABLE IF NOT EXISTS organization (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    ulb_type ulb_type_enum NOT NULL DEFAULT 'municipal_corporation',
    state VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index on organization code
CREATE INDEX IF NOT EXISTS idx_organization_code ON organization(code);

-- 4. Enable Row-Level Security (Hard Rule 5: RLS is the real authorization boundary)
ALTER TABLE organization ENABLE ROW LEVEL SECURITY;

-- 5. Define Initial RLS Policies
-- Service role (trusted background workers) has full access
DROP POLICY IF EXISTS "service_role_full_access" ON organization;
CREATE POLICY "service_role_full_access"
    ON organization
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Authenticated staff users can view organizations
DROP POLICY IF EXISTS "authenticated_read_organizations" ON organization;
CREATE POLICY "authenticated_read_organizations"
    ON organization
    FOR SELECT
    TO authenticated
    USING (true);

-- Anonymous / unauthenticated clients cannot read organization rows
-- (Implicitly denied because no policy grants access to anon)

-- 6. Table Grants for PostgREST Roles
GRANT ALL ON TABLE organization TO postgres, service_role;
GRANT SELECT ON TABLE organization TO authenticated;
GRANT SELECT ON TABLE organization TO anon;
