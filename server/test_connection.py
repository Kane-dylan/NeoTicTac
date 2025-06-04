#!/usr/bin/env python3
"""
Test Supabase connection and setup
"""
import os
import sys
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')
    
    print("=== Supabase Connection Test ===")
    print(f"SUPABASE_URL: {url}")
    print(f"SUPABASE_SERVICE_KEY: {'Set' if key else 'Not set'}")
    
    if not url or not key:
        print("❌ Missing environment variables")
        return False
    
    try:
        from supabase import create_client
        print("✅ Supabase package imported successfully")
        
        # Create client
        supabase = create_client(url, key)
        print("✅ Supabase client created successfully")
        
        # Test connection
        try:
            result = supabase.table('users').select('id').limit(1).execute()
            print("✅ Database connection successful!")
            print(f"Users table exists and is accessible")
            return True
        except Exception as e:
            error_msg = str(e)
            if 'relation "users" does not exist' in error_msg:
                print("⚠️  Users table doesn't exist - need to create schema")
                return "schema_needed"
            else:
                print(f"❌ Database query error: {e}")
                return False
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1)
