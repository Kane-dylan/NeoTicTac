from dotenv import load_dotenv
import os
load_dotenv()

try:
    from app import create_app, socketio, db
    
    # Create the app instance
    app = create_app()    # Initialize database tables
    def init_db():
        """Initialize database tables"""
        with app.app_context():
            try:
                print("Initializing database...")
                print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
                  # Test database connection
                with db.engine.connect() as connection:
                    connection.execute(db.text('SELECT 1'))
                print("Database connection successful")
                
                # Create tables
                db.create_all()
                print("Database tables created successfully")
                
                # Test table creation by querying User table
                from app.models.user import User
                user_count = User.query.count()
                print(f"User table accessible, current count: {user_count}")
                
            except Exception as e:
                print(f"Database error: {e}")
                print(f"Database error type: {type(e)}")
                import traceback
                print(f"Full traceback: {traceback.format_exc()}")
                print("Server will continue but database operations may fail")

    # Initialize database on startup
    init_db()

    if __name__ == '__main__':
        # Development server only
        print("Starting development server...")
        try:
            socketio.run(
                app, 
                host='0.0.0.0', 
                port=int(os.getenv('PORT', 5000)),
                debug=os.getenv('FLASK_ENV') == 'development',
                allow_unsafe_werkzeug=True
            )
        except Exception as e:
            print(f"Failed to start server: {e}")
    
    # For production (Gunicorn will import 'app' from this module)
    # This makes the 'app' variable available to Gunicorn
            
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required dependencies:")
    print("pip install flask flask-cors flask-sqlalchemy flask-migrate flask-jwt-extended flask-socketio python-dotenv psycopg2-binary")
except Exception as e:
    print(f"Startup error: {e}")
    # Create a dummy app for Gunicorn if there's an error
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return {'status': 'error', 'message': 'Server failed to initialize properly'}
