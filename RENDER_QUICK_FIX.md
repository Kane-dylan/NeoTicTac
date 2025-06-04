# 🚀 Quick Render Setup Guide

## Immediate Fix for "SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables are required" Error

### Option 1: Manual Environment Variables Setup (Recommended)

1. **Go to your Render Dashboard**

   - Navigate to your service
   - Click on "Environment" tab

2. **Add these environment variables:**

```bash
# Required for production
SECRET_KEY=6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9
JWT_SECRET_KEY=c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177
FLASK_ENV=production

# Supabase Configuration (replace with your actual values)
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_SERVICE_KEY=YOUR_SUPABASE_SERVICE_ROLE_KEY
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:6543/postgres?pgbouncer=true

# Frontend URL
CLIENT_URL=https://tic-tac-toe-ten-murex-86.vercel.app
```

3. **Get your Supabase values:**
   - Go to [Supabase Dashboard](https://app.supabase.com)
   - Select your project
   - Go to **Settings** → **API**
   - Copy **Project URL** → use as `SUPABASE_URL`
   - Copy **service_role** key → use as `SUPABASE_SERVICE_KEY`
   - Go to **Settings** → **Database** → **Connection info**
   - Copy connection details for `DATABASE_URL`

### Option 2: Use Updated render.yaml (Automated)

The `render.yaml` file has been updated with the correct environment variables. You just need to:

1. **Replace the placeholder values in render.yaml:**

   - `YOUR_PROJECT_ID` → your Supabase project ID
   - `YOUR_SUPABASE_PASSWORD` → your Supabase database password
   - `YOUR_SUPABASE_SERVICE_ROLE_KEY` → your service role key

2. **Redeploy your service**

### Option 3: Quick Test Deploy (Temporary)

If you want to test the deployment without Supabase first:

1. **Add only these environment variables in Render:**

```bash
SECRET_KEY=6f5cf78a0b29bafb868889e61cd18935619312de3fa90c8a985e40753e1730a9
JWT_SECRET_KEY=c567f56715e915f4ec9a8f1544b2b17afcd420c029f8368e0303495c0e2ca177
FLASK_ENV=development
CLIENT_URL=https://tic-tac-toe-ten-murex-86.vercel.app
```

2. **The app will run with SQLite temporarily** (data won't persist)

3. **Add Supabase variables later** when ready

## 🔧 Troubleshooting

### If deployment still fails:

1. **Check Render logs:**

   - Look for specific error messages
   - Verify all environment variables are set

2. **Common issues:**

   - Missing environment variables
   - Wrong Supabase project ID
   - Wrong database password
   - Network restrictions in Supabase

3. **Test connection:**
   - Verify Supabase connection in dashboard
   - Check if connection pooling is enabled
   - Ensure network restrictions allow Render IPs

## ✅ Success Checklist

- [ ] Environment variables set in Render
- [ ] Supabase project configured
- [ ] Database tables created
- [ ] Service deploys successfully
- [ ] Health check passes
- [ ] API endpoints respond
- [ ] Frontend can connect to backend

## 📞 Need Help?

If you're still having issues:

1. Share the Render deployment logs
2. Confirm your Supabase project is set up
3. Check if environment variables are correctly set in Render dashboard
