# SQLite to Supabase Migration - Deployment Checklist

## ✅ Pre-Migration Checklist

### 1. Supabase Setup

- [ ] Supabase project created
- [ ] Database connection pooling enabled
- [ ] Network restrictions configured (allow Render IPs)
- [ ] Service role key copied securely

### 2. Environment Variables Ready

- [ ] `DATABASE_URL` (PostgreSQL connection string with pooling)
- [ ] `SUPABASE_URL` (project URL)
- [ ] `SUPABASE_SERVICE_KEY` (service role key)
- [ ] `SECRET_KEY` (generated secure key)
- [ ] `JWT_SECRET_KEY` (generated secure key)
- [ ] `CLIENT_URL` (your frontend URL)

### 3. Code Preparation

- [ ] Updated models for PostgreSQL
- [ ] Removed Flask-Migrate dependencies
- [ ] Updated config.py for production
- [ ] Cleaned up SQLite-specific code

## 🚀 Migration Steps

### Step 1: Backup Current Data

```bash
# Run the migration script to backup data
cd server
python migrate_to_supabase.py
```

### Step 2: Create Supabase Tables

Run these SQL commands in your Supabase SQL Editor:

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

### Step 3: Migrate Data

The migration script will handle data transfer automatically.

### Step 4: Update Render Environment

1. Go to your Render service dashboard
2. Navigate to Environment tab
3. Add all environment variables listed above
4. Save changes

### Step 5: Deploy Updated Code

```bash
# Commit and push changes
git add .
git commit -m "Migrate from SQLite to Supabase"
git push origin main
```

### Step 6: Verify Deployment

- [ ] Check Render logs for successful startup
- [ ] Test user registration/login
- [ ] Test game creation and gameplay
- [ ] Verify data persistence

## 🔧 Troubleshooting

### Common Issues:

1. **Connection Errors**

   - Verify DATABASE_URL format
   - Check Supabase network restrictions
   - Ensure connection pooling is enabled

2. **Migration Errors**

   - Check table creation in Supabase dashboard
   - Verify service role key permissions
   - Review migration script logs

3. **Authentication Issues**
   - Confirm JWT_SECRET_KEY is set
   - Check SECRET_KEY configuration
   - Verify password hashing compatibility

### Rollback Plan:

1. Keep SQLite backup files
2. Revert environment variables
3. Redeploy previous version if needed

## 📊 Post-Migration Verification

### Data Integrity Checks:

- [ ] User count matches previous database
- [ ] Game states are preserved
- [ ] All relationships are intact
- [ ] Timestamps are correct

### Performance Monitoring:

- [ ] Response times are acceptable
- [ ] Database connections are stable
- [ ] No memory leaks in production

### Security Verification:

- [ ] Environment variables are secure
- [ ] Database access is restricted
- [ ] SSL connections are enforced

## 🎯 Success Criteria

✅ **Migration is successful when:**

- All users can log in with existing credentials
- Games can be created and played normally
- Data persists across server restarts
- Performance is equal or better than SQLite
- No SQLite-related errors in logs

## 📞 Support

If you encounter issues:

1. Check Render deployment logs
2. Verify Supabase dashboard for errors
3. Test database connectivity
4. Review environment variable configuration
