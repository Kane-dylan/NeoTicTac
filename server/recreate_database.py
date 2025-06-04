"""
Direct Database Cleanup and Recreate
This will forcefully clean the database and recreate it
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables  
load_dotenv()

def get_db_connection():
    """Get direct database connection"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found")
    
    # Parse the database URL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return psycopg2.connect(database_url)

def force_drop_all_tables():
    """Force drop all tables using direct SQL"""
    print("🗑️ Force dropping all tables...")
    
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Get all tables
        cur.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        
        tables = [row[0] for row in cur.fetchall()]
        print(f"Found tables to drop: {tables}")
        
        # Drop all tables with CASCADE
        for table in tables:
            print(f"Dropping table: {table}")
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
        
        # Also drop any sequences that might exist
        cur.execute("""
            SELECT sequence_name 
            FROM information_schema.sequences 
            WHERE sequence_schema = 'public'
        """)
        
        sequences = [row[0] for row in cur.fetchall()]
        for seq in sequences:
            print(f"Dropping sequence: {seq}")
            cur.execute(f"DROP SEQUENCE IF EXISTS {seq} CASCADE")
        
        cur.close()
        conn.close()
        
        print("✅ All tables and sequences dropped successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        return False

def create_users_table():
    """Create users table with correct schema"""
    print("👤 Creating users table...")
    
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE users (
                id BIGSERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                last_login TIMESTAMP NULL
            )
        """)
        
        # Create index on username
        cur.execute("CREATE INDEX idx_users_username ON users(username)")
        
        cur.close()
        conn.close()
        
        print("✅ Users table created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating users table: {e}")
        return False

def create_game_table():
    """Create game table with correct schema"""
    print("🎮 Creating game table...")
    
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE game (
                id SERIAL PRIMARY KEY,
                player_x VARCHAR(80) NOT NULL,
                player_o VARCHAR(80) NULL,
                board TEXT DEFAULT '["","","","","","","","",""]' NOT NULL,
                current_turn VARCHAR(1) DEFAULT 'X' NOT NULL,
                winner VARCHAR(1) NULL,
                is_draw BOOLEAN DEFAULT FALSE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            )
        """)
        
        cur.close()
        conn.close()
        
        print("✅ Game table created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating game table: {e}")
        return False

def test_tables():
    """Test that tables work correctly"""
    print("🧪 Testing tables...")
    
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Test users table
        cur.execute("""
            INSERT INTO users (username, password_hash) 
            VALUES ('test_user', 'test_hash')
        """)
        
        cur.execute("SELECT id, username FROM users WHERE username = 'test_user'")
        user_result = cur.fetchone()
        
        if user_result:
            print(f"✅ Users table test passed: {user_result}")
            user_id = user_result[0]
            
            # Clean up test user
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        else:
            print("❌ Users table test failed")
            return False
        
        # Test game table
        cur.execute("""
            INSERT INTO game (player_x) 
            VALUES ('test_player')
        """)
        
        cur.execute("SELECT id, player_x FROM game WHERE player_x = 'test_player'")
        game_result = cur.fetchone()
        
        if game_result:
            print(f"✅ Game table test passed: {game_result}")
            game_id = game_result[0]
            
            # Clean up test game
            cur.execute("DELETE FROM game WHERE id = %s", (game_id,))
        else:
            print("❌ Game table test failed")
            return False
        
        cur.close()
        conn.close()
        
        print("✅ All table tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Table test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting direct database cleanup and recreate...")
    print("="*50)
    
    try:
        # Step 1: Force drop all tables
        if not force_drop_all_tables():
            return False
        
        # Step 2: Create users table
        if not create_users_table():
            return False
        
        # Step 3: Create game table
        if not create_game_table():
            return False
        
        # Step 4: Test tables
        if not test_tables():
            return False
        
        print("\n" + "="*50)
        print("🎉 DATABASE RECREATED SUCCESSFULLY!")
        print("✅ Users table: username, password_hash")
        print("✅ Game table: player_x, player_o")
        print("✅ All tests passed")
        print("🚀 Ready for server testing!")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Database recreate failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
