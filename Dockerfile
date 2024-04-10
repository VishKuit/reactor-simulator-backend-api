# syntax=docker/dockerfile:1

# Official Python image
FROM python:3.9-alpine3.19

# Set the working directory
WORKDIR /app

# Copy the app source code to the container's working directory
COPY . /app

# Initialize the python environment
RUN python3 -m venv venv/

# Install the required packages (requirements.txt)
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/python -m pip install -r requirements.txt

# Execute the entrypoint script
CMD ["sh", "docker/entrypoint.sh"]

# Expose the port
EXPOSE 5000