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
        # Get ALL games from the database, ordered by newest first
        games = Game.query.order_by(Game.created_at.desc()).all()
        
        game_list = []
        for game in games:
            # Determine game status
            if game.winner or game.is_draw:
                status = 'completed'
                playerCount = 2 if game.player_o else 1
            elif game.player_o:
                status = 'in_progress'
                playerCount = 2
            else:
                status = 'waiting'
                playerCount = 1
            
            game_data = {
                'id': game.id,
                'host': game.player_x,
                'player_o': game.player_o,
                'createdAt': game.created_at.isoformat() if game.created_at else None,
                'playerCount': playerCount,
                'status': status,
                'winner': game.winner,
                'is_draw': game.is_draw,
                'current_turn': game.current_turn
            }
            game_list.append(game_data)
            
        return jsonify(game_list)
    except Exception as e:
        print(f"Error fetching active games: {str(e)}")
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
        game = Game.query.get(game_id)
        if not game:
            return jsonify({
                'msg': f'Game with ID {game_id} not found',
                'available_games': [g.id for g in Game.query.all()]
            }), 404
            
        # Ensure board is properly formatted
        board = game.board if hasattr(game, 'board') and game.board else [""] * 9
        if isinstance(board, str):
            try:
                import json
                board = json.loads(board)
            except:
                board = [""] * 9
        
        return jsonify({
            'id': game.id,
            'player_x': game.player_x,
            'player_o': game.player_o,
            'board': board,
            'current_turn': game.current_turn,
            'winner': game.winner,
            'is_draw': game.is_draw
        })
    except Exception as e:
        print(f"Error fetching game {game_id}: {str(e)}")
        return jsonify({
            'msg': 'Failed to fetch game', 
            'error': str(e),
            'game_id': game_id
        }), 500
