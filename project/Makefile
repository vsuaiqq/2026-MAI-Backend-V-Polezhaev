.PHONY: build up down migrate makemigrations seed logs ps shell test coverage coverage-html

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

seed:
	docker compose run --rm web python manage.py seed

logs:
	docker compose logs -f

ps:
	docker compose ps

shell:
	docker compose run --rm web python manage.py shell

test:
	docker compose run --rm -e SKIP_SELENIUM=1 web python manage.py test catalog -v 2

coverage:
	docker compose run --rm -e SKIP_SELENIUM=1 web sh -c "coverage run --source=catalog manage.py test catalog && coverage report -m"

coverage-html:
	docker compose run --rm -e SKIP_SELENIUM=1 web sh -c "coverage run --source=catalog manage.py test catalog && coverage html -d /app/htmlcov"
