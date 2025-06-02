import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'devkey')
    # Fallback to SQLite if DATABASE_URL is not set or connection fails
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or 'sqlite:///tictactoe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    # Add JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire for this demo
