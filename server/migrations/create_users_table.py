"""Migration script to update users table structure"""

import os
import sys
from datetime import datetime

# Add the parent directory to sys.path to be able to import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from sqlalchemy import text

app = create_app()

def upgrade():
    """Add new columns to users table"""
    with app.app_context():
        try:
            # Check if columns already exist
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'created_at'"))
                created_at_exists = result.fetchone() is not None

                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'last_login'"))
                last_login_exists = result.fetchone() is not None

            # Add created_at column if it doesn't exist
            if not created_at_exists:
                print("Adding created_at column to users table...")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT NOW()"))

            # Add last_login column if it doesn't exist
            if not last_login_exists:
                print("Adding last_login column to users table...")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN last_login TIMESTAMP NULL"))

            # Commit transaction
            db.session.commit()
            print("Users table updated successfully!")

        except Exception as e:
            print(f"Error upgrading users table: {e}")
            db.session.rollback()
            raise

def downgrade():
    """Remove added columns from users table"""
    with app.app_context():
        try:
            # Drop last_login column
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE users DROP COLUMN IF EXISTS last_login"))

            # Drop created_at column
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE users DROP COLUMN IF EXISTS created_at"))

            # Commit transaction
            db.session.commit()
            print("Downgrade completed successfully!")

        except Exception as e:
            print(f"Error downgrading users table: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "downgrade":
        downgrade()
    else:
        upgrade()
