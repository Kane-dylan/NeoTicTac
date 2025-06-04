#!/usr/bin/env python3
"""
Migration script to transfer data from SQLite to Supabase
"""
import os
import json
import sqlite3
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_supabase_client():
    """Initialize Supabase client"""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    
    return create_client(url, key)

def extract_sqlite_data():
    """Extract data from SQLite database"""
    db_path = os.path.join('instance', 'tictactoe.db')
    if not os.path.exists(db_path):
        print(f"SQLite database not found at {db_path}")
        return None, None
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    
    # Extract users
    users = []
    cursor = conn.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        user_data = dict(row)
        # Convert datetime string to ISO format if needed
        if user_data.get('created_at'):
            try:
                # Handle different datetime formats
                dt = datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00'))
                user_data['created_at'] = dt.isoformat()
            except:
                user_data['created_at'] = datetime.utcnow().isoformat()
        users.append(user_data)
    
    # Extract games
    games = []
    cursor = conn.execute("SELECT * FROM game")
    for row in cursor.fetchall():
        game_data = dict(row)
        # Convert SQLite boolean integers to actual booleans
        if 'is_draw' in game_data:
            game_data['is_draw'] = bool(game_data['is_draw'])
        
        # Ensure board is properly formatted
        if isinstance(game_data.get('board'), str):
            try:
                # Validate JSON
                json.loads(game_data['board'])
            except:
                game_data['board'] = '["","","","","","","","",""]'
        
        # Handle datetime
        if game_data.get('created_at'):
            try:
                dt = datetime.fromisoformat(game_data['created_at'].replace('Z', '+00:00'))
                game_data['created_at'] = dt.isoformat()
            except:
                game_data['created_at'] = datetime.utcnow().isoformat()
        
        games.append(game_data)
    
    conn.close()
    return users, games

def create_supabase_tables(supabase: Client):
    """Create tables in Supabase using SQL"""
    
    # Users table
    users_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        username VARCHAR(80) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
    """
    
    # Games table
    games_sql = """
    CREATE TABLE IF NOT EXISTS game (
        id SERIAL PRIMARY KEY,
        player_x VARCHAR(80) NOT NULL,
        player_o VARCHAR(80),
        board TEXT DEFAULT '["","","","","","","","",""]',
        current_turn VARCHAR(1) DEFAULT 'X',
        winner VARCHAR(1),
        is_draw BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    
    try:
        # Execute table creation
        supabase.rpc('exec_sql', {'sql': users_sql}).execute()
        print("✓ Users table created/verified")
        
        supabase.rpc('exec_sql', {'sql': games_sql}).execute()
        print("✓ Games table created/verified")
        
    except Exception as e:
        print(f"Error creating tables via RPC. Creating via direct SQL...")
        # Alternative: Use Supabase dashboard SQL editor to run these commands
        print("Please run these SQL commands in your Supabase SQL Editor:")
        print("\n--- USERS TABLE ---")
        print(users_sql)
        print("\n--- GAMES TABLE ---")
        print(games_sql)
        raise e

def migrate_data(supabase: Client, users, games):
    """Migrate data to Supabase"""
    
    # Migrate users
    if users:
        try:
            # Clear existing data (optional - remove if you want to keep existing data)
            # supabase.table('users').delete().neq('id', 0).execute()
            
            # Insert users
            response = supabase.table('users').insert(users).execute()
            print(f"✓ Migrated {len(users)} users")
        except Exception as e:
            print(f"✗ Error migrating users: {e}")
            # Try inserting one by one to identify problematic records
            for user in users:
                try:
                    supabase.table('users').insert(user).execute()
                except Exception as user_error:
                    print(f"  ✗ Failed to insert user {user.get('username', 'unknown')}: {user_error}")
    
    # Migrate games
    if games:
        try:
            # Clear existing games (optional)
            # supabase.table('game').delete().neq('id', 0).execute()
            
            # Insert games
            response = supabase.table('game').insert(games).execute()
            print(f"✓ Migrated {len(games)} games")
        except Exception as e:
            print(f"✗ Error migrating games: {e}")
            # Try inserting one by one
            for game in games:
                try:
                    supabase.table('game').insert(game).execute()
                except Exception as game_error:
                    print(f"  ✗ Failed to insert game {game.get('id', 'unknown')}: {game_error}")

def backup_sqlite_data():
    """Backup existing SQLite data to JSON files"""
    users, games = extract_sqlite_data()
    
    if users:
        with open('migration_data/users_backup.json', 'w') as f:
            json.dump(users, f, indent=2, default=str)
        print(f"✓ Backed up {len(users)} users to migration_data/users_backup.json")
    
    if games:
        with open('migration_data/games_backup.json', 'w') as f:
            json.dump(games, f, indent=2, default=str)
        print(f"✓ Backed up {len(games)} games to migration_data/games_backup.json")
    
    return users, games

def main():
    """Main migration process"""
    print("🚀 Starting SQLite to Supabase migration...\n")
    
    try:
        # Step 1: Setup Supabase client
        print("1. Setting up Supabase connection...")
        supabase = setup_supabase_client()
        print("✓ Connected to Supabase")
        
        # Step 2: Backup and extract data
        print("\n2. Extracting and backing up SQLite data...")
        users, games = backup_sqlite_data()
        
        if not users and not games:
            print("No data found to migrate. Exiting.")
            return
        
        # Step 3: Create tables (you may need to do this manually in Supabase dashboard)
        print("\n3. Creating/verifying Supabase tables...")
        try:
            create_supabase_tables(supabase)
        except Exception as e:
            print(f"⚠️  Could not create tables automatically: {e}")
            print("Please create the tables manually in Supabase dashboard using the SQL provided above.")
            input("Press Enter after creating the tables manually...")
        
        # Step 4: Migrate data
        print("\n4. Migrating data to Supabase...")
        migrate_data(supabase, users, games)
        
        print("\n🎉 Migration completed!")
        print("\nNext steps:")
        print("1. Verify data in your Supabase dashboard")
        print("2. Test your application with the new database")
        print("3. Update your Render environment variables")
        print("4. Deploy your updated application")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("Please check your environment variables and Supabase configuration.")

if __name__ == "__main__":
    main()
