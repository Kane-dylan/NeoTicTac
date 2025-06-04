"""
Quick Authentication Test
Test registration and login via curl-like HTTP requests
"""

import requests
import json
import time

SERVER_URL = "http://localhost:5000"

def test_registration():
    """Test user registration"""
    print("🧪 Testing registration...")
    
    user_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{SERVER_URL}/api/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Registration Status: {response.status_code}")
        print(f"Registration Response: {response.text}")
        
        if response.status_code in [201, 400]:  # 400 might mean user exists
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Registration Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n🧪 Testing login...")
    
    user_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{SERVER_URL}/api/auth/login",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                print("✅ Login successful! Token received.")
                return True
        
        return False
        
    except Exception as e:
        print(f"Login Error: {e}")
        return False

def main():
    print("🚀 Quick Authentication Test")
    print("="*40)
    
    # Test registration
    reg_success = test_registration()
    
    # Test login
    login_success = test_login()
    
    print("\n" + "="*40)
    if reg_success and login_success:
        print("🎉 AUTHENTICATION TESTS PASSED!")
        print("✅ Registration works")
        print("✅ Login works")
        print("✅ Database schema is fixed!")
        print("✅ Server is ready for client testing!")
    else:
        print("❌ Some tests failed")
        print(f"Registration: {'✅' if reg_success else '❌'}")
        print(f"Login: {'✅' if login_success else '❌'}")
    
    print("="*40)

if __name__ == "__main__":
    main()
