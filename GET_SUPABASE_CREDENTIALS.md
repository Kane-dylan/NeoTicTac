# 🚀 Quick Render Fix - Get Supabase Credentials

## Step 1: Get Your Supabase Project Details

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project** or create a new one if needed
3. **Collect the following information**:

### A. Project ID

- Found in your project URL: `https://supabase.com/dashboard/project/[PROJECT_ID]`
- Also in Settings → General → Reference ID

### B. Database Password

- Settings → Database → Database password
- If you forgot it, you can reset it here

### C. Service Role Key

- Settings → API → Service Role Key (secret)
- This is the `service_role` key, NOT the `anon` key

## Step 2: Update render.yaml

Run the configuration update script:

```bash
cd server
python update_render_config.py
```

**OR manually update these values in `render.yaml`:**

```yaml
envVars:
  - key: DATABASE_URL
    value: postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:6543/postgres?pgbouncer=true
  - key: SUPABASE_URL
    value: https://YOUR_PROJECT_ID.supabase.co
  - key: SUPABASE_SERVICE_KEY
    value: YOUR_SERVICE_ROLE_KEY
```

## Step 3: Create Database Tables

Run this SQL in your Supabase SQL Editor:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

## Step 4: Deploy

1. **Commit and push changes**:

   ```bash
   git add .
   git commit -m "Configure Supabase for production deployment"
   git push
   ```

2. **Check Render deployment**:
   - Go to your Render dashboard
   - Your service should automatically redeploy
   - Check the logs for any errors

## Step 5: Test

Test your endpoints:

- `GET /health` - Should return OK
- `POST /auth/register` - Try creating a user
- `GET /users` - Should return empty array initially

## 🆘 If Still Having Issues

1. **Check Render Logs**: Look for specific error messages
2. **Verify Environment Variables**: Make sure all values are correct
3. **Test Database Connection**: Use Supabase SQL editor to verify tables exist
4. **Check Network**: Make sure Supabase allows connections from Render

## 📞 Common Issues

**"CORS error"**: Update CLIENT_URL in render.yaml to match your frontend URL
**"Database connection failed"**: Double-check your DATABASE_URL format
**"Authentication failed"**: Verify your service role key is correct
**"Table doesn't exist"**: Make sure you ran the SQL schema creation

---

**Need help?** Check the full migration guide: `COMPLETE_MIGRATION_GUIDE.md`
