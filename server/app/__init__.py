import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )

    app.logger.info('Tic Tac Toe App startup')
    
    # Log configuration details for debugging
    from config import Config
    Config.log_configuration()
    app.logger.info(f"Database URI configured: {bool(app.config.get('SQLALCHEMY_DATABASE_URI'))}")
    app.logger.info(f"Supabase URL configured: {bool(app.config.get('SUPABASE_URL'))}")    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ['http://localhost:5173']),
         allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
         supports_credentials=True)
    
    # Configure SocketIO
    socketio.init_app(app, 
                     cors_allowed_origins=app.config.get('CORS_ORIGINS', ['http://localhost:5173']),
                     logger=app.debug,
                     engineio_logger=app.debug)

    # Import models to register them with SQLAlchemy
    from app.models import user, game

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.game import bp as game_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)

    # Register socket handlers
    from app.sockets import handlers

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created successfully")
        except Exception as e:
            app.logger.error(f"Error creating database tables: {e}")
            raise

    return app
