"""
Database Connection Test Script
Run this to verify your Supabase connection
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def test_direct_connection():
    """Test direct psycopg2 connection"""
    print("🔍 Testing direct database connection...")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    print(f"📝 Using DATABASE_URL: {database_url[:50]}...")
    
    try:
        # Parse connection details
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Direct connection successful!")
        print(f"📊 PostgreSQL version: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Direct connection failed: {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    print("\n🔍 Testing SQLAlchemy connection...")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Create engine with specific settings
        engine = create_engine(
            database_url,
            pool_size=1,
            pool_pre_ping=True,
            connect_args={
                'connect_timeout': 10,
                'sslmode': 'require',
                'application_name': 'tictactoe-test'
            }
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ SQLAlchemy connection successful!")
            print(f"📊 PostgreSQL version: {version}")
            
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

def test_table_operations():
    """Test basic table operations"""
    print("\n🔍 Testing table operations...")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Test creating a simple table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS connection_test (
                    id SERIAL PRIMARY KEY,
                    test_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Insert test data
            conn.execute(text("""
                INSERT INTO connection_test (test_data) 
                VALUES ('Connection test successful')
            """))
            
            # Query test data
            result = conn.execute(text("SELECT * FROM connection_test LIMIT 1"))
            row = result.fetchone()
            
            if row:
                print(f"✅ Table operations successful!")
                print(f"📊 Test data: {row}")
            
            # Clean up
            conn.execute(text("DROP TABLE IF EXISTS connection_test"))
            conn.commit()
            
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Table operations failed: {e}")
        return False

def main():
    print("🚀 Starting database connection tests...\n")
    
    # Check environment variables
    required_vars = ['DATABASE_URL', 'SECRET_KEY', 'JWT_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file or environment variable configuration")
        return False
    
    print("✅ All required environment variables found")
    
    # Run tests
    tests = [
        ("Direct Connection", test_direct_connection),
        ("SQLAlchemy Connection", test_sqlalchemy_connection),
        ("Table Operations", test_table_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your database connection is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check your database configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
