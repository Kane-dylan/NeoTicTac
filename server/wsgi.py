"""
WSGI entry point for production deployment
"""
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debug environment variables
print(f"Production: Environment check - FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"Production: Environment check - DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
print(f"Production: Environment check - PORT: {os.getenv('PORT', 'NOT SET')}")
print(f"Production: Environment check - SECRET_KEY: {'SET' if os.getenv('SECRET_KEY') else 'NOT SET'}")
print(f"Production: Environment check - JWT_SECRET_KEY: {'SET' if os.getenv('JWT_SECRET_KEY') else 'NOT SET'}")
print(f"Production: Environment check - CLIENT_URL: {os.getenv('CLIENT_URL', 'NOT SET')}")
print(f"Production: Current working directory: {os.getcwd()}")
print(f"Production: Python path: {os.path.dirname(__file__)}")

try:
    print("Production: Starting application initialization...")
    from app import create_app, socketio, db
    
    # Create the Flask application
    print("Production: Creating Flask app...")
    app = create_app()
    print(f"Production: Flask app created successfully with config: {app.config.get('FLASK_ENV', 'unknown')}")
    
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

# Ensure the app variable is available for Gunicorn
application = app

if __name__ == "__main__":
    print("This is the WSGI entry point. Use Gunicorn in production.")
