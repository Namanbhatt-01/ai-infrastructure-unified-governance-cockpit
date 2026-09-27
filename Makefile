.PHONY: up down status logs test verify clean

up:
	docker compose up -d --build

down:
	docker compose down -v

status:
	docker compose ps

logs:
	docker compose logs -f

verify:
	python3 verify_unified_cockpit.py

test:
	pytest -v

clean: down
	@echo "Cleaned up all Tier 6 Unified Cockpit containers and volumes."
