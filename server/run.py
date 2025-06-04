from dotenv import load_dotenv
import os
load_dotenv()

try:
    from app import create_app, socketio, db
    
    # Create the app instance
    app = create_app()
    
    # Initialize database tables
    def init_db():
        """Initialize database tables"""
        with app.app_context():
            try:
                db.create_all()
                print("Database tables created successfully")
            except Exception as e:
                print(f"Database initialization error: {e}")
                # For production, ensure we have a working database
                if os.getenv('FLASK_ENV') != 'development':
                    try:
                        # Fallback to SQLite for emergency
                        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tictactoe.db'
                        from sqlalchemy import create_engine
                        db.engine = create_engine('sqlite:///tictactoe.db')
                        db.create_all()
                        print("Fallback SQLite database created")
                    except Exception as fallback_error:
                        print(f"Fallback database failed: {fallback_error}")

    # Initialize database on startup
    init_db()

    if __name__ == '__main__':
        # Check if this is running in production (Render sets PORT)
        port = int(os.getenv('PORT', 5000))
        is_production = os.getenv('PORT') is not None
        
        if is_production:
            print(f"Running in production mode on port {port}")
            # Use socketio.run for production with proper settings
            socketio.run(
                app, 
                host='0.0.0.0', 
                port=port,
                debug=False,
                allow_unsafe_werkzeug=True
            )
        else:
            print("Running in development mode")
            # Development server
            socketio.run(
                app, 
                host='0.0.0.0', 
                port=port,
                debug=os.getenv('FLASK_ENV') == 'development',
                allow_unsafe_werkzeug=True
            )
    
    # For production (Gunicorn will import 'app' from this module)
            
except ImportError as e:
    print(f"Import error: {e}")
    # Create a dummy app for Gunicorn if there's an error
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return {'status': 'error', 'message': 'Server failed to initialize properly'}
        
except Exception as e:
    print(f"Startup error: {e}")
    # Create a dummy app for Gunicorn if there's an error
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return {'status': 'error', 'message': 'Server failed to initialize properly'}
