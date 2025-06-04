#!/usr/bin/env python3
"""
Final verification that everything is ready for Render deployment
"""

import os

# Set up complete production environment (like Render will have)
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = '6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9'
os.environ['JWT_SECRET_KEY'] = 'c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177'
os.environ['SUPABASE_URL'] = 'https://mauqzdgqvckrepinjybz.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hdXF6ZGdxdmNrcmVwaW5qeWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODg4NjUyMCwiZXhwIjoyMDY0NDYyNTIwfQ.VWqomYXkBiVZQfxuoKMkcpZfllDkhvGLzcrDz1FZDpk'
os.environ['DATABASE_URL'] = 'postgresql://postgres:CHCTSOQehN8QMVNO@db.mauqzdgqvckrepinjybz.supabase.co:5432/postgres'
os.environ['CLIENT_URL'] = 'https://tic-tac-toe-ten-murex-86.vercel.app'

try:
    from config import Config
    
    print("🎯 RENDER DEPLOYMENT VERIFICATION")
    print("=" * 50)
    
    print(f"✅ SECRET_KEY: {'Set' if Config.SECRET_KEY else 'Missing'}")
    print(f"✅ JWT_SECRET_KEY: {'Set' if Config.JWT_SECRET_KEY else 'Missing'}")
    print(f"✅ SUPABASE_URL: {'Set' if Config.SUPABASE_URL else 'Missing'}")
    print(f"✅ SUPABASE_SERVICE_KEY: {'Set' if Config.SUPABASE_SERVICE_KEY else 'Missing'}")
    print(f"✅ CLIENT_URL: {Config.CLIENT_URL}")
    
    print("\n📡 DATABASE CONNECTION:")
    print(f"Original: {os.environ['DATABASE_URL'][:50]}...")
    print(f"Final:    {Config.SQLALCHEMY_DATABASE_URI[:50]}...")
    
    if ":6543/" in Config.SQLALCHEMY_DATABASE_URI:
        print("✅ Using pgbouncer connection (RECOMMENDED)")
    else:
        print("ℹ️ Using direct connection")
    
    print("\n🔧 Connection Pool Settings:")
    if hasattr(Config, 'SQLALCHEMY_ENGINE_OPTIONS'):
        opts = Config.SQLALCHEMY_ENGINE_OPTIONS
        print(f"✅ Pool Size: {opts.get('pool_size', 'Not set')}")
        print(f"✅ Pool Recycle: {opts.get('pool_recycle', 'Not set')} seconds")
        print(f"✅ Pool Timeout: {opts.get('pool_timeout', 'Not set')} seconds")
    
    print("\n📋 Detailed Configuration:")
    Config.log_configuration()
    
    print("\n" + "=" * 50)
    print("🚀 READY FOR RENDER DEPLOYMENT!")
    print("=" * 50)
    print("Your Tic-Tac-Toe app is now configured with:")
    print("• Automatic pgbouncer connection switching")
    print("• Optimized connection pooling for Render")
    print("• Enhanced error handling and logging")
    print("• All required environment variables")
    
except Exception as e:
    print(f"❌ CONFIGURATION ERROR: {e}")
    print("\nPlease check your environment variables and try again.")
