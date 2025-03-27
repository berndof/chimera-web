#!/bin/bash

echo "Executando migrações Alembic..."
uv run --env-file .env alembic upgrade head

echo "Iniciando o FastAPI..."
uv run --env-file .env fastapi run --host 0.0.0.0 --port 9090 --reload