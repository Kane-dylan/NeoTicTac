# 🚀 FINAL MIGRATION STEPS

## Current Status

✅ **Environment configured** - All credentials and environment variables are set  
✅ **Code updated** - All files migrated to PostgreSQL/Supabase compatibility  
✅ **Render config ready** - `render.yaml` is properly configured  
⏳ **Database schema** - Needs to be created manually in Supabase  
⏳ **Data migration** - Ready to run after schema creation  
⏳ **Testing** - Ready to validate complete setup

---

## 🎯 IMMEDIATE ACTIONS REQUIRED

### Step 1: Create Database Schema in Supabase

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project**: `mauqzdgqvckrepinjybz`
3. **Navigate to**: SQL Editor
4. **Create new query** and paste this SQL:

```sql
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
```

5. **Click "Run"** to execute the schema

### Step 2: Verify Schema Creation

Run this command to test the database setup:

```bash
cd server
python test_setup.py
```

### Step 3: Test Local Application

```bash
cd server
python run.py
```

### Step 4: Deploy to Render

1. **Push code to GitHub** (if not already done)
2. **Go to Render Dashboard**: https://dashboard.render.com
3. **Trigger manual deploy** or push will auto-deploy
4. **Monitor deployment logs** for any issues

---

## 🔧 VERIFICATION COMMANDS

After schema creation, run these to verify everything works:

```bash
# Test Supabase connection and operations
cd server
python test_setup.py

# Test data migration (if you had existing data)
python run_migration.py

# Test local app
python run.py
```

---

## 🏆 SUCCESS CRITERIA

✅ **Schema created**: `python test_setup.py` passes all tests  
✅ **Local app works**: Can register/login users and create games  
✅ **Render deployment**: App starts without environment variable errors  
✅ **Data persistence**: Games and users persist between sessions

---

## 🚨 IF ISSUES OCCUR

### Database Connection Issues

- Verify Supabase credentials in Render dashboard
- Check that connection string uses port 6543 (pgBouncer)
- Ensure service role key has proper permissions

### Render Deployment Issues

- Check deployment logs in Render dashboard
- Verify all environment variables are set
- Ensure `render.yaml` is in project root

### Application Errors

- Check Flask logs for detailed error messages
- Verify models are properly imported
- Test individual components with `test_setup.py`

---

## 📞 NEXT STEP

**Execute Step 1 above** (create schema in Supabase), then run the verification commands. Once that's complete, the migration will be finished!
