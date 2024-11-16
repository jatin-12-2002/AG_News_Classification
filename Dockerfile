# Use Python slim image
FROM python:3.8-slim-buster

# Install necessary system packages, including AWS CLI and Redis server
RUN apt-get update -y && apt-get install -y awscli redis-server curl

# Set the working directory
WORKDIR /app

# Copy application code to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports (FastAPI: 8080, Redis: 6379)
EXPOSE 8080 6379

# Start Redis server and FastAPI app
CMD bash -c "redis-server --daemonize yes && uvicorn app:app --host 0.0.0.0 --port 8080"