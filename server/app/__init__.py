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
    app.config.from_object("config.Config")    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    
    app.logger.info('Tic Tac Toe App startup')
    
    # Log configuration details for debugging
    try:
        from config import Config
        if hasattr(Config, 'log_configuration'):
            Config.log_configuration()
        app.logger.info(f"Database URI configured: {bool(app.config.get('SQLALCHEMY_DATABASE_URI'))}")
    except Exception as e:
        app.logger.error(f"Config logging error: {e}")
    
    # Log Supabase status (optional feature)
    supabase_configured = bool(app.config.get('SUPABASE_URL')) and bool(app.config.get('SUPABASE_SERVICE_KEY'))
    app.logger.info(f"Supabase configured: {supabase_configured}")
    if not supabase_configured:
        app.logger.info("Supabase not configured - using direct database connection only")
    
    # Initialize extensions with app
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
    from app.models import user, game    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.game import bp as game_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)    # Add health check endpoint for Render
    @app.route('/')
    @app.route('/health')
    def health_check():
        db_status = 'connected'
        try:
            # Test database connection using modern SQLAlchemy syntax
            with db.engine.connect() as connection:
                from sqlalchemy import text
                connection.execute(text('SELECT 1'))
        except Exception as e:
            db_status = f'disconnected: {str(e)[:100]}'
            app.logger.error(f"Database health check failed: {e}")
        
        return {
            'status': 'healthy',
            'message': 'Tic-Tac-Toe API is running',
            'database': db_status,
            'supabase': 'configured' if app.config.get('SUPABASE_URL') else 'not configured'
        }, 200

    # Add database connection test endpoint
    @app.route('/api/test-db')
    def test_database():
        try:
            # Test database connection
            result = db.session.execute('SELECT version()')
            version = result.fetchone()[0] if result else 'Unknown'
            
            # Test table creation
            db.create_all()
            
            return {
                'status': 'success',
                'message': 'Database connection successful',
                'version': version,
                'tables_created': True
            }, 200
        except Exception as e:
            app.logger.error(f"Database test failed: {e}")
            return {
                'status': 'error',
                'message': 'Database connection failed',
                'error': str(e)
            }, 500

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
