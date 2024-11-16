# Use Python slim image
FROM python:3.8-slim-buster

# Install necessary system packages, including AWS CLI, Redis server, and Supervisor
RUN apt-get update -y && apt-get install -y \
    awscli \
    redis-server \
    supervisor \
    curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application code to the container
COPY . /app

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports (FastAPI: 8080, Redis: 6379)
EXPOSE 8080 6379

# Start Supervisor to manage all processes
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]