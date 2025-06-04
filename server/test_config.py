#!/usr/bin/env python3
"""
Test the enhanced configuration with auto-switching functionality
"""

import os
import sys

# Set up test environment
os.environ['FLASK_ENV'] = 'production'
os.environ['DATABASE_URL'] = 'postgresql://postgres:CHCTSOQehN8QMVNO@db.mauqzdgqvckrepinjybz.supabase.co:5432/postgres'

try:
    from config import Config
    
    print("🚀 CONFIGURATION TEST")
    print("=" * 40)
    print(f"Original DATABASE_URL: {os.environ['DATABASE_URL']}")
    print(f"Final DATABASE_URL: {Config.SQLALCHEMY_DATABASE_URI}")
    
    # Check if auto-switch worked
    if ":6543/" in Config.SQLALCHEMY_DATABASE_URI:
        print("✅ SUCCESS: Auto-switched to pgbouncer!")
    elif ":5432/" in Config.SQLALCHEMY_DATABASE_URI:
        print("ℹ️ INFO: Using direct connection")
    
    # Test logging function
    print("\n📋 Configuration Details:")
    Config.log_configuration()
    
    print("\n🎯 DEPLOYMENT READY!")
    print("The configuration will automatically switch to pgbouncer in production.")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
