run:
	docker compose up

run-d:
	docker compose up -d

build:
	docker compose build

createsuperuser:
	docker compose run --rm django python manage.py createsuperuser

build-no-cache:
	docker compose build --no-cache

down:
	docker compose down

down-volumes:
	docker compose down --volumes