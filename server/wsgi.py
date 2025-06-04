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
    app = create_app()
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Production: Database initialization error: {e}")
    
except Exception as e:
    print(f"Production: Failed to initialize application: {e}")
    # Create a minimal error app
    from flask import Flask
    application = Flask(__name__)
    app = application
    
    @app.route('/')
    def error():
        return {'error': 'Application failed to initialize', 'message': str(e)}, 500

# Ensure the app variable is available for Gunicorn
application = app

if __name__ == "__main__":
    print("This is the WSGI entry point. Use Gunicorn in production.")
