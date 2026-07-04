#!/bin/bash
set -e

echo "Waiting for database..."
max_retries=30
counter=0

while ! python -c "
import sys, os, psycopg
try:
    url = os.environ.get('DATABASE_URL')
    if url and '+asyncpg' in url:
        url = url.replace('+asyncpg', '')
    psycopg.connect(url)
except Exception as e:
    print(f'DB connection failed: {e}', file=sys.stderr)
    sys.exit(1)
sys.exit(0)
"; do
  sleep 1
  counter=$((counter + 1))
  if [ $counter -ge $max_retries ]; then
    echo "Database connection timed out after $max_retries seconds."
    exit 1
  fi
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
