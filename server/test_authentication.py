"""
Authentication Test Script
This will test user registration and login functionality
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test configuration
SERVER_URL = "http://localhost:5000"  # For local testing
# SERVER_URL = "https://tictactoe-nj7l.onrender.com"  # For production testing

def test_user_registration():
    """Test user registration"""
    print("🧪 Testing user registration...")
    
    test_user = {
        "username": "test_user_auth",
        "password": "test_password123"
    }
    
    try:
        response = requests.post(
            f"{SERVER_URL}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Registration status: {response.status_code}")
        print(f"Registration response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print("ℹ️ User already exists, proceeding to login test")
            return True
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_user_login():
    """Test user login"""
    print("🧪 Testing user login...")
    
    test_user = {
        "username": "test_user_auth", 
        "password": "test_password123"
    }
    
    try:
        response = requests.post(
            f"{SERVER_URL}/api/auth/login",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Login status: {response.status_code}")
        print(f"Login response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                print("✅ Login successful!")
                print(f"Token received: {data['token'][:20]}...")
                return data["token"]
            else:
                print("❌ Login response missing token")
                return None
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_server_health():
    """Test server health endpoint"""
    print("🧪 Testing server health...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/auth/health", timeout=10)
        
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Server health check passed!")
            return True
        else:
            print("❌ Server health check failed!")
            return False
            
    except Exception as e:
        print(f"❌ Server health check error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting authentication tests...")
    print(f"Testing server at: {SERVER_URL}")
    print("="*50)
    
    # Test 1: Server health
    if not test_server_health():
        print("❌ Server is not responding. Please start the server first.")
        return False
    
    print("\n" + "="*50)
    
    # Test 2: User registration
    if not test_user_registration():
        print("❌ Registration test failed")
        return False
    
    print("\n" + "="*50)
    
    # Test 3: User login
    token = test_user_login()
    if not token:
        print("❌ Login test failed")
        return False
    
    print("\n" + "="*50)
    print("🎉 ALL AUTHENTICATION TESTS PASSED!")
    print("✅ Database schema is working correctly")
    print("✅ User registration works")
    print("✅ User login works")
    print("✅ JWT token generation works")
    print("="*50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
