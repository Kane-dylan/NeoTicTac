#!/usr/bin/env python3
"""
Cleanup script to remove SQLite-specific files and prepare for Supabase migration
"""
import os
import shutil
import glob

def cleanup_sqlite_files():
    """Remove SQLite database files and related artifacts"""
    sqlite_patterns = [
        'server/instance/*.db',
        'server/instance/*.db-*',
        'server/*.db',
        'server/*.db-*'
    ]
    
    removed_files = []
    for pattern in sqlite_patterns:
        for file_path in glob.glob(pattern):
            if os.path.exists(file_path):
                os.remove(file_path)
                removed_files.append(file_path)
    
    # Remove instance directory if empty
    instance_dir = 'server/instance'
    if os.path.exists(instance_dir) and not os.listdir(instance_dir):
        os.rmdir(instance_dir)
        removed_files.append(instance_dir)
    
    return removed_files

def cleanup_migration_files():
    """Remove Flask-Migrate related files"""
    migration_paths = [
        'server/migrations',
        'server/alembic.ini'
    ]
    
    removed_files = []
    for path in migration_paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            removed_files.append(path)
    
    return removed_files

def cleanup_debug_scripts():
    """Remove debug and development scripts"""
    debug_scripts = [
        'server/debug_deployment.py',
        'server/inspect_db.py',
        'server/test_db.py',
        'server/database_test.py'
    ]
    
    removed_files = []
    for script in debug_scripts:
        if os.path.exists(script):
            os.remove(script)
            removed_files.append(script)
    
    return removed_files

def cleanup_deployment_configs():
    """Remove unused deployment configurations"""
    configs = [
        'server/railway.json',
        'server/Dockerfile.old',
        'server/docker-compose.yml'
    ]
    
    removed_files = []
    for config in configs:
        if os.path.exists(config):
            os.remove(config)
            removed_files.append(config)
    
    return removed_files

def cleanup_pycache():
    """Remove Python cache files"""
    removed_dirs = []
    for root, dirs, files in os.walk('server'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            removed_dirs.append(pycache_path)
    
    # Also remove .pyc files
    removed_files = []
    for root, dirs, files in os.walk('server'):
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                removed_files.append(file_path)
    
    return removed_dirs + removed_files

def create_gitignore():
    """Create/update .gitignore for the cleaned up project"""
    gitignore_content = """# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.db-*
instance/

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

# Flask
instance/
.webassets-cache

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

# Logs
*.log
logs/

# Node modules (for client)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
"""
    
    gitignore_path = '.gitignore'
    with open(gitignore_path, 'w') as f:
        f.write(gitignore_content)
    
    return gitignore_path

def main():
    """Main cleanup process"""
    print("🧹 Starting comprehensive codebase cleanup...\n")
    
    # Change to project root
    os.chdir('d:/Repos/Tic-Tac-Toe')
    
    all_removed = []
    
    # 1. Cleanup SQLite files
    print("1. Removing SQLite database files...")
    removed = cleanup_sqlite_files()
    all_removed.extend(removed)
    if removed:
        for file in removed:
            print(f"   ✓ Removed: {file}")
    else:
        print("   ✓ No SQLite files found")
    
    # 2. Cleanup migration files
    print("\n2. Removing Flask-Migrate files...")
    removed = cleanup_migration_files()
    all_removed.extend(removed)
    if removed:
        for file in removed:
            print(f"   ✓ Removed: {file}")
    else:
        print("   ✓ No migration files found")
    
    # 3. Cleanup debug scripts
    print("\n3. Removing debug scripts...")
    removed = cleanup_debug_scripts()
    all_removed.extend(removed)
    if removed:
        for file in removed:
            print(f"   ✓ Removed: {file}")
    else:
        print("   ✓ No debug scripts found")
    
    # 4. Cleanup deployment configs
    print("\n4. Removing unused deployment configs...")
    removed = cleanup_deployment_configs()
    all_removed.extend(removed)
    if removed:
        for file in removed:
            print(f"   ✓ Removed: {file}")
    else:
        print("   ✓ No unused configs found")
    
    # 5. Cleanup Python cache
    print("\n5. Removing Python cache files...")
    removed = cleanup_pycache()
    all_removed.extend(removed)
    if removed:
        print(f"   ✓ Removed {len(removed)} cache files/directories")
    else:
        print("   ✓ No cache files found")
    
    # 6. Create/update .gitignore
    print("\n6. Creating/updating .gitignore...")
    gitignore_path = create_gitignore()
    print(f"   ✓ Created/updated: {gitignore_path}")
    
    print(f"\n🎉 Cleanup completed! Removed {len(all_removed)} files/directories.")
    
    print("\n📋 Summary of changes:")
    print("   • Removed SQLite database files")
    print("   • Removed Flask-Migrate dependencies")
    print("   • Removed debug scripts")
    print("   • Removed unused deployment configs")
    print("   • Cleaned Python cache files")
    print("   • Updated .gitignore")
    
    print("\n⚠️  Next steps:")
    print("   1. Run the migration script: python server/migrate_to_supabase.py")
    print("   2. Update your Render environment variables")
    print("   3. Test the application locally")
    print("   4. Deploy to Render")

if __name__ == "__main__":
    main()
