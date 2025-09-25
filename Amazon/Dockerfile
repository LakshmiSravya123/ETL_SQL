# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY etl/ ./etl/
COPY data/ ./data/

# Create a non-root user
RUN useradd --create-home --shell /bin/bash etl_user
RUN chown -R etl_user:etl_user /app
USER etl_user

# Set default command
CMD ["python", "etl/extract_transform.py"]
