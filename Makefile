up:
	docker compose up -d

rebuild:
	docker-compose rm -fsv app
	docker compose up -d