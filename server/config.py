import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'devkey')
    
    # For production deployment, use SQLite to avoid database connection issues
    # This can be changed back to external database once connection issues are resolved
    USE_SQLITE_PRODUCTION = os.getenv('USE_SQLITE_PRODUCTION', 'true').lower() == 'true'
    
    # Database configuration with fallback to SQLite
    database_url = os.getenv("DATABASE_URL")
    
    if USE_SQLITE_PRODUCTION:
        print("Using SQLite database for production deployment")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///tictactoe.db'
        EXTERNAL_DATABASE_URL = None
    elif database_url and database_url.strip():
        # Fix for newer SQLAlchemy versions that require postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        EXTERNAL_DATABASE_URL = database_url
        SQLALCHEMY_DATABASE_URI = database_url
        print(f"Attempting to use external database: {database_url[:50]}...")
    else:
        # Use SQLite for local development or when no external DB is available
        SQLALCHEMY_DATABASE_URI = 'sqlite:///tictactoe.db'
        EXTERNAL_DATABASE_URL = None
        print("No external database URL found. Using SQLite database: tictactoe.db")
    
    # Store fallback database URI
    FALLBACK_DATABASE_URI = 'sqlite:///tictactoe.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Add JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire for this demo
    
    # CORS configuration for production
    CORS_ORIGINS = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Alternative dev port
        "https://tic-tac-toe-ten-murex-86.vercel.app", # Specific Vercel deployment
        "https://*.vercel.app",   # Vercel deployments (kept for broader matching)
        os.getenv('CLIENT_URL', 'http://localhost:5173')  # Custom client URL
    ]
