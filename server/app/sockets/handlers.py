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

            if auth and 'token' in auth:
                token = auth['token']
                if token and token not in ['null', 'undefined', '']:
                    decoded_token = decode_token(token)
                    username = decoded_token['sub']
                    active_connections[username] = request.sid

                    emit('connection_confirmed', {'username': username})
                    return True

            return True
        except (DecodeError, InvalidTokenError, ValueError) as e:

            return True
        except Exception as e:

            return True    @socketio.on('disconnect')
    def on_disconnect():
        username = None
        for user, sid in list(active_connections.items()):
            if sid == request.sid:
                username = user
                break
        
        if username:
            del active_connections[username]

            # Cancel any pending play again invitations
            try:
                for game_id, room_data in game_rooms.items():
                    if 'play_again_invites' in room_data:
                        invites_to_remove = []
                        for invite_key, invite_data in room_data['play_again_invites'].items():
                            if invite_data['inviter'] == username or invite_data['invitee'] == username:
                                invites_to_remove.append(invite_key)
                                
                                # Notify the other player
                                other_player = invite_data['invitee'] if invite_data['inviter'] == username else invite_data['inviter']
                                if other_player in active_connections:
                                    emit('play_again_cancelled', {
                                        'gameId': game_id,
                                        'inviter': invite_data['inviter'],
                                        'reason': 'player_disconnected'
                                    }, room=active_connections[other_player])
                        
                        # Remove the invitations
                        for invite_key in invites_to_remove:
                            del room_data['play_again_invites'][invite_key]
            except Exception as e:
                pass  # Handle exception gracefully

            # Notify games where this user was playing
            try:
                games = Game.query.filter(
                    (Game.player_x == username) | (Game.player_o == username),
                    Game.winner.is_(None),
                    Game.is_draw == False
                ).all()
                
                for game in games:
                    room_name = f"game_{game.id}"
                    # Clean up rematch requests for disconnected player
                    if game.id in game_rooms and 'rematch_requests' in game_rooms[game.id]:
                        game_rooms[game.id]['rematch_requests'].discard(username)
                    
                    emit('player_disconnected', {
                        'player': username,
                        'game_id': game.id,
                        'message': f'{username} has disconnected'
                    }, room=room_name)
            except Exception as e:
                pass  # Handle exception if needed

            else:
                pass  # No additional action needed

    @socketio.on('join_lobby')
    def on_join_lobby():
        join_room('lobby')        # Send current active games
        try:
            active_games = Game.query.filter(
                Game.player_o.is_(None),
                Game.winner.is_(None),
                Game.is_draw == False            ).all()
            
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
            emit('lobby_games_update', {'games': []})
    
    @socketio.on('leave_lobby')
    def on_leave_lobby():        leave_room('lobby')
    
    @socketio.on('join_room')
    def on_join_room(data):
        try:
            game_id = data['room']
            player = data['player'].strip() if data.get('player') else None
            
            if not player:
                emit('error', {'message': 'Player name is required'})
                return
                
            room_name = f"game_{game_id}"
            join_room(room_name)
        except Exception as e:
            emit('error', {'message': 'Failed to join room'})
            return
          # Initialize game room tracking
        if game_id not in game_rooms:
            game_rooms[game_id] = {
                'players': set(), 
                'spectators': set(),                'room_name': room_name
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

            elif game.player_o == player:
                # Player O rejoining
                game_rooms[game_id]['players'].add(player)
                is_player = True
                player_role = 'O'

            elif not game.player_o and game.player_x != player:
                # New player joining as O
                game.player_o = player
                game_rooms[game_id]['players'].add(player)
                is_player = True
                player_role = 'O'
                
                try:
                    db.session.commit()

                    # Send updated game state immediately to all players
                    updated_game_state = {
                        'game': game.to_dict(),
                        'room_info': {
                            'players': list(game_rooms[game_id]['players']),
                            'spectators': list(game_rooms[game_id]['spectators'])
                        },
                        'player_o_joined': True,
                        'both_players_present': True
                    }
                    
                    # Notify lobby that game is no longer available
                    emit('game_started', {
                        'game_id': game.id,
                        'players': [game.player_x, game.player_o]
                    }, room='lobby')
                    
                    # Update player count for lobby
                    emit('player_count_updated', {
                        'game_id': game.id, 
                        'playerCount': 2
                    }, room='lobby')
                    
                    # Send game state update to all players first
                    emit('game_state_update', updated_game_state, room=room_name)
                      # Then notify all players in the game that it's ready to start
                    emit('game_ready', {
                        'message': 'Game is ready! Both players have joined.',
                        'game': game.to_dict(),
                        'both_players_joined': True                    }, room=room_name)
                    
                except Exception as e:
                    db.session.rollback()
                    emit('error', {'message': 'Failed to join game'})
                    return
                    
            else:
                # Join as spectator
                game_rooms[game_id]['spectators'].add(player)
                player_role = 'spectator'

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
            
            # Send game state to all players in the room
            emit('game_state_update', game_state, room=room_name)
            
            # Notify about player joining with clear role information
            emit('player_joined', {
                'player': player,
                'is_player': is_player,
                'role': player_role,
                'game_ready': game.player_o is not None,
                'message': f"{player} joined as {player_role.upper() if player_role != 'spectator' else 'spectator'}"
            }, room=room_name)            # If this was player O joining, send a special broadcast to ensure UI updates
            if player_role == 'O' and was_waiting:
                emit('game_state_update', {
                    'game': game.to_dict(),
                    'player_o_joined': True,
                    'both_players_present': True
                }, room=room_name)
                
        except Exception as e:
            emit('error', {'message': 'Failed to join room'})    @socketio.on('make_move')
    def on_make_move(data):
        game_id = data['room']
        index = data['index']
        player = data.get('player', '').strip()
        
        if not player:
            emit('error', {'message': 'Player name is required'})
            return

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
            result = check_winner(board)
            winner = result['winner']
            winning_line = result['winning_line']
            
            print(f"🏆 Server Debug - Game {game_id}:")
            print(f"  - Winner: {winner}")
            print(f"  - Winning line: {winning_line}")
            
            if winner:
                game.winner = winner
                game.winning_line_data = winning_line
                print(f"  - Set game.winning_line_data: {game.winning_line_data}")

            elif is_draw(board):
                game.is_draw = True

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
            
            print(f"  - Move data game.winning_line: {move_data['game'].get('winning_line')}")
            
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

        except Exception as e:

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

    @socketio.on('typing_indicator')
    def on_typing_indicator(data):
        room_id = f"game_{data['room']}"
        emit('user_typing', {
            'user': data['user'],
            'is_typing': data['is_typing']
        }, room=room_id, include_self=False)

    @socketio.on('send_play_again_invite')
    def on_send_play_again_invite(data):
        """Handle sending play again invitation"""
        try:
            game_id = data['gameId']
            inviter = data['inviter']
            invitee = data['invitee']
            
            # Verify game exists and is completed
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
                
            if not (game.winner or game.is_draw):
                emit('error', {'message': 'Game is not completed yet'})
                return
                
            # Verify the inviter is a player in this game
            if inviter not in [game.player_x, game.player_o]:
                emit('error', {'message': 'Only game players can send invitations'})
                return
                
            # Check if invitee is still connected
            if invitee not in active_connections:
                emit('error', {'message': f'{invitee} is not connected'})
                return
                
            # Initialize play again tracking for this game
            if game_id not in game_rooms:
                game_rooms[game_id] = {'players': set(), 'spectators': set(), 'room_name': f'game_{game_id}'}
                
            if 'play_again_invites' not in game_rooms[game_id]:
                game_rooms[game_id]['play_again_invites'] = {}
                
            # Prevent duplicate invites
            invite_key = f"{inviter}_{invitee}"
            if invite_key in game_rooms[game_id]['play_again_invites']:
                emit('error', {'message': 'Invitation already sent'})
                return
                
            # Store the invitation
            game_rooms[game_id]['play_again_invites'][invite_key] = {
                'inviter': inviter,
                'invitee': invitee,
                'timestamp': datetime.utcnow(),
                'status': 'pending'
            }
            
            # Send invitation to the invitee
            invitee_sid = active_connections.get(invitee)
            if invitee_sid:
                emit('play_again_invite', {
                    'gameId': game_id,
                    'inviter': inviter,
                    'invitee': invitee,
                    'timestamp': datetime.utcnow().isoformat()
                }, room=invitee_sid)
                
        except Exception as e:
            emit('error', {'message': 'Failed to send play again invitation'})

    @socketio.on('respond_to_play_again')
    def on_respond_to_play_again(data):
        """Handle response to play again invitation"""
        try:
            game_id = data['gameId']
            inviter = data['inviter']
            invitee = data['invitee']
            accepted = data['accepted']
            
            # Verify game exists
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
                
            # Check invitation exists
            if game_id not in game_rooms or 'play_again_invites' not in game_rooms[game_id]:
                emit('error', {'message': 'No invitation found'})
                return
                
            invite_key = f"{inviter}_{invitee}"
            if invite_key not in game_rooms[game_id]['play_again_invites']:
                emit('error', {'message': 'Invitation not found or expired'})
                return
                
            # Remove the invitation
            del game_rooms[game_id]['play_again_invites'][invite_key]
            
            # Send response to inviter
            inviter_sid = active_connections.get(inviter)
            if inviter_sid:
                emit('play_again_response', {
                    'gameId': game_id,
                    'inviter': inviter,
                    'invitee': invitee,
                    'accepted': accepted,
                    'timestamp': datetime.utcnow().isoformat()
                }, room=inviter_sid)
            
            if accepted:
                # Reset the game state
                game.board_data = [''] * 9
                game.current_turn = 'X'
                game.winner = None
                game.is_draw = False
                
                db.session.commit()
                
                # Notify both players that game has restarted
                room_name = f"game_{game_id}"
                emit('game_restarted', {
                    'game': game.to_dict(),
                    'message': f'New game started! {invitee} accepted the invitation.',
                    'restarted_by': 'mutual_agreement'
                }, room=room_name)
                
                # Send updated game state
                emit('game_state_update', {
                    'game': game.to_dict(),
                    'restart': True
                }, room=room_name)
                
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': 'Failed to process play again response'})

    @socketio.on('cancel_play_again_invite')
    def on_cancel_play_again_invite(data):
        """Handle cancellation of play again invitation"""
        try:
            game_id = data['gameId']
            inviter = data['inviter']
            invitee = data['invitee']
            
            if game_id in game_rooms and 'play_again_invites' in game_rooms[game_id]:
                invite_key = f"{inviter}_{invitee}"
                if invite_key in game_rooms[game_id]['play_again_invites']:
                    del game_rooms[game_id]['play_again_invites'][invite_key]
                    
                    # Notify invitee that invitation was cancelled
                    invitee_sid = active_connections.get(invitee)
                    if invitee_sid:
                        emit('play_again_cancelled', {
                            'gameId': game_id,
                            'inviter': inviter,
                            'reason': 'cancelled_by_inviter'
                        }, room=invitee_sid)
                        
        except Exception as e:
            emit('error', {'message': 'Failed to cancel invitation'})

    @socketio.on('delete_game_from_lobby')
    def on_delete_game_from_lobby(data):
        """Handle game deletion from lobby"""
        try:
            game_id = data['game_id']
            player = data['player']
            
            # Verify game exists
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
                
            # Verify the player can delete this game (is one of the players)
            if player not in [game.player_x, game.player_o]:
                emit('error', {'message': 'Only game players can delete the game'})
                return
                
            # Verify game is completed
            if not (game.winner or game.is_draw):
                emit('error', {'message': 'Cannot delete active game'})
                return
                
            # Remove game from database
            db.session.delete(game)
            db.session.commit()
            
            # Notify lobby about game deletion
            emit('game_deleted', {
                'game_id': game_id,
                'deleted_by': player
            }, room='lobby')
            
            # Notify any remaining players in the game room
            room_name = f"game_{game_id}"
            emit('game_deleted', {
                'game_id': game_id,
                'deleted_by': player,
                'message': 'Game has been deleted'
            }, room=room_name)
            
            # Clean up room tracking
            if game_id in game_rooms:
                del game_rooms[game_id]                
        except Exception as e:
            db.session.rollback()
            emit('error', {'message': 'Failed to delete game'})
    def on_request_game_restart(data):
        game_id = data['room']
        player = data.get('player')
        room_name = f"game_{game_id}"

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

            else:
                # First vote, notify other player about restart request
                emit('restart_requested', {
                    'requesting_player': player,
                    'other_player': other_player,
                    'votes_needed': 2 - len(game_rooms[game_id]['restart_votes']),
                    'message': f'{player} wants to restart the game. Waiting for {other_player} to accept.'
                }, room=room_name)

        except Exception as e:

            db.session.rollback()
            emit('error', {'message': 'Failed to restart game'})    @socketio.on('accept_restart')
    def on_accept_restart(data):
        # This will trigger the same voting logic as request_game_restart
        on_request_game_restart(data)    # Rematch functionality handlers
    @socketio.on('rematch_request')
    def on_rematch_request(data):
        """
        Handle rematch request from a player.
        
        Validates the request, prevents duplicates, handles simultaneous requests,
        and notifies the target player.
        
        Args:
            data (dict): {
                'room': game_id,
                'requesting_player': username,
                'target_player': target_username
            }
        """
        game_id = data['room']
        requesting_player = data.get('requesting_player')
        target_player = data.get('target_player')
        room_name = f"game_{game_id}"

        try:
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
            
            # Only allow rematch if game is completed
            if not (game.winner or game.is_draw):
                emit('error', {'message': 'Game is still in progress'})
                return
            
            # Check if player is one of the game participants
            if requesting_player not in [game.player_x, game.player_o]:
                emit('error', {'message': 'Only game players can request rematch'})
                return
            
            # Initialize rematch tracking if not exists
            if game_id not in game_rooms:
                game_rooms[game_id] = {'players': set(), 'spectators': set(), 'room_name': room_name}
            
            if 'rematch_requests' not in game_rooms[game_id]:
                game_rooms[game_id]['rematch_requests'] = set()
            
            # Check for duplicate request
            if requesting_player in game_rooms[game_id]['rematch_requests']:
                emit('error', {'message': 'Rematch request already pending'})
                return
            
            # Store rematch request
            game_rooms[game_id]['rematch_requests'].add(requesting_player)
            
            # Check if both players requested rematch simultaneously
            other_player = game.player_o if requesting_player == game.player_x else game.player_x
            if other_player in game_rooms[game_id]['rematch_requests']:
                # Both players requested, automatically start new game
                _reset_game_for_rematch(game, game_id, room_name)
                return
            
            # Send rematch request to the target player
            emit('rematch_requested', {
                'requesting_player': requesting_player,
                'target_player': target_player,
                'game_id': game_id
            }, room=room_name)

        except Exception as e:
            db.session.rollback()
            emit('error', {'message': 'Failed to send rematch request'})

    @socketio.on('rematch_accept')
    def on_rematch_accept(data):
        """
        Handle rematch acceptance.
        
        Resets the game state and starts a new game when a player accepts
        a rematch request.
        
        Args:
            data (dict): {
                'room': game_id,
                'accepting_player': username,
                'requesting_player': requester_username
            }
        """
        game_id = data['room']
        accepting_player = data.get('accepting_player')
        requesting_player = data.get('requesting_player')
        room_name = f"game_{game_id}"

        try:
            game = Game.query.get(game_id)
            if not game:
                emit('error', {'message': 'Game not found'})
                return
            
            # Check if player is one of the game participants
            if accepting_player not in [game.player_x, game.player_o]:
                emit('error', {'message': 'Only game players can accept rematch'})
                return
            
            # Reset game for rematch
            _reset_game_for_rematch(game, game_id, room_name)

        except Exception as e:
            db.session.rollback()
            emit('error', {'message': 'Failed to accept rematch'})

    @socketio.on('rematch_decline')
    def on_rematch_decline(data):
        """
        Handle rematch decline.
        
        Clears the pending rematch request and notifies all players
        that the rematch was declined.
        
        Args:
            data (dict): {
                'room': game_id,
                'declining_player': username,
                'requesting_player': requester_username
            }
        """
        game_id = data['room']
        declining_player = data.get('declining_player')
        requesting_player = data.get('requesting_player')
        room_name = f"game_{game_id}"

        try:
            # Clear rematch requests for this game
            if game_id in game_rooms and 'rematch_requests' in game_rooms[game_id]:
                game_rooms[game_id]['rematch_requests'].discard(requesting_player)
            
            # Notify players about the decline
            emit('rematch_declined', {
                'declining_player': declining_player,
                'requesting_player': requesting_player,
                'game_id': game_id
            }, room=room_name)

        except Exception as e:
            emit('error', {'message': 'Failed to decline rematch'})

    def _reset_game_for_rematch(game, game_id, room_name):
        """
        Helper function to reset game state for rematch.
        
        Resets the board, turn order, winner status, and cleans up
        tracking data. Commits changes and notifies all players.
        
        Args:
            game (Game): The game object to reset
            game_id (int): The game ID
            room_name (str): The socket room name
            
        Raises:
            Exception: If database operations fail
        """
        try:
            # Reset game state
            game.board_data = [''] * 9
            game.current_turn = 'X'
            game.winner = None
            game.is_draw = False
            
            # Clear rematch requests
            if game_id in game_rooms and 'rematch_requests' in game_rooms[game_id]:
                game_rooms[game_id]['rematch_requests'] = set()
            
            db.session.commit()
            
            # Notify all players that rematch was accepted and new game started
            emit('rematch_accepted', {
                'game': game.to_dict(),
                'message': 'New game started!',
                'game_id': game_id
            }, room=room_name)
            
            emit('game_state_update', {
                'game': game.to_dict(),
                'rematch': True
            }, room=room_name)

        except Exception as e:
            db.session.rollback()
            raise e

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
            
    except Exception as e:

        db.session.rollback()
