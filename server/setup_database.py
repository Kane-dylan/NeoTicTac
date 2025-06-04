#!/usr/bin/env python3
"""
Script to create database tables in Supabase
This will set up the required schema for the Tic-Tac-Toe application
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_supabase_schema():
    """Create the required tables in Supabase"""
    
    print("🗄️  Setting up Supabase Database Schema")
    print("=" * 50)
    
    # Get Supabase credentials
    supabase_url = "https://mauqzdgqvckrepinjybz.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hdXF6ZGdxdmNrcmVwaW5qeWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODg4NjUyMCwiZXhwIjoyMDY0NDYyNTIwfQ.VWqomYXkBiVZQfxuoKMkcpZfllDkhvGLzcrDz1FZDpk"
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase credentials not found!")
        return False
    
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase")
        
        # SQL to create tables
        schema_sql = """
        -- Enable UUID extension
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        -- Drop tables if they exist (for clean setup)
        DROP TABLE IF EXISTS games CASCADE;
        DROP TABLE IF EXISTS users CASCADE;

        -- Users table
        CREATE TABLE users (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        -- Games table  
        CREATE TABLE games (
            id BIGSERIAL PRIMARY KEY,
            board TEXT NOT NULL DEFAULT '["","","","","","","","",""]',
            current_player VARCHAR(1) NOT NULL DEFAULT 'X',
            winner VARCHAR(1),
            is_finished BOOLEAN NOT NULL DEFAULT FALSE,
            player_x_id BIGINT REFERENCES users(id),
            player_o_id BIGINT REFERENCES users(id),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );

        -- Add indexes for better performance
        CREATE INDEX idx_users_username ON users(username);
        CREATE INDEX idx_users_email ON users(email);
        CREATE INDEX idx_games_player_x ON games(player_x_id);
        CREATE INDEX idx_games_player_o ON games(player_o_id);
        CREATE INDEX idx_games_finished ON games(is_finished);
        """
        
        print("🔄 Creating database tables...")
        
        # Execute the schema creation
        result = supabase.rpc('exec_sql', {'sql': schema_sql}).execute()
        
        print("✅ Database schema created successfully!")
        
        # Verify tables were created
        print("\n🔍 Verifying table creation...")
        
        # Test users table
        users_result = supabase.table('users').select('*').limit(1).execute()
        print("✅ Users table verified")
        
        # Test games table  
        games_result = supabase.table('games').select('*').limit(1).execute()
        print("✅ Games table verified")
        
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 Summary:")
        print("   - users table: ✅ Created with indexes")
        print("   - games table: ✅ Created with indexes") 
        print("   - Foreign keys: ✅ Configured")
        print("   - Indexes: ✅ Added for performance")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\n🔧 Manual Setup Required:")
        print("   1. Go to your Supabase SQL Editor")
        print("   2. Run the schema from supabase_schema.sql")
        print("   3. Verify tables are created")
        return False

if __name__ == "__main__":
    success = setup_supabase_schema()
    if not success:
        print("\n📖 Check the supabase_schema.sql file for manual setup")
