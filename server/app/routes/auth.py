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
        
        if not data or 'username' not in data or 'password' not in data:
            current_app.logger.warning("Missing username or password in request")
            return jsonify({'msg': 'Username and password required'}), 400
        
        # Check if user exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            current_app.logger.info(f"User {data['username']} already exists")
            return jsonify({'msg': 'User already exists'}), 400
                
        # Create new user
        current_app.logger.info(f"Creating new user: {data['username']}")
        user = User(username=data['username'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        current_app.logger.info(f"User {data['username']} registered successfully")
        return jsonify({'msg': 'User registered'}), 201
        
    except Exception as e:
        current_app.logger.error(f"Registration failed: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'msg': 'Registration failed', 'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        current_app.logger.info("Login attempt started")
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            current_app.logger.warning("Missing username or password in login request")
            return jsonify({'msg': 'Username and password required'}), 400
                
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            current_app.logger.warning(f"Invalid login attempt for user: {data['username']}")
            return jsonify({'msg': 'Invalid credentials'}), 401
            
        current_app.logger.info(f"Successful login for user: {data['username']}")
        token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(days=1))
        return jsonify({'token': token})
        
    except Exception as e:
        current_app.logger.error(f"Login failed: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'msg': 'Login failed', 'error': str(e)}), 500

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with db.engine.connect() as connection:
            connection.execute(db.text('SELECT 1'))
        
        return jsonify({
            'status': 'healthy',
            'message': 'Tic-Tac-Toe API is running',
            'database': 'connected',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Health check failed',
            'database': f'failed: {str(e)}',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 500
    return jsonify({
        'status': 'running',
        'message': 'Tic-Tac-Toe API is operational',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }), 200
