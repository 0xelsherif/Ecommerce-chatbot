# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Set environment variables (optional)
# ENV NAME=Value

# Expose port 80 for the application
EXPOSE 80

# Define the command to run the application
# For example, if your main script is in src/chat.py, you would use:
CMD ["python", "src/chat.py"]

# Optionally, you can include any additional setup commands or environment configurations as needed
