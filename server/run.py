from dotenv import load_dotenv
load_dotenv()

try:
    from app import create_app, socketio, db
    
    app = create_app()

    # Create database tables if they don't exist
    with app.app_context():
        try:
            print("Initializing database...")
            db.create_all()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database error: {e}")
            print("Server will continue but database operations may fail")

    if __name__ == '__main__':
        
        try:
            socketio.run(
                app, 
                host='0.0.0.0', 
                port=5000, 
                debug=True,
                allow_unsafe_werkzeug=True
            )
        except Exception as e:
            print(f"Failed to start server: {e}")
            
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required dependencies:")
    print("pip install flask flask-cors flask-sqlalchemy flask-migrate flask-jwt-extended flask-socketio python-dotenv")
except Exception as e:
    print(f"Startup error: {e}")
