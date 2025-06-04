-- Run these commands in your Supabase SQL Editor:

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