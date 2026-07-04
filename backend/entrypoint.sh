#!/bin/bash
set -e

echo "Waiting for database..."
while ! python -c "
import sys, os, psycopg
try:
    psycopg.connect(os.environ.get('DATABASE_URL'))
except Exception as e:
    sys.exit(1)
sys.exit(0)
" 2>/dev/null; do
  sleep 1
done

echo "Running database migrations..."
cd /app/backend
alembic upgrade head

echo "Seeding legal corpus (if configured)..."
cd /app
python backend/scripts/seed_corpus.py || {
  echo "WARNING: Corpus seed skipped or failed. API will start without pre-loaded data."
}

echo "Starting API server..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
