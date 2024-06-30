# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables 
ENV PYTHONUNBUFFERED = 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . /app/

# Expose port 5000 for the application
EXPOSE 5000

# Define the command to run the application
# For example, if your main script is in src/chat.py, you would use:
CMD ["python", "src/app.py"]

# Optionally, you can include any additional setup commands or environment configurations as needed
