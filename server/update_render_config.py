#!/usr/bin/env python3
"""
Script to update render.yaml with actual Supabase credentials
Run this after getting your Supabase project details from the dashboard
"""

import re

def update_render_yaml():
    """Update render.yaml with actual Supabase credentials"""
    
    print("🔧 Supabase Render Configuration Updater")
    print("=" * 50)
    
    # Get Supabase project details from user
    print("\n📋 Please provide your Supabase project details:")
    print("   (You can find these in your Supabase dashboard)")
    
    project_id = input("\n1. Enter your Supabase PROJECT ID: ").strip()
    if not project_id:
        print("❌ Project ID is required!")
        return False
    
    password = input("2. Enter your database PASSWORD: ").strip()  
    if not password:
        print("❌ Database password is required!")
        return False
    
    service_key = input("3. Enter your SERVICE ROLE KEY: ").strip()
    if not service_key:
        print("❌ Service role key is required!")
        return False
    
    # Read current render.yaml
    try:
        with open('render.yaml', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ render.yaml not found!")
        return False
    
    # Update placeholder values
    print("\n🔄 Updating render.yaml...")
      # Replace DATABASE_URL
    old_db_url = r'postgresql://postgres:YOUR_SUPABASE_PASSWORD@db\.YOUR_PROJECT_ID\.supabase\.co:6543/postgres\?pgbouncer=true'
    new_db_url = f'postgresql://postgres:{password}@db.{project_id}.supabase.co:5432/postgres'
    content = re.sub(old_db_url, new_db_url, content)
    
    # Replace SUPABASE_URL
    old_supabase_url = r'https://YOUR_PROJECT_ID\.supabase\.co'
    new_supabase_url = f'https://{project_id}.supabase.co'
    content = re.sub(old_supabase_url, new_supabase_url, content)
    
    # Replace SUPABASE_SERVICE_KEY
    content = content.replace('YOUR_SUPABASE_SERVICE_ROLE_KEY', service_key)
    
    # Write updated content
    try:
        with open('render.yaml', 'w') as f:
            f.write(content)
        print("✅ render.yaml updated successfully!")
        
        # Show what was updated
        print("\n📝 Updated values:")
        print(f"   - Project ID: {project_id}")
        print(f"   - Database URL: postgresql://postgres:***@db.{project_id}.supabase.co:5432/postgres")
        print(f"   - Supabase URL: https://{project_id}.supabase.co")
        print(f"   - Service Key: {service_key[:20]}...")
        
        print("\n🚀 Next steps:")
        print("   1. Commit and push these changes to your repository")
        print("   2. Redeploy your Render service")
        print("   3. Check the deployment logs for any issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing render.yaml: {e}")
        return False

if __name__ == "__main__":
    success = update_render_yaml()
    if success:
        print("\n🎉 Configuration updated successfully!")
    else:
        print("\n💥 Configuration update failed!")
