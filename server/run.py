import os
from dotenv import load_dotenv
load_dotenv()

try:
    from app import create_app, socketio, db
    
    # Create the app instance
    app = create_app()    # Initialize database tables
    def init_db():
        """Initialize database tables with improved retry logic"""
        with app.app_context():
            max_retries = 5
            retry_delay = 3
            
            for attempt in range(max_retries):
                try:
                    # Test connection with explicit text() wrapper for newer SQLAlchemy
                    from sqlalchemy import text
                    with db.engine.connect() as conn:
                        result = conn.execute(text("SELECT 1"))
                        result.close()
                    
                    # Create tables if connection successful
                    db.create_all()
                    app.logger.info("✅ Database tables created successfully")
                    return True
                    
                except Exception as e:
                    app.logger.error(f"❌ Database initialization attempt {attempt + 1} failed: {e}")
                    
                    if attempt < max_retries - 1:
                        app.logger.info(f"⏳ Retrying in {retry_delay} seconds...")
                        import time
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 1.5, 30)  # Exponential backoff with cap
                    else:
                        app.logger.error("❌ All connection attempts failed")
                        # Don't modify URI in production - log the error and continue
                        app.logger.warning("⚠️  Database unavailable - server will run with limited functionality")
                        return False
            
            return False

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
