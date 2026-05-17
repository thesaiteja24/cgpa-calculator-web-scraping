# Use a lightweight python slim base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output for real-time logs/inputs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper source code
COPY scrapper.py .

# Run the python script directly as the default entrypoint.
# Using ENTRYPOINT allows passing CLI arguments directly to the docker run command!
ENTRYPOINT ["python", "scrapper.py"]
