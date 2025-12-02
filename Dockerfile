# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# # Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#            build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first for better caching
COPY pyproject.toml ./
COPY uv.lock ./

# Install uv first
RUN pip install --no-cache-dir uv

# Install Python dependencies
RUN uv pip install --system -e .

# Copy the entire app source
COPY . .

# Create the data directory for memories
RUN mkdir -p app/data

# Expose the application port
EXPOSE 7330

# Run the application
CMD ["python", "manage.py"]