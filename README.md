# Python Microservices Demo ✅

A minimal, opinionated microservices demo using FastAPI that demonstrates: type hints, Pydantic models, dependency injection, unit testing, logging, Docker, and CI.

## Services
- `user_service` — users CRUD (in-memory storage)
- `product_service` — products CRUD (in-memory storage)

## Quickstart

- Create virtualenv and install dev deps (Poetry recommended):

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -U pip
pip install poetry
poetry install
```

- Run a service locally:

```bash
uvicorn services.user_service.app.main:app --reload --port 8001
uvicorn services.product_service.app.main:app --reload --port 8002
```

- Run tests:

```bash
pytest -q
```

## Development
- Formatting: `black`
- Linting: `ruff`
- Pre-commit hooks configured

---

## API Examples 🔧

All services run locally on different ports (example):
- User service: http://localhost:8001
- Product service: http://localhost:8002

Users
- Create user:

```bash
curl -s -X POST http://localhost:8001/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}' | jq
```

Sample response:
```json
{
  "id": "u_1a2b3c4d",
  "name": "Alice",
  "email": "alice@example.com"
}
```

- Get user:
```bash
curl -s http://localhost:8001/users/u_1a2b3c4d | jq
```

Products
- Create product:

```bash
curl -s -X POST http://localhost:8002/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget","price":12.5}' | jq
```

- Get product:
```bash
curl -s http://localhost:8002/products/p_1a2b3c4d | jq
```

---

## Architecture & Design Notes 🏗️

This repository is a minimal, opinionated demonstration of microservice patterns in Python:

- Each service is a small FastAPI application with its own models, routes, and tests. Services are independent and communicate via HTTP (or could use async messaging in a production setup).
- `libs/common` contains shared Pydantic models and small utilities. Keep this strictly to stable, interface-level things — avoid business logic in shared libs.
- Repositories in the services are simple in-memory stores for demo and tests. In real systems, replace with an asynchronous DB client and explicit connection management.
- Dependency Injection: each route declares a `Depends` hook that returns a repository instance, making it simple to replace or mock for tests.
- Tests use `httpx` ASGI transport and `pytest` with `pytest-asyncio` for fast, isolated tests.
- Each service exposes `/health` and `/metrics` endpoints. `/health` returns `{"status":"ok"}`; `/metrics` returns a small JSON object with `uptime_seconds` and counters (this is a demo; for production use `prometheus_client`).

## Running with Docker 🐳

Build and run both services using docker-compose:

```bash
docker-compose build --pull
docker-compose up
```

Each service listens on the ports defined in `docker-compose.yml`.

## Testing & CI ✅

- Unit tests: `pytest -q`
- CI is configured (`.github/workflows/ci.yml`) to run linters and tests on PRs.

## Coding Standards & Tips ✅

- Use type hints and small, focused functions. Prefer composition and single responsibility.
- Format with `black` and lint with `ruff`. Pre-commit hooks are configured for convenience.
- Keep Pydantic models in `libs/common` for shared DTOs and use `model_dump()` (Pydantic v2) to serialize models if you upgrade. Current code may raise deprecation warnings about `dict()`.

---

Refer to each service folder for additional API examples and the service-level tests.
