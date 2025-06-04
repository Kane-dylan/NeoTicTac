#!/usr/bin/env python3
"""
Test script to check for startup issues
"""

def test_app_startup():
    """Test app startup to identify any remaining issues"""
    try:
        print("Testing app import...")
        from app import create_app, db
        print("✓ App modules imported successfully")
        
        print("Testing app creation...")
        app = create_app()
        print("✓ App created successfully")
        
        print("Testing routes import...")
        with app.app_context():
            from app.routes.user import bp as user_bp
            from app.routes.auth import bp as auth_bp
            from app.routes.game import bp as game_bp
            print("✓ All route blueprints imported successfully")
        
        print("✅ All startup tests passed!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        print(f"   File: {e.filename}")
        print(f"   Line: {e.lineno}")
        print(f"   Text: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Import/Startup Error: {e}")
        return False

if __name__ == "__main__":
    print("=== App Startup Test ===")
    test_app_startup()
