FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements.txt ./team_requirements.txt
RUN pip install --no-cache-dir -r team_requirements.txt

# Copy application code
COPY . .

# Pre-download the SentenceTransformer model to cache it in the image
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# Set Python path to find both the root modules (rag_chat, retrieval) and backend modules (app)
ENV PYTHONPATH=/app/backend:/app

# Expose port
EXPOSE 8000

# Command to run the application (running from root directory to allow imports)
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
