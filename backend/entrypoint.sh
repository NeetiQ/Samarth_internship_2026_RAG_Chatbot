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

echo "Starting systematic binary-search of imports..."
python -c "
import sys, os
def trace(msg):
    print(msg, flush=True)

trace('STARTING IMPORT TRACE')
try:
    trace('Importing backend...')
    import backend
    trace('OK: imported backend')

    trace('Importing backend.app...')
    import backend.app
    trace('OK: imported backend.app')

    trace('Importing backend.app.core.settings...')
    from backend.app.core import settings
    trace('OK: imported backend.app.core.settings')

    trace('Importing backend.app.database.session...')
    from backend.app.database import session
    trace('OK: imported backend.app.database.session')
    
    trace('Importing backend.app.models.all_models...')
    from backend.app.models import all_models
    trace('OK: imported backend.app.models.all_models')

    trace('Importing backend.app.api.v1.auth...')
    from backend.app.api.v1 import auth
    trace('OK: imported backend.app.api.v1.auth')

    trace('Importing backend.app.api.v1.documents...')
    from backend.app.api.v1 import documents
    trace('OK: imported backend.app.api.v1.documents')

    trace('Importing backend.app.api.v1.chat...')
    from backend.app.api.v1 import chat
    trace('OK: imported backend.app.api.v1.chat')

    trace('Importing backend.app.api.v1.retrieval...')
    from backend.app.api.v1 import retrieval
    trace('OK: imported backend.app.api.v1.retrieval')

    trace('Importing backend.app.api.v1.__init__...')
    import backend.app.api.v1
    trace('OK: imported backend.app.api.v1')

    trace('Importing backend.app.main...')
    import backend.app.main
    trace('OK: imported backend.app.main')

    trace('SUCCESS: All imports finished without blocking.')
except Exception as e:
    import traceback
    trace('EXCEPTION CAUGHT:')
    traceback.print_exc()
    sys.exit(1)
"

