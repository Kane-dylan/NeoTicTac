"""
Database Inspection Script
Check what tables and columns exist in the database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from sqlalchemy import create_engine, text, inspect
import traceback

def inspect_database():
    """Inspect the current database structure"""
    print("🔍 Inspecting database structure...")
    
    try:
        database_url = os.getenv('DATABASE_URL')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        # Get all table names
        tables = inspector.get_table_names()
        print(f"📊 Found {len(tables)} tables: {tables}")
        
        # Inspect each table
        for table_name in tables:
            print(f"\n🔧 Table: {table_name}")
            columns = inspector.get_columns(table_name)
            
            for column in columns:
                print(f"  - {column['name']}: {column['type']} {'(Primary Key)' if column.get('primary_key') else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database inspection failed: {e}")
        print(traceback.format_exc())
        return False

def test_direct_query():
    """Test direct SQL queries"""
    print("\n🧪 Testing direct SQL queries...")
    
    try:
        database_url = os.getenv('DATABASE_URL')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Database version: {version}")
            
            # Check if tables exist
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ Tables in public schema: {tables}")
            
            # If users table exists, check its structure
            if 'users' in tables:
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'users'
                    ORDER BY ordinal_position
                """))
                
                print("\n👤 Users table structure:")
                for row in result.fetchall():
                    print(f"  - {row[0]}: {row[1]} ({'NULL' if row[2] == 'YES' else 'NOT NULL'})")
            
            # If games/game table exists, check its structure
            for game_table in ['game', 'games']:
                if game_table in tables:
                    result = conn.execute(text(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns 
                        WHERE table_name = '{game_table}'
                        ORDER BY ordinal_position
                    """))
                    
                    print(f"\n🎮 {game_table} table structure:")
                    for row in result.fetchall():
                        print(f"  - {row[0]}: {row[1]} ({'NULL' if row[2] == 'YES' else 'NOT NULL'})")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct query test failed: {e}")
        print(traceback.format_exc())
        return False

def main():
    """Main inspection function"""
    print("🚀 Starting database inspection...")
    print("="*50)
    
    if not inspect_database():
        return False
    
    if not test_direct_query():
        return False
    
    print("\n" + "="*50)
    print("✅ Database inspection completed!")
    print("="*50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
