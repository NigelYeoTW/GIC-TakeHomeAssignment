FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-root --no-interaction

COPY . .

RUN mkdir -p uploads

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
