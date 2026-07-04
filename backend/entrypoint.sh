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

echo "Starting diagnostic imports..."
python -c "
import traceback
import sys
import os
from urllib.parse import urlparse

print('1. Current working directory:', os.getcwd())
print('2. sys.path:', sys.path)
print('3. Python version:', sys.version)
print('4. PORT:', os.environ.get('PORT', 'Not set'))

db_url = os.environ.get('DATABASE_URL')
if db_url:
    print('5. DATABASE_URL scheme:', urlparse(db_url).scheme)
else:
    print('5. DATABASE_URL is not set')

print('6. Directory checks:')
print('   /app exists:', os.path.exists('/app'))
print('   /app/backend exists:', os.path.exists('/app/backend'))
print('   backend/app/main.py exists:', os.path.exists('backend/app/main.py'))

print('\n7. Attempting import...')
try:
    from backend.app.main import app
    print('Import successful')
    
    print('\n8. Starting Uvicorn programmatically...')
    import uvicorn
    # Strip any carriage return from PORT if present
    port_str = os.environ.get('PORT', '8000').strip()
    uvicorn.run(app, host='0.0.0.0', port=int(port_str))
except Exception:
    traceback.print_exc()
    sys.exit(1)
"

