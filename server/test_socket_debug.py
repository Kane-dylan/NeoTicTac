#!/usr/bin/env python3
"""
Socket debugging test to verify the join_room functionality
"""

import requests
import time

# Test game creation and room joining
def test_game_room_logic():
    base_url = "http://localhost:5000"
      # Test 1: Check if game 10 exists
    try:
        response = requests.get(f"{base_url}/api/game/10")
        print(f"Game 10 status: {response.status_code}")
        if response.status_code == 200:
            game_data = response.json()
            print(f"Game 10 data: {game_data}")
        else:
            print(f"Game 10 not found or error: {response.text}")
    except Exception as e:
        print(f"Error checking game 10: {e}")
      # Test 2: Check all active games
    try:
        response = requests.get(f"{base_url}/api/game/active", headers={
            'Authorization': 'Bearer dummy'  # We'll need a proper token but let's test without auth first
        })
        print(f"Active games status: {response.status_code}")
        if response.status_code == 200:
            games_data = response.json()
            print(f"Active games: {games_data}")
        else:
            print(f"Error getting active games: {response.text}")
    except Exception as e:
        print(f"Error getting active games: {e}")

if __name__ == "__main__":
    print("🔍 Testing game room logic...")
    test_game_room_logic()
