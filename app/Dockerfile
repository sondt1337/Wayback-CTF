# Use Python 3.9
FROM python:3.9-slim

# Set timezone to UTC to avoid time-related issues during apt update
ENV TZ=UTC

# Install necessary packages
RUN apt-get update --allow-releaseinfo-change && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy application files into the container
COPY . /app

# Install required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Run Flask startup command
CMD ["python", "app.py"]
