from dotenv import load_dotenv
load_dotenv()

try:
    from app import create_app, socketio, db
    
    app = create_app()

    # Create database tables and handle migrations
    with app.app_context():
        try:
            # Drop and recreate tables to fix schema issues
            print("Recreating database tables...")
            db.drop_all()
            db.create_all()
            print("Database tables created successfully")
            
            # Check if any games exist
            from app.models.game import Game
            from app.models.user import User
            
            game_count = Game.query.count()
            user_count = User.query.count()
            
            print(f"Current games in database: {game_count}")
            print(f"Current users in database: {user_count}")
            
            if game_count == 0:
                print("No games found in database. Users will need to create new games.")
                
        except Exception as e:
            print(f"Database error: {e}")
            print("Server will continue but database operations may fail")

    if __name__ == '__main__':
        print("Starting server on http://localhost:5000")
        print("Socket.IO will be available at ws://localhost:5000")
        print("Available endpoints:")
        print("  - http://localhost:5000/api/auth/login")
        print("  - http://localhost:5000/api/auth/register") 
        print("  - http://localhost:5000/api/game/active")
        print("  - http://localhost:5000/api/game/create")
        
        try:
            print("Starting socketio server...")
            socketio.run(
                app, 
                host='0.0.0.0', 
                port=5000, 
                debug=True,
                allow_unsafe_werkzeug=True  # Allow for development
            )
        except Exception as e:
            print(f"Failed to start server: {e}")
            import traceback
            traceback.print_exc()
            
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required dependencies:")
    print("pip install flask flask-cors flask-sqlalchemy flask-migrate flask-jwt-extended flask-socketio python-dotenv")
except Exception as e:
    print(f"Startup error: {e}")
