#!/usr/bin/env python3
"""
Automated deployment preparation script for Supabase migration
"""
import os
import secrets
import subprocess
import sys

def generate_secure_keys():
    """Generate secure keys for Flask and JWT"""
    secret_key = secrets.token_hex(32)
    jwt_key = secrets.token_hex(32)
    return secret_key, jwt_key

def create_env_template():
    """Create environment template with secure keys"""
    secret_key, jwt_key = generate_secure_keys()
    
    env_template = f"""# Generated environment configuration
# Copy these values to your Render environment variables

SECRET_KEY={secret_key}
JWT_SECRET_KEY={jwt_key}

# Supabase Configuration (replace with your values)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Database Configuration (replace with your Supabase connection string)
DATABASE_URL=postgresql://postgres:your-password@db.your-project-id.supabase.co:6543/postgres?pgbouncer=true

# Client URL (replace with your frontend URL)
CLIENT_URL=https://your-frontend-url.vercel.app
"""
    
    with open('.env.production', 'w') as f:
        f.write(env_template)
    
    return secret_key, jwt_key

def validate_requirements():
    """Validate that all required packages are in requirements.txt"""
    required_packages = [
        'flask',
        'flask-cors',
        'flask-sqlalchemy',
        'flask-jwt-extended',
        'flask-socketio',
        'python-dotenv',
        'psycopg2-binary',
        'supabase',
        'eventlet',
        'gunicorn'
    ]
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read().lower()
        
        missing = []
        for package in required_packages:
            if package not in content:
                missing.append(package)
        
        if missing:
            print(f"⚠️  Missing packages in requirements.txt: {', '.join(missing)}")
            return False
        else:
            print("✅ All required packages present in requirements.txt")
            return True
    
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def check_file_structure():
    """Verify project structure is correct"""
    required_files = [
        'config.py',
        'requirements.txt',
        'run.py',
        'wsgi.py',
        'Procfile',
        'app/__init__.py',
        'app/models/user.py',
        'app/models/game.py',
        'app/routes/auth.py',
        'app/routes/game.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def print_supabase_sql():
    """Print SQL commands for Supabase setup"""
    sql_commands = """
-- Run these commands in your Supabase SQL Editor:

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Games table
CREATE TABLE IF NOT EXISTS game (
    id SERIAL PRIMARY KEY,
    player_x VARCHAR(80) NOT NULL,
    player_o VARCHAR(80),
    board TEXT DEFAULT '["","","","","","","","",""]',
    current_turn VARCHAR(1) DEFAULT 'X',
    winner VARCHAR(1),
    is_draw BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""
    
    with open('supabase_schema.sql', 'w') as f:
        f.write(sql_commands.strip())
    
    print("📄 SQL schema saved to: supabase_schema.sql")
    return sql_commands

def main():
    """Main deployment preparation process"""
    print("🚀 Preparing deployment for Supabase migration...\n")
    
    # Change to server directory
    if not os.path.exists('config.py'):
        print("❌ Not in server directory. Please run from server/ folder.")
        return False
    
    # 1. Validate file structure
    print("1. Checking file structure...")
    if not check_file_structure():
        return False
    
    # 2. Validate requirements
    print("\n2. Validating requirements.txt...")
    if not validate_requirements():
        return False
    
    # 3. Generate environment template
    print("\n3. Generating secure environment configuration...")
    secret_key, jwt_key = create_env_template()
    print("✅ Created .env.production with secure keys")
    
    # 4. Create Supabase SQL schema
    print("\n4. Generating Supabase SQL schema...")
    sql_commands = print_supabase_sql()
    
    # 5. Print deployment instructions
    print("\n" + "="*60)
    print("🎯 DEPLOYMENT READY!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Set up your Supabase project:")
    print("   • Create a new Supabase project")
    print("   • Enable connection pooling")
    print("   • Run the SQL commands from supabase_schema.sql")
    print("   • Configure network restrictions for Render")
    
    print("\n2. Configure Render environment variables:")
    print("   • Copy values from .env.production")
    print("   • Update SUPABASE_URL with your project URL")
    print("   • Update SUPABASE_SERVICE_KEY with your service role key")
    print("   • Update DATABASE_URL with your connection string")
    print("   • Update CLIENT_URL with your frontend URL")
    
    print("\n3. Migrate existing data (if any):")
    print("   • Set environment variables locally")
    print("   • Run: python migrate_to_supabase.py")
    
    print("\n4. Deploy to Render:")
    print("   • Commit and push your changes")
    print("   • Render will automatically deploy")
    
    print("\n5. Verify deployment:")
    print("   • Check Render logs")
    print("   • Test API endpoints")
    print("   • Verify database connections")
    
    print(f"\n🔑 Generated Keys:")
    print(f"SECRET_KEY: {secret_key}")
    print(f"JWT_SECRET_KEY: {jwt_key}")
    print("\n⚠️  Keep these keys secure and use them in your Render environment!")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Deployment preparation completed successfully!")
    else:
        print("\n❌ Deployment preparation failed!")
        sys.exit(1)
