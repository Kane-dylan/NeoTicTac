# 🚨 IMMEDIATE FIX: Render Environment Variables

## Problem

You're getting: `SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables are required`

## ✅ Solution 1: Manual Environment Variables (FASTEST FIX)

**Go to your Render service dashboard and add these environment variables:**

1. **Open Render Dashboard** → Your Service → **Environment** tab
2. **Add each of these variables:**

```
SECRET_KEY=6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9
JWT_SECRET_KEY=c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177
DATABASE_URL=postgresql://postgres:CHCTSOQehN8QMVNO@db.mauqzdgqvckrepinjybz.supabase.co:6543/postgres?pgbouncer=true
SUPABASE_URL=https://mauqzdgqvckrepinjybz.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hdXF6ZGdxdmNrcmVwaW5qeWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODg4NjUyMCwiZXhwIjoyMDY0NDYyNTIwfQ.VWqomYXkBiVZQfxuoKMkcpZfllDkhvGLzcrDz1FZDpk
FLASK_ENV=production
CLIENT_URL=https://tic-tac-toe-ten-murex-86.vercel.app
```

3. **Save changes**
4. **Redeploy your service**

## ✅ Solution 2: Fixed render.yaml (AUTOMATED)

I've moved and fixed your `render.yaml` file:

- Moved from `server/render.yaml` → `render.yaml` (project root)
- Updated build and start commands to work from root
- All environment variables are properly configured

**To use this:**

1. Commit and push the updated `render.yaml`
2. Render should automatically pick up the environment variables
3. Redeploy

## 🔍 Why This Happened

1. **render.yaml location**: Render looks for `render.yaml` in project root, but yours was in `server/`
2. **Environment variable loading**: Manual setup is more reliable than yaml in some cases

## ⚡ Quick Test

After setting the environment variables, your app should start successfully. You can test:

- Health check: `https://your-app.onrender.com/`
- API endpoints: `https://your-app.onrender.com/auth/register`

## 📞 If Still Having Issues

1. Check Render logs for detailed error messages
2. Verify all environment variables are set in Render dashboard
3. Ensure Supabase project is active and accessible
4. Test database connection from Render's IP range

**Most likely this will fix your deployment! 🚀**
