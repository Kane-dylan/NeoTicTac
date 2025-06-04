#!/usr/bin/env python3
"""
Final deployment readiness check
"""
import os
import sys
from dotenv import load_dotenv

def check_environment_variables():
    """Check all required environment variables"""
    load_dotenv()
    
    required_vars = {
        'SECRET_KEY': 'Flask secret key',
        'JWT_SECRET_KEY': 'JWT secret key', 
        'SUPABASE_URL': 'Supabase project URL',
        'SUPABASE_SERVICE_KEY': 'Supabase service role key',
        'DATABASE_URL': 'PostgreSQL connection string',
        'CLIENT_URL': 'Client application URL'
    }
    
    print("🔍 Environment Variables Check:")
    print("-" * 40)
    
    all_set = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'URL' in var:
                display_value = f"{value[:20]}..." if len(value) > 20 else value
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET ({description})")
            all_set = False
    
    return all_set

def check_file_structure():
    """Check that all required files exist"""
    required_files = [
        'render.yaml',
        'server/requirements.txt',
        'server/wsgi.py',
        'server/config.py',
        'server/app/__init__.py',
        'server/app/models/user.py',
        'server/app/models/game.py',
        'server/supabase_schema.sql'
    ]
    
    print("\n🗂️  File Structure Check:")
    print("-" * 40)
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}: MISSING")
            all_exist = False
    
    return all_exist

def check_render_config():
    """Check render.yaml configuration"""
    if not os.path.exists('render.yaml'):
        print("\n❌ render.yaml not found")
        return False
    
    print("\n⚙️  Render Configuration Check:")
    print("-" * 40)
    
    with open('render.yaml', 'r') as f:
        content = f.read()
    
    checks = [
        ('Python service type', 'type: web' in content and 'env: python' in content),
        ('Build command', 'pip install -r requirements.txt' in content),
        ('Start command', 'gunicorn' in content and 'wsgi:app' in content),
        ('Environment variables', 'SECRET_KEY' in content and 'SUPABASE_URL' in content),
        ('Correct paths', 'cd server' in content)
    ]
    
    all_good = True
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_good = False
    
    return all_good

def check_supabase_schema():
    """Check if Supabase schema file is ready"""
    schema_file = 'server/supabase_schema.sql'
    if not os.path.exists(schema_file):
        print(f"\n❌ Schema file not found: {schema_file}")
        return False
    
    print("\n🗄️  Database Schema Check:")
    print("-" * 40)
    
    with open(schema_file, 'r') as f:
        content = f.read()
    
    required_elements = [
        ('Users table', 'CREATE TABLE users' in content),
        ('Games table', 'CREATE TABLE games' in content),
        ('Indexes', 'CREATE INDEX' in content),
        ('UUID extension', 'uuid-ossp' in content),
        ('Proper data types', 'BIGSERIAL' in content and 'TIMESTAMP WITH TIME ZONE' in content)
    ]
    
    all_present = True
    for element, check in required_elements:
        status = "✅" if check else "❌"
        print(f"{status} {element}")
        if not check:
            all_present = False
    
    return all_present

def display_next_steps():
    """Display final deployment steps"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT READINESS SUMMARY")
    print("="*60)
    print("\n📋 MANUAL STEPS REQUIRED:")
    print("\n1. 🗄️  CREATE DATABASE SCHEMA:")
    print("   • Go to https://supabase.com/dashboard")
    print("   • Select project: your-project-id")
    print("   • Go to SQL Editor")
    print("   • Copy contents of server/supabase_schema.sql")
    print("   • Run the SQL commands")
    
    print("\n2. 🧪 VERIFY SETUP:")
    print("   • cd server")
    print("   • python test_setup.py")
    
    print("\n3. 🚀 DEPLOY TO RENDER:")
    print("   • Push code to GitHub")
    print("   • Render will auto-deploy")
    print("   • Monitor logs for any issues")
    
    print("\n4. ✅ TEST PRODUCTION:")
    print("   • Visit your Render app URL")
    print("   • Test user registration/login")  
    print("   • Create and play a game")
    print("   • Verify data persistence")

def main():
    """Run all deployment checks"""
    print("🎯 TIC-TAC-TOE DEPLOYMENT READINESS CHECK")
    print("="*60)
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("File Structure", check_file_structure), 
        ("Render Configuration", check_render_config),
        ("Database Schema", check_supabase_schema)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name}: Error - {e}")
            results.append((check_name, False))
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n📊 CHECKS PASSED: {passed}/{total}")
    
    for check_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED! Ready for deployment.")
        display_next_steps()
        return True
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
