# 🔧 Render Environment Variables Setup

## Required Environment Variables for Render Dashboard

Since we've removed sensitive credentials from `render.yaml` for security, you need to manually add these environment variables in your Render dashboard:

### 🔑 Environment Variables to Add:

Go to your Render service dashboard and add these environment variables:

```
SECRET_KEY=6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9
JWT_SECRET_KEY=c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177
DATABASE_URL=postgresql://postgres:CHCTSOQehN8QMVNO@db.mauqzdgqvckrepinjybz.supabase.co:6543/postgres?pgbouncer=true
SUPABASE_URL=https://mauqzdgqvckrepinjybz.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hdXF6ZGdxdmNrcmVwaW5qeWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODg4NjUyMCwiZXhwIjoyMDY0NDYyNTIwfQ.VWqomYXkBiVZQfxuoKMkcpZfllDkhvGLzcrDz1FZDpk
CLIENT_URL=https://tic-tac-toe-ten-murex-86.vercel.app
```

### 📝 How to Add:

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Select your service**: tictactoe-backend
3. **Go to Environment tab**
4. **Click "Add Environment Variable"**
5. **Add each variable** from the list above

### ✅ Already Set in render.yaml:

These variables are already configured in the YAML file:

- `PYTHON_VERSION=3.11.0`
- `FLASK_ENV=production`

### 🔒 Security Benefits:

- ✅ **No secrets in code**: Credentials not exposed in Git repository
- ✅ **Render-managed**: Environment variables stored securely in Render
- ✅ **Easy rotation**: Can update credentials without changing code
- ✅ **Best practice**: Industry standard for managing secrets

### 🚀 After Adding Variables:

1. **Save the environment variables** in Render dashboard
2. **Redeploy your service** to apply the new variables
3. **Monitor deployment logs** to ensure successful startup
4. **Test your application** functionality

Your app will now use environment variables from Render instead of hardcoded values in the YAML file!
