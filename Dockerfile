# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for postgres (libpq-dev) and building (gcc)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the application using Gunicorn (Production Server)
# -w 4: Use 4 worker processes (better performance)
# -b 0.0.0.0:5000: Bind to all network interfaces on port 5000
# app:app: Look for the file 'app.py' and the variable 'app' inside it
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]