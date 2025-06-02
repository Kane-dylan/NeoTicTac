from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.game import Game
from app.models.user import User
from app import db

bp = Blueprint('game', __name__, url_prefix='/api/game')

@bp.route('/active', methods=['GET'])
@jwt_required() 
def get_active_games():
    try:
        games = Game.query.filter(Game.player_o.is_(None), Game.winner.is_(None)).all()
        return jsonify([{
            'id': game.id,
            'host': game.player_x,
            'createdAt': game.id,
            'playerCount': 1 if game.player_o is None else 2
        } for game in games])
    except Exception as e:
        return jsonify({'msg': 'Failed to fetch games', 'error': str(e)}), 500

@bp.route('/create', methods=['POST'])
@jwt_required()
def create_game():
    try:
        username = get_jwt_identity()
        game = Game(player_x=username)
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'gameId': game.id,
            'msg': 'Game created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to create game', 'error': str(e)}), 500

@bp.route('/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    try:
        game = Game.query.get_or_404(game_id)
        return jsonify({
            'id': game.id,
            'player_x': game.player_x,
            'player_o': game.player_o,
            'board': game.board,
            'current_turn': game.current_turn,
            'winner': game.winner,
            'is_draw': game.is_draw
        })
    except Exception as e:
        return jsonify({'msg': 'Game not found', 'error': str(e)}), 404
