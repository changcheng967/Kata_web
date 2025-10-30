# DouEssay v10.0.0 License System - Quick Start Guide

Get up and running with the license system in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### 1. Install Dependencies

```bash
pip install cryptography flask flask-cors supabase
```

### 2. Generate RSA Keys

```bash
cd /home/runner/work/Kata_web/Kata_web
python license_generator.py
```

This creates:
- `private_key.pem` - **Keep this SECRET!**
- `public_key.pem` - Can be distributed

## Basic Usage

### Generate a License

```python
from license_generator import LicenseGenerator, LicenseManager

# Initialize
generator = LicenseGenerator()
manager = LicenseManager(generator)

# Generate a professional license
license = generator.generate_license_key(
    company_name="Your Company",
    email="admin@company.com",
    license_type="PROFESSIONAL",
    max_users=50,
    expiration_days=365,
    hardware_binding=True
)

print(f"Activation Code: {license['activation_code']}")
```

### Validate a License

```python
# Validate the license
is_valid, info, error = manager.validate_and_cache(
    license['license_key'],
    license['signature']
)

if is_valid:
    print(f"✓ License valid for {info['company_name']}")
    print(f"  Features: {', '.join(info['features'])}")
else:
    print(f"✗ License invalid: {error}")
```

## Run Examples

```bash
python license_example.py
```

This will run 10 comprehensive examples showing all features.

## Start API Server

### 1. Set Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and set your values
nano .env
```

### 2. Start the Server

```bash
python license_api.py
```

The API will be available at `http://localhost:5000`

## Test API Endpoints

### Generate License

```bash
curl -X POST http://localhost:5000/api/v1/license/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-this-in-production" \
  -d '{
    "company_name": "Test Company",
    "email": "test@company.com",
    "license_type": "PROFESSIONAL",
    "max_users": 50,
    "expiration_days": 365
  }'
```

### Validate License

```bash
curl -X POST http://localhost:5000/api/v1/license/validate \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "YOUR_LICENSE_KEY",
    "signature": "YOUR_SIGNATURE"
  }'
```

## Setup Database (Optional)

1. Create a Supabase account at https://supabase.com
2. Create a new project
3. Run the SQL schema: `supabase_schema.sql`
4. Update `.env` with your Supabase credentials

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

## License Types

| Type | Max Users | Features | Price/Year |
|------|-----------|----------|------------|
| BASIC | 5 | Core features, Standard support | $999 |
| PROFESSIONAL | 50 | + Analytics, Priority support, API | $4,999 |
| ENTERPRISE | 500 | + White-label, Integrations, SLA | $19,999 |
| UNLIMITED | ∞ | All features, Custom development | $49,999 |

## Security Features

✓ **RSA-4096** - Military-grade encryption  
✓ **Hardware Binding** - Prevent license cloning  
✓ **HMAC Verification** - Tamper-proof integrity  
✓ **Offline Validation** - No internet required  
✓ **Audit Logging** - Complete activity trail  
✓ **Revocation Support** - Instant license deactivation  

## Next Steps

- Read the full documentation: [LICENSE_SYSTEM_README.md](LICENSE_SYSTEM_README.md)
- Review security best practices
- Set up production environment
- Configure Supabase database
- Implement email notifications
- Deploy to production

## Support

- GitHub Issues: [Create an issue](https://github.com/changcheng967/Kata_web/issues)
- Documentation: `LICENSE_SYSTEM_README.md`
- Examples: `license_example.py`

## Important Security Notes

⚠️ **NEVER** commit `private_key.pem` to version control  
⚠️ Store private keys in secure vault (AWS KMS, Azure Key Vault)  
⚠️ Change default API keys in production  
⚠️ Use HTTPS in production  
⚠️ Enable rate limiting in production  

---

**Ready to generate secure licenses!** 🎉
