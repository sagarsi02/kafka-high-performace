# Use a lightweight Python image
FROM python:3.11-slim

# Create and set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY kafkaListener.py /app/

# Default command (can be overridden)
CMD ["python", "kafkaListener.py"]