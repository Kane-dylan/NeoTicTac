#!/usr/bin/env python3
"""
Test server startup directly
"""
import sys
import os
sys.path.append('.')

try:
    print("Testing import...")
    from app import create_app
    print("✅ Import successful")
    
    print("Creating app...")
    app = create_app()
    print("✅ App created")
    
    print("Testing database connection...")
    with app.app_context():
        from app.models.user import User
        from app.models.game import Game
        print("✅ Models imported")
        
    print("🎉 Server startup test successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
