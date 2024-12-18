FROM python:3.12.0 AS base

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Copy only the dependency files to take advantage of Docker cache
COPY pyproject.toml poetry.lock* /usr/src/app/

RUN pip install poetry && \
    poetry install --no-root --only main && \
    poetry add --no-cache gunicorn

#dev stage
FROM base AS dev
RUN poetry install --no-root --with dev

# Copy the rest of the application code
COPY . /usr/src/app

#prod stage
FROM base AS prod
RUN poetry install
COPY . .