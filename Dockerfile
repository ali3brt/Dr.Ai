# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the image
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container, including the model directory
COPY . /app/

# Expose the port the app runs on
EXPOSE 8080

# Run the Flask app using Gunicorn for production
CMD ["gunicorn", "-w", "1", "--timeout", "300", "-b", "0.0.0.0:8080", "app:app"]
