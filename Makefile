PYTHON=python

.PHONY: test lint start-user start-product

test:
	poetry run pytest -q

lint:
	poetry run ruff check .
	poetry run black --check .

start-user:
	poetry run uvicorn services.user_service.app.main:app --reload --port 8001

start-product:
	poetry run uvicorn services.product_service.app.main:app --reload --port 8002
