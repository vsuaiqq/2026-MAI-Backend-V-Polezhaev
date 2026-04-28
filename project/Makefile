.PHONY: build up down migrate makemigrations logs ps shell

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose build web
	docker compose run --rm web python manage.py migrate

makemigrations:
	docker compose run --rm web python manage.py makemigrations

logs:
	docker compose logs -f

ps:
	docker compose ps

shell:
	docker compose run --rm web python manage.py shell
