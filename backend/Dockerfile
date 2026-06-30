FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements.txt ./team_requirements.txt
RUN pip install --no-cache-dir -r team_requirements.txt || true

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application (running from root directory to allow imports)
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
