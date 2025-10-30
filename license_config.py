"""
DouEssay v10.0.0 - License System Configuration
Centralized configuration for the license key system.
"""

import os
from typing import Dict, List


class LicenseConfig:
    """Configuration settings for the license system."""
    
    # Version
    VERSION = "10.0.0"
    
    # Cryptographic settings
    RSA_KEY_SIZE = 4096
    RSA_PUBLIC_EXPONENT = 65537
    HMAC_ALGORITHM = 'sha512'
    SIGNATURE_ALGORITHM = 'sha512'
    
    # Key file paths
    PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH', 'private_key.pem')
    PUBLIC_KEY_PATH = os.getenv('PUBLIC_KEY_PATH', 'public_key.pem')
    MASTER_SECRET = os.getenv('MASTER_SECRET', None)  # Set in production
    
    # Database configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your-supabase-anon-key')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'your-service-role-key')
    
    # API configuration
    API_SECRET_KEY = os.getenv('LICENSE_API_SECRET', 'change-this-in-production')
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_DEBUG = os.getenv('API_DEBUG', 'False').lower() == 'true'
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_PER_HOUR = int(os.getenv('RATE_LIMIT_PER_HOUR', 1000))
    
    # License validation
    VALIDATION_CACHE_TTL = int(os.getenv('VALIDATION_CACHE_TTL', 3600))  # 1 hour
    GRACE_PERIOD_DAYS = int(os.getenv('GRACE_PERIOD_DAYS', 7))
    REQUIRE_ONLINE_CHECK = os.getenv('REQUIRE_ONLINE_CHECK', 'False').lower() == 'true'
    ONLINE_CHECK_INTERVAL_DAYS = int(os.getenv('ONLINE_CHECK_INTERVAL_DAYS', 7))
    
    # Hardware binding
    HARDWARE_BINDING_STRICT = os.getenv('HARDWARE_BINDING_STRICT', 'True').lower() == 'true'
    ALLOW_HARDWARE_TRANSFER = os.getenv('ALLOW_HARDWARE_TRANSFER', 'True').lower() == 'true'
    MAX_HARDWARE_TRANSFERS = int(os.getenv('MAX_HARDWARE_TRANSFERS', 3))
    
    # License types and features
    LICENSE_TYPES: Dict[str, Dict] = {
        'BASIC': {
            'display_name': 'Basic License',
            'features': ['core_features', 'standard_support'],
            'max_users_default': 5,
            'price_yearly': 999.00,
            'price_monthly': 99.00,
            'description': 'Entry-level license for small teams'
        },
        'PROFESSIONAL': {
            'display_name': 'Professional License',
            'features': ['core_features', 'advanced_analytics', 'priority_support', 'api_access'],
            'max_users_default': 50,
            'price_yearly': 4999.00,
            'price_monthly': 499.00,
            'description': 'Advanced features for growing businesses'
        },
        'ENTERPRISE': {
            'display_name': 'Enterprise License',
            'features': [
                'core_features', 'advanced_analytics', 'priority_support', 
                'api_access', 'white_label', 'custom_integrations', 
                'dedicated_support', 'sla_99_9'
            ],
            'max_users_default': 500,
            'price_yearly': 19999.00,
            'price_monthly': 1999.00,
            'description': 'Full-featured license for large organizations'
        },
        'UNLIMITED': {
            'display_name': 'Unlimited License',
            'features': ['all_features', 'unlimited_users', 'premium_support', 'custom_development'],
            'max_users_default': -1,  # Unlimited
            'price_yearly': 49999.00,
            'price_monthly': 4999.00,
            'description': 'Unlimited users and features'
        }
    }
    
    # Feature descriptions
    FEATURE_DESCRIPTIONS: Dict[str, str] = {
        'core_features': 'Access to all core application features',
        'standard_support': 'Email support with 48-hour response time',
        'advanced_analytics': 'Advanced analytics and reporting dashboards',
        'priority_support': 'Priority email and chat support with 4-hour response',
        'api_access': 'Full REST API access for integrations',
        'white_label': 'White-label branding options',
        'custom_integrations': 'Custom integration development support',
        'dedicated_support': 'Dedicated support representative',
        'sla_99_9': '99.9% uptime SLA guarantee',
        'all_features': 'Access to all current and future features',
        'unlimited_users': 'Unlimited concurrent users',
        'premium_support': '24/7 premium support with 1-hour response',
        'custom_development': 'Custom feature development included'
    }
    
    # Trial license defaults
    TRIAL_DURATION_DAYS = int(os.getenv('TRIAL_DURATION_DAYS', 30))
    TRIAL_MAX_USERS = int(os.getenv('TRIAL_MAX_USERS', 5))
    TRIAL_LICENSE_TYPE = 'BASIC'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'license_system.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Email notifications (optional)
    EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_FROM = os.getenv('SMTP_FROM', 'noreply@douessay.com')
    
    # Notification settings
    NOTIFY_EXPIRING_DAYS = [30, 14, 7, 3, 1]  # Days before expiration to send notifications
    NOTIFY_ON_GENERATION = os.getenv('NOTIFY_ON_GENERATION', 'True').lower() == 'true'
    NOTIFY_ON_REVOCATION = os.getenv('NOTIFY_ON_REVOCATION', 'True').lower() == 'true'
    
    # Security settings
    REQUIRE_HTTPS = os.getenv('REQUIRE_HTTPS', 'True').lower() == 'true'
    ALLOWED_IP_RANGES: List[str] = os.getenv('ALLOWED_IP_RANGES', '').split(',') if os.getenv('ALLOWED_IP_RANGES') else []
    BLOCK_VPN = os.getenv('BLOCK_VPN', 'False').lower() == 'true'
    
    # Monitoring and analytics
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'True').lower() == 'true'
    METRICS_PORT = int(os.getenv('METRICS_PORT', 9090))
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """
        Validate configuration and return list of warnings/errors.
        
        Returns:
            List of validation messages
        """
        messages = []
        
        # Check critical settings
        if cls.MASTER_SECRET is None or len(cls.MASTER_SECRET) < 32:
            messages.append("WARNING: MASTER_SECRET not set or too short. Use a secure random string in production.")
        
        if cls.API_SECRET_KEY == 'change-this-in-production':
            messages.append("WARNING: API_SECRET_KEY is set to default value. Change it in production.")
        
        if cls.SUPABASE_URL == 'https://your-project.supabase.co':
            messages.append("WARNING: SUPABASE_URL not configured. Database features will not work.")
        
        if cls.SUPABASE_KEY == 'your-supabase-anon-key':
            messages.append("WARNING: SUPABASE_KEY not configured. Database features will not work.")
        
        if not os.path.exists(cls.PRIVATE_KEY_PATH):
            messages.append(f"WARNING: Private key not found at {cls.PRIVATE_KEY_PATH}. Generate keys first.")
        
        if not os.path.exists(cls.PUBLIC_KEY_PATH):
            messages.append(f"WARNING: Public key not found at {cls.PUBLIC_KEY_PATH}. Generate keys first.")
        
        if cls.API_DEBUG and cls.REQUIRE_HTTPS:
            messages.append("INFO: Debug mode enabled. HTTPS requirement relaxed for development.")
        
        return messages
    
    @classmethod
    def print_config(cls):
        """Print current configuration (safe - no secrets)."""
        print("="*80)
        print("License System Configuration")
        print("="*80)
        print(f"Version: {cls.VERSION}")
        print(f"RSA Key Size: {cls.RSA_KEY_SIZE}")
        print(f"API Host: {cls.API_HOST}:{cls.API_PORT}")
        print(f"Debug Mode: {cls.API_DEBUG}")
        print(f"Database: {'Configured' if cls.SUPABASE_URL != 'https://your-project.supabase.co' else 'Not configured'}")
        print(f"Rate Limiting: {'Enabled' if cls.RATE_LIMIT_ENABLED else 'Disabled'} ({cls.RATE_LIMIT_PER_HOUR}/hour)")
        print(f"Cache TTL: {cls.VALIDATION_CACHE_TTL}s")
        print(f"Hardware Binding: {'Strict' if cls.HARDWARE_BINDING_STRICT else 'Flexible'}")
        print(f"Email Notifications: {'Enabled' if cls.EMAIL_ENABLED else 'Disabled'}")
        print(f"Metrics: {'Enabled' if cls.ENABLE_METRICS else 'Disabled'}")
        print("="*80)
        
        # Print validation messages
        messages = cls.validate_config()
        if messages:
            print("\nConfiguration Warnings:")
            for msg in messages:
                print(f"  • {msg}")
            print()
    
    @classmethod
    def get_license_type_config(cls, license_type: str) -> Dict:
        """Get configuration for a specific license type."""
        return cls.LICENSE_TYPES.get(license_type, cls.LICENSE_TYPES['BASIC'])
    
    @classmethod
    def get_feature_description(cls, feature: str) -> str:
        """Get description for a specific feature."""
        return cls.FEATURE_DESCRIPTIONS.get(feature, 'No description available')


# Environment-specific configurations
class DevelopmentConfig(LicenseConfig):
    """Development environment configuration."""
    API_DEBUG = True
    REQUIRE_HTTPS = False
    RATE_LIMIT_ENABLED = False
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(LicenseConfig):
    """Production environment configuration."""
    API_DEBUG = False
    REQUIRE_HTTPS = True
    RATE_LIMIT_ENABLED = True
    HARDWARE_BINDING_STRICT = True
    LOG_LEVEL = 'INFO'


class TestingConfig(LicenseConfig):
    """Testing environment configuration."""
    API_DEBUG = True
    REQUIRE_HTTPS = False
    RATE_LIMIT_ENABLED = False
    HARDWARE_BINDING_STRICT = False
    LOG_LEVEL = 'DEBUG'
    VALIDATION_CACHE_TTL = 0  # No caching in tests


# Get configuration based on environment
def get_config():
    """Get configuration based on ENVIRONMENT variable."""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig


# Export current config
config = get_config()


if __name__ == '__main__':
    # Print configuration when run directly
    config.print_config()
    
    # Print license types
    print("\nAvailable License Types:")
    for type_name, type_config in config.LICENSE_TYPES.items():
        print(f"\n  {type_name} - {type_config['display_name']}")
        print(f"    {type_config['description']}")
        print(f"    Max Users: {type_config['max_users_default']}")
        print(f"    Price: ${type_config['price_yearly']}/year or ${type_config['price_monthly']}/month")
        print(f"    Features: {', '.join(type_config['features'][:3])}...")
