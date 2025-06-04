from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import BigInteger
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    # Use BIGSERIAL for PostgreSQL auto-increment
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Use timezone-aware timestamp for PostgreSQL
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    games_as_player1 = db.relationship('Game', foreign_keys='Game.player1_id', backref='player1', lazy=True)
    games_as_player2 = db.relationship('Game', foreign_keys='Game.player2_id', backref='player2', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.username}>'
