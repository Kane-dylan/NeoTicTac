"""
Simple Server Test
Test if the server can start and handle basic authentication
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_server_import():
    """Test if we can import the server without errors"""
    print("🧪 Testing server import...")
      try:
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models.user import User
            from app.models.game import Game
            from app import db
            from sqlalchemy import text
            
            # Test database connection
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Server import and database connection successful!")
            return True
            
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_user_model():
    """Test the User model directly"""
    print("🧪 Testing User model...")
    
    try:
        from app import create_app
        from app.models.user import User
        from app import db
        
        app = create_app()
        
        with app.app_context():
            # Try to create a user instance
            test_user = User(username="direct_test_user")
            test_user.set_password("test_password")
            
            # Add to session
            db.session.add(test_user)
            db.session.commit()
            
            # Query back
            retrieved = User.query.filter_by(username="direct_test_user").first()
            
            if retrieved and retrieved.check_password("test_password"):
                print("✅ User model test successful!")
                
                # Clean up
                db.session.delete(retrieved)
                db.session.commit()
                return True
            else:
                print("❌ User model test failed - couldn't retrieve user")
                return False
                
    except Exception as e:
        print(f"❌ User model test failed: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_game_model():
    """Test the Game model directly"""
    print("🧪 Testing Game model...")
    
    try:
        from app import create_app
        from app.models.game import Game
        from app import db
        
        app = create_app()
        
        with app.app_context():
            # Try to create a game instance
            test_game = Game(player_x="direct_test_player")
            
            # Add to session
            db.session.add(test_game)
            db.session.commit()
            
            # Query back
            retrieved = Game.query.filter_by(player_x="direct_test_player").first()
            
            if retrieved:
                print("✅ Game model test successful!")
                
                # Clean up
                db.session.delete(retrieved)
                db.session.commit()
                return True
            else:
                print("❌ Game model test failed - couldn't retrieve game")
                return False
                
    except Exception as e:
        print(f"❌ Game model test failed: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """Main test function"""
    print("🚀 Starting simple server tests...")
    print("="*50)
    
    # Test 1: Server import
    if not test_server_import():
        return False
    
    print("\n" + "="*50)
    
    # Test 2: User model
    if not test_user_model():
        return False
    
    print("\n" + "="*50)
    
    # Test 3: Game model
    if not test_game_model():
        return False
    
    print("\n" + "="*50)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Server can be imported successfully")
    print("✅ Database connection works")
    print("✅ User model works (username + password)")
    print("✅ Game model works")
    print("🚀 Ready to start server!")
    print("="*50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
