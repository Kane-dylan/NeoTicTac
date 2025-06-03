import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'devkey')
    
    # Handle Railway/production database URL correctly
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        # Fix for newer SQLAlchemy versions that require postgresql://
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///tictactoe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Add JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire for this demo
    
    # CORS configuration for production
    CORS_ORIGINS = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Alternative dev port
        "https://*.vercel.app",   # Vercel deployments
        os.getenv('CLIENT_URL', 'http://localhost:5173')  # Custom client URL
    ]
