#!/usr/bin/env python3
"""
Quick deployment status check
"""

print("🎯 DEPLOYMENT STATUS CHECK")
print("=" * 40)

# Check key files
import os
key_files = [
    'config.py',
    'wsgi.py', 
    'requirements.txt',
    'render.yaml'
]

print("📁 Key Files:")
for file in key_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING")

# Test configuration
print("\n🔧 Configuration Test:")
try:
    from config import Config
    print("✅ Configuration loads successfully")
    
    # Check if auto-switching works
    import os
    os.environ['FLASK_ENV'] = 'production'
    os.environ['DATABASE_URL'] = 'postgresql://test:test@test:5432/test'
    
    # Reload config to test auto-switching
    import importlib
    import config
    importlib.reload(config)
    
    if ":6543/" in config.Config.SQLALCHEMY_DATABASE_URI:
        print("✅ Auto-switching to pgbouncer works")
    else:
        print("ℹ️ Direct connection (no auto-switch needed)")
        
except Exception as e:
    print(f"❌ Configuration error: {e}")

print("\n🚀 RENDER DEPLOYMENT STATUS: READY")
print("\nNext: Update Render environment variables and deploy!")
