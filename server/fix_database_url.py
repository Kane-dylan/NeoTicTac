#!/usr/bin/env python3
"""
Debug DATABASE_URL issues for Render deployment
"""
import os
from dotenv import load_dotenv

def debug_database_url():
    """Debug DATABASE_URL configuration"""
    load_dotenv()
    
    print("🔍 DATABASE_URL DEBUG")
    print("-" * 40)
    
    # Get DATABASE_URL from environment
    db_url = os.getenv('DATABASE_URL')
    print(f"Raw DATABASE_URL: {db_url}")
    
    if db_url:
        # Check for problematic parameters
        if 'pgbouncer' in db_url:
            print("❌ Found 'pgbouncer' parameter in DATABASE_URL")
            # Remove pgbouncer parameter
            clean_url = db_url.split('?')[0]  # Remove all query parameters
            print(f"✅ Cleaned URL: {clean_url}")
            
            # Write corrected URL back to .env
            with open('.env', 'r') as f:
                content = f.read()
            
            content = content.replace(db_url, clean_url)
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print("✅ Updated .env file with clean DATABASE_URL")
        else:
            print("✅ No pgbouncer parameter found")
    else:
        print("❌ DATABASE_URL not found in environment")
    
    # Test connection string format
    if db_url and db_url.startswith('postgresql://'):
        print("✅ Correct PostgreSQL format")
    elif db_url and db_url.startswith('postgres://'):
        print("⚠️ Old postgres:// format detected")
    
    print("\n🔧 RENDER CONFIGURATION NOTES:")
    print("- Render will load environment variables from the dashboard")
    print("- Make sure to set these in Render dashboard (not render.yaml)")
    print("- Use port 5432 (direct connection) instead of 6543 (pgbouncer)")

if __name__ == "__main__":
    debug_database_url()
