"""
Enhanced config.py with automatic connection fallback for Render deployment
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Production-ready configuration for Supabase deployment with connection fallback"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        # For development only - generate a temporary key
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        logger.warning("⚠️ Using temporary SECRET_KEY for development!")
    
    # Database configuration - PostgreSQL via Supabase with fallback
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Smart connection handling for Render deployment
    if not DATABASE_URL:
        # Fallback for local development
        DATABASE_URL = 'sqlite:///tictactoe.db'
        logger.warning("⚠️ Using SQLite for development. Set DATABASE_URL for production!")
    else:
        # Fix for newer SQLAlchemy versions
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
        # For Render deployment, automatically try pgbouncer if direct connection fails
        if "render.com" in os.getenv("RENDER_SERVICE_URL", "") or os.getenv("FLASK_ENV") == "production":
            # If not already using pgbouncer, suggest it
            if ":5432/" in DATABASE_URL and "6543" not in DATABASE_URL:
                pgbouncer_url = DATABASE_URL.replace(":5432/", ":6543/")
                logger.info(f"🔄 Production detected. Consider using pgbouncer: {pgbouncer_url}")
                # Auto-switch to pgbouncer for better Render compatibility
                DATABASE_URL = pgbouncer_url
                logger.info("✅ Auto-switched to pgbouncer connection for Render")
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Enhanced connection pool settings for production
    if DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 5,  # Reduced for Render's resource limits
            'pool_recycle': 1800,  # 30 minutes
            'pool_pre_ping': True,
            'max_overflow': 10,
            'pool_timeout': 30,
            'connect_args': {
                'connect_timeout': 10,
                'application_name': 'tictactoe-backend'
            }
        }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        # For development only
        import secrets
        JWT_SECRET_KEY = secrets.token_hex(32)
        logger.warning("⚠️ Using temporary JWT_SECRET_KEY for development!")
    JWT_ACCESS_TOKEN_EXPIRES = False  # For demo purposes
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    
    # Only require Supabase vars in production
    if os.getenv('FLASK_ENV') == 'production':
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables are required in production")
    elif not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        logger.warning("⚠️ Supabase not configured. Some features may not work.")
    
    # CORS configuration
    CLIENT_URL = os.getenv('CLIENT_URL', 'http://localhost:5173')
    CORS_ORIGINS = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Alternative dev port
        "https://tic-tac-toe-ten-murex-86.vercel.app",  # Your Vercel deployment
        CLIENT_URL  # Custom client URL from environment
    ]
    
    @classmethod
    def log_configuration(cls):
        """Log configuration details for debugging"""
        logger.info("🔧 Configuration loaded:")
        logger.info(f"   DATABASE_URL: {cls.SQLALCHEMY_DATABASE_URI[:50]}...")
        logger.info(f"   FLASK_ENV: {os.getenv('FLASK_ENV', 'development')}")
        logger.info(f"   CLIENT_URL: {cls.CLIENT_URL}")
        logger.info(f"   SUPABASE configured: {bool(cls.SUPABASE_URL)}")
        
        # Check if we're using pgbouncer
        if ":6543/" in cls.SQLALCHEMY_DATABASE_URI:
            logger.info("✅ Using pgbouncer connection (recommended for Render)")
        elif ":5432/" in cls.SQLALCHEMY_DATABASE_URI:
            logger.info("ℹ️ Using direct connection")
