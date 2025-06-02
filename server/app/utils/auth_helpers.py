from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

def get_current_user():
    """Get the current authenticated user"""
    username = get_jwt_identity()
    return User.query.filter_by(username=username).first()

def auth_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function
