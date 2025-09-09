# Use an official Python runtime as a parent image
# This specific version is slim, meaning it's smaller and has fewer unneeded packages
FROM python:3.11-slim

# Set the working directory inside the container to /app
# All subsequent commands will be run from this directory
WORKDIR /app

# Copy the requirements file into the container at /app
# This is done first to leverage Docker's layer caching.
# If requirements.txt doesn't change, Docker won't reinstall packages on rebuilds.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache, which makes the image smaller
# --upgrade pip: Ensures you have the latest version of pip
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copy the rest of your application's code into the container at /app
COPY . .

# Expose port 8000 to allow traffic to the container
# This is the port your FastAPI application will run on
EXPOSE 8000

# Define the command to run your application using uvicorn
# This command will be executed when the container starts.
# --host 0.0.0.0 makes the app accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]