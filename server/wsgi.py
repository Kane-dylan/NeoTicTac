"""
WSGI entry point for production deployment
"""
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

try:
    from app import create_app, socketio, db
    
    # Create the Flask application
    application = create_app()
    app = application  # Alias for compatibility
    
    # Initialize database
    with application.app_context():
        try:
            print("Production: Initializing database...")
            db.create_all()
            print("Production: Database initialized successfully")
        except Exception as e:
            print(f"Production: Database error: {e}")
    
    print("Production: WSGI application ready")
    
except Exception as e:
    print(f"Production: Failed to initialize application: {e}")
    # Create a minimal error app
    from flask import Flask
    application = Flask(__name__)
    app = application
    
    @app.route('/')
    def error():
        return {'error': 'Application failed to initialize', 'message': str(e)}, 500

if __name__ == "__main__":
    print("This is the WSGI entry point. Use Gunicorn in production.")
