#!/usr/bin/env python3
"""
Test the complete application setup after migration
"""
import os
import sys
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

def test_supabase_connection():
    """Test basic Supabase connection and schema"""
    load_dotenv()
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY')
    
    if not url or not key:
        print("❌ Missing Supabase credentials")
        return False
    
    try:
        supabase = create_client(url, key)
        print("✅ Supabase connection successful")
        
        # Test users table
        result = supabase.table('users').select('count').execute()
        print("✅ Users table accessible")
        
        # Test games table
        result = supabase.table('games').select('count').execute()
        print("✅ Games table accessible")
        
        return True
    except Exception as e:
        print(f"❌ Connection/Schema error: {e}")
        return False

def test_user_operations():
    """Test user creation and authentication operations"""
    load_dotenv()
    supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))
    
    try:
        # Test user creation
        test_user = {
            'username': f'testuser_{int(datetime.now().timestamp())}',
            'email': f'test_{int(datetime.now().timestamp())}@example.com',
            'password_hash': 'test_hash_123'
        }
        
        result = supabase.table('users').insert(test_user).execute()
        print("✅ User creation successful")
        
        user_id = result.data[0]['id']
        
        # Test user lookup
        result = supabase.table('users').select('*').eq('username', test_user['username']).execute()
        print("✅ User lookup successful")
        
        # Clean up test user
        supabase.table('users').delete().eq('id', user_id).execute()
        print("✅ Test cleanup successful")
        
        return True
    except Exception as e:
        print(f"❌ User operations error: {e}")
        return False

def test_game_operations():
    """Test game creation and management operations"""
    load_dotenv()
    supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))
    
    try:
        # Create test users first
        test_user1 = {
            'username': f'player1_{int(datetime.now().timestamp())}',
            'email': f'player1_{int(datetime.now().timestamp())}@example.com',
            'password_hash': 'test_hash_123'
        }
        
        test_user2 = {
            'username': f'player2_{int(datetime.now().timestamp())}',
            'email': f'player2_{int(datetime.now().timestamp())}@example.com',
            'password_hash': 'test_hash_456'
        }
        
        user1_result = supabase.table('users').insert(test_user1).execute()
        user2_result = supabase.table('users').insert(test_user2).execute()
        
        user1_id = user1_result.data[0]['id']
        user2_id = user2_result.data[0]['id']
        
        # Test game creation
        test_game = {
            'board': '["","","","","","","","",""]',
            'current_player': 'X',
            'player_x_id': user1_id,
            'player_o_id': user2_id
        }
        
        result = supabase.table('games').insert(test_game).execute()
        game_id = result.data[0]['id']
        print("✅ Game creation successful")
        
        # Test game update
        updated_board = '["X","","","","","","","",""]'
        supabase.table('games').update({'board': updated_board, 'current_player': 'O'}).eq('id', game_id).execute()
        print("✅ Game update successful")
        
        # Test game lookup
        result = supabase.table('games').select('*').eq('id', game_id).execute()
        print("✅ Game lookup successful")
        
        # Clean up
        supabase.table('games').delete().eq('id', game_id).execute()
        supabase.table('users').delete().eq('id', user1_id).execute()
        supabase.table('users').delete().eq('id', user2_id).execute()
        print("✅ Test cleanup successful")
        
        return True
    except Exception as e:
        print(f"❌ Game operations error: {e}")
        return False

def test_flask_app_config():
    """Test Flask application configuration"""
    try:
        # Add server directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from config import Config
        config = Config()
        
        print("✅ Flask config loaded successfully")
        print(f"✅ Database URL configured: {bool(config.DATABASE_URL)}")
        print(f"✅ Secret key configured: {bool(config.SECRET_KEY)}")
        print(f"✅ JWT secret configured: {bool(config.JWT_SECRET_KEY)}")
        
        return True
    except Exception as e:
        print(f"❌ Flask config error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Complete Application Setup")
    print("=" * 50)
    
    tests = [
        ("Supabase Connection", test_supabase_connection),
        ("User Operations", test_user_operations),
        ("Game Operations", test_game_operations),
        ("Flask Configuration", test_flask_app_config)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your application is ready for deployment.")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Please fix the issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
