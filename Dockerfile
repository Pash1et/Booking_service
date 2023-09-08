FROM python:3.11-alpine

WORKDIR /app

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . .
