from dotenv import load_dotenv
import os
load_dotenv()

try:
    from app import create_app, socketio, db
    
    # Create the app instance
    app = create_app()    # Initialize database tables
    def init_db():
        """Initialize database tables with fallback to SQLite"""
        with app.app_context():
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            external_db_url = app.config.get('EXTERNAL_DATABASE_URL')
            fallback_db_uri = app.config.get('FALLBACK_DATABASE_URI', 'sqlite:///tictactoe.db')
            
            print("Initializing database...")
            print(f"Primary Database URI: {db_uri}")
            
            # First attempt with primary database
            success = False
            try:
                print("Testing primary database connection...")
                with db.engine.connect() as connection:
                    result = connection.execute(db.text('SELECT 1'))
                    print("Primary database connection successful")
                
                # Create tables
                print("Creating database tables...")
                db.create_all()
                print("Database tables created successfully")
                
                # Test table creation by querying User table
                try:
                    from app.models.user import User
                    user_count = User.query.count()
                    print(f"User table accessible, current count: {user_count}")
                    success = True
                except Exception as table_error:
                    print(f"Warning: Could not query User table: {table_error}")
                    success = True  # Connection works, table query failed but that's ok
                
            except Exception as e:
                print(f"Primary database error: {e}")
                print(f"Database error type: {type(e)}")
                
                # Attempt fallback to SQLite if we have an external database URL that failed
                if external_db_url and db_uri != fallback_db_uri:
                    print("Attempting fallback to SQLite...")
                    try:
                        # Update the database URI to SQLite
                        app.config['SQLALCHEMY_DATABASE_URI'] = fallback_db_uri
                        
                        # Re-initialize database with SQLite
                        from sqlalchemy import create_engine
                        from flask_sqlalchemy import SQLAlchemy
                        
                        # Create new engine for SQLite
                        sqlite_engine = create_engine(fallback_db_uri)
                        db.engine = sqlite_engine
                          
                        # Test the fallback connection
                        with db.engine.connect() as connection:
                            result = connection.execute(db.text('SELECT 1'))
                            print("Fallback database connection successful")
                        
                        # Create tables in SQLite
                        print("Creating database tables in SQLite...")
                        db.create_all()
                        print("SQLite database tables created successfully")
                        
                        # Test SQLite table creation
                        try:
                            from app.models.user import User
                            user_count = User.query.count()
                            print(f"SQLite User table accessible, current count: {user_count}")
                            success = True
                        except Exception as sqlite_table_error:
                            print(f"Warning: Could not query SQLite User table: {sqlite_table_error}")
                            success = True  # Connection works, table query failed but that's ok
                            
                    except Exception as fallback_error:
                        print(f"Fallback to SQLite also failed: {fallback_error}")
                        import traceback
                        print(f"Full fallback traceback: {traceback.format_exc()}")
                else:
                    print("No fallback database configured or already using fallback.")
                    import traceback
                    print(f"Full traceback: {traceback.format_exc()}")
            
            if not success:
                print("All database initialization attempts failed.")
                # For production, create a minimal working database setup
                if os.getenv('FLASK_ENV') != 'development':
                    print("Production environment: Creating emergency SQLite fallback...")
                    try:
                        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emergency.db'
                        from sqlalchemy import create_engine
                        emergency_engine = create_engine('sqlite:///emergency.db')
                        db.engine = emergency_engine
                        db.create_all()
                        print("Emergency SQLite database created successfully")
                    except Exception as emergency_error:
                        print(f"Emergency fallback failed: {emergency_error}")
                        print("Server will start but database operations will fail.")

    # Initialize database on startup
    init_db()

    if __name__ == '__main__':
        # Development server only
        print("Starting development server...")
        try:
            socketio.run(
                app, 
                host='0.0.0.0', 
                port=int(os.getenv('PORT', 5000)),
                debug=os.getenv('FLASK_ENV') == 'development',
                allow_unsafe_werkzeug=True
            )
        except Exception as e:
            print(f"Failed to start server: {e}")
    
    # For production (Gunicorn will import 'app' from this module)
    # This makes the 'app' variable available to Gunicorn
            
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required dependencies:")
    print("pip install flask flask-cors flask-sqlalchemy flask-migrate flask-jwt-extended flask-socketio python-dotenv psycopg2-binary")
except Exception as e:
    print(f"Startup error: {e}")
    # Create a dummy app for Gunicorn if there's an error
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return {'status': 'error', 'message': 'Server failed to initialize properly'}
