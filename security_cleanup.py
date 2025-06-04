#!/usr/bin/env python3
"""
Security cleanup script - removes sensitive data from configuration files
"""
import os
import re

def clean_sensitive_data():
    """Remove sensitive data from configuration files"""
    
    print("🔒 SECURITY CLEANUP - Removing Sensitive Data")
    print("=" * 60)
    
    # Files to clean and their sensitive patterns
    cleanup_targets = {
        'render.yaml': [
            (r'value: [a-f0-9]{64}', 'value: your-secret-key-here'),
            (r'value: eyJ[A-Za-z0-9+/=]+', 'value: your-service-role-key-here'),
            (r'value: postgresql://postgres:[^@]+@[^/]+', 'value: postgresql://postgres:your-password@db.your-project-id.supabase.co:6543/postgres?pgbouncer=true'),
            (r'value: https://[a-z]+\.supabase\.co', 'value: https://your-project-id.supabase.co'),
            (r'value: https://[^.]+\.vercel\.app', 'value: https://your-frontend-url.vercel.app'),
            (r'value: https://[^.]+\.onrender\.com', 'value: https://your-backend-url.onrender.com')
        ],
        'server/.env': [
            (r'SECRET_KEY=[a-f0-9]{64}', 'SECRET_KEY=your-secret-key-here'),
            (r'JWT_SECRET_KEY=[a-f0-9]{64}', 'JWT_SECRET_KEY=your-jwt-secret-key-here'),
            (r'SUPABASE_SERVICE_KEY=eyJ[A-Za-z0-9+/=]+', 'SUPABASE_SERVICE_KEY=your-service-role-key-here'),
            (r'DATABASE_URL=postgresql://postgres:[^@]+@[^/]+', 'DATABASE_URL=postgresql://postgres:your-password@db.your-project-id.supabase.co:6543/postgres?pgbouncer=true'),
            (r'SUPABASE_URL=https://[a-z]+\.supabase\.co', 'SUPABASE_URL=https://your-project-id.supabase.co'),
            (r'CLIENT_URL=https://[^.]+\.vercel\.app', 'CLIENT_URL=https://your-frontend-url.vercel.app')
        ],
        'client/.env': [
            (r'VITE_SUPABASE_URL=https://[a-z]+\.supabase\.co', 'VITE_SUPABASE_URL=https://your-project-id.supabase.co'),
            (r'VITE_SUPABASE_ANON_KEY=eyJ[A-Za-z0-9+/=]+', 'VITE_SUPABASE_ANON_KEY=your-anon-key-here'),
            (r'VITE_API_URL=https://[^.]+\.onrender\.com', 'VITE_API_URL=https://your-render-app.onrender.com/api'),
            (r'VITE_SOCKET_URL=https://[^.]+\.onrender\.com', 'VITE_SOCKET_URL=https://your-render-app.onrender.com')
        ]
    }
    
    cleaned_files = []
    
    for file_path, patterns in cleanup_targets.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                original_content = content
                
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(file_path, 'w') as f:
                        f.write(content)
                    print(f"✅ Cleaned {file_path}")
                    cleaned_files.append(file_path)
                else:
                    print(f"ℹ️  {file_path} - already clean")
                    
            except Exception as e:
                print(f"❌ Error cleaning {file_path}: {e}")
        else:
            print(f"⚠️  {file_path} not found")
    
    return cleaned_files

def create_env_templates():
    """Create secure .env.example templates"""
    
    server_env_example = """# Environment variables for local development
# Copy this file to .env and fill in your actual values

# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Database Configuration (use Supabase connection string)
DATABASE_URL=postgresql://postgres:your-password@db.your-project-id.supabase.co:6543/postgres?pgbouncer=true

# Client URL (for CORS)
CLIENT_URL=http://localhost:5173

# Flask Environment
FLASK_ENV=development
"""
    
    client_env_example = """# Client environment variables
# Copy this file to .env and fill in your actual values

# Supabase Configuration (public keys)
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here

# Backend URLs
VITE_API_URL=http://localhost:5000/api
VITE_SOCKET_URL=http://localhost:5000
"""
    
    # Write templates
    os.makedirs('server', exist_ok=True)
    os.makedirs('client', exist_ok=True)
    
    with open('server/.env.example', 'w') as f:
        f.write(server_env_example)
    
    with open('client/.env.example', 'w') as f:
        f.write(client_env_example)
    
    print("✅ Created secure .env.example templates")

def check_gitignore():
    """Ensure .gitignore properly excludes sensitive files"""
    
    gitignore_content = """# Environment variables
.env
.env.local
.env.production
.env.development

# Database
*.db
*.db-*
instance/

# API Keys and Secrets
secrets.json
credentials.json

# Logs
*.log
logs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Node.js (for client)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Updated .gitignore with comprehensive security exclusions")

def main():
    """Run complete security cleanup"""
    
    print("🛡️  SECURITY CLEANUP PROCESS")
    print("=" * 60)
    
    # Step 1: Clean sensitive data from files
    cleaned_files = clean_sensitive_data()
    
    print("\n📝 Creating secure templates...")
    # Step 2: Create secure .env.example templates
    create_env_templates()
    
    # Step 3: Update .gitignore
    check_gitignore()
    
    print("\n🎯 CLEANUP SUMMARY:")
    print("-" * 40)
    if cleaned_files:
        print(f"✅ Cleaned {len(cleaned_files)} files:")
        for file in cleaned_files:
            print(f"   - {file}")
    else:
        print("ℹ️  All files were already clean")
    
    print("\n📋 NEXT STEPS:")
    print("-" * 40)
    print("1. ✅ Sensitive data removed from configuration files")
    print("2. ✅ Secure .env.example templates created")
    print("3. ✅ .gitignore updated to prevent future leaks")
    print("4. 🔐 Configure actual credentials in deployment environment")
    print("5. 🚫 NEVER commit actual .env files or credentials")
    
    print("\n⚠️  IMPORTANT SECURITY REMINDERS:")
    print("-" * 40)
    print("• Always use environment variables for credentials")
    print("• Never commit .env files to version control")
    print("• Rotate secrets if they were accidentally exposed")
    print("• Use different credentials for development/production")
    print("• Regularly audit your repository for sensitive data")

if __name__ == "__main__":
    main()
