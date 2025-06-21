from app import db
from sqlalchemy import Text, DateTime, Integer, String, Boolean
import json
from datetime import datetime

class Game(db.Model):
    __tablename__ = 'game'
    
    # Use SERIAL for PostgreSQL auto-increment
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    player_x = db.Column(String(80), nullable=False)
    player_o = db.Column(String(80), nullable=True)
    board = db.Column(Text, default='["","","","","","","","",""]', nullable=False)
    current_turn = db.Column(String(1), default='X', nullable=False)
    winner = db.Column(String(1), nullable=True)
    is_draw = db.Column(Boolean, default=False, nullable=False)
    winning_line = db.Column(Text, nullable=True)  # Store winning line indices as JSON
    # Use timezone-aware timestamp for PostgreSQL
    created_at = db.Column(DateTime(timezone=True), default=db.func.now(), nullable=False)
    
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
    
    @property
    def winning_line_data(self):
        """Get winning line as a list"""
        try:
            if self.winning_line and isinstance(self.winning_line, str):
                return json.loads(self.winning_line)
            elif isinstance(self.winning_line, list):
                return self.winning_line
            else:
                return None
        except (json.JSONDecodeError, TypeError):
            return None
    
    @winning_line_data.setter
    def winning_line_data(self, value):
        """Set winning line from a list"""
        if isinstance(value, list):
            self.winning_line = json.dumps(value)
        else:
            self.winning_line = None
    
    def to_dict(self):
        """Convert game object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'player_x': self.player_x,
            'player_o': self.player_o,
            'board': self.board_data,
            'current_turn': self.current_turn,
            'winner': self.winner,
            'is_draw': self.is_draw,
            'winning_line': self.winning_line_data,
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
