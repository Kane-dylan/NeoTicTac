# Tic-Tac-Toe Backend Server

A Flask-based real-time multiplayer tic-tac-toe game backend with PostgreSQL (Supabase) integration.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database (Supabase recommended)
- Environment variables configured

### Installation

```bash
cd server
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://postgres:password@host:6543/postgres?pgbouncer=true
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
CLIENT_URL=http://localhost:5173
```

### Database Setup

1. Create tables in your Supabase dashboard using the SQL Editor:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Games table
CREATE TABLE IF NOT EXISTS game (
    id SERIAL PRIMARY KEY,
    player_x VARCHAR(80) NOT NULL,
    player_o VARCHAR(80),
    board TEXT DEFAULT '["","","","","","","","",""]',
    current_turn VARCHAR(1) DEFAULT 'X',
    winner VARCHAR(1),
    is_draw BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Development

```bash
python run.py
```

Server will start on `http://localhost:5000`

### Production (Render)

The app is configured for Render deployment with:

- `gunicorn` WSGI server
- PostgreSQL connection pooling
- Environment-based configuration
- CORS configuration for frontend

## 📊 Architecture

### Tech Stack

- **Framework**: Flask 2.3.3
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy 3.0.5
- **Authentication**: JWT (Flask-JWT-Extended)
- **Real-time**: Socket.IO
- **WSGI Server**: Gunicorn (production)

### Project Structure

```
server/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # Database models
│   │   ├── user.py         # User model
│   │   └── game.py         # Game model
│   ├── routes/              # API endpoints
│   │   ├── auth.py         # Authentication routes
│   │   └── game.py         # Game routes
│   ├── services/            # Business logic
│   │   └── game_logic.py   # Game logic service
│   ├── sockets/             # WebSocket handlers
│   │   └── handlers.py     # Socket event handlers
│   └── utils/               # Utilities
│       └── auth_helpers.py # Auth helper functions
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── run.py                 # Development server
├── wsgi.py               # Production WSGI entry point
└── Procfile              # Render deployment config
```

## 🔧 API Documentation

### Authentication Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Game Endpoints

- `GET /game/lobby` - Get available games
- `POST /game/create` - Create new game
- `POST /game/join/<game_id>` - Join existing game
- `POST /game/move` - Make a move

### WebSocket Events

- `join_game` - Join game room
- `leave_game` - Leave game room
- `make_move` - Real-time move updates
- `game_update` - Game state changes

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Werkzeug
- CORS protection
- Environment-based secrets
- SQL injection protection via ORM

## 🚀 Deployment

### Render Setup

1. Connect your GitHub repository
2. Configure environment variables
3. Deploy automatically on git push

### Environment Variables (Production)

```
SECRET_KEY=<generated-secret>
JWT_SECRET_KEY=<generated-secret>
DATABASE_URL=<supabase-connection-string>
SUPABASE_URL=<supabase-project-url>
SUPABASE_SERVICE_KEY=<supabase-service-key>
CLIENT_URL=<frontend-url>
```

### Health Check

The server responds to health checks at `/` endpoint.

## 📈 Monitoring

### Logging

- Structured logging in production
- Error tracking and debugging
- Database connection monitoring

### Performance

- Connection pooling for database
- Efficient WebSocket handling
- Optimized query patterns

## 🔧 Development

### Local Development

1. Set up virtual environment
2. Install dependencies
3. Configure `.env` file
4. Run development server

### Testing

```bash
# Run tests (when implemented)
python -m pytest
```

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Document functions and classes

## 📞 Support

For issues and questions:

1. Check deployment logs in Render dashboard
2. Verify database connectivity in Supabase
3. Review environment variable configuration
4. Test API endpoints individually
