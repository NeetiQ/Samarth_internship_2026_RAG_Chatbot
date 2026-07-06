# Deployment Guide

## Live Deployments

| Service   | Platform | URL                                                                    |
| --------- | -------- | ---------------------------------------------------------------------- |
| Frontend  | Vercel   | https://samarth-internship-2026-rag-chatbot.vercel.app                |
| Backend   | Render   | https://legal-rag-backend-zf50.onrender.com                           |
| Database  | Render   | PostgreSQL (managed, connection string in `DATABASE_URL`)             |
| Vector DB | Pinecone | Cloud-hosted index (API key in `PINECONE_API_KEY`)                    |

---

## Frontend Deployment (Vercel)

### Initial Setup

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) → **Add New Project**
2. Import the `Samarth_internship_2026_RAG_Chatbot` repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
4. Add Environment Variable:
   - `VITE_API_URL` = `https://legal-rag-backend-zf50.onrender.com`
5. Click **Deploy**

### SPA Routing

The frontend uses React Router with `BrowserRouter`. A `vercel.json` file in the `frontend/` directory handles client-side routing rewrites:

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

This ensures all routes (`/chat`, `/dashboard`, `/settings`, etc.) serve `index.html` instead of returning 404.

### Auto-Deployment

Vercel auto-deploys on every push to the `main` branch. Preview deployments are created for pull requests.

---

## Backend Deployment (Render)

### Configuration

The backend deploys as a Docker web service on Render. It uses the `backend/Dockerfile` for the build.

### Environment Variables

Set the following in Render's dashboard:

| Variable                   | Description                                    |
| -------------------------- | ---------------------------------------------- |
| `DATABASE_URL`             | PostgreSQL connection string (Render managed)  |
| `GEMINI_API_KEY`           | Google Gemini API key                          |
| `SECRET_KEY`               | JWT signing secret                             |
| `PINECONE_API_KEY`         | Pinecone API key                               |
| `PINECONE_INDEX`           | Pinecone index name                            |
| `PINECONE_NAMESPACE`       | Pinecone namespace (default: `default`)        |
| `EMBEDDING_MODEL`          | Embedding model name (default: `all-MiniLM-L6-v2`) |
| `EMBEDDING_DIMENSION`      | Embedding vector dimension (default: `384`)    |

### CORS Configuration

CORS origins are explicitly defined in `backend/app/main.py`:

```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost",
    "https://samarth-internship-2026-rag-chatbot.vercel.app",
    "https://samarth-internship-2026-rag-chatbot-dgxzw5len.vercel.app"
]
```

> **Important**: When adding new Vercel deployment URLs (e.g., preview deployments), update this list and push to `main` to trigger a Render redeploy.

### Health Checks

- **Liveness**: `GET /health` — Returns `{"status": "ok"}`
- **Readiness**: `GET /ready` — Checks PostgreSQL connectivity, returns `{"status": "ready"}` or HTTP 503

---

## Local Development

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/NeetiQ/Samarth_internship_2026_RAG_Chatbot.git
cd legal-rag

# Copy environment template
cp .env.example .env

# Edit .env with your settings (DATABASE_URL, GEMINI_API_KEY, PINECONE_API_KEY, etc.)
```

### 2. Backend (Local)

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`.
Swagger UI: `http://localhost:8000/api/v1/docs`

### 3. Frontend (Local)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 4. Docker Compose (Full Stack)

```bash
# Build and start all services
docker-compose up --build

# Or in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f
```

Services:
- **API**: `http://localhost:8000`
- **Frontend**: `http://localhost:3000`

---

## Database Migrations

### Run Migrations

```bash
cd backend
python -m alembic upgrade head
```

### Create New Migration

```bash
cd backend
python -m alembic revision --autogenerate -m "description"
```

---

## Docker Configuration

### Frontend Dockerfile

Multi-stage build: Node 20 (build) → Nginx Alpine (serve).

- Builds the Vite app with `VITE_API_URL` injected at build time
- Serves static files via Nginx with production-ready configuration
- Includes `.dockerignore` to exclude `node_modules`, `.env`, etc.

### Nginx Configuration (`frontend/nginx.conf`)

Production-ready with:
- SPA routing (`try_files $uri $uri/ /index.html`)
- Security headers (X-Frame-Options, X-XSS-Protection, X-Content-Type-Options)
- Static asset caching (1 year for hashed assets)
- Gzip compression

### Docker Compose (`docker-compose.yml`)

Orchestrates:
- `api`: Backend FastAPI service with environment variables and health checks
- `frontend`: Nginx-served React SPA

---

## Troubleshooting

### CORS Errors

If the frontend gets CORS errors:
1. Check that the frontend URL is listed in `backend/app/main.py` `allow_origins`
2. Commit, push to `main`, and wait for Render to redeploy

### Vercel 404 on Routes

If direct navigation to `/chat`, `/dashboard`, etc. returns 404:
1. Ensure `frontend/vercel.json` exists with the SPA rewrite rule
2. Push to `main` and trigger a Vercel redeploy

### Backend Not Starting

```bash
# Check logs on Render dashboard
# Common issues:
# 1. Missing environment variables (DATABASE_URL, SECRET_KEY)
# 2. Database migration not applied
# 3. Pinecone API key invalid or expired
```

### Database Connection Errors

```bash
# Verify the DATABASE_URL is correct
# Check that the Render PostgreSQL instance is running
# Ensure SSL mode is configured if required
```
