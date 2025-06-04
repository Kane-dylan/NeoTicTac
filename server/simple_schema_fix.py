#!/usr/bin/env python3
"""
Simple Database Schema Fix Script
"""
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path to be able to import from app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app import create_app, db
from sqlalchemy import text

def main():
    print("🚀 Starting simple database schema fix...")
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🗑️  Dropping existing tables...")
            
            # Drop tables in correct order
            with db.engine.connect() as conn:
                trans = conn.begin()
                try:
                    # Drop tables that might exist                    conn.execute(text("DROP TABLE IF EXISTS game CASCADE"))
                    print("   ✅ Dropped game table")
                    
                    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
                    print("   ✅ Dropped users table")
                    
                    conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
                    print("   ✅ Dropped user table (if existed)")
                    
                    trans.commit()
                    
                except Exception as e:
                    trans.rollback()
                    raise e
            
            print("🏗️  Creating new tables...")
            
            # Create all tables using SQLAlchemy models
            db.create_all()
            
            print("✅ Tables created successfully!")
            
            # Test the tables
            print("🧪 Testing tables...")
            
            with db.engine.connect() as conn:
                # Check users table
                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"))
                users_columns = [row[0] for row in result.fetchall()]
                print(f"   Users table columns: {users_columns}")
                
                # Check game table
                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'game' ORDER BY ordinal_position"))
                game_columns = [row[0] for row in result.fetchall()]
                print(f"   Game table columns: {game_columns}")
            
            print("🎉 Database schema fix completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
