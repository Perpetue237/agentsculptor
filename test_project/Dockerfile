```dockerfile
# Base stage
FROM python:3.10-slim AS base
WORKDIR /app

# App stage
FROM base AS app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
ENV APP_ENV=development
CMD ["python", "app/main.py"]

# Worker stage
FROM base AS worker
COPY worker-requirements.txt .
RUN pip install --no-cache-dir -r worker-requirements.txt
COPY worker/ ./worker/
ENV WORKER_ENV=production
CMD ["python", "worker/worker_main.py"]