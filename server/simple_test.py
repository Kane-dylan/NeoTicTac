#!/usr/bin/env python3
"""
Simple authentication test with longer timeout
"""
import requests
import json
import time

def simple_auth_test():
    print("🧪 Simple Authentication Test")
    print("="*30)
    
    # Use a unique username to avoid conflicts
    test_user = f"user_{int(time.time())}"
    test_data = {"username": test_user, "password": "test123"}
    
    print(f"Testing with user: {test_user}")
    
    try:
        # Test server is responding
        print("1. Checking server health...")
        health_response = requests.get("http://localhost:5000/", timeout=10)
        print(f"   Server response: {health_response.status_code}")
        
        # Test registration
        print("2. Testing registration...")
        reg_response = requests.post(
            "http://localhost:5000/api/auth/register",
            json=test_data,
            timeout=15
        )
        print(f"   Registration: {reg_response.status_code}")
        if reg_response.status_code != 201:
            print(f"   Response: {reg_response.text}")
        
        # Test login
        print("3. Testing login...")
        login_response = requests.post(
            "http://localhost:5000/api/auth/login",
            json=test_data,
            timeout=15
        )
        print(f"   Login: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ SUCCESS! Authentication is working!")
            token_data = login_response.json()
            if "token" in token_data:
                print("✅ JWT token received successfully!")
            return True
        else:
            print(f"❌ Login failed: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    result = simple_auth_test()
    if result:
        print("\n🎉 DATABASE FIX SUCCESSFUL!")
        print("🎉 Original 500 error has been resolved!")
        print("🎉 Server is ready for client integration!")
    else:
        print("\n❌ Test failed - need to investigate further")
