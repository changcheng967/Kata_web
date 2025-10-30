"""
DouEssay v10.0.0 - License Management REST API
Provides secure REST endpoints for license generation, validation, and management.
Integrates with Supabase database for persistent storage.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import os
import hmac
import hashlib
from datetime import datetime
from typing import Optional, Dict
import json

# Database integration (using supabase-py)
try:
    from supabase import create_client, Client
except ImportError:
    print("Warning: supabase-py not installed. Install with: pip install supabase")
    Client = None

from license_generator import LicenseGenerator, LicenseManager


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Configuration
API_SECRET_KEY = os.getenv('LICENSE_API_SECRET', 'change-this-secret-key-in-production')
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your-supabase-anon-key')
PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH', 'private_key.pem')
PUBLIC_KEY_PATH = os.getenv('PUBLIC_KEY_PATH', 'public_key.pem')

# Initialize Supabase client
supabase: Optional[Client] = None
if Client:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        print("Warning: Could not connect to Supabase")

# Initialize license generator
license_generator = LicenseGenerator(PRIVATE_KEY_PATH, PUBLIC_KEY_PATH)
license_manager = LicenseManager(license_generator)


# =====================================================================
# AUTHENTICATION MIDDLEWARE
# =====================================================================

def require_api_key(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        # Validate API key against database or secret
        if not validate_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def validate_api_key(api_key: str) -> bool:
    """Validate API key against database or configuration."""
    # In production, validate against database
    if supabase:
        try:
            response = supabase.table('api_keys').select('*').eq('api_key', api_key).eq('is_active', True).execute()
            if response.data and len(response.data) > 0:
                # Update last_used_at
                supabase.table('api_keys').update({'last_used_at': datetime.utcnow().isoformat()}).eq('api_key', api_key).execute()
                return True
        except:
            pass
    
    # Fallback to static key for development
    return api_key == API_SECRET_KEY


def get_client_info():
    """Extract client information from request."""
    return {
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'timestamp': datetime.utcnow().isoformat()
    }


# =====================================================================
# LICENSE GENERATION ENDPOINTS
# =====================================================================

@app.route('/api/v1/license/generate', methods=['POST'])
@require_api_key
def generate_license():
    """
    Generate a new license key.
    
    Request body:
    {
        "company_name": "Acme Corp",
        "email": "admin@acme.com",
        "license_type": "PROFESSIONAL",
        "max_users": 50,
        "expiration_days": 365,
        "hardware_binding": true,
        "custom_features": ["feature1", "feature2"],
        "metadata": {"contract_id": "CTR-001"}
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_name', 'email', 'license_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if company exists, create if not
        company_id = None
        if supabase:
            # Check existing company
            company_response = supabase.table('companies').select('*').eq('email', data['email']).execute()
            
            if company_response.data and len(company_response.data) > 0:
                company_id = company_response.data[0]['id']
            else:
                # Create new company
                company_data = {
                    'company_name': data['company_name'],
                    'email': data['email'],
                    'phone': data.get('phone'),
                    'country': data.get('country'),
                    'contact_person': data.get('contact_person')
                }
                company_insert = supabase.table('companies').insert(company_data).execute()
                company_id = company_insert.data[0]['id']
        
        # Generate license
        license_data = license_generator.generate_license_key(
            company_name=data['company_name'],
            email=data['email'],
            license_type=data['license_type'],
            max_users=data.get('max_users', 10),
            expiration_days=data.get('expiration_days', 365),
            hardware_binding=data.get('hardware_binding', True),
            custom_features=data.get('custom_features'),
            metadata=data.get('metadata')
        )
        
        # Store in database
        if supabase and company_id:
            # Get license type ID
            license_type_response = supabase.table('license_types').select('id').eq('type_name', data['license_type']).execute()
            license_type_id = license_type_response.data[0]['id'] if license_type_response.data else None
            
            if license_type_id:
                # Parse license to get details
                import base64
                license_bytes = base64.b64decode(license_data['license_key'])
                license_json = json.loads(license_bytes.decode('utf-8'))
                
                db_license = {
                    'license_id': license_data['license_id'],
                    'company_id': company_id,
                    'license_type_id': license_type_id,
                    'license_key': license_data['license_key'],
                    'signature': license_data['signature'],
                    'activation_code': license_data['activation_code'],
                    'max_users': data.get('max_users', 10),
                    'hardware_id': license_json.get('hardware_id'),
                    'custom_features': json.dumps(data.get('custom_features', [])),
                    'metadata': json.dumps(data.get('metadata', {})),
                    'status': 'active',
                    'issue_date': license_json['issue_date'],
                    'expiration_date': license_json.get('expiration_date'),
                    'created_by': request.headers.get('X-User-ID', 'api')
                }
                
                supabase.table('licenses').insert(db_license).execute()
        
        return jsonify({
            'success': True,
            'license': license_data,
            'message': 'License generated successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/license/validate', methods=['POST'])
def validate_license():
    """
    Validate a license key.
    
    Request body:
    {
        "license_key": "base64-encoded-key",
        "signature": "base64-encoded-signature",
        "check_hardware": true
    }
    """
    try:
        data = request.get_json()
        
        if 'license_key' not in data or 'signature' not in data:
            return jsonify({'error': 'Missing license_key or signature'}), 400
        
        # Validate license
        check_hardware = data.get('check_hardware', True)
        is_valid, license_data, error = license_manager.validate_and_cache(
            data['license_key'],
            data['signature'],
            check_hardware=check_hardware
        )
        
        # Log validation attempt
        client_info = get_client_info()
        if supabase and license_data:
            try:
                # Get license ID from database
                license_response = supabase.table('licenses').select('id').eq('license_id', license_data['license_id']).execute()
                if license_response.data:
                    db_license_id = license_response.data[0]['id']
                    
                    # Record validation
                    validation_record = {
                        'license_id': db_license_id,
                        'validation_result': is_valid,
                        'error_message': error,
                        'hardware_id': license_data.get('hardware_id'),
                        'ip_address': client_info['ip_address'],
                        'user_agent': client_info['user_agent']
                    }
                    supabase.table('license_validations').insert(validation_record).execute()
            except:
                pass  # Don't fail validation if logging fails
        
        if is_valid:
            # Calculate remaining days
            remaining_days = license_manager.get_remaining_days(license_data)
            
            return jsonify({
                'valid': True,
                'license_info': {
                    'company_name': license_data['company_name'],
                    'license_type': license_data['license_type'],
                    'max_users': license_data['max_users'],
                    'features': license_data['features'],
                    'expiration_date': license_data.get('expiration_date'),
                    'remaining_days': remaining_days,
                    'is_perpetual': license_data.get('expiration_date') is None
                }
            }), 200
        else:
            return jsonify({
                'valid': False,
                'error': error
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/license/info', methods=['POST'])
def get_license_info():
    """
    Get license information without full validation.
    
    Request body:
    {
        "license_key": "base64-encoded-key",
        "signature": "base64-encoded-signature"
    }
    """
    try:
        data = request.get_json()
        
        if 'license_key' not in data or 'signature' not in data:
            return jsonify({'error': 'Missing license_key or signature'}), 400
        
        info = license_generator.get_license_info(data['license_key'], data['signature'])
        
        if info:
            return jsonify({
                'success': True,
                'info': info
            }), 200
        else:
            return jsonify({'error': 'Could not parse license'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/license/activate', methods=['POST'])
def activate_license():
    """
    Activate a license on a specific machine.
    
    Request body:
    {
        "activation_code": "XXXX-XXXX-XXXX-XXXX-XXXX",
        "machine_name": "WORKSTATION-01",
        "os_info": "Windows 11"
    }
    """
    try:
        data = request.get_json()
        
        if 'activation_code' not in data:
            return jsonify({'error': 'Missing activation_code'}), 400
        
        # Get license from database
        if not supabase:
            return jsonify({'error': 'Database not configured'}), 500
        
        license_response = supabase.table('licenses').select('*').eq('activation_code', data['activation_code']).execute()
        
        if not license_response.data or len(license_response.data) == 0:
            return jsonify({'error': 'Invalid activation code'}), 404
        
        license_record = license_response.data[0]
        
        # Check if license is active
        if license_record['status'] != 'active':
            return jsonify({'error': f'License is {license_record["status"]}'}), 400
        
        # Get hardware ID
        hardware_id = license_generator.get_hardware_id()
        
        # Record activation
        client_info = get_client_info()
        activation_record = {
            'license_id': license_record['id'],
            'hardware_id': hardware_id,
            'machine_name': data.get('machine_name'),
            'os_info': data.get('os_info'),
            'ip_address': client_info['ip_address'],
            'user_agent': client_info['user_agent'],
            'activation_status': 'success'
        }
        
        supabase.table('license_activations').insert(activation_record).execute()
        
        return jsonify({
            'success': True,
            'license_key': license_record['license_key'],
            'signature': license_record['signature'],
            'message': 'License activated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================================
# LICENSE MANAGEMENT ENDPOINTS
# =====================================================================

@app.route('/api/v1/license/revoke', methods=['POST'])
@require_api_key
def revoke_license():
    """
    Revoke a license.
    
    Request body:
    {
        "license_id": "uuid",
        "reason": "Payment failed",
        "notes": "Additional notes"
    }
    """
    try:
        data = request.get_json()
        
        if 'license_id' not in data or 'reason' not in data:
            return jsonify({'error': 'Missing license_id or reason'}), 400
        
        if not supabase:
            return jsonify({'error': 'Database not configured'}), 500
        
        # Call revoke function
        revoked_by = request.headers.get('X-User-ID', 'api')
        
        result = supabase.rpc('revoke_license', {
            'p_license_id': data['license_id'],
            'p_revoked_by': revoked_by,
            'p_reason': data['reason'],
            'p_notes': data.get('notes')
        }).execute()
        
        return jsonify({
            'success': True,
            'message': 'License revoked successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/licenses', methods=['GET'])
@require_api_key
def list_licenses():
    """
    List all licenses with optional filtering.
    
    Query parameters:
    - status: Filter by status (active, expired, revoked, suspended)
    - company_name: Filter by company name
    - license_type: Filter by license type
    - limit: Number of results (default 50, max 100)
    - offset: Pagination offset
    """
    try:
        if not supabase:
            return jsonify({'error': 'Database not configured'}), 500
        
        # Build query
        query = supabase.table('active_licenses_summary').select('*')
        
        # Apply filters
        status = request.args.get('status')
        if status:
            query = query.eq('status', status)
        
        company_name = request.args.get('company_name')
        if company_name:
            query = query.ilike('company_name', f'%{company_name}%')
        
        license_type = request.args.get('license_type')
        if license_type:
            query = query.eq('license_type', license_type)
        
        # Pagination
        limit = min(int(request.args.get('limit', 50)), 100)
        offset = int(request.args.get('offset', 0))
        
        query = query.range(offset, offset + limit - 1)
        
        response = query.execute()
        
        return jsonify({
            'success': True,
            'licenses': response.data,
            'count': len(response.data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/license/<license_id>/usage', methods=['GET'])
@require_api_key
def get_license_usage(license_id):
    """Get usage statistics for a specific license."""
    try:
        if not supabase:
            return jsonify({'error': 'Database not configured'}), 500
        
        # Get usage stats
        usage_response = supabase.table('license_usage_stats').select('*').eq('license_id', license_id).execute()
        
        if not usage_response.data:
            return jsonify({'error': 'License not found'}), 404
        
        return jsonify({
            'success': True,
            'usage': usage_response.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================================
# HEALTH CHECK AND INFO ENDPOINTS
# =====================================================================

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': license_generator.VERSION,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/v1/features', methods=['GET'])
def list_features():
    """List available license features and types."""
    return jsonify({
        'success': True,
        'version': license_generator.VERSION,
        'license_types': {
            'BASIC': {
                'features': license_generator.FEATURES['BASIC'],
                'description': 'Entry-level license for small teams'
            },
            'PROFESSIONAL': {
                'features': license_generator.FEATURES['PROFESSIONAL'],
                'description': 'Advanced features for growing businesses'
            },
            'ENTERPRISE': {
                'features': license_generator.FEATURES['ENTERPRISE'],
                'description': 'Full-featured license for large organizations'
            },
            'UNLIMITED': {
                'features': license_generator.FEATURES['UNLIMITED'],
                'description': 'Unlimited users and features'
            }
        }
    }), 200


# =====================================================================
# ERROR HANDLERS
# =====================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# =====================================================================
# MAIN
# =====================================================================

if __name__ == '__main__':
    print("="*80)
    print("DouEssay v10.0.0 - License Management API Server")
    print("="*80)
    print(f"Version: {license_generator.VERSION}")
    print(f"Database: {'Connected' if supabase else 'Not connected'}")
    print("="*80)
    print("\nAvailable endpoints:")
    print("  POST /api/v1/license/generate     - Generate new license")
    print("  POST /api/v1/license/validate     - Validate license")
    print("  POST /api/v1/license/info         - Get license info")
    print("  POST /api/v1/license/activate     - Activate license")
    print("  POST /api/v1/license/revoke       - Revoke license")
    print("  GET  /api/v1/licenses             - List licenses")
    print("  GET  /api/v1/license/<id>/usage   - Get license usage")
    print("  GET  /api/v1/health               - Health check")
    print("  GET  /api/v1/features             - List features")
    print("="*80)
    print()
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )
