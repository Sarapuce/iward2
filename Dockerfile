FROM python:3.12-slim

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PASSWORD=password

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR
COPY iward2 ./iward2

RUN poetry install

WORKDIR /app/iward2
EXPOSE 8000
ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
