#!/usr/bin/env python3
"""
Quick verification that authentication endpoints are working
"""
import requests
import json
import time

def verify_authentication():
    print("🔍 Verifying Authentication Fix")
    print("="*40)
    
    # Test unique user for verification
    timestamp = int(time.time())
    test_user = f"verifyuser{timestamp}"
    test_data = {"username": test_user, "password": "testpass123"}
    
    try:
        # Test registration
        print(f"1. Testing registration for user: {test_user}")
        reg_response = requests.post(
            "http://localhost:5000/api/auth/register",
            json=test_data,
            timeout=3
        )
        
        if reg_response.status_code == 201:
            print("✅ Registration successful!")
        else:
            print(f"❌ Registration failed: {reg_response.status_code} - {reg_response.text}")
            return False
        
        # Test login
        print("2. Testing login...")
        login_response = requests.post(
            "http://localhost:5000/api/auth/login",
            json=test_data,
            timeout=3
        )
        
        if login_response.status_code == 200:
            print("✅ Login successful!")
            response_data = login_response.json()
            if "token" in response_data:
                print("✅ JWT token received!")
                print(f"   Token preview: {response_data['token'][:50]}...")
            print("\n🎉 SUCCESS: Database and authentication fully fixed!")
            print("🎉 The original 500 error has been resolved!")
            return True
        else:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running on port 5000?")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    verify_authentication()
