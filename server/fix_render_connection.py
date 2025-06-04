#!/usr/bin/env python3
"""
Fix Render-to-Supabase Connection Issues
This script provides multiple connection string options and tests them.
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

# Your Supabase credentials
SUPABASE_HOST = "db.mauqzdgqvckrepinjybz.supabase.co"
SUPABASE_PASSWORD = "CHCTSOQehN8QMVNO"
SUPABASE_USER = "postgres"
SUPABASE_DB = "postgres"

def test_connection(connection_string, description):
    """Test a database connection string"""
    print(f"\n🔍 Testing: {description}")
    print(f"📡 Connection: {connection_string}")
    
    try:
        # Parse the connection string
        parsed = urlparse(connection_string)
        
        # Connect using psycopg2
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/'),
            user=parsed.username,
            password=parsed.password
        )
        
        # Test the connection
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"✅ SUCCESS! Connected to PostgreSQL")
        print(f"📋 Version: {version[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def main():
    """Test multiple connection approaches for Render deployment"""
    
    print("🚀 RENDER-SUPABASE CONNECTION FIXER")
    print("=" * 50)
    
    # Connection string options for Render
    connection_options = [
        {
            "name": "Direct Connection (Port 5432)",
            "url": f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:5432/{SUPABASE_DB}"
        },
        {
            "name": "Pgbouncer Connection (Port 6543)",
            "url": f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:6543/{SUPABASE_DB}"
        },
        {
            "name": "Pgbouncer with SSL (Port 6543)",
            "url": f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:6543/{SUPABASE_DB}?sslmode=require"
        },
        {
            "name": "Direct with SSL (Port 5432)",
            "url": f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:5432/{SUPABASE_DB}?sslmode=require"
        },
        {
            "name": "Pgbouncer Pool Mode Transaction",
            "url": f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:6543/{SUPABASE_DB}?pgbouncer=true&pool_mode=transaction"
        }
    ]
    
    working_connections = []
    
    for option in connection_options:
        if test_connection(option["url"], option["name"]):
            working_connections.append(option)
    
    print("\n" + "=" * 50)
    print("📊 CONNECTION TEST RESULTS")
    print("=" * 50)
    
    if working_connections:
        print(f"✅ Found {len(working_connections)} working connection(s)!")
        print("\n🎯 RECOMMENDED FOR RENDER:")
        
        # Prefer pgbouncer for production
        pgbouncer_connections = [c for c in working_connections if "6543" in c["url"]]
        if pgbouncer_connections:
            best_connection = pgbouncer_connections[0]
        else:
            best_connection = working_connections[0]
        
        print(f"📋 Connection Name: {best_connection['name']}")
        print(f"🔗 DATABASE_URL: {best_connection['url']}")
        
        print("\n📝 RENDER DEPLOYMENT STEPS:")
        print("1. Go to: https://dashboard.render.com")
        print("2. Select your 'tictactoe-backend' service")
        print("3. Click 'Environment' tab")
        print(f"4. Set DATABASE_URL = {best_connection['url']}")
        print("5. Save and redeploy")
        
        # Generate environment file
        env_content = f"""# Render Environment Variables
SECRET_KEY=6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9
JWT_SECRET_KEY=c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177
SUPABASE_URL=https://mauqzdgqvckrepinjybz.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hdXF6ZGdxdmNrcmVwaW5qeWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODg4NjUyMCwiZXhwIjoyMDY0NDYyNTIwfQ.VWqomYXkBiVZQfxuoKMkcpZfllDkhvGLzcrDz1FZDpk
DATABASE_URL={best_connection['url']}
FLASK_ENV=production
CLIENT_URL=https://tic-tac-toe-ten-murex-86.vercel.app
"""
        
        with open('render_environment.txt', 'w') as f:
            f.write(env_content)
        
        print(f"\n💾 Environment variables saved to: render_environment.txt")
        
    else:
        print("❌ No working connections found!")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Check if Supabase credentials are correct")
        print("2. Verify network connectivity")
        print("3. Check Supabase project status")
        print("4. Try connecting from a different network")

if __name__ == "__main__":
    main()
