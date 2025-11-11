# 🚀 Render Quick Start - EasyTailor

## Before You Start

1. ✅ Code is ready (Procfile, requirements.txt, settings.py all configured)
2. ✅ Push your code to GitHub

## 5-Minute Deployment

### 1. Create Database (2 min)
- Render Dashboard → "New +" → "PostgreSQL"
- Name: `easytailor-db`
- Plan: Free
- **Copy the Internal Database URL** 📋

### 2. Create Web Service (2 min)
- Render Dashboard → "New +" → "Web Service"
- Connect GitHub repo
- Settings:
  - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
  - **Start Command**: `gunicorn easytailor.wsgi:application --bind 0.0.0.0:$PORT`

### 3. Set Environment Variables (1 min)
In Web Service → Environment tab, add:

```
SECRET_KEY=<generate-using-command-below>
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
DATABASE_URL=<paste-internal-database-url-from-step-1>
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Deploy & Migrate
- Click "Create Web Service"
- Wait for deployment (2-3 minutes)
- Go to "Shell" tab → Run: `python manage.py migrate`

### 5. Done! 🎉
Visit: `https://your-service-name.onrender.com`

---

## Full Guide
See `RENDER_DEPLOYMENT.md` for detailed instructions and troubleshooting.

