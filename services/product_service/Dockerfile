FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-dev -n
COPY . /app
EXPOSE 8002
CMD ["uvicorn", "services.product_service.app.main:app", "--host", "0.0.0.0", "--port", "8002"]}