ENV_FILE := ${PWD}/.env
up:
	@echo "Running docker compose"
	@docker compose up -d --build

down:
	@echo "Stopping docker compose"
	@docker compose down

migration:
	@read -p "nome da migração: " MIGRATION_NAME; 
	@uv run --env-file ${ENV_FILE} alembic revision --autogenerate -m "${MIGRATION_NAME}"

migrate:
	@uv run --env-file ${ENV_FILE} alembic upgrade head

clean:dock'''
	@docker network remove backend postgres
	@docker volume remove postgres pgadmin


.PHONY: migration, up , down, clean, migrate
