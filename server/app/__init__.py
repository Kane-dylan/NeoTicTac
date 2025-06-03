from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, decode_token
from flask_socketio import SocketIO
from jwt.exceptions import DecodeError, InvalidTokenError
import threading
import time
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Add logging for loaded config if possible (Flask's logger is available after app creation)
    # Example: app.logger.info(f"Loaded CORS_ORIGINS from config: {app.config.get('CORS_ORIGINS')}")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enhanced CORS configuration
    # Get origins from config, default to an empty list if not found
    configured_origins = app.config.get('CORS_ORIGINS', [])

    # Define a base set of required origins, including the one from the error message
    required_origins = [
        "https://tic-tac-toe-ten-murex-86.vercel.app",  # Client origin from the error
        "http://localhost:5173",  # Common Vite dev server
        "http://localhost:5174"   # Alternative dev port
    ]
    
    # Combine configured origins with required origins, ensuring no duplicates
    effective_origins = list(set(configured_origins + required_origins))
    
    # Log the effective origins that will be used by Flask-CORS
    # Note: app.logger is available after Flask app object is created.
    # For logging before that, use standard Python logging.
    # This log will appear in your server logs (e.g., on Render).
    # import logging
    # logging.basicConfig(level=logging.INFO)
    # logging.info(f"Calculated effective CORS origins: {effective_origins}")
    # If app.logger is available and configured:
    # app.logger.info(f"Effective CORS origins for Flask-CORS: {effective_origins}")


    CORS(app, 
         origins=effective_origins, # Use the combined and deduplicated list
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'], # Added common X-Requested-With
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         supports_credentials=True,
         expose_headers=['Content-Length'], # Expose common headers if needed
         max_age=86400 # Cache preflight responses for 1 day
    )
    
    # Enhanced socket initialization with better authentication handling
    @socketio.on('connect')
    def handle_connect(auth):
        try:
            if auth and 'token' in auth:
                token = auth['token']
                # Validate token format
                if not token or token == 'null' or token == 'undefined':
                    print("Socket connection rejected: Invalid token format")
                    return False
                    
                decoded_token = decode_token(token)
                username = decoded_token['sub']
                print(f"Socket authenticated for user: {username}")
                return True
            else:
                # Allow connections without auth for now (can be restricted later)
                print("Socket connection allowed without authentication")
                return True
        except (DecodeError, InvalidTokenError, ValueError) as e:
            print(f"Socket JWT error: {e}")
            # Allow connection but log the error
            return True
        except Exception as e:
            print(f"Socket authentication failed: {e}")
            # Allow connection but log the error
            return True
    
    # Initialize SocketIO with production settings
    socketio.init_app(app, 
                     cors_allowed_origins=effective_origins, # Use the same effective_origins
                     logger=app.config.get('DEBUG', False),  # Use app.debug status for logger
                     engineio_logger=app.config.get('DEBUG', False),  # Use app.debug status for engineio_logger
                     async_mode='eventlet')

    # Import models to register them with SQLAlchemy
    from app.models import user, game

    from app.routes import auth, game
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)

    from app.sockets.handlers import register_socket_handlers
    register_socket_handlers(socketio)

    # Start background cleanup task only in production or when explicitly enabled
    if not app.debug or os.getenv('ENABLE_CLEANUP', 'false').lower() == 'true':
        def start_cleanup_scheduler():
            """Start the background cleanup task"""
            def cleanup_scheduler():
                while True:
                    try:
                        time.sleep(3600)  # Run every hour
                        with app.app_context():
                            from app.sockets.handlers import cleanup_old_games
                            cleanup_old_games()
                    except Exception as e:
                        print(f"Error in cleanup scheduler: {e}")
            
            cleanup_thread = threading.Thread(target=cleanup_scheduler, daemon=True)
            cleanup_thread.start()
            print("Game cleanup scheduler started (runs every hour)")
        
        # Start the cleanup scheduler
        start_cleanup_scheduler()

    return app
