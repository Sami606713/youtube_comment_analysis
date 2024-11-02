# Start from the Python 3.10 slim base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the required files into the container
COPY requirements.txt /app
COPY app.py /app
COPY src/ /app/src/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]