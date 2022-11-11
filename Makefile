run-dev:
	docker-compose up -d

import-data:
	docker-compose exec fast_api sh -c "python -m app.commands.import import-pharmacy-data -f 'data/pharmacies.json'"
	docker-compose exec fast_api sh -c "python -m app.commands.import import-user-data -f 'data/users.json'"

add-test-user:
	docker-compose exec fast_api sh -c "python -m app.commands.import create-test-user"

build-local:
	docker-compose up -d --build
	docker-compose exec fast_api sh -c "alembic upgrade head"

stop-dev:
	docker-compose down -v
