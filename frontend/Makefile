
dev:
	@echo "Running docker in dev mode"
	@docker compose up -d

up:
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down:
	@echo "Stopping docker compose"
	@docker compose down


.PHONY: down, up, dev
