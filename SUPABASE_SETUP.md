# 🚀 Supabase Setup Guide for Bookstore App

## 📋 Overview
This guide will walk you through setting up Supabase as your PostgreSQL database provider for the bookstore app.

## 🎯 What You'll Get
- **Free PostgreSQL Database** (up to 500MB)
- **Real-time subscriptions** (bonus feature)
- **Built-in authentication** (if you want to use it later)
- **Dashboard for database management**
- **Automatic backups**

## 🔗 Step 1: Create Supabase Account

1. **Visit Supabase**: Go to [https://supabase.com](https://supabase.com)
2. **Sign Up**: Click "Start your project"
3. **Choose Method**: 
   - GitHub (recommended)
   - Google
   - Email signup

## 🏗️ Step 2: Create New Project

1. **Click "New Project"**
2. **Fill in Details**:
   ```
   Name: bookstore
   Database Password: [Create a strong password - SAVE THIS!]
   Region: Choose closest to your location
   ```
3. **Select "Free" plan**
4. **Click "Create new project"**
5. **Wait 1-2 minutes** for setup to complete

## 🔑 Step 3: Get Database Connection String

1. **Go to Settings**:
   - Click the gear icon ⚙️ in left sidebar
   - Select "Database"

2. **Find Connection Info**:
   - Scroll down to "Connection string"
   - Click the "URI" tab
   - Copy the connection string

3. **Example Connection String**:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.abcdefghijklmnop.supabase.co:5432/postgres
   ```

4. **Replace [YOUR-PASSWORD]** with your actual password

## ⚙️ Step 4: Configure Your App

### Option A: Automatic Setup (Recommended)
```bash
python setup_supabase.py
```

### Option B: Manual Setup

1. **Install PostgreSQL Driver**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Update .env file**:
   ```bash
   # Replace the DATABASE_URL line with:
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

3. **Set Environment Variable**:
   ```bash
   # PowerShell
   $env:DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
   
   # Command Prompt
   set DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

## 🧪 Step 5: Test Connection

```bash
python test_supabase_connection.py
```

Expected output:
```
✅ Connected successfully!
🐘 PostgreSQL version: PostgreSQL 15.x
📊 Database: postgres
👤 User: postgres
```

## 📦 Step 6: Run Database Migration

```bash
python migrate_to_postgres.py
```

This will:
- Create all database tables
- Migrate existing SQLite data (if any)
- Create sample books and admin user

## 🚀 Step 7: Test Your App

```bash
# Test app imports
python -c "import app.main; print('✅ App ready!')"

# Start your app
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Visit: http://localhost:8000

## 🎯 Step 8: Deploy to Vercel

1. **Set Vercel Environment Variables**:
   ```bash
   vercel env add DATABASE_URL
   vercel env add SECRET_KEY
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

## 🔍 Supabase Dashboard Features

### Database Management
- **Table Editor**: View/edit data directly
- **SQL Editor**: Run custom queries
- **Schema Visualizer**: See table relationships

### Monitoring
- **Database Health**: Monitor performance
- **API Usage**: Track requests
- **Storage**: Monitor database size

### Security
- **Row Level Security**: Advanced access control
- **API Keys**: Manage access tokens
- **Network Restrictions**: Control access

## 📊 Free Tier Limits

| Feature | Limit |
|---------|-------|
| Database Size | 500MB |
| API Requests | 50,000/month |
| File Storage | 1GB |
| Bandwidth | 2GB/month |
| Auth Users | 50,000 |

## 🆘 Troubleshooting

### Connection Issues
```bash
# Test connection
python test_supabase_connection.py

# Check connection string format
echo $DATABASE_URL
```

### Common Errors

1. **"Connection refused"**
   - Check if project is fully set up
   - Verify connection string format
   - Ensure password is correct

2. **"Authentication failed"**
   - Double-check password
   - Make sure you're using the correct project

3. **"Database does not exist"**
   - Use `postgres` as database name
   - Don't change the database name in connection string

### Get Help
- **Supabase Docs**: https://supabase.com/docs
- **Community**: https://github.com/supabase/supabase/discussions
- **Discord**: https://discord.supabase.com

## 🎉 You're Ready!

Once setup is complete, you'll have:
- ✅ PostgreSQL database hosted on Supabase
- ✅ All tables created with sample data
- ✅ Admin user: `admin@bookstore.com` / `admin123`
- ✅ Ready for Vercel deployment

Your bookstore app is now powered by a professional, scalable database! 🚀
