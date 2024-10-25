FROM python:3.12.0

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Copy only the dependency files to take advantage of Docker cache
COPY pyproject.toml poetry.lock* /usr/src/app/

RUN pip install poetry && \
    poetry install && \
    poetry add --no-cache gunicorn

# Copy the rest of the application code
COPY . .