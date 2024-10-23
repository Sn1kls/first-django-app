FROM python:3.12.0

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY pyproject.toml /usr/src/app/

RUN pip install poetry && \
    poetry install && \
    poetry add --no-cache gunicorn

COPY . .

