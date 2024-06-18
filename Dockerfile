FROM python:3.8-slim

WORKDIR /flaskwebapi

# Install system dependencies
RUN apt-get update && \
    apt-get install -y sudo git libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create logs directory and set permissions
RUN mkdir -p /flaskwebapi/logs && chmod -R 777 /flaskwebapi/logs

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"]
