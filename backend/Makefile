run:
	docker compose up

run-d:
	docker compose up -d

build:
	docker compose build

build-no-cache:
	docker compose build --no-cache

db-shell:
	docker compose run  --rm django python manage.py dbshell

shell-plus:
	docker compose run --rm django python manage.py shell_plus --ipython

createsuperuser:
	docker compose run --rm django python manage.py createsuperuser

makemigrations:
	docker compose run --rm django python manage.py makemigrations $(ARGS)

migrate:
	docker compose run --rm django python manage.py migrate $(ARGS)

check:
	pre-commit run --all-files

down:
	docker compose down

down-volumes:
	docker compose down --volumes

logs:
	docker compose logs -f django celeryworker mongo

test:
	docker compose run --rm django pytest