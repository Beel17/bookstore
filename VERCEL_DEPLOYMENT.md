# 🚀 Vercel Deployment Guide for Bookstore App

## ⚠️ Important Note
Vercel is designed for serverless functions and static sites. While it can host FastAPI apps, there are some limitations:
- **No persistent file storage** (SQLite won't work)
- **Function timeout limits** (10 seconds for hobby, 60 seconds for pro)
- **Cold starts** may cause slower initial responses

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Database**: You'll need a cloud database (PostgreSQL recommended)

## 🗄️ Database Setup Options

### Option 1: Supabase (Recommended - Free Tier)
```bash
# 1. Go to https://supabase.com
# 2. Create a new project
# 3. Get your database URL from Settings > Database
# 4. Use format: postgresql://postgres:[password]@[host]:5432/[database]
```

### Option 2: Railway PostgreSQL
```bash
# 1. Go to https://railway.app
# 2. Create a new PostgreSQL database
# 3. Get connection string from Variables tab
```

### Option 3: Neon PostgreSQL
```bash
# 1. Go to https://neon.tech
# 2. Create a new database
# 3. Get connection string from dashboard
```

## 🚀 Deployment Steps

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy from your project directory
```bash
# Navigate to your project
cd C:\Users\Nabeel\OneDrive\Desktop\bookstore

# Deploy to Vercel
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? bookstore (or your preferred name)
# - Directory? ./
# - Override settings? No
```

### Step 4: Set Environment Variables
```bash
# Set database URL
vercel env add DATABASE_URL

# Set secret key
vercel env add SECRET_KEY

# Set Paystack keys (optional)
vercel env add PAYSTACK_SECRET_KEY
vercel env add PAYSTACK_PUBLIC_KEY
```

Or via Vercel Dashboard:
1. Go to your project dashboard
2. Settings > Environment Variables
3. Add the following variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | Production |
| `SECRET_KEY` | `your-super-secret-key-here` | Production |
| `PAYSTACK_SECRET_KEY` | `sk_test_...` | Production |
| `PAYSTACK_PUBLIC_KEY` | `pk_test_...` | Production |

### Step 5: Redeploy with Environment Variables
```bash
vercel --prod
```

## 🔧 Database Migration

Since you're moving from SQLite to PostgreSQL, you'll need to:

### Option 1: Use the setup script
```bash
# After deployment, visit your Vercel URL
# Go to /admin and create books manually
# Or run the setup script locally with the new DATABASE_URL
```

### Option 2: Manual database setup
1. Connect to your PostgreSQL database
2. Create tables using the models from `app/models.py`
3. Insert sample data

## 📁 Project Structure for Vercel

```
bookstore/
├── api/
│   └── index.py          # Vercel entry point
├── app/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Configuration
│   ├── models.py         # Database models
│   ├── templates/        # HTML templates
│   ├── static/           # Static files
│   └── ...               # Other app files
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── README.md
```

## 🧪 Testing Your Deployment

1. **Visit your Vercel URL** (provided after deployment)
2. **Test the main page**: Should show the bookstore
3. **Test authentication**: Register/login functionality
4. **Test database**: Create books via admin panel
5. **Test static files**: Favicon and images should load

## 🔍 Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Check DATABASE_URL format
   - Ensure database is accessible from internet
   - Verify credentials

2. **Function Timeout**
   - Optimize database queries
   - Consider upgrading Vercel plan
   - Use connection pooling

3. **Static Files Not Loading**
   - Check file paths in templates
   - Ensure files are in `app/static/`
   - Verify Vercel routes configuration

4. **Import Errors**
   - Check Python path in `api/index.py`
   - Verify all dependencies in `requirements.txt`

### Debug Commands:
```bash
# Check deployment logs
vercel logs

# Local development with Vercel
vercel dev

# Check environment variables
vercel env ls
```

## 🎯 Post-Deployment Checklist

- [ ] Home page loads correctly
- [ ] User registration works
- [ ] User login works
- [ ] Admin panel accessible
- [ ] Book CRUD operations work
- [ ] Cart functionality works
- [ ] Orders can be created
- [ ] Static files (images, CSS) load
- [ ] Favicon displays in browser tab
- [ ] Mobile responsive design works

## 🔄 Continuous Deployment

Once set up, Vercel will automatically deploy when you push to your connected Git repository:

```bash
git add .
git commit -m "Deploy to Vercel"
git push origin main
```

## 💰 Cost Considerations

- **Hobby Plan**: Free tier available
- **Pro Plan**: $20/month for better performance
- **Database**: Free tiers available on Supabase/Railway/Neon

## 🆘 Alternative Deployment Options

If Vercel doesn't work well for your needs, consider:
- **Railway**: Better for full-stack apps
- **Render**: Similar to Heroku
- **DigitalOcean App Platform**: More control
- **AWS/GCP**: Enterprise solutions

## 📞 Support

- Vercel Documentation: https://vercel.com/docs
- FastAPI on Vercel: https://vercel.com/guides/deploying-fastapi
- Vercel Community: https://github.com/vercel/vercel/discussions
