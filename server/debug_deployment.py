#!/usr/bin/env python3
"""
Deployment debugging script for Render
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== DEPLOYMENT DEBUG INFO ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Script location: {os.path.dirname(__file__)}")
print(f"Python path: {sys.path}")

print("\n=== ENVIRONMENT VARIABLES ===")
env_vars = [
    'FLASK_ENV',
    'DATABASE_URL',
    'PORT',
    'SECRET_KEY',
    'JWT_SECRET_KEY',
    'CLIENT_URL',
    'PYTHON_VERSION'
]

for var in env_vars:
    value = os.getenv(var)
    if var in ['SECRET_KEY', 'JWT_SECRET_KEY', 'DATABASE_URL']:
        print(f"{var}: {'SET' if value else 'NOT SET'}")
    else:
        print(f"{var}: {value or 'NOT SET'}")

print("\n=== CHECKING IMPORTS ===")
try:
    print("Importing Flask...")
    import flask
    print(f"Flask version: {flask.__version__}")
except ImportError as e:
    print(f"Flask import failed: {e}")

try:
    print("Importing app module...")
    from app import create_app
    print("App module imported successfully")
except ImportError as e:
    print(f"App import failed: {e}")
    sys.exit(1)

print("\n=== TESTING APP CREATION ===")
try:
    app = create_app()
    print("App created successfully")
    print(f"App name: {app.name}")
    print(f"App config: {app.config.get('FLASK_ENV')}")
    
    print("\n=== REGISTERED ROUTES ===")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
        
except Exception as e:
    print(f"App creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n=== DEPLOYMENT DEBUG COMPLETE ===")