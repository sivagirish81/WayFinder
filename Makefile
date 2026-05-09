.PHONY: up down logs seed migrate test lint format api worker web check-env

COMPOSE ?= docker compose

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

seed:
	python scripts/seed_demo.py

migrate:
	cd apps/api && alembic upgrade head

test:
	cd apps/api && pytest
	cd apps/worker && pytest
	cd apps/web && npm test -- --run

lint:
	cd apps/api && ruff check .
	cd apps/worker && ruff check .
	cd apps/web && npm run lint

format:
	cd apps/api && ruff format .
	cd apps/worker && ruff format .
	cd apps/web && npm run format

api:
	cd apps/api && uvicorn wayfinder_api.main:app --reload --host 0.0.0.0 --port 8000

worker:
	cd apps/worker && python -m wayfinder_worker.worker

web:
	cd apps/web && npm run dev -- --host 0.0.0.0

check-env:
	python scripts/check_env.py
