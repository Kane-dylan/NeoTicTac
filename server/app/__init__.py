from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    socketio.init_app(app)

    # Import models to register them with SQLAlchemy
    from app.models import user, game

    from app.routes import auth, game
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)

    from app.sockets.handlers import register_socket_handlers
    register_socket_handlers(socketio)

    return app
