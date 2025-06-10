import os
import logging
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app import db

# Set up logging
logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Log incoming request data (sanitized)
        logger.info(f"Registration attempt for username: {data.get('username', 'unknown')}")

        # Validate input
        if not data or not data.get('username') or not data.get('password'):
            logger.warning("Invalid registration data provided")
            return jsonify({'message': 'Username and password required'}), 400

        # Check if user already exists
        try:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                logger.warning(f"Registration failed: Username '{data['username']}' already exists")
                return jsonify({'message': 'Username already exists'}), 409
        except SQLAlchemyError as e:
            logger.error(f"Database error when checking existing user: {str(e)}")
            return jsonify({
                'message': 'Server encountered a database error',
                'error': 'database_error'
            }), 500

        # Create new user
        try:
            new_user = User(
                username=data['username'],
                password_hash=generate_password_hash(data['password'])
            )
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error when creating user: {str(e)}")
            return jsonify({
                'message': 'Server encountered a database error',
                'error': 'database_error'
            }), 500

        # Create access token
        access_token = create_access_token(identity=new_user.id)

        logger.info(f"User registered successfully: {data['username']}")
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': new_user.id,
                'username': new_user.username
            }
        }), 201

    except Exception as e:
        logger.error(f"Unexpected error in registration: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred',
            'error': 'server_error',
            'error_details': str(e) if current_app.debug else None
        }), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Log login attempt (username only)
        logger.info(f"Login attempt for username: {data.get('username', 'unknown')}")

        # Validate input
        if not data or not data.get('username') or not data.get('password'):
            logger.warning("Invalid login data provided")
            return jsonify({'message': 'Username and password required'}), 400

        try:
            # Find user
            user = User.query.filter_by(username=data['username']).first()

            # Check password
            if not user or not check_password_hash(user.password_hash, data['password']):
                logger.warning(f"Failed login attempt for username: {data.get('username')}")
                return jsonify({'message': 'Invalid username or password'}), 401
        except SQLAlchemyError as e:
            logger.error(f"Database error during login: {str(e)}")
            return jsonify({
                'message': 'Server encountered a database error',
                'error': 'database_error'
            }), 500

        # Create access token
        access_token = create_access_token(identity=user.id)

        logger.info(f"User logged in successfully: {user.username}")
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 200

    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred',
            'error': 'server_error',
            'error_details': str(e) if current_app.debug else None
        }), 500

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        # Get user ID from JWT
        user_id = get_jwt_identity()

        try:
            # Find user
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"Profile request for non-existent user ID: {user_id}")
                return jsonify({'message': 'User not found'}), 404
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching user profile: {str(e)}")
            return jsonify({
                'message': 'Server encountered a database error',
                'error': 'database_error'
            }), 500

        logger.info(f"Profile retrieved for user: {user.username}")
        return jsonify({
            'id': user.id,
            'username': user.username
        }), 200

    except Exception as e:
        logger.error(f"Unexpected error in profile endpoint: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred',
            'error': 'server_error',
            'error_details': str(e) if current_app.debug else None
        }), 500

# Health check endpoint for the auth service
@bp.route('/health', methods=['GET'])
def health():
    try:
        # Test database connection
        from sqlalchemy import text
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.close()

        return jsonify({
            'status': 'healthy',
            'message': 'Auth service is up and running',
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'message': 'Auth service is running but database is disconnected',
            'database': 'disconnected',
            'error': str(e) if current_app.debug else 'Database connection error'
        }), 503
