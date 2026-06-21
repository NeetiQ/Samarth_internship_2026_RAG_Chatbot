# Deployment Guide

TBD - Add deployment procedures and infrastructure documentation here.

## Local Development

### 1. Setup Environment

```bash
# Clone the repository
git clone <repo-url>
cd legal-rag

# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 2. Start Services

```bash
# Build and start all services
docker-compose up --build

# Or in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f
```

### 3. Verify Services

```bash
# Check service health
curl http://localhost:8000/health
curl http://localhost:3000

# Check database
docker-compose exec postgres psql -U legal_user -d legal_rag -c "SELECT 1"
```

## Production Deployment

### Docker Hub / Container Registry

```bash
# Build images
docker build -f deployment/docker/backend.Dockerfile -t legal-rag-backend:latest .
docker build -f deployment/docker/frontend.Dockerfile -t legal-rag-frontend:latest .

# Push to registry
docker tag legal-rag-backend:latest myregistry/legal-rag-backend:latest
docker push myregistry/legal-rag-backend:latest
```

### Kubernetes Deployment

```yaml
# deployment/kubernetes/backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: legal-rag-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: legal-rag-backend
  template:
    metadata:
      labels:
        app: legal-rag-backend
    spec:
      containers:
      - name: backend
        image: myregistry/legal-rag-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: legal-rag-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

Deploy:
```bash
kubectl apply -f deployment/kubernetes/
kubectl get pods
```

### AWS ECS Deployment

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name legal-rag

# Register task definitions
aws ecs register-task-definition \
  --cli-input-json file://deployment/ecs/backend-task.json

# Create service
aws ecs create-service \
  --cluster legal-rag \
  --service-name legal-rag-backend \
  --task-definition legal-rag-backend:1 \
  --desired-count 3
```

## Database Migration

### Initialize Database

```bash
# Run migrations
python -m alembic upgrade head

# Verify
docker-compose exec postgres psql -U legal_user -d legal_rag -c "\dt"
```

### Backup

```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump \
  -U legal_user legal_rag > backup.sql

# Backup Vector DB (Pinecone)
# Use Pinecone UI or API for snapshots
```

### Restore

```bash
# Restore PostgreSQL
docker-compose exec -T postgres psql \
  -U legal_user legal_rag < backup.sql
```

## SSL/TLS Configuration

### Self-Signed Certificate (Development)

```bash
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365
```

### Production Certificate (Let's Encrypt)

```bash
# Using Certbot
certbot certonly --standalone -d legal-rag.com

# Update docker-compose.yml with certificate paths
```

## Monitoring & Logging

### Prometheus Metrics

Access metrics:
```
http://localhost:9090
```

### ELK Stack (Optional)

```bash
# In docker-compose.yml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0

logstash:
  image: docker.elastic.co/logstash/logstash:8.0.0

kibana:
  image: docker.elastic.co/kibana/kibana:8.0.0
```

### CloudWatch (AWS)

```python
# In backend/app/core/logger.py
import boto3

cloudwatch = boto3.client('logs')
# Configure logging to CloudWatch
```

## Health Checks

### Liveness Probe

```bash
curl http://localhost:8000/health
```

### Readiness Probe

```bash
curl http://localhost:8000/health?check=full
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Load balancing (via reverse proxy)
# Configure nginx.conf or use AWS ALB
```

### Vertical Scaling

```yaml
# Increase resource limits in docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

## Security Hardening

### Network Security

```yaml
# docker-compose.yml
services:
  backend:
    networks:
      - legal-rag-network
    environment:
      - CORS_ORIGINS=https://legal-rag.com
      - CORS_CREDENTIALS=true
```

### Secret Management

```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name legal-rag/database-url \
  --secret-string "postgresql://..."

# Environment variable
export DATABASE_URL=$(aws secretsmanager get-secret-value \
  --secret-id legal-rag/database-url \
  --query SecretString --output text)
```

### Vulnerability Scanning

```bash
# Trivy for container scanning
trivy image myregistry/legal-rag-backend:latest

# Dependency checking
safety check  # for Python
npm audit      # for Node.js
```

## CI/CD Pipelines

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build images
        run: docker build -t legal-rag-backend:latest .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | \
          docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myregistry/legal-rag-backend:latest
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster legal-rag \
            --service legal-rag-backend \
            --force-new-deployment
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Port already in use
netstat -an | grep LISTEN

# 2. Database connection
docker-compose exec backend python -c \
  "import psycopg2; psycopg2.connect('...')"

# 3. Missing environment variables
docker-compose exec backend env | grep -E "DB|LLM"
```

### High Memory Usage

```bash
# Check memory
docker stats

# Reduce vector DB cache
# Implement query pagination
# Use connection pooling
```

### Slow Queries

```bash
# Enable query logging
# In PostgreSQL
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

# Analyze slow queries
# In Vector DB
# Use Pinecone monitoring dashboard
```

## Rollback Procedures

### Docker Compose

```bash
# Keep previous version tagged
docker tag myregistry/legal-rag-backend:latest \
           myregistry/legal-rag-backend:v1.0.0

# Rollback
docker-compose down
docker tag myregistry/legal-rag-backend:v1.0.0 \
           myregistry/legal-rag-backend:latest
docker-compose up -d
```

### Kubernetes

```bash
# View rollout history
kubectl rollout history deployment/legal-rag-backend

# Rollback to previous version
kubectl rollout undo deployment/legal-rag-backend
```

## Maintenance

### Regular Tasks

- [ ] Monitor disk space
- [ ] Rotate logs
- [ ] Update dependencies
- [ ] Backup data weekly
- [ ] Review security logs
- [ ] Check certificate expiration

### Update Procedures

```bash
# Pull latest changes
git pull

# Update dependencies
pip install --upgrade -r requirements.txt
npm update

# Rebuild and restart
docker-compose up -d --build
```
