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

    # Initialize logging
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        # You might want to configure the log file path and level
        # For Render, stdout/stderr logging is usually preferred.
        # This is an example for file-based logging if needed.
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/tictactoe.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Tic Tac Toe App startup')

    app.logger.info(f"Flask App Name: {app.name}")
    app.logger.info(f"CORS_ORIGINS from config: {app.config.get('CORS_ORIGINS')}")
    app.logger.info(f"DATABASE_URL from config: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    app.logger.info(f"JWT_SECRET_KEY is set: {'JWT_SECRET_KEY' in app.config}")


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enhanced CORS configuration
    configured_origins = app.config.get('CORS_ORIGINS', [])
    app.logger.info(f"Configured CORS Origins: {configured_origins}")

    default_required_origins = [
        "https://tic-tac-toe-ten-murex-86.vercel.app",  # Your Vercel deployment
        "http://localhost:5173",                      # Common Vite dev server
        "http://localhost:3000",                      # Common React dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # Combine configured origins with default required origins, ensuring no duplicates
    # and filtering out any None or empty string values if they somehow get in.
    effective_origins = list(set([origin for origin in configured_origins + default_required_origins if origin]))
    
    app.logger.info(f"Effective CORS origins for Flask-CORS: {effective_origins}")

    CORS(app, 
         origins=effective_origins, 
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         supports_credentials=True,
         expose_headers=['Content-Length'], 
         max_age=86400 
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
                     logger=app.config.get('DEBUG', False),
                     engineio_logger=app.config.get('DEBUG', False),
                     async_mode=app.config.get('ASYNC_MODE', 'eventlet')) # Get async_mode from config or default

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
