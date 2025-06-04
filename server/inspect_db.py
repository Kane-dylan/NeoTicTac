#!/usr/bin/env python3
"""
Script to inspect the current SQLite database and export data for migration
"""
import sqlite3
import json
import os
from datetime import datetime

def inspect_database():
    db_path = os.path.join('instance', 'tictactoe.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=== DATABASE SCHEMA ===")
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("Columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) {'PRIMARY KEY' if col[5] else ''} {'NOT NULL' if col[3] else ''}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Row count: {count}")
        
        # Show sample data if exists
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            print("Sample data:")
            for row in rows:
                print(f"  {row}")
    
    conn.close()

def export_data():
    """Export data to JSON files for migration"""
    db_path = os.path.join('instance', 'tictactoe.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    # Create export directory
    export_dir = 'migration_data'
    os.makedirs(export_dir, exist_ok=True)
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table_name in tables:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        data = []
        for row in rows:
            row_dict = {}
            for key in row.keys():
                value = row[key]
                # Handle datetime conversion if needed
                if isinstance(value, str) and 'created_at' in key.lower():
                    try:
                        # Try to parse as datetime
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        pass
                row_dict[key] = value
            data.append(row_dict)
        
        # Save to JSON file
        export_file = os.path.join(export_dir, f"{table_name}.json")
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"Exported {len(data)} rows from {table_name} to {export_file}")
    
    conn.close()

if __name__ == "__main__":
    print("Inspecting SQLite database...")
    inspect_database()
    print("\n" + "="*50)
    print("Exporting data for migration...")
    export_data()
