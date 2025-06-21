#!/usr/bin/env python3
"""
Simple migration script to add winning_line column
This script connects to the live database and adds the column if it doesn't exist
"""

import psycopg2
import os
import json
from urllib.parse import urlparse

def main():
    # Database connection parameters from environment or defaults
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("No DATABASE_URL found. This migration requires a live database connection.")
        print("Please ensure you have DATABASE_URL set in your environment.")
        return
    
    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        
        # Fix postgres:// to postgresql://
        if parsed.scheme == 'postgres':
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Connect to the database
        print(f"Connecting to database...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Check if the column already exists
        print("Checking if winning_line column exists...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'game' AND column_name = 'winning_line';
        """)
        
        result = cur.fetchone()
        
        if result:
            print("winning_line column already exists in the game table.")
        else:
            print("Adding winning_line column to game table...")
            cur.execute("ALTER TABLE game ADD COLUMN winning_line TEXT NULL;")
            conn.commit()
            print("Successfully added winning_line column to game table!")
            
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
