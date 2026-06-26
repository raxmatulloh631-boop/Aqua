FROM python:3.12-slim

# Server sozlamalari
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha kodi
COPY . .

# Static files
RUN python manage.py collectstatic --noinput

# Port
EXPOSE 8000

# Production: gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
