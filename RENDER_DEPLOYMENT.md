# EasyTailor - Render Deployment Guide

Step-by-step guide to deploy EasyTailor on Render.

## 📋 Prerequisites

- GitHub account with your EasyTailor repository
- Render account (sign up at [render.com](https://render.com) - free tier available)

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code

Your code is already prepared! The following are ready:
- ✅ `Procfile` configured correctly
- ✅ `requirements.txt` with all dependencies
- ✅ Settings configured for environment variables
- ✅ WhiteNoise configured for static files
- ✅ Migrations configured to run automatically during build

### Step 2: Push to GitHub

If your code isn't on GitHub yet:

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Render deployment"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 3: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended for easy repo connection)

### Step 4: Create PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `easytailor-db` (or your choice)
   - **Database**: `easytailor` (or leave default)
   - **User**: Leave default
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: Latest (14 or 15)
   - **Plan**: Free tier is fine to start
3. Click **"Create Database"**
4. **Important**: Copy the **Internal Database URL** (you'll need this in Step 6)
   - It looks like: `postgresql://user:password@host:port/dbname`

### Step 5: Create Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect account"** if not connected
   - Select your EasyTailor repository
   - Click **"Connect"**
3. Configure the service:
   - **Name**: `easytailor` (or your choice)
   - **Region**: Same as database (recommended)
   - **Branch**: `main` (or `master`)
   - **Root Directory**: Leave empty (or `.` if needed)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
     ```
     *Note: Migrations run automatically during build (no shell access needed)*
   - **Start Command**: 
     ```
     gunicorn easytailor.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free tier is fine to start
4. Click **"Advanced"** to set environment variables (or do it after creation)

### Step 6: Set Environment Variables

In your Web Service settings, go to **"Environment"** tab and add:

1. **SECRET_KEY**
   - Generate one using this command locally:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Or use this online tool: https://djecrety.ir/
   - Add as: `SECRET_KEY` = `<your-generated-key>`

2. **DEBUG**
   - Add as: `DEBUG` = `False`

3. **ALLOWED_HOSTS**
   - Add as: `ALLOWED_HOSTS` = `your-service-name.onrender.com`
   - Replace `your-service-name` with your actual service name from Step 5
   - If you have a custom domain later, add it like: `yourdomain.com,www.yourdomain.com`

4. **DATABASE_URL**
   - Paste the **Internal Database URL** you copied in Step 4
   - Add as: `DATABASE_URL` = `<paste-internal-database-url>`

**Example Environment Variables:**
```
SECRET_KEY=django-insecure-abc123xyz789...
DEBUG=False
ALLOWED_HOSTS=easytailor.onrender.com
DATABASE_URL=postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com/easytailor
```

### Step 7: Deploy

1. Click **"Create Web Service"** (or **"Save Changes"** if editing)
2. Render will automatically start building and deploying
3. Watch the build logs - it should show:
   - Installing dependencies
   - Collecting static files
   - Running database migrations
   - Starting the service

### Step 8: Database Migrations (Automatic!)

**Good news!** Migrations run automatically during the build process. No shell access needed!

The Build Command already includes `python manage.py migrate --noinput`, so your database will be migrated every time you deploy.

**If you need to create a superuser:**

**Option A: Using Django Admin (Recommended)**
1. After deployment, visit your app URL: `https://your-service-name.onrender.com/admin/`
2. Click "Register" to create a new user account
3. The first user created will have admin access (if your settings allow it)

**Option B: Add to Build Command (One-time setup)**
If you want to create a superuser automatically, temporarily modify the Build Command to:
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'your-password')" | python manage.py shell
```
⚠️ **Important**: Change `'admin'`, `'admin@example.com'`, and `'your-password'` to your desired values, then remove this from the Build Command after first deployment for security.

**Option C: Seed Demo Data (Optional)**
To seed demo data, temporarily add to Build Command:
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py seed
```
Remove the `&& python manage.py seed` part after first deployment.

### Step 9: Access Your Application

1. Your app will be available at: `https://your-service-name.onrender.com`
2. Visit the URL and test:
   - Home page loads
   - User registration works
   - Login works
   - Orders can be created

---

## 🔧 Post-Deployment Configuration

### Custom Domain (Optional)

1. Go to your service → **"Settings"** → **"Custom Domains"**
2. Add your domain
3. Update `ALLOWED_HOSTS` environment variable to include your domain
4. Follow DNS configuration instructions from Render

### Auto-Deploy

Render automatically deploys when you push to your main branch. To disable:
- Go to **Settings** → **Build & Deploy** → Toggle **"Auto-Deploy"**

### Environment Variables Updates

To update environment variables:
1. Go to your service → **"Environment"**
2. Edit or add variables
3. Click **"Save Changes"**
4. Service will automatically restart

---

## 🐛 Troubleshooting

### Build Fails

**Error: "Error loading psycopg2 or psycopg module"**
- This error occurs when the PostgreSQL adapter cannot be loaded
- **Solution**: The project now uses `psycopg[binary]` (psycopg3) which is compatible with Python 3.13+
- If you still see this error, ensure `requirements.txt` includes `psycopg[binary]>=3.2.2` (not `psycopg2-binary`)
- Alternative: Pin Python to 3.11 or 3.12 by creating a `runtime.txt` file with `python-3.11.9` or `python-3.12.4`

**Error: "Module not found"**
- Check `requirements.txt` includes all dependencies
- Verify Python version compatibility

**Error: "collectstatic failed"**
- Check static files configuration
- Ensure `STATIC_ROOT` is set correctly (already configured)

### Application Crashes

**500 Internal Server Error**
- Check logs in Render dashboard → **"Logs"** tab
- Verify all environment variables are set
- Check `ALLOWED_HOSTS` includes your domain

**Database Connection Error**
- Verify `DATABASE_URL` is correct
- Check database is running (Render dashboard)
- Ensure database and web service are in same region

### Static Files Not Loading

- Verify `collectstatic` ran during build (check build logs)
- Check `STATIC_URL` and `STATIC_ROOT` in settings
- Ensure WhiteNoise middleware is enabled (already configured)

### Migrations Not Applied

**If migrations aren't running:**
- Verify the Build Command includes: `python manage.py migrate --noinput`
- Check build logs to see if migrations ran (look for "Running migrations" messages)
- Ensure `DATABASE_URL` environment variable is set correctly
- Check that the database is running and accessible

---

## 📊 Monitoring

### View Logs

1. Go to your service dashboard
2. Click **"Logs"** tab
3. View real-time application logs

### View Metrics

- Render provides basic metrics on free tier
- Upgrade for more detailed analytics

---

## 🔄 Updating Your Application

1. Make changes locally
2. Test locally
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
4. Render will automatically detect and deploy the changes
5. Monitor the deployment in Render dashboard

---

## 💰 Pricing

**Free Tier Includes:**
- 750 hours/month (enough for 24/7 operation)
- 512 MB RAM
- Shared CPU
- PostgreSQL database (90 days retention on free tier)

**Limitations:**
- Service may spin down after 15 minutes of inactivity (free tier)
- First request after spin-down may be slow (cold start)
- Database backups limited on free tier
- **No shell access** - Use build command or startup script for migrations

**Upgrade Options:**
- Starter: $7/month (always-on, more resources)
- Professional: $25/month (better performance)

---

## ✅ Quick Checklist

Before going live, verify:

- [ ] All environment variables set correctly
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` includes your Render domain
- [ ] Database migrations applied
- [ ] Static files collected (check build logs)
- [ ] Test user registration/login
- [ ] Test order creation
- [ ] Test tailor services (if applicable)
- [ ] Admin panel accessible (if created superuser)

---

## 🎉 You're Live!

Your EasyTailor application should now be running on Render!

**Your app URL**: `https://your-service-name.onrender.com`

**Next Steps:**
- Share your app with users
- Monitor logs for any issues
- Consider upgrading if you need better performance
- Set up custom domain (optional)

---

## 📞 Need Help?

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

Good luck! 🚀

