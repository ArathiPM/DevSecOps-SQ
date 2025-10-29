# Multi-arch friendly slim image
FROM python:3.10-slim

# System settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    REDIS_DB=0

WORKDIR /app

# Install runtime deps (curl used by healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer caching)
COPY python-app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY python-app/ /app/

# Create non-root user
RUN useradd -r -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Simple healthcheck against the Flask root endpoint
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://127.0.0.1:5000/ || exit 1

# Gunicorn for production serving
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "--timeout", "60", "-b", "0.0.0.0:5000", "app:app"]
