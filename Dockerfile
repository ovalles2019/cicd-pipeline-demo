# Build stage — install deps and keep the final image lean
# linux/amd64 required for Render image-backed services
FROM --platform=linux/amd64 python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime image
FROM --platform=linux/amd64 python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=local \
    APP_VERSION=0.0.0

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app ./app

# Non-root user for safer container runs
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

# Render (and most PaaS) inject $PORT — bind 0.0.0.0 so the service is reachable
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
