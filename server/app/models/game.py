from app import db
from sqlalchemy.dialects.sqlite import JSON

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_x = db.Column(db.String(80))
    player_o = db.Column(db.String(80))
    board = db.Column(JSON, default=[""] * 9)
    current_turn = db.Column(db.String(1), default='X')
    winner = db.Column(db.String(1), nullable=True)
    is_draw = db.Column(db.Boolean, default=False)
