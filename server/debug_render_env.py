#!/usr/bin/env python3
"""
Render Environment Variable Setup Script
Helps debug and fix environment variable issues in Render deployment
"""
import os

def print_render_env_vars():
    """Print the environment variables for Render dashboard setup"""
    
    print("🔧 RENDER ENVIRONMENT VARIABLES SETUP")
    print("="*60)
    print("Copy these to your Render service Environment tab:")
    print("="*60)
      env_vars = {
        "SECRET_KEY": "your-secret-key-here",
        "JWT_SECRET_KEY": "your-jwt-secret-key-here",
        "DATABASE_URL": "postgresql://postgres:your-password@db.your-project-id.supabase.co:6543/postgres?pgbouncer=true",
        "SUPABASE_URL": "https://your-project-id.supabase.co",
        "SUPABASE_SERVICE_KEY": "your-service-role-key-here",
        "FLASK_ENV": "production",
        "CLIENT_URL": "https://your-frontend-url.vercel.app"
    }
    
    for key, value in env_vars.items():
        print(f"{key}={value}")
    
    print("\n" + "="*60)
    print("📋 MANUAL SETUP INSTRUCTIONS:")
    print("="*60)
    print("1. Go to your Render service dashboard")
    print("2. Click on 'Environment' tab")
    print("3. Add each variable above as a new environment variable")
    print("4. Save changes")
    print("5. Redeploy your service")

def create_debug_config():
    """Create a debug version of config.py that provides more information"""
    
    debug_config = '''import os
import logging

class Config:
    """Debug configuration to identify environment variable issues"""
    
    # Enable debug logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Print all environment variables for debugging
    logger.info("=== ENVIRONMENT VARIABLES DEBUG ===")
    for key, value in os.environ.items():
        if any(keyword in key.upper() for keyword in ['SECRET', 'JWT', 'DATABASE', 'SUPABASE', 'FLASK']):
            # Mask sensitive values
            masked_value = value[:10] + "..." if len(value) > 10 else value
            logger.info(f"{key} = {masked_value}")
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    logger.info(f"SECRET_KEY loaded: {bool(SECRET_KEY)}")
    if not SECRET_KEY:
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        logger.warning("Using temporary SECRET_KEY for development!")
    
    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    logger.info(f"DATABASE_URL loaded: {bool(DATABASE_URL)}")
    if not DATABASE_URL:
        DATABASE_URL = 'sqlite:///tictactoe.db'
        logger.warning("Using SQLite for development. Set DATABASE_URL for production!")
    
    # Fix for newer SQLAlchemy versions
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PostgreSQL connection options
    if DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'max_overflow': 20
        }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    logger.info(f"JWT_SECRET_KEY loaded: {bool(JWT_SECRET_KEY)}")
    if not JWT_SECRET_KEY:
        import secrets
        JWT_SECRET_KEY = secrets.token_hex(32)
        logger.warning("Using temporary JWT_SECRET_KEY for development!")
    JWT_ACCESS_TOKEN_EXPIRES = False
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    
    logger.info(f"SUPABASE_URL loaded: {bool(SUPABASE_URL)}")
    logger.info(f"SUPABASE_SERVICE_KEY loaded: {bool(SUPABASE_SERVICE_KEY)}")
    
    # Check if we're in production
    flask_env = os.getenv('FLASK_ENV', 'development')
    logger.info(f"FLASK_ENV: {flask_env}")
    
    if flask_env == 'production':
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            logger.error("Missing required Supabase environment variables!")
            logger.error(f"SUPABASE_URL present: {bool(SUPABASE_URL)}")
            logger.error(f"SUPABASE_SERVICE_KEY present: {bool(SUPABASE_SERVICE_KEY)}")
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables are required in production")
        else:
            logger.info("✅ All required Supabase environment variables are present")
    elif not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        logger.warning("Supabase not configured. Some features may not work.")
    
    # CORS configuration
    CLIENT_URL = os.getenv('CLIENT_URL', 'http://localhost:5173')
    logger.info(f"CLIENT_URL: {CLIENT_URL}")
    
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:5174",
        "https://tic-tac-toe-ten-murex-86.vercel.app",
        CLIENT_URL
    ]
    
    logger.info("=== CONFIGURATION LOADED SUCCESSFULLY ===")
'''
    
    with open('config_debug.py', 'w') as f:
        f.write(debug_config)
    
    print("✅ Created config_debug.py for troubleshooting")
    print("   Replace 'config.py' with 'config_debug.py' temporarily to see detailed logs")

def main():
    """Main function to help debug Render deployment"""
    print("🔍 RENDER DEPLOYMENT DEBUGGER")
    print("="*60)
    
    print("\n1. Environment Variables for Manual Setup:")
    print_render_env_vars()
    
    print("\n\n2. Debug Configuration:")
    create_debug_config()
    
    print("\n\n🚀 TROUBLESHOOTING STEPS:")
    print("="*60)
    print("1. IMMEDIATE FIX - Manual Environment Variables:")
    print("   - Copy the environment variables above")
    print("   - Set them manually in Render dashboard")
    print("   - Redeploy")
    
    print("\n2. DEBUG render.yaml loading:")
    print("   - Ensure render.yaml is in project root (not server/)")
    print("   - Commit and push the file")
    print("   - Force a new deployment")
    
    print("\n3. DETAILED DEBUGGING:")
    print("   - Use config_debug.py temporarily")
    print("   - Check Render logs for environment variable details")
    print("   - Verify Supabase credentials are valid")
    
    print("\n4. VERIFY SUPABASE SETUP:")
    print("   - Check Supabase project is active")
    print("   - Verify service role key permissions")
    print("   - Test connection string format")
    
    print("\n✅ Most likely fix: Set environment variables manually in Render dashboard")

if __name__ == "__main__":
    main()
