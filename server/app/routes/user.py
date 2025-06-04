import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.models.game import Game
from app import db

logger = logging.getLogger(__name__)

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get the current user's profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Count the user's games
        games_as_player1 = Game.query.filter_by(player1_id=user.id).count()
        games_as_player2 = Game.query.filter_by(player2_id=user.id).count()
        total_games = games_as_player1 + games_as_player2

        # Format timestamps
        created_at = user.created_at.isoformat() if user.created_at else None
        last_login = user.last_login.isoformat() if user.last_login else None

        return jsonify({
            'id': user.id,
            'username': user.username,
            'created_at': created_at,
            'last_login': last_login,
            'stats': {
                'total_games': total_games
            }
        }), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error in profile endpoint: {e}")
        return jsonify({
            'message': 'Database error',
            'error': str(e)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in profile endpoint: {e}")
        return jsonify({
            'message': 'An unexpected error occurred',
            'error': str(e)
        }), 500

@bp.route('/update', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the current user's profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json()

        # Only allow updating certain fields
        if 'username' in data and data['username'] != user.username:
            # Check if username is already taken
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'message': 'Username already taken'}), 409

            user.username = data['username']

        # Update password if provided
        if 'password' in data and data['password']:
            from werkzeug.security import generate_password_hash
            user.password_hash = generate_password_hash(data['password'])

        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in update profile endpoint: {e}")
        return jsonify({
            'message': 'Database error',
            'error': str(e)
        }), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in update profile endpoint: {e}")
        return jsonify({
            'message': 'An unexpected error occurred',
            'error': str(e)
        }), 500
