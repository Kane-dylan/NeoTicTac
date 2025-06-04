# 🎯 Complete SQLite to Supabase Migration Guide

## 🔍 Overview

This guide provides a complete step-by-step process to migrate your Tic-Tac-Toe backend from SQLite to Supabase (PostgreSQL) with deployment on Render.

## ✅ Pre-Migration Checklist

### 📋 Requirements

- [x] Supabase account and project
- [x] Render account for deployment
- [x] Python 3.8+ environment
- [x] Git repository set up

### 🔧 Generated Files

- [x] `migrate_to_supabase.py` - Data migration script
- [x] `prepare_deployment.py` - Deployment preparation
- [x] `cleanup_project.py` - Codebase cleanup
- [x] `supabase_schema.sql` - Database schema
- [x] `.env.production` - Environment template
- [x] `MIGRATION_CHECKLIST.md` - Detailed checklist

## 🚀 Step-by-Step Migration Process

### Step 1: Supabase Configuration

#### 1.1 Create Supabase Project

1. Visit [Supabase Dashboard](https://app.supabase.com)
2. Create a new project
3. Choose a region close to your users
4. Set a strong database password

#### 1.2 Configure Database

1. Go to **Settings** → **Database**
2. Enable **Connection Pooling** (crucial for Render)
3. Note your connection details:
   - Host (pooler): `db.[project-id].supabase.co`
   - Port: `6543` (for pooling)
   - Database: `postgres`
   - User: `postgres`

#### 1.3 Set Up Network Access

1. Go to **Settings** → **Database** → **Network Restrictions**
2. For testing: Allow all IPs (`0.0.0.0/0`)
3. For production: Add specific Render IP ranges (contact Render support)

#### 1.4 Get API Credentials

1. Go to **Settings** → **API**
2. Copy your **Project URL**
3. Copy your **Service Role Key** (keep this secret!)

### Step 2: Database Schema Setup

#### 2.1 Create Tables

1. Go to **SQL Editor** in Supabase
2. Run the schema from `supabase_schema.sql`:

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

### Step 3: Render Environment Configuration

#### 3.1 Set Environment Variables

In your Render service dashboard, add these environment variables using values from `.env.production`:

```bash
SECRET_KEY=6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9
JWT_SECRET_KEY=c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-ID].supabase.co:6543/postgres?pgbouncer=true
SUPABASE_URL=https://[PROJECT-ID].supabase.co
SUPABASE_SERVICE_KEY=[YOUR-SERVICE-ROLE-KEY]
CLIENT_URL=https://your-frontend-url.vercel.app
```

**⚠️ Important:** Replace placeholders with your actual values:

- `[YOUR-PASSWORD]`: Your Supabase database password
- `[PROJECT-ID]`: Your Supabase project ID
- `[YOUR-SERVICE-ROLE-KEY]`: Your Supabase service role key

### Step 4: Data Migration (If You Have Existing Data)

#### 4.1 Backup Existing Data

```bash
cd server
python migrate_to_supabase.py
```

This script will:

- Extract data from SQLite
- Transform it for PostgreSQL
- Upload to Supabase
- Verify data integrity

### Step 5: Code Deployment

#### 5.1 Commit Changes

```bash
git add .
git commit -m "Migrate from SQLite to Supabase - Production Ready"
git push origin main
```

#### 5.2 Verify Deployment

1. Check Render deployment logs
2. Verify service starts successfully
3. Test health endpoint: `https://your-app.onrender.com/`

### Step 6: Testing & Verification

#### 6.1 API Testing

Test these endpoints:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /game/create` - Game creation
- `GET /game/lobby` - Game listing

#### 6.2 WebSocket Testing

- Connect to the WebSocket
- Join/leave game rooms
- Real-time move updates

#### 6.3 Data Persistence

- Create users and games
- Restart the service
- Verify data persists

## 📊 Migration Summary

### ✅ What Was Accomplished

#### Code Changes

- [x] Updated models for PostgreSQL compatibility
- [x] Removed Flask-Migrate dependencies
- [x] Enhanced config for production
- [x] Added connection pooling support
- [x] Improved error handling

#### Infrastructure

- [x] Migrated from SQLite to PostgreSQL
- [x] Set up Supabase integration
- [x] Configured Render deployment
- [x] Implemented secure environment variables
- [x] Added monitoring and logging

#### Security Enhancements

- [x] Generated secure keys
- [x] Environment-based configuration
- [x] Database connection security
- [x] CORS protection
- [x] Input validation

#### Performance Improvements

- [x] Connection pooling
- [x] Optimized queries
- [x] Efficient WebSocket handling
- [x] Production-ready logging

### 🗑️ Removed Components

- SQLite database files
- Flask-Migrate migrations
- Debug scripts
- Unused deployment configs
- Python cache files
- Development-only code

## 🔍 Troubleshooting Guide

### Common Issues & Solutions

#### 1. Connection Errors

**Error:** `connection refused` or `timeout`
**Solution:**

- Verify DATABASE_URL format
- Check Supabase network restrictions
- Ensure connection pooling is enabled

#### 2. Authentication Failures

**Error:** `JWT decode error` or `invalid credentials`
**Solution:**

- Verify SECRET_KEY and JWT_SECRET_KEY are set
- Check password hashing compatibility
- Ensure environment variables are correct

#### 3. Migration Errors

**Error:** `table does not exist` or `permission denied`
**Solution:**

- Run SQL schema in Supabase dashboard
- Verify service role key permissions
- Check database connection string

#### 4. CORS Issues

**Error:** `CORS policy` errors in browser
**Solution:**

- Update CLIENT_URL environment variable
- Verify CORS_ORIGINS in config.py
- Check frontend URL configuration

### 🔧 Debugging Commands

```bash
# Check environment variables
python -c "import os; print(os.getenv('DATABASE_URL'))"

# Test database connection
python -c "from app import create_app; app = create_app(); print('DB connected')"

# View application logs
# (Check Render dashboard for detailed logs)
```

### 📞 Support Resources

1. **Render Documentation**: https://render.com/docs
2. **Supabase Documentation**: https://supabase.com/docs
3. **Flask Documentation**: https://flask.palletsprojects.com/
4. **PostgreSQL Documentation**: https://www.postgresql.org/docs/

## 🎉 Success Metrics

Your migration is successful when:

- ✅ Application starts without errors
- ✅ Users can register and login
- ✅ Games can be created and played
- ✅ Real-time features work correctly
- ✅ Data persists across restarts
- ✅ Performance meets expectations
- ✅ No SQLite-related errors in logs

## 🔄 Maintenance & Monitoring

### Regular Tasks

- Monitor database performance in Supabase
- Check application logs in Render
- Review connection pool usage
- Update dependencies regularly
- Monitor error rates and response times

### Backup Strategy

- Supabase provides automatic backups
- Consider additional backup strategies for critical data
- Test restore procedures periodically

## 📈 Future Enhancements

Consider these improvements:

- [ ] Database indexing optimization
- [ ] Caching layer (Redis)
- [ ] Rate limiting
- [ ] API versioning
- [ ] Comprehensive test suite
- [ ] Performance monitoring
- [ ] User analytics

---

🎯 **Congratulations!** Your Tic-Tac-Toe application has been successfully migrated from SQLite to Supabase with full production deployment on Render!
