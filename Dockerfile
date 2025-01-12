# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV MONGO_DB_URI="mongodb+srv://dheerajsharmatechno:AsvY87FjENc5DMcd@cluster0.wd2em.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ENV MONGO_DB_NAME="GPL_DB"

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . /app

# Expose the port that the app runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]