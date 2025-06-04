import os

class Config:
    """Production-ready configuration for Supabase deployment"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        # For development only - generate a temporary key
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        print("⚠️ WARNING: Using temporary SECRET_KEY for development!")
    
    # Database configuration - PostgreSQL via Supabase
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        # Fallback for local development
        DATABASE_URL = 'sqlite:///tictactoe.db'
        print("⚠️ WARNING: Using SQLite for development. Set DATABASE_URL for production!")
    
    # Fix for newer SQLAlchemy versions that require postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Only set pool options for PostgreSQL
    if DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'max_overflow': 20
        }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        # For development only
        import secrets
        JWT_SECRET_KEY = secrets.token_hex(32)
        print("⚠️ WARNING: Using temporary JWT_SECRET_KEY for development!")
    JWT_ACCESS_TOKEN_EXPIRES = False  # For demo purposes
    
    # Supabase Configuration (optional for development)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    
    # Only require Supabase vars in production
    if os.getenv('FLASK_ENV') == 'production':
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables are required in production")
    elif not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("⚠️ WARNING: Supabase not configured. Some features may not work.")
    
    # CORS configuration
    CLIENT_URL = os.getenv('CLIENT_URL', 'http://localhost:5173')
    CORS_ORIGINS = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Alternative dev port
        "https://tic-tac-toe-ten-murex-86.vercel.app",  # Your Vercel deployment
        CLIENT_URL  # Custom client URL from environment
    ]
