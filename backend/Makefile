dev:
	@echo "Running docker in dev mode"
	@docker volume rm backend_database
	@docker compose up -d --build

up:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down:
	@echo "Stopping docker compose"
	@docker compose down

clean_db:
	@echo "Cleaning Database please run 'make migrate' again"
	@docker volume rm backend_database backend_pgadmin

migration:
	@bash -c 'read -p "nome da migração: " MIGRATION_NAME; docker exec api alembic revision --autogenerate -m "$$MIGRATION_NAME"'

migrate:
	@docker exec api uv run --env-file .env alembic upgrade head

api_logs:
	@docker logs -f api

database_logs:
	@docker logs -f database


.PHONY: migration, migrate, down, up, dev, api_logs, database_logs, clean_db
