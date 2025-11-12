#!/bin/bash
# Startup script for Render deployment
# Runs migrations automatically before starting the server

set -e  # Exit on error

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Ensuring superuser exists..."
python manage.py ensure_superuser

echo "Starting Gunicorn..."
exec gunicorn easytailor.wsgi:application --bind 0.0.0.0:$PORT

