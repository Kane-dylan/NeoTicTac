from app import db
from sqlalchemy import Text, DateTime
import json
from datetime import datetime

class Game(db.Model):
    __tablename__ = 'game'
    
    id = db.Column(db.Integer, primary_key=True)
    player_x = db.Column(db.String(80), nullable=False)
    player_o = db.Column(db.String(80), nullable=True)
    board = db.Column(Text, default='["","","","","","","","",""]')
    current_turn = db.Column(db.String(1), default='X')
    winner = db.Column(db.String(1), nullable=True)
    is_draw = db.Column(db.Boolean, default=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        if not self.board:
            self.board = '["","","","","","","","",""]'
    
    @property
    def board_data(self):
        """Get board as a list"""
        try:
            if isinstance(self.board, str):
                return json.loads(self.board)
            elif isinstance(self.board, list):
                return self.board
            else:
                return [""] * 9
        except (json.JSONDecodeError, TypeError):
            return [""] * 9
    
    @board_data.setter
    def board_data(self, value):
        """Set board from a list"""
        if isinstance(value, list):
            self.board = json.dumps(value)
        else:
            self.board = '["","","","","","","","",""]'
    
    def to_dict(self):
        return {
            'id': self.id,
            'player_x': self.player_x,
            'player_o': self.player_o,
            'board': self.board_data,
            'current_turn': self.current_turn,
            'winner': self.winner,
            'is_draw': self.is_draw,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def is_player_turn(self, username):
        """Check if it's the given player's turn"""
        if self.current_turn == 'X':
            return username == self.player_x
        elif self.current_turn == 'O':
            return username == self.player_o
        return False
    
    def can_make_move(self, username):
        """Check if player can make a move"""
        if self.winner or self.is_draw:
            return False
        if not self.player_o:  # Need both players
            return False
        return self.is_player_turn(username)
