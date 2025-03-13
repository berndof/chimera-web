
dev:
	@echo "Running docker in dev mode"
	@docker compose up -d --build

up:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down:
	@echo "Stopping docker compose"
	@docker compose down

migration:
	@read -p "nome da migração: " MIGRATION_NAME; 
	@docker exec backend_api alembic revision --autogenerate -m "${MIGRATION_NAME}"

migrate:
	@docker exec backend_api uv run --env-file .env alembic upgrade head

clean:
	@docker network remove backend postgres
	@docker volume remove postgres pgadmin


.PHONY: migration, migrate, clean, down, up, dev
