# Use an official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /fastapi-ml-service

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose port (FastAPI runs on 8000 by default)
EXPOSE 8000

# Command to run the app
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]