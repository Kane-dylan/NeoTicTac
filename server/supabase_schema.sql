-- Supabase PostgreSQL Schema for Tic-Tac-Toe Application
-- Run these commands in your Supabase SQL Editor:

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Games table  
CREATE TABLE games (
    id BIGSERIAL PRIMARY KEY,
    board TEXT NOT NULL DEFAULT '["","","","","","","","",""]',
    current_player VARCHAR(1) NOT NULL DEFAULT 'X',
    winner VARCHAR(1),
    is_finished BOOLEAN NOT NULL DEFAULT FALSE,
    player_x_id BIGINT REFERENCES users(id),
    player_o_id BIGINT REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_games_player_x ON games(player_x_id);
CREATE INDEX idx_games_player_o ON games(player_o_id);
CREATE INDEX idx_games_finished ON games(is_finished);