from flask_socketio import emit, join_room, leave_room
from flask import request
from flask_jwt_extended import decode_token
from jwt.exceptions import DecodeError, InvalidTokenError
from app.models.game import Game
from app.services.game_logic import check_winner, is_draw
from app import db, socketio
from datetime import datetime

# Store active connections and game rooms
active_connections = {}  # {username: socket_id}
game_rooms = {}  # {game_id: {players: set(), spectators: set(), room_name: str}}

def register_socket_handlers(socketio):
    @socketio.on('connect')
    def on_connect(auth):
        try:
            print(f"New socket connection: {request.sid}")
            if auth and 'token' in auth:
                token = auth['token']
                if token and token not in ['null', 'undefined', '']:
                    decoded_token = decode_token(token)
                    username = decoded_token['sub']
                    active_connections[username] = request.sid
                    print(f"User {username} connected with socket {request.sid}")
                    emit('connection_confirmed', {'username': username})
                    return True
            
            print(f"Anonymous connection allowed: {request.sid}")
            return True
        except (DecodeError, InvalidTokenError, ValueError) as e:
            print(f"Token decode error: {e}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return True

    @socketio.on('disconnect')
    def on_disconnect():
        username = None
        for user, sid in list(active_connections.items()):
            if sid == request.sid:
                username = user
                break
        
        if username:
            del active_connections[username]
            print(f"User {username} disconnected")
            
            # Notify games where this user was playing
            try:
                games = Game.query.filter(
                    (Game.player_x == username) | (Game.player_o == username),
                    Game.winner.is_(None),
                    Game.is_draw == False
                ).all()
                
                for game in games:
                    room_name = f"game_{game.id}"
                    emit('player_disconnected', {
                        'player': username,
                        'game_id': game.id,
                        'message': f'{username} has disconnected'
                    }, room=room_name)
            except Exception as e:
                print(f"Error notifying disconnection: {e}")
        else:
            print(f"Anonymous user disconnected: {request.sid}")

    @socketio.on('join_lobby')
    def on_join_lobby():
        join_room('lobby')
        print(f"User joined lobby: {request.sid}")
        
        # Send current active games
        try:
            active_games = Game.query.filter(
                Game.player_o.is_(None),
                Game.winner.is_(None),
                Game.is_draw == False
            ).all()
            
            games_data = []
            for game in active_games:
                games_data.append({
                    'id': game.id,
                    'host': game.player_x,
                    'createdAt': game.created_at.isoformat() if game.created_at else None,
                    'playerCount': 1 if game.player_o is None else 2
                })
            
            emit('lobby_games_update', {'games': games_data})
        except Exception as e:
            print(f"Error fetching lobby games: {e}")
            emit('lobby_games_update', {'games': []})

    @socketio.on('leave_lobby')
    def on_leave_lobby():
        leave_room('lobby')
        print(f"User left lobby: {request.sid}")

    @socketio.on('join_room')
    def on_join_room(data):
        game_id = data['room']
        player = data['player']
        room_name = f"game_{game_id}"
        
        print(f"Player {player} joining game {game_id}")
        
        join_room(room_name)
        
        # Initialize game room tracking
        if game_id not in game_rooms:
            game_rooms[game_id] = {
                'players': set(), 
                'spectators': set(),
                'room_name': room_name
            }
        
        try:
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': f'Game {game_id} not found'})
                return
            
            is_player = False
            player_role = 'spectator'
            was_waiting = game.player_o is None
            
            # Player assignment logic
            if game.player_x == player:
                # Player X rejoining
                game_rooms[game_id]['players'].add(player)
                is_player = True
                player_role = 'X'
                print(f"Player X {player} rejoined game {game_id}")
                
            elif game.player_o == player:
                # Player O rejoining
                game_rooms[game_id]['players'].add(player)
                is_player = True
                player_role = 'O'
                print(f"Player O {player} rejoined game {game_id}")
                
            elif not game.player_o and game.player_x != player:
                # New player joining as O
                game.player_o = player
                game_rooms[game_id]['players'].add(player)
                is_player = True
                player_role = 'O'
                
                try:
                    db.session.commit()
                    print(f"Player {player} joined as O in game {game_id}")
                    
                    # Notify lobby that game is no longer available
                    emit('game_started', {
                        'game_id': game.id,
                        'players': [game.player_x, game.player_o]
                    }, room='lobby')
                    
                    # Notify all players in the game that it's ready to start
                    emit('game_ready', {
                        'message': 'Game is ready! Both players have joined.',
                        'game': game.to_dict()
                    }, room=room_name)
                    
                except Exception as e:
                    print(f"Error updating game: {e}")
                    db.session.rollback()
                    emit('error', {'message': 'Failed to join game'})
                    return
            else:
                # Join as spectator
                game_rooms[game_id]['spectators'].add(player)
                player_role = 'spectator'
                print(f"Player {player} joined as spectator in game {game_id}")
            
            # Send comprehensive game state with clear role information
            game_state = {
                'game': game.to_dict(),
                'room_info': {
                    'players': list(game_rooms[game_id]['players']),
                    'spectators': list(game_rooms[game_id]['spectators'])
                },
                'player_role': player_role,
                'is_your_turn': (
                    (player_role == 'X' and game.current_turn == 'X') or
                    (player_role == 'O' and game.current_turn == 'O')
                ) if player_role != 'spectator' else False
            }
            
            emit('game_state_update', game_state, room=room_name)
            
            # Notify about player joining with clear role information
            emit('player_joined', {
                'player': player,
                'is_player': is_player,
                'role': player_role,
                'game_ready': game.player_o is not None,
                'message': f"{player} joined as {player_role.upper() if player_role != 'spectator' else 'spectator'}"
            }, room=room_name)
            
        except Exception as e:
            print(f"Error in join_room: {e}")
            emit('error', {'message': 'Failed to join room'})

    @socketio.on('make_move')
    def on_make_move(data):
        game_id = data['room']
        index = data['index']
        player = data.get('player')
        
        print(f"Move attempt: Player {player}, Game {game_id}, Position {index}")
        
        try:
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
            
            # Validate move
            if not game.can_make_move(player):
                reasons = []
                if game.winner:
                    reasons.append("Game already won")
                elif game.is_draw:
                    reasons.append("Game is a draw")
                elif not game.player_o:
                    reasons.append("Waiting for second player")
                elif not game.is_player_turn(player):
                    reasons.append("Not your turn")
                
                emit('error', {'message': f'Invalid move: {", ".join(reasons)}'})
                return
            
            board = game.board_data
            if index < 0 or index > 8 or board[index] != "":
                emit('error', {'message': 'Position already taken or invalid'})
                return
            
            # Make the move
            symbol = game.current_turn
            board[index] = symbol
            game.board_data = board
            
            # Check for winner or draw
            winner = check_winner(board)
            if winner:
                game.winner = winner
                print(f"Game {game_id} won by {winner}")
            elif is_draw(board):
                game.is_draw = True
                print(f"Game {game_id} ended in draw")
            else:
                # Switch turns
                game.current_turn = 'O' if game.current_turn == 'X' else 'X'
            
            db.session.commit()
            
            # Prepare move data
            move_data = {
                'game': game.to_dict(),
                'last_move': {
                    'index': index,
                    'symbol': symbol,
                    'player': player,
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
            
            room_name = f"game_{game_id}"
            
            # Emit to all players in the game
            emit('game_state_update', move_data, room=room_name)
            emit('move_made', move_data['last_move'], room=room_name)
            
            # Handle game end
            if game.winner or game.is_draw:
                game_end_data = {
                    'winner': game.winner,
                    'is_draw': game.is_draw,
                    'final_board': game.board_data,
                    'timestamp': datetime.utcnow().isoformat(),
                    'winner_name': game.player_x if game.winner == 'X' else game.player_o if game.winner == 'O' else None
                }
                
                emit('game_over', game_end_data, room=room_name)
                
                # Update lobby
                emit('game_completed', {'game_id': game.id}, room='lobby')
                
                print(f"Game {game_id} completed. Winner: {game.winner}, Draw: {game.is_draw}")
            
        except Exception as e:
            print(f"Error making move: {e}")
            db.session.rollback()
            emit('error', {'message': 'Failed to make move'})

    @socketio.on('send_message')
    def on_send_message(data):
        room_id = f"game_{data['room']}"
        message = {
            'sender': data['sender'],
            'text': data['text'],
            'timestamp': datetime.utcnow().isoformat(),
            'message_id': f"{data['room']}_{datetime.utcnow().timestamp()}"
        }
        emit('receive_message', message, room=room_id)
        print(f"Message sent in {room_id}: {data['sender']}: {data['text']}")
        
    @socketio.on('leave_room')
    def on_leave_room(data):
        game_id = data['room']
        player = data.get('player', 'Unknown')
        room_name = f"game_{game_id}"
        
        leave_room(room_name)
        
        # Remove from room tracking
        if game_id in game_rooms:
            game_rooms[game_id]['players'].discard(player)
            game_rooms[game_id]['spectators'].discard(player)
        
        emit('player_left', {
            'player': player,
            'timestamp': datetime.utcnow().isoformat()
        }, room=room_name)
        
        print(f"Player {player} left game {game_id}")

    @socketio.on('typing_indicator')
    def on_typing_indicator(data):
        room_id = f"game_{data['room']}"
        emit('user_typing', {
            'user': data['user'],
            'is_typing': data['is_typing']
        }, room=room_id, include_self=False)

    @socketio.on('request_game_restart')
    def on_request_game_restart(data):
        game_id = data['room']
        player = data.get('player')
        room_name = f"game_{game_id}"
        
        print(f"Game restart requested by {player} for game {game_id}")
        
        try:
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
            
            # Only allow restart if game is completed
            if not (game.winner or game.is_draw):
                emit('error', {'message': 'Game is still in progress'})
                return
            
            # Check if player is one of the game participants
            if player not in [game.player_x, game.player_o]:
                emit('error', {'message': 'Only game players can request restart'})
                return
            
            # Initialize restart votes if not exists
            if game_id not in game_rooms:
                game_rooms[game_id] = {'players': set(), 'spectators': set(), 'room_name': room_name}
            
            if 'restart_votes' not in game_rooms[game_id]:
                game_rooms[game_id]['restart_votes'] = set()
            
            # Store restart vote
            game_rooms[game_id]['restart_votes'].add(player)
            
            # Determine other player
            other_player = game.player_o if player == game.player_x else game.player_x
            
            print(f"Restart votes: {game_rooms[game_id]['restart_votes']}, needed: 2")
            
            # Check if both players voted for restart
            if len(game_rooms[game_id]['restart_votes']) >= 2:
                # Both players agreed, restart the game
                game.board_data = [''] * 9
                game.current_turn = 'X'
                game.winner = None
                game.is_draw = False
                
                # Clear restart votes
                game_rooms[game_id]['restart_votes'] = set()
                
                db.session.commit()
                
                # Notify all players that game restarted
                emit('game_restarted', {
                    'game': game.to_dict(),
                    'message': 'Game has been restarted by mutual agreement!'
                }, room=room_name)
                
                emit('game_state_update', {
                    'game': game.to_dict(),
                    'restart': True
                }, room=room_name)
                
                print(f"Game {game_id} has been restarted by mutual agreement")
            else:
                # First vote, notify other player about restart request
                emit('restart_requested', {
                    'requesting_player': player,
                    'other_player': other_player,
                    'votes_needed': 2 - len(game_rooms[game_id]['restart_votes']),
                    'message': f'{player} wants to restart the game. Waiting for {other_player} to accept.'
                }, room=room_name)
                
                print(f"Restart request sent to {other_player}, waiting for acceptance")
            
        except Exception as e:
            print(f"Error restarting game: {e}")
            db.session.rollback()
            emit('error', {'message': 'Failed to restart game'})

    @socketio.on('accept_restart')
    def on_accept_restart(data):
        # This will trigger the same voting logic as request_game_restart
        print(f"Restart accepted by {data.get('player')} for game {data['room']}")
        on_request_game_restart(data)

    @socketio.on('delete_finished_game')
    def on_delete_finished_game(data):
        game_id = data['room']
        player = data.get('player')
        
        print(f"Game deletion requested by {player} for game {game_id}")
        
        try:
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
            
            # Only allow deletion if game is completed
            if not (game.winner or game.is_draw):
                emit('error', {'message': 'Cannot delete game in progress'})
                return
            
            # Check if player is one of the game participants
            if player not in [game.player_x, game.player_o]:
                emit('error', {'message': 'Only game players can delete the game'})
                return
            
            # Store game info for logging
            game_info = {
                'id': game.id,
                'player_x': game.player_x,
                'player_o': game.player_o,
                'winner': game.winner,
                'is_draw': game.is_draw
            }
            
            # Delete the game from database
            db.session.delete(game)
            db.session.commit()
            
            # Clean up room tracking
            if game_id in game_rooms:
                del game_rooms[game_id]
            
            # Notify all players in the room
            room_name = f"game_{game_id}"
            emit('game_deleted', {
                'game_id': game_id,
                'message': f'Game has been deleted by {player}',
                'deleted_by': player,
                'redirect_to_lobby': True
            }, room=room_name)
            
            print(f"Game {game_id} deleted by {player}. Game info: {game_info}")
            
        except Exception as e:
            print(f"Error deleting game {game_id}: {e}")
            db.session.rollback()
            emit('error', {'message': 'Failed to delete game. Please try again.'})

def cleanup_old_games():
    """Background task to clean up old finished games"""
    try:
        from datetime import datetime, timedelta
        
        # Delete games that finished more than 24 hours ago
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        old_games = Game.query.filter(
            (Game.winner.isnot(None)) | (Game.is_draw == True),
            Game.updated_at < cutoff_time
        ).all()
        
        for game in old_games:
            print(f"Auto-deleting old game {game.id} (finished: {game.updated_at})")
            
            # Notify if anyone is still in the room
            room_name = f"game_{game.id}"
            socketio.emit('game_auto_deleted', {
                'game_id': game.id,
                'message': 'Game automatically deleted due to inactivity',
                'redirect_to_lobby': True
            }, room=room_name)
            
            # Clean up tracking
            if game.id in game_rooms:
                del game_rooms[game.id]
            
            db.session.delete(game)
        
        if old_games:
            db.session.commit()
            print(f"Cleaned up {len(old_games)} old finished games")
            
    except Exception as e:
        print(f"Error during game cleanup: {e}")
        db.session.rollback()
