#!/bin/bash
set -e

echo "Running database migrations..."
cd /app/backend
alembic upgrade head

echo "Seeding legal corpus (if configured)..."
cd /app
python backend/scripts/seed_corpus.py || {
  echo "WARNING: Corpus seed skipped or failed. API will start without pre-loaded data."
}

echo "Starting API server..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
