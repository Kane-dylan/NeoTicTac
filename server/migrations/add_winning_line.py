"""Add winning_line column to games table

Revision ID: add_winning_line
Revises: 
Create Date: 2024-06-22

"""
import sys
import os

# Add the server directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def upgrade():
    """Add the winning_line column to store winning line indices"""
    try:
        from app import create_app, db
        from sqlalchemy import text
        
        # Check if we're in a test environment
        app = create_app()
        
        # If no database is configured, use SQLite for development
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tic_tac_toe_dev.db'
        
        with app.app_context():
            # Check if column already exists
            try:
                # Try a more compatible way to check for column existence
                inspector = db.inspect(db.engine)
                columns = [col['name'] for col in inspector.get_columns('game')]
                
                if 'winning_line' not in columns:
                    # Add the new column
                    if 'sqlite' in str(db.engine.url):
                        sql = "ALTER TABLE game ADD COLUMN winning_line TEXT NULL;"
                    else:
                        sql = "ALTER TABLE game ADD COLUMN IF NOT EXISTS winning_line TEXT NULL;"
                    
                    db.session.execute(text(sql))
                    db.session.commit()
                    print("Successfully added winning_line column to game table")
                else:
                    print("winning_line column already exists in game table")
                    
            except Exception as e:
                print(f"Error checking/adding column: {e}")
                # If we can't inspect, just try to add and handle the error
                try:
                    if 'sqlite' in str(db.engine.url):
                        sql = "ALTER TABLE game ADD COLUMN winning_line TEXT NULL;"
                    else:
                        sql = "ALTER TABLE game ADD COLUMN IF NOT EXISTS winning_line TEXT NULL;"
                    
                    db.session.execute(text(sql))
                    db.session.commit()
                    print("Successfully added winning_line column to game table")
                except Exception as e2:
                    if "duplicate column name" in str(e2).lower() or "already exists" in str(e2).lower():
                        print("winning_line column already exists in game table")
                    else:
                        raise e2
        
    except Exception as e:
        print(f"Error adding winning_line column: {e}")
        try:
            db.session.rollback()
        except:
            pass

def downgrade():
    """Remove the winning_line column"""
    try:
        from app import create_app, db
        
        app = create_app()
        with app.app_context():
            sql = """
            ALTER TABLE game 
            DROP COLUMN IF EXISTS winning_line;
            """
            
            db.session.execute(sql)
            db.session.commit()
            print("Successfully removed winning_line column from game table")
        
    except Exception as e:
        print(f"Error removing winning_line column: {e}")
        try:
            db.session.rollback()
        except:
            pass

if __name__ == "__main__":
    upgrade()
