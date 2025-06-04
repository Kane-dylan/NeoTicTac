#!/usr/bin/env python3
"""
Test script to verify that config import is working correctly
"""

def test_config_import():
    """Test that config.Config can be imported successfully"""
    try:
        print("Testing config import...")
        import config
        print("✓ Config module imported successfully")
        
        # Check if Config class exists
        if hasattr(config, 'Config'):
            print("✓ Config class found")
            
            # Test accessing Config attributes without env vars
            Config = config.Config
            print(f"✓ Config.SECRET_KEY: {'SET' if Config.SECRET_KEY else 'NOT SET'}")
            print(f"✓ Config.JWT_SECRET_KEY: {'SET' if Config.JWT_SECRET_KEY else 'NOT SET'}")
            print(f"✓ Config.CLIENT_URL: {Config.CLIENT_URL}")
            
            # Test validation method
            try:
                Config.validate_config()
                print("✓ Configuration validation passed")
            except ValueError as e:
                print(f"⚠ Configuration validation failed (expected without env vars): {e}")
                
            print("✓ All import tests passed!")
            return True
        else:
            print("✗ Config class not found")
            return False
            
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_app_import():
    """Test that app can be imported successfully"""
    try:
        print("\nTesting app import...")
        from app import create_app
        print("✓ App import successful")
        return True
    except Exception as e:
        print(f"✗ App import failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Config Import Test ===")
    
    config_ok = test_config_import()
    app_ok = test_app_import()
    
    if config_ok and app_ok:
        print("\n🎉 All tests passed! The import error should be resolved.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
