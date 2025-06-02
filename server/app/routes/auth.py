from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token
import datetime

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'msg': 'Username and password required'}), 400
            
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'msg': 'User already exists'}), 400
            
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'msg': 'User registered'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Registration failed', 'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'msg': 'Username and password required'}), 400
            
        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'msg': 'Invalid credentials'}), 401
            
        token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(days=1))
        return jsonify({'token': token})
        
    except Exception as e:
        return jsonify({'msg': 'Login failed', 'error': str(e)}), 500
