# 🚀 Bookstore Application Deployment Guide

This guide covers various deployment options for your FastAPI bookstore application.

## 📋 Pre-Deployment Checklist

✅ **Application Features Ready:**
- [x] FastAPI backend with authentication
- [x] SQLite database with sample data
- [x] Bootstrap frontend with book images
- [x] Static files (images, CSS) properly configured
- [x] Docker configuration ready
- [x] Environment configuration setup

## 🌐 Deployment Options

### Option 1: Render.com (Recommended for Beginners)

**Pros:** Easy setup, automatic deployments, free tier
**Cons:** Limited free tier resources

#### Steps:
1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add book images and static files"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Sign up/login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service:**
   - **Name:** bookstore-app
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python setup.py`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Auto-Deploy:** Yes

4. **Environment Variables:**
   ```
   ENVIRONMENT=production
   SECRET_KEY=your-super-secure-secret-key-here
   DATABASE_URL=sqlite:///./bookstore.db
   ```

5. **Deploy:** Click "Create Web Service"

### Option 2: Railway.app

**Pros:** Simple deployment, good free tier, PostgreSQL included
**Cons:** Newer platform

#### Steps:
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Deploy:**
   ```bash
   railway init
   railway up
   ```

3. **Set Environment Variables:**
   ```bash
   railway variables set ENVIRONMENT=production
   railway variables set SECRET_KEY=your-secret-key
   ```

### Option 3: Fly.io

**Pros:** Global deployment, good performance, Docker support
**Cons:** More complex setup

#### Steps:
1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. **Initialize:**
   ```bash
   fly launch
   ```

3. **Set Secrets:**
   ```bash
   fly secrets set SECRET_KEY=your-secret-key
   fly secrets set ENVIRONMENT=production
   ```

4. **Deploy:**
   ```bash
   fly deploy
   ```

### Option 4: Heroku (Paid)

**Pros:** Mature platform, extensive documentation
**Cons:** No free tier anymore

#### Steps:
1. **Install Heroku CLI**
2. **Create app:**
   ```bash
   heroku create your-bookstore-app
   ```
3. **Set config vars:**
   ```bash
   heroku config:set ENVIRONMENT=production
   heroku config:set SECRET_KEY=your-secret-key
   ```
4. **Deploy:**
   ```bash
   git push heroku main
   ```

### Option 5: Docker Deployment

For any cloud provider that supports Docker:

#### Steps:
1. **Build image:**
   ```bash
   docker build -t bookstore-app .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 \
     -e ENVIRONMENT=production \
     -e SECRET_KEY=your-secret-key \
     bookstore-app
   ```

## 🔧 Production Configuration

### Environment Variables
Create a `.env.production` file:
```env
ENVIRONMENT=production
SECRET_KEY=your-super-secure-secret-key-here-change-this
DATABASE_URL=postgresql://user:password@host:port/dbname
PAYSTACK_SECRET_KEY=sk_live_your_live_paystack_key
PAYSTACK_PUBLIC_KEY=pk_live_your_live_paystack_key
```

### Database Migration (Production)
For production, consider using PostgreSQL:

1. **Update requirements.txt:**
   ```
   psycopg2-binary>=2.9.0
   ```

2. **Update DATABASE_URL** in environment variables

3. **Run migrations:**
   ```bash
   python setup.py
   ```

### Security Considerations

1. **Change default secret key**
2. **Use HTTPS in production**
3. **Set up proper CORS origins**
4. **Use environment variables for sensitive data**
5. **Enable database backups**

## 📊 Monitoring & Maintenance

### Health Checks
Your app includes a health check endpoint:
```
GET /health
```

### Logs
Monitor application logs for errors:
- Render: Built-in logging
- Railway: `railway logs`
- Fly.io: `fly logs`

### Database Backup
For SQLite (development):
```bash
cp bookstore.db bookstore_backup.db
```

For PostgreSQL (production):
```bash
pg_dump $DATABASE_URL > backup.sql
```

## 🎯 Post-Deployment Steps

1. **Test all endpoints:**
   - Visit your deployed URL
   - Test user registration/login
   - Test book browsing
   - Test admin panel

2. **Configure domain (optional):**
   - Add custom domain in your platform's settings
   - Update CORS settings if needed

3. **Set up monitoring:**
   - Configure uptime monitoring
   - Set up error tracking (Sentry, etc.)

4. **Performance optimization:**
   - Enable caching
   - Optimize database queries
   - Use CDN for static files

## 🚨 Troubleshooting

### Common Issues:

1. **Static files not loading:**
   - Check if static directory exists
   - Verify static file mounting in main.py

2. **Database errors:**
   - Ensure database is created
   - Check DATABASE_URL format

3. **Authentication issues:**
   - Verify SECRET_KEY is set
   - Check JWT token expiration

4. **Build failures:**
   - Check requirements.txt
   - Verify Python version compatibility

### Debug Commands:
```bash
# Check if app imports correctly
python -c "from app.main import app; print('OK')"

# Test database connection
python -c "from app.database import engine; print('DB OK')"

# Run setup
python setup.py
```

## 📈 Scaling Considerations

For high traffic:
1. **Database:** Upgrade to PostgreSQL with connection pooling
2. **Caching:** Add Redis for session storage
3. **Load Balancing:** Use multiple app instances
4. **CDN:** Serve static files from CDN
5. **Monitoring:** Add application performance monitoring

---

**Your bookstore is now ready for deployment! 🎉**

Choose the deployment option that best fits your needs and budget. Render.com is recommended for getting started quickly.
