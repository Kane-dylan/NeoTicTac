from dotenv import load_dotenv
load_dotenv()

from app import create_app, socketio, db

app = create_app()

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
