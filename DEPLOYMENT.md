# EasyTailor Deployment Guide

This guide will help you deploy your EasyTailor Django application to production.

## 📋 Pre-Deployment Checklist

### 1. Security Settings
- [ ] Generate a new `SECRET_KEY` for production
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Ensure `SECRET_KEY` is never committed to version control

### 2. Database
- [ ] Set up PostgreSQL database (recommended for production)
- [ ] SQLite is fine for development but NOT recommended for production
- [ ] Backup your local database if you have important data

### 3. Static Files
- [ ] WhiteNoise is already configured for static file serving
- [ ] Run `collectstatic` during deployment

### 4. Dependencies
- [ ] All dependencies are listed in `requirements.txt`
- [ ] Python version: 3.8+ (Django 4.2 requirement)

---

## 🚀 Deployment Options

### Option 1: Render (Recommended - Easy & Free Tier Available)

**Steps:**

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Create a PostgreSQL Database**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Name it (e.g., `easytailor-db`)
   - Note the **Internal Database URL** (you'll need this)

3. **Create a Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `easytailor` (or your choice)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - **Start Command**: `gunicorn easytailor.wsgi:application --bind 0.0.0.0:$PORT`
     - **Plan**: Free tier is fine to start

4. **Set Environment Variables**
   In the Render dashboard, go to your service → Environment:
   ```
   SECRET_KEY=<generate-a-new-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_URL=<paste-the-internal-database-url-from-step-2>
   ```

5. **Generate Secret Key**
   Run this locally to generate a secure key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Deploy**
   - Render will automatically deploy when you push to your main branch
   - Or click "Manual Deploy" → "Deploy latest commit"

7. **Run Migrations**
   - After first deployment, go to your service → "Shell"
   - Run: `python manage.py migrate`
   - (Optional) Run: `python manage.py createsuperuser`

8. **Access Your App**
   - Your app will be available at: `https://your-app-name.onrender.com`

---

### Option 2: Railway

**Steps:**

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your EasyTailor repository

3. **Add PostgreSQL Database**
   - Click "+ New" → "Database" → "Add PostgreSQL"
   - Railway will automatically set `DATABASE_URL`

4. **Configure Environment Variables**
   - Go to your service → "Variables"
   - Add:
     ```
     SECRET_KEY=<generate-new-secret-key>
     DEBUG=False
     ALLOWED_HOSTS=*.railway.app
     ```

5. **Configure Build Settings**
   - Railway auto-detects Python projects
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start command: `gunicorn easytailor.wsgi:application --bind 0.0.0.0:$PORT`

6. **Deploy**
   - Railway auto-deploys on git push
   - Run migrations: `railway run python manage.py migrate`

---

### Option 3: Heroku

**Steps:**

1. **Install Heroku CLI**
   - Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add PostgreSQL Addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
   (This automatically sets `DATABASE_URL`)

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="<generate-new-secret-key>"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

### Option 4: DigitalOcean App Platform

**Steps:**

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://www.digitalocean.com)

2. **Create App**
   - Go to App Platform → "Create App"
   - Connect GitHub repository

3. **Configure App**
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Run Command**: `gunicorn easytailor.wsgi:application --bind 0.0.0.0:$PORT`

4. **Add Database**
   - Add PostgreSQL database component
   - DigitalOcean sets `DATABASE_URL` automatically

5. **Set Environment Variables**
   - Add in App Settings → Environment Variables:
     ```
     SECRET_KEY=<generate-new-secret-key>
     DEBUG=False
     ALLOWED_HOSTS=your-app-name.ondigitalocean.app
     ```

6. **Deploy**
   - Click "Create Resources"
   - Run migrations via console or add to build command

---

## 🔧 Post-Deployment Steps

### 1. Run Database Migrations
```bash
# On Render/Railway: Use their shell/console
python manage.py migrate
```

### 2. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 3. Seed Demo Data (Optional)
```bash
python manage.py seed
```

### 4. Verify Static Files
- Check that CSS/JS files load correctly
- If not, ensure `collectstatic` ran during build

### 5. Test Your Application
- [ ] Visit your deployed URL
- [ ] Test user registration
- [ ] Test login/logout
- [ ] Test order creation (if customer)
- [ ] Test service management (if tailor)

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use strong SECRET_KEY** - Generate a new one for production
3. **Set DEBUG=False** - Always in production
4. **Use HTTPS** - Most platforms provide this automatically
5. **Keep dependencies updated** - Regularly update `requirements.txt`
6. **Use PostgreSQL** - SQLite is not suitable for production

---

## 🐛 Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` runs during build
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Verify WhiteNoise middleware is enabled (already configured)

### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Check database credentials
- Ensure database is accessible from your hosting platform

### 500 Internal Server Error
- Check application logs in your hosting platform
- Verify `ALLOWED_HOSTS` includes your domain
- Ensure `DEBUG=False` in production (but check logs for errors)

### Migration Errors
- Run `python manage.py migrate` manually via platform shell
- Check for conflicting migrations

---

## 📝 Environment Variables Reference

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | Generated string | Yes (production) |
| `DEBUG` | Debug mode | `False` | Yes (production) |
| `ALLOWED_HOSTS` | Comma-separated domains | `example.com,www.example.com` | Yes (production) |
| `DATABASE_URL` | Database connection string | `postgresql://...` | Recommended |

---

## 🔄 Continuous Deployment

Most platforms support automatic deployment:
- **Render**: Auto-deploys on push to main branch
- **Railway**: Auto-deploys on push
- **Heroku**: Deploy with `git push heroku main`
- **DigitalOcean**: Auto-deploys on push (if configured)

---

## 📞 Need Help?

- Check platform-specific documentation
- Review Django deployment checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Check application logs in your hosting platform dashboard

---

## ✅ Quick Start (Render Example)

```bash
# 1. Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. Push to GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main

# 3. On Render:
# - Create PostgreSQL database
# - Create Web Service
# - Set environment variables
# - Deploy

# 4. Run migrations (via Render shell)
python manage.py migrate
```

Good luck with your deployment! 🚀

