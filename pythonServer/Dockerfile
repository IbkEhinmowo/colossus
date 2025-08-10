# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system deps needed for common Python packages (psycopg2, lxml, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer cache)
COPY requirements.txt ./
RUN pip install -r requirements.txt \
    && useradd -m -u 1000 appuser \
    && chown -R appuser /app

# Copy source
COPY . .

USER appuser

EXPOSE 8000

# Single-process entry: bot starts FastAPI internally
CMD ["python", "bot.py"]
