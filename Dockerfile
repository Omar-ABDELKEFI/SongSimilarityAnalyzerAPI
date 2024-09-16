# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg

# Copy the current directory contents into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run Gunicorn with a specified timeout
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "app:create_app()"]
