"""
Final Authentication Test
"""
import requests
import json

def test_final():
    print("🧪 Final Authentication Test")
    print("="*40)
    
    # Test registration
    print("Testing registration...")
    reg_data = {"username": "finaltest", "password": "password123"}
    
    try:
        reg_response = requests.post(
            "http://localhost:5000/api/auth/register",
            json=reg_data,
            timeout=5
        )
        print(f"Registration: {reg_response.status_code} - {reg_response.text[:100]}")
        
        # Test login
        print("Testing login...")
        login_response = requests.post(
            "http://localhost:5000/api/auth/login", 
            json=reg_data,
            timeout=5
        )
        print(f"Login: {login_response.status_code} - {login_response.text[:100]}")
        
        if login_response.status_code == 200:
            print("✅ SUCCESS! Authentication is working!")
            print("✅ Database schema fixed!")
            print("✅ Server ready for client testing!")
            return True
        else:
            print("❌ Login failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    test_final()

if __name__ == "__main__":
    main()
