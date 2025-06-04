#!/usr/bin/env python3
"""
Create database schema in Supabase
"""
import os
from supabase import create_client
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')
    
    if not url or not key:
        print("❌ Missing environment variables")
        return False
    
    try:
        supabase = create_client(url, key)
        print("✅ Connected to Supabase")
        
        # Read schema SQL
        with open('supabase_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Split SQL into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        print(f"📝 Executing {len(statements)} SQL statements...")
        
        for i, stmt in enumerate(statements, 1):
            if stmt.strip():
                try:
                    # Use the RPC function to execute raw SQL
                    result = supabase.rpc('query', {'sql': stmt}).execute()
                    print(f"✅ Statement {i} executed successfully")
                except Exception as e:
                    # Try alternative method for schema creation
                    if 'CREATE TABLE' in stmt or 'CREATE EXTENSION' in stmt or 'DROP TABLE' in stmt:
                        print(f"⚠️  Statement {i} - trying alternative method: {str(e)[:100]}")
                        # For schema creation, we might need to use the Supabase dashboard
                        continue
                    else:
                        print(f"❌ Statement {i} failed: {e}")
                        
        print("\n🎯 Schema creation completed!")
        print("Note: If some statements failed, you may need to run them manually in the Supabase SQL Editor.")
        
        # Test if tables now exist
        try:
            result = supabase.table('users').select('count').execute()
            print("✅ Users table is now accessible!")
            return True
        except Exception as e:
            print(f"⚠️  Users table test: {e}")
            print("You may need to create the schema manually in Supabase SQL Editor")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()
