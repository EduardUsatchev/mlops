# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required system libraries (including libgomp1)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app and model files into the container
COPY src/ /app/src/
COPY static/ /app/static/
COPY models/ /app/models/

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "src/serve_model.py"]
