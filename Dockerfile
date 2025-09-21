# Use Python 3.11 as the base image
# This provides a clean environment with Python 3.11 installed
FROM python:3.11

# Set the working directory inside the container to /app
# All subsequent commands will be run in this directory
WORKDIR /app

# Copy the requirements file to the container
# This file lists all Python dependencies needed for the project
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size by not storing cache files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
# This includes all Django files, static files, and other resources
COPY . .

# Expose port 8000 to the host
# This allows the container to communicate with the outside world on port 8000
EXPOSE 8000

# Command to run when the container starts
# This starts the Django development server, binding to all network interfaces (0.0.0.0)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
