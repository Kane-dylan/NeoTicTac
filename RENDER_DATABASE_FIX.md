# 🔧 RENDER ENVIRONMENT VARIABLE FIX

## ❌ CURRENT ERROR

```
(psycopg2.ProgrammingError) invalid dsn: invalid connection option "pgbouncer"
```

## 🎯 SOLUTION

The issue is that Render still has the old DATABASE_URL with `pgbouncer=true` parameter. You need to update the environment variables in the Render dashboard.

---

## 📋 STEP-BY-STEP FIX

### 1. Go to Render Dashboard

- Visit: https://dashboard.render.com
- Select your `tictactoe-backend` service

### 2. Update Environment Variables

Click on **Environment** tab and set these variables:

```bash
SECRET_KEY=6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9
JWT_SECRET_KEY=c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177
SUPABASE_URL=https://mauqzdgqvckrepinjybz.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hdXF6ZGdxdmNrcmVwaW5qeWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODg4NjUyMCwiZXhwIjoyMDY0NDYyNTIwfQ.VWqomYXkBiVZQfxuoKMkcpZfllDkhvGLzcrDz1FZDpk
DATABASE_URL=postgresql://postgres:CHCTSOQehN8QMVNO@db.mauqzdgqvckrepinjybz.supabase.co:5432/postgres
FLASK_ENV=production
CLIENT_URL=https://tic-tac-toe-ten-murex-86.vercel.app
```

### 3. Key Changes Made

- ✅ **Removed pgbouncer parameter** from DATABASE_URL
- ✅ **Using port 5432** (direct connection) instead of 6543
- ✅ **Clean PostgreSQL connection string**

### 4. Trigger Redeploy

- After updating environment variables
- Click **Manual Deploy** or push a new commit
- Monitor the deployment logs

---

## ✅ VERIFICATION

After deployment, you should see:

```
Database tables created successfully
✅ Flask app started successfully
```

Instead of the pgbouncer error.

---

## 🚨 IMPORTANT NOTES

1. **Don't use pgbouncer parameters** in DATABASE_URL for SQLAlchemy
2. **Use direct connection** (port 5432) for better compatibility
3. **Update in Render dashboard** - render.yaml no longer contains env vars
4. **Environment variables** are now managed through Render UI

---

## 📞 IF STILL ISSUES

If you still get connection errors, try this alternative DATABASE_URL:

```
DATABASE_URL=postgresql://postgres:CHCTSOQehN8QMVNO@db.mauqzdgqvckrepinjybz.supabase.co:5432/postgres?sslmode=require
```

This adds SSL requirement which some PostgreSQL servers expect.
