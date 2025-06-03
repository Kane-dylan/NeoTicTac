from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token
import datetime
import traceback

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    try:
        current_app.logger.info("Registration attempt started")
        data = request.get_json()
        current_app.logger.info(f"Received data keys: {list(data.keys()) if data else 'None'}")
        
        if not data or 'username' not in data or 'password' not in data:
            current_app.logger.warning("Missing username or password in request")
            return jsonify({'msg': 'Username and password required'}), 400
        
        # Test database connection first
        try:
            current_app.logger.info("Testing database connection...")
            # Simple database test
            db.session.execute(db.text('SELECT 1'))
            current_app.logger.info("Database connection verified")
        except Exception as db_test_error:
            current_app.logger.error(f"Database connection failed: {db_test_error}")
            return jsonify({'msg': 'Database service temporarily unavailable', 'error': str(db_test_error)}), 503
        
        # Check if user exists
        try:
            current_app.logger.info(f"Checking if user {data['username']} exists...")
            existing_user = User.query.filter_by(username=data['username']).first()
            current_app.logger.info("User existence check successful")
            
            if existing_user:
                current_app.logger.info(f"User {data['username']} already exists")
                return jsonify({'msg': 'User already exists'}), 400
                
        except Exception as db_error:
            current_app.logger.error(f"Database query failed: {str(db_error)}")
            current_app.logger.error(f"Database error traceback: {traceback.format_exc()}")
            return jsonify({'msg': 'Database connection failed', 'error': str(db_error)}), 500
            
        # Create new user
        current_app.logger.info(f"Creating new user: {data['username']}")
        user = User(username=data['username'])
        user.set_password(data['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f"User {data['username']} registered successfully")
            return jsonify({'msg': 'User registered'}), 201
            
        except Exception as commit_error:
            db.session.rollback()
            current_app.logger.error(f"Database commit failed: {str(commit_error)}")
            current_app.logger.error(f"Commit error traceback: {traceback.format_exc()}")
            return jsonify({'msg': 'Failed to save user', 'error': str(commit_error)}), 500
        
    except Exception as e:
        current_app.logger.error(f"Registration failed with unexpected error: {str(e)}")
        current_app.logger.error(f"Full traceback: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'msg': 'Registration failed', 'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        current_app.logger.info("Login attempt started")
        data = request.get_json()
        current_app.logger.info(f"Login attempt for username: {data.get('username') if data else 'None'}")
        
        if not data or 'username' not in data or 'password' not in data:
            current_app.logger.warning("Missing username or password in login request")
            return jsonify({'msg': 'Username and password required'}), 400
        
        try:
            current_app.logger.info("Querying database for user...")
            user = User.query.filter_by(username=data['username']).first()
            current_app.logger.info("Database query completed")
            
            if not user or not user.check_password(data['password']):
                current_app.logger.warning(f"Invalid login attempt for user: {data['username']}")
                return jsonify({'msg': 'Invalid credentials'}), 401
                
            current_app.logger.info(f"Successful login for user: {data['username']}")
            token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(days=1))
            return jsonify({'token': token})
            
        except Exception as db_error:
            current_app.logger.error(f"Database error during login: {str(db_error)}")
            current_app.logger.error(f"Login database error traceback: {traceback.format_exc()}")
            return jsonify({'msg': 'Database error during login', 'error': str(db_error)}), 500
        
    except Exception as e:
        current_app.logger.error(f"Login failed with unexpected error: {str(e)}")
        current_app.logger.error(f"Login full traceback: {traceback.format_exc()}")
        return jsonify({'msg': 'Login failed', 'error': str(e)}), 500

@bp.route('/check', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    try:
        current_app.logger.info("Health check endpoint accessed")
        # Test database connection
        try:
            with db.engine.connect() as connection:
                connection.execute(db.text('SELECT 1'))
            current_app.logger.info("Database connection successful")
            db_status = "connected"
        except Exception as db_error:
            current_app.logger.error(f"Database connection failed: {str(db_error)}")
            db_status = f"failed: {str(db_error)}"
        
        return jsonify({
            'status': 'healthy',
            'message': 'Tic-Tac-Toe API is running',
            'database': db_status,
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Health check failed',
            'error': str(e),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 500

@bp.route('/status', methods=['GET'])
def simple_status():
    """Simple status endpoint that doesn't require database"""
    return jsonify({
        'status': 'running',
        'message': 'Tic-Tac-Toe API is operational',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }), 200
        
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Health check failed',
            'error': str(e),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 500
