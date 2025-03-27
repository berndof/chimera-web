dev:
	@echo "Running docker in dev mode"
	@docker compose up -d --build

up:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down:
	@echo "Stopping docker compose"
	@docker compose down

migration:
	@bash -c 'read -p "nome da migração: " MIGRATION_NAME; docker exec api alembic revision --autogenerate -m "$$MIGRATION_NAME"'

migrate:
	@docker exec api uv run --env-file .env alembic upgrade head

api_logs:
	@docker logs -f api

database_logs:
	@docker logs -f database

clean_database:
	@docker volume rm database 

.PHONY: migration, migrate, clean, down, up, dev, api_logs, clean_database, database_logs
