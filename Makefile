# Makefile for sensor-app

.PHONY: up migrate seed test shell

# 1️⃣ Build and start containers (db + web)
up:
	docker-compose up --build

# 2️⃣ Run Django migrations
migrate:
	docker-compose run --rm web python manage.py migrate

# 3️⃣ Load seed data (management command)
seed:
	docker-compose run --rm web python manage.py seed_data

# 4️⃣ Run tests (pytest)
test:
	docker-compose run --rm web pytest

# 5️⃣ Open Django shell
shell:
	docker-compose run --rm web python manage.py shell
