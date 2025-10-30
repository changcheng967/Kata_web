-- =====================================================================
-- DouEssay v10.0.0 - Supabase Database Schema for License Management
-- =====================================================================
-- This schema provides comprehensive license tracking, audit logging,
-- and security features for the license key system.
-- =====================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================================
-- SYSTEM_CONFIG TABLE
-- Stores system-wide configuration settings
-- =====================================================================
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default configuration values
INSERT INTO system_config (key, value, description) VALUES
('expiring_licenses_warning_days', '30', 'Number of days before expiration to show in expiring licenses view'),
('grace_period_days', '7', 'Grace period days after license expiration'),
('max_hardware_transfers', '3', 'Maximum number of hardware transfers allowed per license')
ON CONFLICT (key) DO NOTHING;

-- =====================================================================
-- COMPANIES TABLE
-- Stores information about licensed companies
-- =====================================================================
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    address TEXT,
    country VARCHAR(100),
    tax_id VARCHAR(100),
    contact_person VARCHAR(255),
    contact_phone VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Indexes for performance
    CONSTRAINT companies_email_unique UNIQUE (email)
);

CREATE INDEX idx_companies_email ON companies(email);
CREATE INDEX idx_companies_created_at ON companies(created_at);
CREATE INDEX idx_companies_is_active ON companies(is_active);

-- =====================================================================
-- LICENSE_TYPES TABLE
-- Defines different types of licenses available
-- =====================================================================
CREATE TABLE IF NOT EXISTS license_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type_name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    features JSONB NOT NULL DEFAULT '[]'::jsonb,
    max_users_default INTEGER DEFAULT 10,
    price_yearly DECIMAL(10, 2),
    price_monthly DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_license_types_type_name ON license_types(type_name);

-- Insert default license types
INSERT INTO license_types (type_name, display_name, description, features, max_users_default, price_yearly, price_monthly) VALUES
('BASIC', 'Basic License', 'Entry-level license for small teams', 
 '["core_features", "standard_support"]'::jsonb, 5, 999.00, 99.00),
('PROFESSIONAL', 'Professional License', 'Advanced features for growing businesses',
 '["core_features", "advanced_analytics", "priority_support", "api_access"]'::jsonb, 50, 4999.00, 499.00),
('ENTERPRISE', 'Enterprise License', 'Full-featured license for large organizations',
 '["core_features", "advanced_analytics", "priority_support", "api_access", "white_label", "custom_integrations", "dedicated_support", "sla_99_9"]'::jsonb, 500, 19999.00, 1999.00),
('UNLIMITED', 'Unlimited License', 'Unlimited users and features',
 '["all_features", "unlimited_users", "premium_support", "custom_development"]'::jsonb, -1, 49999.00, 4999.00);

-- =====================================================================
-- LICENSES TABLE
-- Core table storing all generated licenses
-- =====================================================================
CREATE TABLE IF NOT EXISTS licenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID NOT NULL UNIQUE, -- From license generator
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    license_type_id UUID NOT NULL REFERENCES license_types(id),
    
    -- License details
    license_key TEXT NOT NULL UNIQUE,
    signature TEXT NOT NULL,
    activation_code VARCHAR(50) NOT NULL UNIQUE,
    
    -- License configuration
    max_users INTEGER NOT NULL DEFAULT 10,
    hardware_id VARCHAR(64), -- SHA256 hash of hardware identifiers
    custom_features JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Status and dates
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, expired, revoked, suspended
    issue_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expiration_date TIMESTAMP WITH TIME ZONE,
    last_validated_at TIMESTAMP WITH TIME ZONE,
    revoked_at TIMESTAMP WITH TIME ZONE,
    revocation_reason TEXT,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(255),
    
    -- Constraints
    CONSTRAINT licenses_status_check CHECK (status IN ('active', 'expired', 'revoked', 'suspended')),
    CONSTRAINT licenses_expiration_check CHECK (expiration_date IS NULL OR expiration_date > issue_date)
);

-- Indexes for performance
CREATE INDEX idx_licenses_license_id ON licenses(license_id);
CREATE INDEX idx_licenses_company_id ON licenses(company_id);
CREATE INDEX idx_licenses_activation_code ON licenses(activation_code);
CREATE INDEX idx_licenses_status ON licenses(status);
CREATE INDEX idx_licenses_expiration_date ON licenses(expiration_date);
CREATE INDEX idx_licenses_hardware_id ON licenses(hardware_id);
CREATE INDEX idx_licenses_created_at ON licenses(created_at);

-- =====================================================================
-- LICENSE_ACTIVATIONS TABLE
-- Tracks license activation attempts and hardware binding
-- =====================================================================
CREATE TABLE IF NOT EXISTS license_activations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID NOT NULL REFERENCES licenses(id) ON DELETE CASCADE,
    
    -- Activation details
    hardware_id VARCHAR(64) NOT NULL,
    machine_name VARCHAR(255),
    os_info VARCHAR(255),
    ip_address INET,
    
    -- Status
    activation_status VARCHAR(20) NOT NULL DEFAULT 'success', -- success, failed, revoked
    activation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deactivation_date TIMESTAMP WITH TIME ZONE,
    
    -- Additional info
    user_agent TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT activations_status_check CHECK (activation_status IN ('success', 'failed', 'revoked'))
);

CREATE INDEX idx_activations_license_id ON license_activations(license_id);
CREATE INDEX idx_activations_hardware_id ON license_activations(hardware_id);
CREATE INDEX idx_activations_activation_date ON license_activations(activation_date);

-- =====================================================================
-- LICENSE_VALIDATIONS TABLE
-- Audit log of all license validation attempts
-- =====================================================================
CREATE TABLE IF NOT EXISTS license_validations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID REFERENCES licenses(id) ON DELETE CASCADE,
    
    -- Validation details
    validation_result BOOLEAN NOT NULL,
    error_message TEXT,
    hardware_id VARCHAR(64),
    ip_address INET,
    user_agent TEXT,
    
    -- Additional context
    feature_requested VARCHAR(255),
    validation_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time_ms INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_validations_license_id ON license_validations(license_id);
CREATE INDEX idx_validations_timestamp ON license_validations(validation_timestamp);
CREATE INDEX idx_validations_result ON license_validations(validation_result);

-- =====================================================================
-- LICENSE_USAGE TABLE
-- Tracks concurrent user usage and feature utilization
-- =====================================================================
CREATE TABLE IF NOT EXISTS license_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID NOT NULL REFERENCES licenses(id) ON DELETE CASCADE,
    
    -- Usage metrics
    active_users INTEGER NOT NULL DEFAULT 0,
    peak_users INTEGER NOT NULL DEFAULT 0,
    feature_usage JSONB DEFAULT '{}'::jsonb,
    
    -- Time period
    usage_date DATE NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT usage_unique_license_date UNIQUE (license_id, usage_date)
);

CREATE INDEX idx_usage_license_id ON license_usage(license_id);
CREATE INDEX idx_usage_usage_date ON license_usage(usage_date);

-- =====================================================================
-- LICENSE_REVOCATIONS TABLE
-- Detailed tracking of license revocations
-- =====================================================================
CREATE TABLE IF NOT EXISTS license_revocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    license_id UUID NOT NULL REFERENCES licenses(id) ON DELETE CASCADE,
    
    -- Revocation details
    revoked_by VARCHAR(255) NOT NULL,
    revocation_reason TEXT NOT NULL,
    revoked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT,
    
    -- Can be restored?
    can_restore BOOLEAN DEFAULT FALSE,
    restored_at TIMESTAMP WITH TIME ZONE,
    restored_by VARCHAR(255)
);

CREATE INDEX idx_revocations_license_id ON license_revocations(license_id);
CREATE INDEX idx_revocations_revoked_at ON license_revocations(revoked_at);

-- =====================================================================
-- API_KEYS TABLE
-- API keys for programmatic license management
-- =====================================================================
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    
    -- API key details
    key_name VARCHAR(255) NOT NULL,
    api_key VARCHAR(64) NOT NULL UNIQUE,
    api_secret_hash VARCHAR(128) NOT NULL, -- bcrypt hash
    
    -- Permissions
    permissions JSONB NOT NULL DEFAULT '["read"]'::jsonb,
    rate_limit INTEGER DEFAULT 1000, -- requests per hour
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(255)
);

CREATE INDEX idx_api_keys_api_key ON api_keys(api_key);
CREATE INDEX idx_api_keys_company_id ON api_keys(company_id);

-- =====================================================================
-- AUDIT_LOGS TABLE
-- Comprehensive audit trail for all operations
-- =====================================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Event details
    event_type VARCHAR(50) NOT NULL, -- license_created, license_validated, license_revoked, etc.
    entity_type VARCHAR(50) NOT NULL, -- license, company, api_key
    entity_id UUID,
    
    -- Actor information
    actor_id VARCHAR(255),
    actor_type VARCHAR(50), -- user, system, api
    ip_address INET,
    
    -- Event data
    action VARCHAR(255) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_entity_type ON audit_logs(entity_type);
CREATE INDEX idx_audit_logs_entity_id ON audit_logs(entity_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- =====================================================================
-- FUNCTIONS AND TRIGGERS
-- =====================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_license_types_updated_at BEFORE UPDATE ON license_types
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_licenses_updated_at BEFORE UPDATE ON licenses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to check and update license expiration status
CREATE OR REPLACE FUNCTION check_license_expiration()
RETURNS void AS $$
BEGIN
    UPDATE licenses
    SET status = 'expired'
    WHERE status = 'active'
      AND expiration_date IS NOT NULL
      AND expiration_date < NOW();
END;
$$ LANGUAGE plpgsql;

-- Function to create audit log entry
CREATE OR REPLACE FUNCTION create_audit_log()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_logs (event_type, entity_type, entity_id, action, new_values)
        VALUES (TG_TABLE_NAME || '_created', TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_logs (event_type, entity_type, entity_id, action, old_values, new_values)
        VALUES (TG_TABLE_NAME || '_updated', TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_logs (event_type, entity_type, entity_id, action, old_values)
        VALUES (TG_TABLE_NAME || '_deleted', TG_TABLE_NAME, OLD.id, TG_OP, row_to_json(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger to licenses table
CREATE TRIGGER audit_licenses AFTER INSERT OR UPDATE OR DELETE ON licenses
    FOR EACH ROW EXECUTE FUNCTION create_audit_log();

-- =====================================================================
-- VIEWS FOR REPORTING
-- =====================================================================

-- View: Active licenses summary
CREATE OR REPLACE VIEW active_licenses_summary AS
SELECT 
    l.id,
    l.license_id,
    c.company_name,
    c.email,
    lt.display_name as license_type,
    l.max_users,
    l.status,
    l.issue_date,
    l.expiration_date,
    CASE 
        WHEN l.expiration_date IS NULL THEN 'Perpetual'
        WHEN l.expiration_date > NOW() THEN CONCAT(EXTRACT(DAY FROM l.expiration_date - NOW()), ' days')
        ELSE 'Expired'
    END as time_remaining,
    l.hardware_id IS NOT NULL as is_hardware_bound
FROM licenses l
JOIN companies c ON l.company_id = c.id
JOIN license_types lt ON l.license_type_id = lt.id
WHERE l.status = 'active';

-- View: License usage statistics
CREATE OR REPLACE VIEW license_usage_stats AS
SELECT 
    l.license_id,
    c.company_name,
    COUNT(DISTINCT lv.id) as total_validations,
    COUNT(DISTINCT CASE WHEN lv.validation_result = true THEN lv.id END) as successful_validations,
    MAX(lv.validation_timestamp) as last_validated,
    COUNT(DISTINCT la.id) as activation_count,
    COALESCE(MAX(lu.peak_users), 0) as peak_concurrent_users
FROM licenses l
JOIN companies c ON l.company_id = c.id
LEFT JOIN license_validations lv ON l.id = lv.license_id
LEFT JOIN license_activations la ON l.id = la.license_id
LEFT JOIN license_usage lu ON l.id = lu.license_id
GROUP BY l.license_id, c.company_name;

-- View: Expiring licenses (configurable warning period)
CREATE OR REPLACE VIEW expiring_licenses AS
SELECT 
    l.id,
    l.license_id,
    c.company_name,
    c.email,
    lt.display_name as license_type,
    l.expiration_date,
    EXTRACT(DAY FROM l.expiration_date - NOW()) as days_until_expiration
FROM licenses l
JOIN companies c ON l.company_id = c.id
JOIN license_types lt ON l.license_type_id = lt.id
WHERE l.status = 'active'
  AND l.expiration_date IS NOT NULL
  AND l.expiration_date BETWEEN NOW() AND NOW() + 
      MAKE_INTERVAL(days => (SELECT value::INTEGER FROM system_config WHERE key = 'expiring_licenses_warning_days'))
ORDER BY l.expiration_date ASC;

-- =====================================================================
-- SECURITY POLICIES (Row Level Security)
-- =====================================================================

-- Enable RLS on sensitive tables
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE license_activations ENABLE ROW LEVEL SECURITY;
ALTER TABLE license_validations ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Policy: Companies can only see their own licenses
CREATE POLICY company_licenses_policy ON licenses
    FOR SELECT
    USING (company_id IN (
        SELECT id FROM companies WHERE email = current_user
    ));

-- Policy: API keys can only access their company's data
CREATE POLICY api_key_access_policy ON licenses
    FOR SELECT
    USING (company_id IN (
        SELECT company_id FROM api_keys WHERE api_key = current_setting('app.api_key', true)
    ));

-- =====================================================================
-- HELPER FUNCTIONS FOR APPLICATION
-- =====================================================================

-- Function to get license by activation code
CREATE OR REPLACE FUNCTION get_license_by_activation_code(p_activation_code VARCHAR)
RETURNS TABLE (
    license_key TEXT,
    signature TEXT,
    company_name VARCHAR,
    license_type VARCHAR,
    status VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        l.license_key,
        l.signature,
        c.company_name,
        lt.type_name,
        l.status
    FROM licenses l
    JOIN companies c ON l.company_id = c.id
    JOIN license_types lt ON l.license_type_id = lt.id
    WHERE l.activation_code = p_activation_code;
END;
$$ LANGUAGE plpgsql;

-- Function to record license validation
CREATE OR REPLACE FUNCTION record_license_validation(
    p_license_id UUID,
    p_validation_result BOOLEAN,
    p_error_message TEXT DEFAULT NULL,
    p_hardware_id VARCHAR DEFAULT NULL,
    p_ip_address INET DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_validation_id UUID;
BEGIN
    INSERT INTO license_validations (
        license_id,
        validation_result,
        error_message,
        hardware_id,
        ip_address
    ) VALUES (
        p_license_id,
        p_validation_result,
        p_error_message,
        p_hardware_id,
        p_ip_address
    ) RETURNING id INTO v_validation_id;
    
    -- Update last_validated_at on license
    UPDATE licenses
    SET last_validated_at = NOW()
    WHERE id = p_license_id;
    
    RETURN v_validation_id;
END;
$$ LANGUAGE plpgsql;

-- Function to revoke license
CREATE OR REPLACE FUNCTION revoke_license(
    p_license_id UUID,
    p_revoked_by VARCHAR,
    p_reason TEXT,
    p_notes TEXT DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Update license status
    UPDATE licenses
    SET status = 'revoked',
        revoked_at = NOW(),
        revocation_reason = p_reason
    WHERE license_id = p_license_id;
    
    -- Insert revocation record
    INSERT INTO license_revocations (
        license_id,
        revoked_by,
        revocation_reason,
        notes
    ) VALUES (
        (SELECT id FROM licenses WHERE license_id = p_license_id),
        p_revoked_by,
        p_reason,
        p_notes
    );
    
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- =====================================================================
-- SCHEDULED JOBS (PostgreSQL cron extension - optional)
-- =====================================================================

-- To use scheduled jobs, enable pg_cron extension in Supabase:
-- CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule daily license expiration check (uncomment if using pg_cron)
-- SELECT cron.schedule(
--     'check-license-expiration',
--     '0 0 * * *', -- Run daily at midnight
--     $$SELECT check_license_expiration()$$
-- );

-- =====================================================================
-- SAMPLE DATA FOR TESTING (Optional - comment out for production)
-- =====================================================================

-- Sample company
INSERT INTO companies (company_name, email, phone, country, contact_person)
VALUES ('Test Company Inc', 'test@example.com', '+1-555-0123', 'USA', 'John Doe')
ON CONFLICT (email) DO NOTHING;

-- =====================================================================
-- SCHEMA COMPLETE
-- =====================================================================

-- Display success message
DO $$
BEGIN
    RAISE NOTICE 'DouEssay v10.0.0 License Management Schema created successfully!';
    RAISE NOTICE 'Tables created: companies, license_types, licenses, license_activations, license_validations, license_usage, license_revocations, api_keys, audit_logs';
    RAISE NOTICE 'Views created: active_licenses_summary, license_usage_stats, expiring_licenses';
    RAISE NOTICE 'Functions created: update_updated_at_column, check_license_expiration, create_audit_log, get_license_by_activation_code, record_license_validation, revoke_license';
END $$;
