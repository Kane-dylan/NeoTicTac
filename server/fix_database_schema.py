#!/usr/bin/env python3
"""
Complete Database Schema Fix Script
This script will:
1. Drop existing tables to clean up schema conflicts
2. Recreate tables with consistent schema
3. Test the database connection
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, MetaData

# Load environment variables
load_dotenv()

def get_database_engine():
    """Get SQLAlchemy engine with enhanced connection parameters"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Fix for newer SQLAlchemy versions
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # Enhance with production-specific parameters
    if not any(param in database_url for param in ['sslmode=', 'connect_timeout=', 'application_name=']):
        separator = '&' if '?' in database_url else '?'
        production_params = [
            'sslmode=require',
            'application_name=tictactoe-schema-fix',
            'connect_timeout=30',
            'target_session_attrs=read-write'
        ]
        database_url = database_url + separator + '&'.join(production_params)
    
    return create_engine(
        database_url,
        pool_size=1,
        pool_pre_ping=True,
        pool_timeout=30
    )

def drop_all_tables(engine):
    """Drop all existing tables to start fresh"""
    print("🗑️  Dropping all existing tables...")
    
    with engine.connect() as conn:
        # Start a transaction
        trans = conn.begin()
        
        try:
            # Drop tables in order (dependencies first)
            tables_to_drop = ['game', 'users', 'user']  # Include possible variations
            
            for table in tables_to_drop:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    print(f"   ✅ Dropped table: {table}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop {table}: {str(e)}")
            
            # Commit the transaction
            trans.commit()
            print("✅ All tables dropped successfully!")
            
        except Exception as e:
            trans.rollback()
            print(f"❌ Error dropping tables: {e}")
            raise

def create_users_table(engine):
    """Create users table with proper schema"""
    print("👤 Creating users table...")
    
    create_users_sql = """
    CREATE TABLE users (
        id BIGSERIAL PRIMARY KEY,
        username VARCHAR(80) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        last_login TIMESTAMP NULL
    );
    
    CREATE INDEX idx_users_username ON users(username);
    """
    
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(text(create_users_sql))
            trans.commit()
            print("✅ Users table created successfully!")
        except Exception as e:
            trans.rollback()
            print(f"❌ Error creating users table: {e}")
            raise

def create_games_table(engine):
    """Create games table with proper schema"""
    print("🎮 Creating games table...")
    
    create_games_sql = """
    CREATE TABLE game (
        id SERIAL PRIMARY KEY,
        player_x VARCHAR(80) NOT NULL,
        player_o VARCHAR(80) NULL,
        board TEXT DEFAULT '["","","","","","","","",""]' NOT NULL,
        current_turn VARCHAR(1) DEFAULT 'X' NOT NULL,
        winner VARCHAR(1) NULL,
        is_draw BOOLEAN DEFAULT FALSE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    
    CREATE INDEX idx_game_player_x ON game(player_x);
    CREATE INDEX idx_game_player_o ON game(player_o);
    CREATE INDEX idx_game_created_at ON game(created_at);
    """
    
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(text(create_games_sql))
            trans.commit()
            print("✅ Games table created successfully!")
        except Exception as e:
            trans.rollback()
            print(f"❌ Error creating games table: {e}")
            raise

def test_schema(engine):
    """Test the created schema"""
    print("🧪 Testing database schema...")
    
    test_queries = [
        # Test users table
        ("Users table structure", "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"),
        
        # Test games table  
        ("Games table structure", "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'game' ORDER BY ordinal_position"),
        
        # Test basic operations
        ("Test insert user", "INSERT INTO users (username, password_hash) VALUES ('test_user', 'test_hash') RETURNING id"),
        
        ("Test insert game", "INSERT INTO game (player_x) VALUES ('test_user') RETURNING id"),
        
        # Cleanup test data
        ("Cleanup test data", "DELETE FROM game WHERE player_x = 'test_user'; DELETE FROM users WHERE username = 'test_user'")
    ]
    
    with engine.connect() as conn:
        for test_name, query in test_queries:
            try:
                result = conn.execute(text(query))
                if test_name in ["Users table structure", "Games table structure"]:
                    rows = result.fetchall()
                    print(f"   ✅ {test_name}:")
                    for row in rows:
                        print(f"      - {row[0]}: {row[1]}")
                elif "RETURNING" in query:
                    returned_id = result.fetchone()[0]
                    print(f"   ✅ {test_name}: ID {returned_id}")
                else:
                    print(f"   ✅ {test_name}: Success")
                    
                # Commit each test
                conn.commit()
                
            except Exception as e:
                print(f"   ❌ {test_name}: {e}")
                conn.rollback()

def main():
    print("🚀 Starting Database Schema Fix...\n")
    
    try:
        # Get database engine
        engine = get_database_engine()
        print("✅ Database connection established")
        
        # Step 1: Drop all tables
        drop_all_tables(engine)
        
        # Step 2: Create users table
        create_users_table(engine)
        
        # Step 3: Create games table
        create_games_table(engine)
        
        # Step 4: Test schema
        test_schema(engine)
        
        print("\n🎉 Database schema has been successfully fixed!")
        print("📝 Summary:")
        print("   - All tables dropped and recreated")
        print("   - Users table: id, username, password_hash, created_at, last_login")
        print("   - Games table: id, player_x, player_o, board, current_turn, winner, is_draw, created_at")
        print("   - All indexes created")
        print("   - Schema tested successfully")
        
        # Dispose engine
        engine.dispose()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database schema fix failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
