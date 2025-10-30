"""
DouEssay v10.0.0 - License System Example Usage
Demonstrates how to use the license key generation and validation system.
"""

from license_generator import LicenseGenerator, LicenseManager
from license_config import config
import json


def print_section(title):
    """Print a section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def example_1_basic_license_generation(generator=None):
    """Example 1: Generate a basic license."""
    print_section("Example 1: Basic License Generation")
    
    # Initialize generator if not provided
    if generator is None:
        generator = LicenseGenerator()
    
    # Generate a basic license
    license_data = generator.generate_license_key(
        company_name="Acme Corporation",
        email="admin@acme.com",
        license_type="BASIC",
        max_users=5,
        expiration_days=30,
        hardware_binding=False  # Disable for demo
    )
    
    print("✓ License generated successfully!")
    print(f"\nCompany: {license_data['company_name']}")
    print(f"License Type: {license_data['license_type']}")
    print(f"Activation Code: {license_data['activation_code']}")
    print(f"Expiration: {license_data['expiration_date']}")
    print(f"\nLicense Key (first 80 chars): {license_data['license_key'][:80]}...")
    print(f"Signature (first 80 chars): {license_data['signature'][:80]}...")
    
    return license_data


def example_2_validate_license(license_data, generator):
    """Example 2: Validate a license."""
    print_section("Example 2: License Validation")
    
    manager = LicenseManager(generator)
    
    # Validate the license
    is_valid, license_info, error = manager.validate_and_cache(
        license_data['license_key'],
        license_data['signature']
    )
    
    if is_valid:
        print("✓ License is VALID!")
        print(f"\nCompany: {license_info['company_name']}")
        print(f"License Type: {license_info['license_type']}")
        print(f"Max Users: {license_info['max_users']}")
        print(f"Features: {', '.join(license_info['features'])}")
        
        remaining_days = manager.get_remaining_days(license_info)
        if remaining_days is not None:
            print(f"Days Remaining: {remaining_days}")
        else:
            print("License Type: Perpetual")
    else:
        print(f"✗ License is INVALID!")
        print(f"Error: {error}")
    
    return is_valid


def example_3_professional_license():
    """Example 3: Generate a professional license with custom features."""
    print_section("Example 3: Professional License with Custom Features")
    
    generator = LicenseGenerator()
    
    license_data = generator.generate_license_key(
        company_name="Tech Innovations Inc",
        email="admin@techinnovations.com",
        license_type="PROFESSIONAL",
        max_users=50,
        expiration_days=365,
        hardware_binding=True,
        custom_features=["custom_reporting", "api_v2_access"],
        metadata={
            "contract_id": "CTR-2025-001",
            "sales_rep": "John Doe",
            "purchase_order": "PO-12345"
        }
    )
    
    print("✓ Professional license generated!")
    print(f"\nActivation Code: {license_data['activation_code']}")
    print(f"Company: {license_data['company_name']}")
    print(f"Type: {license_data['license_type']}")
    print(f"Hardware Bound: {license_data['hardware_bound']}")
    print(f"Max Users: 50")
    print(f"Valid for: 1 year")
    
    return license_data


def example_4_enterprise_perpetual():
    """Example 4: Generate an enterprise perpetual license."""
    print_section("Example 4: Enterprise Perpetual License")
    
    generator = LicenseGenerator()
    
    license_data = generator.generate_license_key(
        company_name="Global Enterprises Ltd",
        email="licensing@globalent.com",
        license_type="ENTERPRISE",
        max_users=500,
        expiration_days=0,  # Perpetual - never expires
        hardware_binding=True,
        metadata={
            "contract_id": "ENT-2025-001",
            "support_tier": "platinum",
            "account_manager": "Jane Smith"
        }
    )
    
    print("✓ Enterprise perpetual license generated!")
    print(f"\nActivation Code: {license_data['activation_code']}")
    print(f"Company: {license_data['company_name']}")
    print(f"Type: {license_data['license_type']}")
    print(f"Expiration: {license_data['expiration_date']}")
    print(f"Max Users: 500")
    
    return license_data


def example_5_feature_check():
    """Example 5: Check specific feature access."""
    print_section("Example 5: Feature Access Check")
    
    generator = LicenseGenerator()
    manager = LicenseManager(generator)
    
    # Generate a professional license
    license_data = generator.generate_license_key(
        company_name="Test Company",
        email="test@test.com",
        license_type="PROFESSIONAL",
        max_users=25,
        expiration_days=365,
        hardware_binding=False
    )
    
    # Validate license
    is_valid, license_info, error = manager.validate_and_cache(
        license_data['license_key'],
        license_data['signature']
    )
    
    if is_valid:
        print("License validated successfully!")
        print("\nFeature Access Check:")
        
        features_to_check = [
            'core_features',
            'advanced_analytics',
            'api_access',
            'white_label',
            'custom_development'
        ]
        
        for feature in features_to_check:
            has_access = manager.check_feature_access(license_info, feature)
            status = "✓ ENABLED" if has_access else "✗ DISABLED"
            print(f"  {feature:25s} - {status}")


def example_6_trial_license():
    """Example 6: Generate a trial license."""
    print_section("Example 6: Trial License")
    
    generator = LicenseGenerator()
    manager = LicenseManager(generator)
    
    # Generate trial license
    trial_license = manager.create_trial_license(
        company_name="Potential Customer Inc",
        email="trial@customer.com",
        trial_days=30
    )
    
    print("✓ Trial license generated!")
    print(f"\nActivation Code: {trial_license['activation_code']}")
    print(f"Company: {trial_license['company_name']}")
    print(f"Type: {trial_license['license_type']}")
    print(f"Duration: 30 days")
    print(f"Max Users: 5")
    print(f"Hardware Bound: No")
    
    return trial_license


def example_7_get_license_info():
    """Example 7: Get license information without full validation."""
    print_section("Example 7: Get License Information")
    
    generator = LicenseGenerator()
    
    # Generate a license
    license_data = generator.generate_license_key(
        company_name="Info Test Company",
        email="info@test.com",
        license_type="ENTERPRISE",
        max_users=100,
        expiration_days=365,
        hardware_binding=True
    )
    
    # Get license info without full validation
    info = generator.get_license_info(
        license_data['license_key'],
        license_data['signature']
    )
    
    if info:
        print("✓ License information extracted!")
        print(f"\nLicense ID: {info['license_id']}")
        print(f"Company: {info['company_name']}")
        print(f"Type: {info['license_type']}")
        print(f"Max Users: {info['max_users']}")
        print(f"Hardware Bound: {info['hardware_bound']}")
        print(f"Issue Date: {info['issue_date']}")
        print(f"Expiration: {info['expiration_date']}")
        print(f"\nFeatures ({len(info['features'])} total):")
        for feature in info['features'][:5]:
            print(f"  • {feature}")
        if len(info['features']) > 5:
            print(f"  ... and {len(info['features']) - 5} more")


def example_8_save_and_load_keys():
    """Example 8: Save and load RSA keys."""
    print_section("Example 8: Save and Load RSA Keys")
    
    # Generate new keys
    generator = LicenseGenerator()
    
    print("✓ New RSA-4096 keys generated")
    
    # Save keys
    generator.save_keys('demo_private_key.pem', 'demo_public_key.pem')
    print("✓ Keys saved to demo_private_key.pem and demo_public_key.pem")
    
    # Load keys
    generator2 = LicenseGenerator('demo_private_key.pem', 'demo_public_key.pem')
    print("✓ Keys loaded from files")
    
    # Test that loaded keys work
    test_license = generator2.generate_license_key(
        company_name="Key Test Co",
        email="test@keytest.com",
        license_type="BASIC",
        max_users=5,
        expiration_days=30,
        hardware_binding=False
    )
    
    is_valid, _, _ = generator2.validate_license(
        test_license['license_key'],
        test_license['signature'],
        check_hardware=False
    )
    
    if is_valid:
        print("✓ License generated and validated with loaded keys!")
    else:
        print("✗ Key loading verification failed")
    
    # Clean up demo keys
    import os
    try:
        os.remove('demo_private_key.pem')
        os.remove('demo_public_key.pem')
        print("✓ Demo keys cleaned up")
    except:
        pass


def example_9_hardware_fingerprint():
    """Example 9: Get hardware fingerprint."""
    print_section("Example 9: Hardware Fingerprint")
    
    hardware_id = LicenseGenerator.get_hardware_id()
    
    print("Current Hardware Fingerprint:")
    print(f"  {hardware_id}")
    print("\nThis fingerprint is used for hardware-bound licenses.")
    print("It's a SHA-256 hash of system identifiers like:")
    print("  • MAC address")
    print("  • CPU serial number")
    print("  • Motherboard serial number")


def example_10_activation_code_verification():
    """Example 10: Verify activation code."""
    print_section("Example 10: Activation Code Verification")
    
    generator = LicenseGenerator()
    
    # Generate a license
    license_data = generator.generate_license_key(
        company_name="Activation Test Inc",
        email="test@activation.com",
        license_type="PROFESSIONAL",
        max_users=10,
        expiration_days=365,
        hardware_binding=False
    )
    
    activation_code = license_data['activation_code']
    license_id = license_data['license_id']
    company_name = license_data['company_name']
    
    print(f"Generated Activation Code: {activation_code}")
    
    # Verify correct activation code
    is_valid = generator.verify_activation_code(
        activation_code,
        license_id,
        company_name
    )
    
    print(f"\nVerification with correct code: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    # Test with incorrect code
    wrong_code = "AAAA-BBBB-CCCC-DDDD-EEEE"
    is_valid = generator.verify_activation_code(
        wrong_code,
        license_id,
        company_name
    )
    
    print(f"Verification with wrong code: {'✓ VALID' if is_valid else '✗ INVALID (expected)'}")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print(" "*20 + "DouEssay v10.0.0 License System Examples")
    print("="*80)
    
    try:
        # Initialize a shared generator for examples that need to share keys
        shared_generator = LicenseGenerator()
        
        # Run examples
        license1 = example_1_basic_license_generation(shared_generator)
        # Pass the same generator to validate the license created in example 1
        example_2_validate_license(license1, shared_generator)
        example_3_professional_license()
        example_4_enterprise_perpetual()
        example_5_feature_check()
        example_6_trial_license()
        example_7_get_license_info()
        example_8_save_and_load_keys()
        example_9_hardware_fingerprint()
        example_10_activation_code_verification()
        
        print("\n" + "="*80)
        print(" "*25 + "All examples completed successfully!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
