FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-dev --no-root

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "monolith.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
