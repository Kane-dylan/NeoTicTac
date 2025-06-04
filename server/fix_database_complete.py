"""
Complete Database Fix Script
This script will:
1. Drop all existing tables
2. Recreate them with the correct schema
3. Test the database connection
4. Verify the models work correctly
"""

import os
import sys
from dotenv import load_dotenv
import traceback

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from app import create_app, db
from app.models.user import User
from app.models.game import Game
from sqlalchemy import text, inspect
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def drop_all_tables():
    """Drop all tables in the database"""
    logger.info("🗑️ Dropping all existing tables...")
    
    try:
        # Get all table names
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if tables:
            logger.info(f"Found tables to drop: {tables}")
            
            # Drop tables in the correct order (avoid foreign key constraints)
            with db.engine.connect() as conn:
                # Disable foreign key checks if using PostgreSQL
                conn.execute(text("SET session_replication_role = replica;"))
                
                for table in tables:
                    logger.info(f"Dropping table: {table}")
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                
                # Re-enable foreign key checks
                conn.execute(text("SET session_replication_role = DEFAULT;"))
                conn.commit()
                
            logger.info("✅ All tables dropped successfully")
        else:
            logger.info("No tables found to drop")
            
    except Exception as e:
        logger.error(f"❌ Error dropping tables: {e}")
        raise

def create_all_tables():
    """Create all tables with the current schema"""
    logger.info("🔧 Creating all tables with current schema...")
    
    try:
        # Create all tables
        db.create_all()
        logger.info("✅ All tables created successfully")
        
        # Verify tables were created
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {tables}")
        
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        raise

def test_user_model():
    """Test the User model"""
    logger.info("🧪 Testing User model...")
    
    try:
        # Create a test user
        test_user = User(username="test_user_fix")
        test_user.set_password("test_password")
        
        db.session.add(test_user)
        db.session.commit()
        
        # Query the user back
        retrieved_user = User.query.filter_by(username="test_user_fix").first()
        
        if retrieved_user and retrieved_user.check_password("test_password"):
            logger.info("✅ User model working correctly")
            
            # Clean up test user
            db.session.delete(retrieved_user)
            db.session.commit()
            
            return True
        else:
            logger.error("❌ User model test failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ User model test error: {e}")
        db.session.rollback()
        return False

def test_game_model():
    """Test the Game model"""
    logger.info("🧪 Testing Game model...")
    
    try:
        # Create a test game
        test_game = Game(player_x="test_player_x")
        test_game.board_data = ["X", "", "O", "", "", "", "", "", ""]
        
        db.session.add(test_game)
        db.session.commit()
        
        # Query the game back
        retrieved_game = Game.query.filter_by(player_x="test_player_x").first()
        
        if retrieved_game and retrieved_game.board_data[0] == "X":
            logger.info("✅ Game model working correctly")
            
            # Clean up test game
            db.session.delete(retrieved_game)
            db.session.commit()
            
            return True
        else:
            logger.error("❌ Game model test failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Game model test error: {e}")
        logger.error(traceback.format_exc())
        db.session.rollback()
        return False

def test_database_connection():
    """Test basic database connection"""
    logger.info("🔍 Testing database connection...")
    
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"✅ Database connection successful")
            logger.info(f"PostgreSQL version: {version}")
            return True
            
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main function to fix the database"""
    logger.info("🚀 Starting complete database fix...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test initial connection
            if not test_database_connection():
                logger.error("❌ Cannot connect to database. Please check your DATABASE_URL")
                return False
            
            # Step 1: Drop all tables
            drop_all_tables()
            
            # Step 2: Create all tables
            create_all_tables()
            
            # Step 3: Test User model
            if not test_user_model():
                logger.error("❌ User model test failed")
                return False
            
            # Step 4: Test Game model  
            if not test_game_model():
                logger.error("❌ Game model test failed")
                return False
            
            logger.info("🎉 Database fix completed successfully!")
            logger.info("✅ All models are working correctly")
            logger.info("🔧 You can now start your server and test authentication")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Database fix failed: {e}")
            logger.error(traceback.format_exc())
            return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n" + "="*50)
        print("✅ DATABASE FIX COMPLETED SUCCESSFULLY!")
        print("🚀 You can now run your server:")
        print("   python run.py")
        print("="*50)
        sys.exit(0)
    else:
        print("\n" + "="*50)
        print("❌ DATABASE FIX FAILED!")
        print("Please check the error messages above.")
        print("="*50)
        sys.exit(1)
