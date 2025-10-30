# DouEssay v10.0.0 - Enterprise License Key Generator

## 🔐 Ultra-Secure License Management System

A comprehensive, enterprise-grade license key generation and validation system with cryptographic signatures, hardware binding, and tamper-proof mechanisms.

---

## 🌟 Features

### Security Features
- **RSA-4096 Cryptographic Signatures** - Tamper-proof license keys with public-key cryptography
- **Hardware Binding** - Locks licenses to specific machines using MAC address, CPU ID, and motherboard serial
- **HMAC Integrity Verification** - Double-layer security with SHA-512 HMAC checksums
- **Anti-Cloning Protection** - Hardware fingerprinting prevents license duplication
- **Cryptographic Random Generation** - Uses `secrets` module for secure key generation
- **Offline Validation** - Can validate licenses without internet connection using public key
- **Signature Verification** - PSS padding with SHA-512 for maximum security

### License Management Features
- **Multiple License Tiers** - Basic, Professional, Enterprise, and Unlimited
- **Feature Flags System** - Granular control over enabled features
- **Time-Based Expiration** - Support for trial, annual, and perpetual licenses
- **Grace Period Support** - Configurable grace periods after expiration
- **License Revocation** - Instant license deactivation with audit trail
- **Activation Codes** - Human-readable codes for easy license activation
- **Concurrent User Tracking** - Monitor and enforce user limits
- **Usage Analytics** - Track feature utilization and validation attempts

### Database Features
- **Supabase Integration** - Cloud-hosted PostgreSQL database
- **Row-Level Security** - Built-in RLS policies for multi-tenant isolation
- **Audit Logging** - Complete audit trail of all operations
- **Automated Expiration** - Scheduled checks for expired licenses
- **Usage Statistics** - Real-time dashboards and reporting views
- **API Key Management** - Secure API access control

### API Features
- **RESTful API** - Clean, well-documented REST endpoints
- **CORS Support** - Cross-origin resource sharing enabled
- **Rate Limiting** - Configurable rate limits per API key
- **Comprehensive Error Handling** - Detailed error messages
- **Health Checks** - Monitor system status
- **Batch Operations** - Generate multiple licenses efficiently

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [Database Setup](#database-setup)
5. [API Documentation](#api-documentation)
6. [Security Best Practices](#security-best-practices)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12+ or Supabase account
- pip package manager

### Install Dependencies

```bash
pip install cryptography flask flask-cors supabase
```

### Generate RSA Keys

```bash
python license_generator.py
```

This will generate:
- `private_key.pem` - Keep this SECRET and secure
- `public_key.pem` - Can be distributed with your application

---

## ⚡ Quick Start

### 1. Generate a License

```python
from license_generator import LicenseGenerator, LicenseManager

# Initialize
generator = LicenseGenerator('private_key.pem', 'public_key.pem')
manager = LicenseManager(generator)

# Generate professional license
license_data = generator.generate_license_key(
    company_name="Acme Corporation",
    email="admin@acme.com",
    license_type="PROFESSIONAL",
    max_users=50,
    expiration_days=365,
    hardware_binding=True
)

print(f"Activation Code: {license_data['activation_code']}")
print(f"License Key: {license_data['license_key'][:50]}...")
```

### 2. Validate a License

```python
# Validate the license
is_valid, license_info, error = manager.validate_and_cache(
    license_data['license_key'],
    license_data['signature']
)

if is_valid:
    print(f"✓ License valid for {license_info['company_name']}")
    print(f"  Features: {', '.join(license_info['features'])}")
else:
    print(f"✗ License invalid: {error}")
```

### 3. Start the API Server

```bash
# Set environment variables
export LICENSE_API_SECRET="your-secret-key"
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-supabase-anon-key"

# Run the API server
python license_api.py
```

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     License Generation                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 1. Collect company info & license parameters         │  │
│  │ 2. Generate unique license ID (UUID)                 │  │
│  │ 3. Get hardware fingerprint (MAC, CPU, MB serial)    │  │
│  │ 4. Create license payload with features & metadata   │  │
│  │ 5. Generate HMAC-SHA512 for integrity                │  │
│  │ 6. Sign with RSA-4096 private key                    │  │
│  │ 7. Base64 encode license & signature                 │  │
│  │ 8. Generate human-readable activation code           │  │
│  │ 9. Store in Supabase database                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     License Validation                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 1. Decode Base64 license key & signature             │  │
│  │ 2. Verify RSA signature with public key              │  │
│  │ 3. Parse JSON license data                           │  │
│  │ 4. Verify HMAC integrity                             │  │
│  │ 5. Check revocation status                           │  │
│  │ 6. Verify version compatibility                      │  │
│  │ 7. Check expiration date                             │  │
│  │ 8. Validate hardware binding                         │  │
│  │ 9. Log validation attempt to database                │  │
│  │ 10. Return validation result                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      Data Flow                               │
│                                                               │
│  Client App  ◄──►  REST API  ◄──►  License Manager          │
│                         │                                     │
│                         │                                     │
│                         ▼                                     │
│                   Supabase DB                                 │
│                  (PostgreSQL)                                 │
│                         │                                     │
│              ┌──────────┴──────────┐                         │
│              ▼                     ▼                          │
│          Licenses              Audit Logs                     │
│          Companies             Validations                    │
│          Activations           Usage Stats                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Database Setup

### 1. Create Supabase Project

1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Note your project URL and API keys

### 2. Run SQL Schema

Execute the SQL schema file in Supabase SQL Editor:

```bash
# Copy the contents of supabase_schema.sql
# Paste into Supabase SQL Editor
# Execute
```

The schema creates:
- **9 tables**: companies, license_types, licenses, license_activations, license_validations, license_usage, license_revocations, api_keys, audit_logs
- **3 views**: active_licenses_summary, license_usage_stats, expiring_licenses
- **6 functions**: update_updated_at_column, check_license_expiration, create_audit_log, get_license_by_activation_code, record_license_validation, revoke_license
- **RLS policies**: Row-level security for multi-tenant isolation

### 3. Configure Connection

```python
# In your application
import os
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

---

## 📚 API Documentation

### Authentication

All API endpoints (except validation and info) require an API key:

```bash
curl -H "X-API-Key: your-api-key" https://api.example.com/api/v1/license/generate
```

### Endpoints

#### Generate License

**POST** `/api/v1/license/generate`

Request:
```json
{
  "company_name": "Acme Corporation",
  "email": "admin@acme.com",
  "license_type": "PROFESSIONAL",
  "max_users": 50,
  "expiration_days": 365,
  "hardware_binding": true,
  "custom_features": ["custom_feature_1"],
  "metadata": {
    "contract_id": "CTR-001",
    "sales_rep": "John Doe"
  }
}
```

Response:
```json
{
  "success": true,
  "license": {
    "license_key": "eyJ...",
    "signature": "gR8...",
    "activation_code": "A1B2-C3D4-E5F6-G7H8-I9J0",
    "license_id": "550e8400-e29b-41d4-a716-446655440000",
    "company_name": "Acme Corporation",
    "license_type": "PROFESSIONAL",
    "expiration_date": "2026-10-30T21:17:41.562Z",
    "hardware_bound": true
  },
  "message": "License generated successfully"
}
```

#### Validate License

**POST** `/api/v1/license/validate`

Request:
```json
{
  "license_key": "eyJ...",
  "signature": "gR8...",
  "check_hardware": true
}
```

Response:
```json
{
  "valid": true,
  "license_info": {
    "company_name": "Acme Corporation",
    "license_type": "PROFESSIONAL",
    "max_users": 50,
    "features": ["core_features", "advanced_analytics", "priority_support", "api_access"],
    "expiration_date": "2026-10-30T21:17:41.562Z",
    "remaining_days": 365,
    "is_perpetual": false
  }
}
```

#### Activate License

**POST** `/api/v1/license/activate`

Request:
```json
{
  "activation_code": "A1B2-C3D4-E5F6-G7H8-I9J0",
  "machine_name": "WORKSTATION-01",
  "os_info": "Windows 11 Pro"
}
```

Response:
```json
{
  "success": true,
  "license_key": "eyJ...",
  "signature": "gR8...",
  "message": "License activated successfully"
}
```

#### Revoke License

**POST** `/api/v1/license/revoke`

Request:
```json
{
  "license_id": "550e8400-e29b-41d4-a716-446655440000",
  "reason": "Payment failed",
  "notes": "Customer account suspended"
}
```

Response:
```json
{
  "success": true,
  "message": "License revoked successfully"
}
```

#### List Licenses

**GET** `/api/v1/licenses?status=active&limit=50&offset=0`

Response:
```json
{
  "success": true,
  "licenses": [
    {
      "license_id": "550e8400-e29b-41d4-a716-446655440000",
      "company_name": "Acme Corporation",
      "license_type": "PROFESSIONAL",
      "status": "active",
      "time_remaining": "365 days"
    }
  ],
  "count": 1
}
```

#### Get License Usage

**GET** `/api/v1/license/{license_id}/usage`

Response:
```json
{
  "success": true,
  "usage": {
    "license_id": "550e8400-e29b-41d4-a716-446655440000",
    "company_name": "Acme Corporation",
    "total_validations": 1500,
    "successful_validations": 1498,
    "last_validated": "2025-10-30T21:17:41.562Z",
    "activation_count": 3,
    "peak_concurrent_users": 45
  }
}
```

---

## 🔒 Security Best Practices

### Key Management

1. **Private Key Security**
   - Store private key in secure key vault (AWS KMS, Azure Key Vault, HashiCorp Vault)
   - Never commit private key to version control
   - Use environment variables or secure configuration management
   - Rotate keys periodically (annually recommended)
   - Implement key backup and disaster recovery

2. **Public Key Distribution**
   - Embed public key in client application
   - Consider code obfuscation for additional protection
   - Use certificate pinning if distributing over network

### API Security

1. **API Key Management**
   - Generate cryptographically random API keys
   - Store hashed versions in database (bcrypt/argon2)
   - Implement rate limiting (1000 requests/hour default)
   - Use HTTPS for all API communication
   - Implement IP whitelisting for sensitive operations

2. **Input Validation**
   - Validate all input parameters
   - Sanitize user inputs to prevent injection attacks
   - Implement request size limits
   - Use parameterized queries for database operations

### License Protection

1. **Hardware Binding**
   - Enable hardware binding for commercial licenses
   - Collect multiple hardware identifiers for robustness
   - Allow hardware change process for legitimate upgrades

2. **Anti-Tampering**
   - All licenses signed with RSA-4096
   - HMAC verification prevents modification
   - Validate signature before processing any license data
   - Implement certificate pinning in client

3. **Offline Validation**
   - Client can validate licenses without internet
   - Periodic online checks (daily/weekly) recommended
   - Implement grace period for temporary offline scenarios

### Monitoring and Auditing

1. **Audit Logging**
   - Log all license generations, validations, and revocations
   - Include IP address, timestamp, and user agent
   - Implement log retention policies
   - Set up alerts for suspicious activity

2. **Usage Monitoring**
   - Track validation attempts and patterns
   - Monitor for unusual activation patterns
   - Implement anomaly detection for license abuse
   - Generate regular compliance reports

---

## 💡 Examples

### Example 1: Trial License Generation

```python
from license_generator import LicenseGenerator, LicenseManager

generator = LicenseGenerator()
manager = LicenseManager(generator)

# Generate 30-day trial
trial = manager.create_trial_license(
    company_name="Potential Customer Inc",
    email="trial@customer.com",
    trial_days=30
)

print(f"Trial Activation Code: {trial['activation_code']}")
```

### Example 2: Commercial License with Custom Features

```python
# Generate enterprise license with custom features
license = generator.generate_license_key(
    company_name="Global Enterprises Ltd",
    email="licensing@globalent.com",
    license_type="ENTERPRISE",
    max_users=500,
    expiration_days=0,  # Perpetual
    hardware_binding=True,
    custom_features=[
        "custom_reporting",
        "white_label_enabled",
        "api_unlimited"
    ],
    metadata={
        "contract_id": "ENT-2025-001",
        "support_tier": "platinum",
        "account_manager": "Jane Smith"
    }
)
```

### Example 3: Feature Access Check

```python
# Validate and check specific feature access
is_valid, license_data, error = manager.validate_and_cache(
    license_key,
    signature
)

if is_valid:
    # Check if specific feature is available
    has_api_access = manager.check_feature_access(
        license_data,
        'api_access'
    )
    
    if has_api_access:
        print("✓ API access enabled")
    else:
        print("✗ API access not available in this license")
```

### Example 4: License Activation in Client App

```python
import requests

# Client application activating license
def activate_license(activation_code):
    response = requests.post(
        'https://api.example.com/api/v1/license/activate',
        json={
            'activation_code': activation_code,
            'machine_name': os.environ.get('COMPUTERNAME'),
            'os_info': platform.platform()
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        # Save license key and signature locally
        save_license_locally(
            data['license_key'],
            data['signature']
        )
        return True
    return False
```

### Example 5: Periodic Validation Check

```python
import time
from datetime import datetime, timedelta

class LicenseValidator:
    def __init__(self, generator):
        self.generator = generator
        self.last_check = None
        self.check_interval = timedelta(hours=24)
    
    def should_check(self):
        if not self.last_check:
            return True
        return datetime.now() - self.last_check > self.check_interval
    
    def validate_with_cache(self, license_key, signature):
        # Use cached validation if recent
        if not self.should_check() and self.cached_valid:
            return True, self.cached_data, None
        
        # Perform validation
        is_valid, data, error = self.generator.validate_license(
            license_key,
            signature
        )
        
        if is_valid:
            self.last_check = datetime.now()
            self.cached_valid = True
            self.cached_data = data
        
        return is_valid, data, error
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Invalid signature" error

**Cause**: License has been modified or wrong public key is being used.

**Solution**:
- Ensure you're using the correct public key that matches the private key used for generation
- Verify the license key and signature haven't been truncated or modified
- Check that Base64 encoding/decoding is working correctly

#### 2. "Hardware ID mismatch" error

**Cause**: License is hardware-bound and being used on a different machine.

**Solution**:
- Verify the license is being used on the originally activated machine
- If hardware was legitimately upgraded, contact support for license transfer
- Consider disabling hardware binding for licenses that need flexibility

#### 3. Database connection failed

**Cause**: Supabase credentials incorrect or network issues.

**Solution**:
```python
# Verify connection
try:
    response = supabase.table('companies').select('count').execute()
    print("✓ Database connected")
except Exception as e:
    print(f"✗ Database error: {e}")
```

#### 4. API key authentication failed

**Cause**: Invalid or expired API key.

**Solution**:
- Check API key is correctly set in request headers
- Verify API key exists and is active in database
- Check rate limits haven't been exceeded

### Debug Mode

Enable debug logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Run with debug mode
if __name__ == '__main__':
    app.run(debug=True)
```

### Testing License System

```python
# Test license generation and validation
def test_license_system():
    generator = LicenseGenerator()
    
    # Generate test license
    license = generator.generate_license_key(
        company_name="Test Company",
        email="test@test.com",
        license_type="BASIC",
        max_users=5,
        expiration_days=30,
        hardware_binding=False  # Disable for testing
    )
    
    # Validate immediately
    is_valid, data, error = generator.validate_license(
        license['license_key'],
        license['signature'],
        check_hardware=False
    )
    
    assert is_valid, f"Validation failed: {error}"
    print("✓ License system test passed")

test_license_system()
```

---

## 📊 Performance Considerations

### Optimization Tips

1. **Caching**
   - Cache license validation results (default: 1 hour)
   - Use Redis for distributed caching in production
   - Implement cache invalidation on license updates

2. **Database Indexing**
   - All foreign keys are indexed
   - Create additional indexes for frequent queries
   - Use database query analyzer to optimize slow queries

3. **Rate Limiting**
   - Implement rate limiting at API gateway level
   - Use token bucket algorithm for smooth rate limiting
   - Set different limits for different license tiers

4. **Batch Operations**
   - Generate multiple licenses in single transaction
   - Bulk validation for enterprise scenarios
   - Use database connection pooling

---

## 🎯 Production Deployment Checklist

- [ ] Generate production RSA keys (4096-bit)
- [ ] Store private key in secure vault
- [ ] Set up Supabase production database
- [ ] Run database schema creation
- [ ] Configure environment variables
- [ ] Set up API key authentication
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS policies
- [ ] Set up monitoring and alerting
- [ ] Implement backup and disaster recovery
- [ ] Test license generation and validation
- [ ] Set up log aggregation
- [ ] Configure rate limiting
- [ ] Implement IP whitelisting
- [ ] Create API documentation
- [ ] Train support team
- [ ] Create runbooks for common issues
- [ ] Set up automated expiration checks
- [ ] Configure email notifications
- [ ] Test revocation procedures
- [ ] Perform security audit

---

## 📞 Support

For issues or questions:
- GitHub Issues: [Create an issue](https://github.com/changcheng967/Kata_web/issues)
- Email: support@douessay.com
- Documentation: This file

---

## 📄 License

This license system is part of DouEssay v10.0.0.
See the LICENSE file for details.

---

## 🔄 Version History

- **v10.0.0** (2025-10-30)
  - Initial release
  - RSA-4096 cryptographic signatures
  - Hardware binding support
  - Supabase database integration
  - RESTful API
  - Comprehensive audit logging
  - Multiple license tiers
  - Feature flag system

---

## 🙏 Credits

Created for DouEssay v10.0.0 by the Kata_web team.

Based on industry best practices for software licensing including:
- NIST cryptographic standards
- OWASP security guidelines
- ISO 27001 information security practices
