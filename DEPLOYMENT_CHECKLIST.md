# ✅ Vercel Deployment Checklist

## 📋 Pre-Deployment Setup

### 1. Database Setup
- [ ] Create PostgreSQL database (Supabase/Railway/Neon)
- [ ] Get database connection string
- [ ] Test database connection

### 2. Environment Variables
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `SECRET_KEY` - Random secret key for JWT
- [ ] `PAYSTACK_SECRET_KEY` - Paystack secret key (optional)
- [ ] `PAYSTACK_PUBLIC_KEY` - Paystack public key (optional)

### 3. Files Ready
- [ ] `vercel.json` - Vercel configuration
- [ ] `api/index.py` - Vercel entry point
- [ ] `requirements.txt` - Python dependencies
- [ ] `migrate_to_postgres.py` - Database migration script

## 🚀 Deployment Steps

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel
```

### Step 4: Set Environment Variables
```bash
vercel env add DATABASE_URL
vercel env add SECRET_KEY
vercel env add PAYSTACK_SECRET_KEY
vercel env add PAYSTACK_PUBLIC_KEY
```

### Step 5: Redeploy
```bash
vercel --prod
```

## 🧪 Testing Checklist

### Basic Functionality
- [ ] Home page loads (`/`)
- [ ] API documentation loads (`/docs`)
- [ ] Health check works (`/health`)

### Authentication
- [ ] User registration works (`/auth/signup`)
- [ ] User login works (`/auth/login`)
- [ ] JWT tokens are generated
- [ ] Protected routes require authentication

### Admin Features
- [ ] Admin panel accessible (`/admin`)
- [ ] Can create new books
- [ ] Can edit existing books
- [ ] Can delete books
- [ ] Can view all orders

### User Features
- [ ] Can browse books (`/index`)
- [ ] Can add books to cart
- [ ] Cart functionality works (`/cart`)
- [ ] Can create orders
- [ ] Can view order history (`/orders`)
- [ ] Checkout process works (`/checkout/{order_id}`)

### Static Files
- [ ] Favicon displays in browser tab
- [ ] Book images load correctly
- [ ] CSS styling is applied
- [ ] JavaScript functionality works

### Database
- [ ] Database tables created
- [ ] Sample data loaded
- [ ] CRUD operations work
- [ ] Data persists between requests

## 🔧 Troubleshooting

### Common Issues
- [ ] Database connection errors
- [ ] Static files not loading
- [ ] Function timeouts
- [ ] Import errors
- [ ] Environment variable issues

### Debug Commands
```bash
# Check deployment logs
vercel logs

# Local development
vercel dev

# Check environment variables
vercel env ls

# View deployment status
vercel ls
```

## 📱 Mobile Testing
- [ ] Responsive design works on mobile
- [ ] Touch interactions work
- [ ] Forms are mobile-friendly
- [ ] Navigation works on small screens

## 🔒 Security Testing
- [ ] Authentication is required for protected routes
- [ ] Admin routes are protected
- [ ] User data is secure
- [ ] API endpoints are properly secured

## 🎯 Performance
- [ ] Pages load quickly
- [ ] Images are optimized
- [ ] No console errors
- [ ] Good user experience

## 📊 Final Verification
- [ ] Complete user journey works
- [ ] Admin can manage inventory
- [ ] Users can purchase books
- [ ] All features function correctly
- [ ] No broken links or errors

---

## 🎉 Deployment Complete!

Once all items are checked, your bookstore is ready for production! 🚀
