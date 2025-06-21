# Tic-Tac-Toe Backend

A Flask-based real-time multiplayer tic-tac-toe game backend with PostgreSQL integration.

## 🚀 Quick Start

### Environment Variables

Create a `.env` file with:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
CLIENT_URL=https://your-frontend-url.com
```

### Installation

```bash
pip install -r requirements.txt
```

### Development

```bash
python run.py
```

### Production

The application is configured for deployment on Render with Gunicorn.

## 🔧 API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/health` - Health check
- `POST /api/game/create` - Create new game
- `GET /api/game/active` - Get active games
- `GET /api/game/<id>` - Get game details

## 🔌 WebSocket Events

Real-time game updates via Socket.IO for moves, chat, game state, and play again invitations.

### Play Again Feature

- `send_play_again_invite` - Send invitation to opponent
- `respond_to_play_again` - Accept/decline invitation
- `play_again_invite` - Receive invitation notification
- `play_again_response` - Receive response to sent invitation
- `game_restarted` - Game state reset and restarted
- `play_again_cancelled` - Invitation cancelled (disconnect/timeout)

### Game Management

- `delete_game_from_lobby` - Delete completed game
- `respond_to_play_again` - Accept/decline invitation
- `play_again_invite` - Receive invitation notification
- `play_again_response` - Receive response to sent invitation
- `game_restarted` - Game state reset and restarted
- `play_again_cancelled` - Invitation cancelled (disconnect/timeout)

## 🚀 Deployment

Configured for Render deployment with automatic database initialization.
