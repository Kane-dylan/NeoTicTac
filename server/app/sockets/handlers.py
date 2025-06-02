from flask_socketio import emit, join_room
from app.models.game import Game
from app import db

def register_socket_handlers(socketio):
    @socketio.on('join_room')
    def on_join(data):
        room = data['room']
        join_room(room)
        emit('player_joined', {'player': data['player']}, room=room)

    @socketio.on('make_move')
    def on_move(data):
        game = Game.query.get(data['room'])
        index = data['index']
        symbol = data['symbol']
        if game.board[index] == "" and game.winner is None:
            game.board[index] = symbol
            db.session.commit()
            emit('move_made', {'index': index, 'symbol': symbol}, room=data['room'])
