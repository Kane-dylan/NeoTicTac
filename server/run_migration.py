#!/usr/bin/env python3
"""
Complete Supabase Migration Process
This script will:
1. Check existing SQLite data
2. Provide schema setup instructions
3. Run data migration when schema is ready
"""
import os
import json
import sqlite3
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

class SupabaseMigration:
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        self.supabase = None
        
    def check_connection(self):
        """Check Supabase connection"""
        if not self.supabase_url or not self.supabase_key:
            print("❌ Missing Supabase credentials in .env file")
            return False
            
        try:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            print("✅ Supabase connection established")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def check_schema(self):
        """Check if database schema exists"""
        try:
            result = self.supabase.table('users').select('count').execute()
            print("✅ Database schema exists")
            return True
        except Exception as e:
            if 'does not exist' in str(e):
                print("⚠️  Database schema not found")
                return False
            print(f"❌ Schema check failed: {e}")
            return False
    
    def extract_sqlite_data(self):
        """Extract existing data from SQLite"""
        db_path = os.path.join('instance', 'tictactoe.db')
        if not os.path.exists(db_path):
            print(f"ℹ️  No existing SQLite database found at {db_path}")
            return None, None
            
        print(f"📂 Found SQLite database: {db_path}")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Extract users
        users = []
        try:
            cursor = conn.execute("SELECT * FROM users")
            for row in cursor.fetchall():
                user_data = dict(row)
                if user_data.get('created_at'):
                    try:
                        dt = datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00'))
                        user_data['created_at'] = dt.isoformat()
                    except:
                        user_data['created_at'] = datetime.utcnow().isoformat()
                users.append(user_data)
            print(f"📊 Found {len(users)} users")
        except Exception as e:
            print(f"⚠️  Error extracting users: {e}")
        
        # Extract games
        games = []
        try:
            cursor = conn.execute("SELECT * FROM games")
            for row in cursor.fetchall():
                game_data = dict(row)
                if game_data.get('created_at'):
                    try:
                        dt = datetime.fromisoformat(game_data['created_at'].replace('Z', '+00:00'))
                        game_data['created_at'] = dt.isoformat()
                    except:
                        game_data['created_at'] = datetime.utcnow().isoformat()
                games.append(game_data)
            print(f"📊 Found {len(games)} games")
        except Exception as e:
            print(f"⚠️  Error extracting games: {e}")
        
        conn.close()
        return users, games
    
    def save_migration_data(self, users, games):
        """Save extracted data for backup"""
        os.makedirs('migration_data', exist_ok=True)
        
        if users:
            with open('migration_data/users.json', 'w') as f:
                json.dump(users, f, indent=2)
            print(f"💾 Saved {len(users)} users to migration_data/users.json")
        
        if games:
            with open('migration_data/games.json', 'w') as f:
                json.dump(games, f, indent=2)
            print(f"💾 Saved {len(games)} games to migration_data/games.json")
    
    def migrate_data(self, users, games):
        """Migrate data to Supabase"""
        if not users and not games:
            print("ℹ️  No data to migrate")
            return True
            
        success = True
        
        # Migrate users
        if users:
            print(f"🔄 Migrating {len(users)} users...")
            for user in users:
                try:
                    # Remove id to let PostgreSQL auto-generate
                    user_data = {k: v for k, v in user.items() if k != 'id'}
                    result = self.supabase.table('users').insert(user_data).execute()
                    print(f"✅ Migrated user: {user.get('username', 'unknown')}")
                except Exception as e:
                    print(f"❌ Failed to migrate user {user.get('username', 'unknown')}: {e}")
                    success = False
        
        # Migrate games
        if games:
            print(f"🔄 Migrating {len(games)} games...")
            for game in games:
                try:
                    # Remove id to let PostgreSQL auto-generate
                    game_data = {k: v for k, v in game.items() if k != 'id'}
                    result = self.supabase.table('games').insert(game_data).execute()
                    print(f"✅ Migrated game: {game.get('id', 'unknown')}")
                except Exception as e:
                    print(f"❌ Failed to migrate game {game.get('id', 'unknown')}: {e}")
                    success = False
        
        return success
    
    def print_schema_instructions(self):
        """Print instructions for manual schema setup"""
        print("\n" + "="*60)
        print("📋 MANUAL SCHEMA SETUP REQUIRED")
        print("="*60)
        print("1. Go to your Supabase dashboard: https://supabase.com/dashboard")
        print("2. Select your project: your-project-id")
        print("3. Go to SQL Editor")
        print("4. Create a new query and copy-paste the following SQL:")
        print("\n" + "-"*40)
        
        with open('supabase_schema.sql', 'r') as f:
            print(f.read())
        
        print("-"*40)
        print("5. Click 'Run' to execute the schema")
        print("6. After successful execution, run this script again")
        print("="*60 + "\n")
    
    def run(self):
        """Run the complete migration process"""
        print("🚀 Starting Supabase Migration Process")
        print("-" * 50)
        
        # Step 1: Check connection
        if not self.check_connection():
            return False
        
        # Step 2: Extract existing data
        users, games = self.extract_sqlite_data()
        
        # Step 3: Save backup
        if users or games:
            self.save_migration_data(users, games)
        
        # Step 4: Check schema
        if not self.check_schema():
            self.print_schema_instructions()
            return False
        
        # Step 5: Migrate data
        print("\n🔄 Starting data migration...")
        if self.migrate_data(users, games):
            print("\n🎉 Migration completed successfully!")
            print("✅ All data has been transferred to Supabase")
            return True
        else:
            print("\n⚠️  Migration completed with some errors")
            return False

def main():
    migration = SupabaseMigration()
    success = migration.run()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Test your application locally")
        print("2. Deploy to Render")
        print("3. Verify production functionality")
    else:
        print("\n❌ Migration incomplete. Please address the issues above.")

if __name__ == "__main__":
    main()
