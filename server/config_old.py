import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Production configuration for Supabase deployment"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
      # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Fix for newer SQLAlchemy versions
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Enhance DATABASE_URL with production-specific parameters
    if not any(param in DATABASE_URL for param in ['sslmode=', 'connect_timeout=', 'application_name=']):
        separator = '&' if '?' in DATABASE_URL else '?'
        production_params = [
            'sslmode=require',
            'application_name=tictactoe-backend',
            'connect_timeout=30',
            'target_session_attrs=read-write'
        ]
        DATABASE_URL = DATABASE_URL + separator + '&'.join(production_params)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pool settings optimized for production deployment
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 3,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 2,
        'pool_timeout': 30,
        'connect_args': {
            'sslmode': 'require',
            'application_name': 'tictactoe-backend',
            'connect_timeout': 30,
            'options': '-c default_transaction_isolation=read_committed -c statement_timeout=30000'
        }
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable is required")
    JWT_ACCESS_TOKEN_EXPIRES = False
    
    # Supabase Configuration (optional - for additional features)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    
    # CORS configuration
    CLIENT_URL = os.getenv('CLIENT_URL', 'https://tic-tac-toe-ten-murex-86.vercel.app')
    CORS_ORIGINS = [CLIENT_URL]
    
    @classmethod
    def log_configuration(cls):
        """Log configuration details for debugging"""
        logger.info("=== Configuration Status ===")
        logger.info(f"SECRET_KEY: {'SET' if cls.SECRET_KEY else 'NOT SET'}")
        logger.info(f"DATABASE_URL: {'SET' if cls.DATABASE_URL else 'NOT SET'}")
        logger.info(f"JWT_SECRET_KEY: {'SET' if cls.JWT_SECRET_KEY else 'NOT SET'}")
        logger.info(f"CLIENT_URL: {cls.CLIENT_URL}")
        logger.info(f"SUPABASE_URL: {'SET' if cls.SUPABASE_URL else 'NOT SET'}")
        logger.info("=============================")
