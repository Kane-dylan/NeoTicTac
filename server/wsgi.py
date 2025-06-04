"""
WSGI entry point for production deployment
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app, socketio, db
    
    # Create the Flask application
    app = create_app()
    
    # Initialize database
    with app.app_context():
        try:
            # Test connection with explicit text() wrapper for SQLAlchemy
            from sqlalchemy import text
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.close()

            # Create tables if connection successful
            db.create_all()
            logger.info("Production: Database initialized successfully")
        except Exception as e:
            logger.error(f"Production: Database initialization error: {e}")
            # Log database URL (removing sensitive info)
            db_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_url:
                safe_url = db_url.split('@')[0].split(':')[0] + ':***@' + db_url.split('@')[1] if '@' in db_url else 'Invalid URL format'
                logger.error(f"Database URL format: {safe_url}")
            # Don't fail completely, let the app start
    
    print(f"Production: WSGI application ready on port {os.getenv('PORT', '5000')}")
    
except Exception as e:
    print(f"Production: Failed to initialize application: {e}")
    import traceback
    traceback.print_exc()
      # Create a minimal error app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/health')
    def error():
        return {'status': 'error', 'message': f'Server failed to initialize: {str(e)}'}, 500

# Ensure the app variable is available for Gunicorn
application = app

if __name__ == "__main__":
    print("This is the WSGI entry point. Use Gunicorn in production.")
