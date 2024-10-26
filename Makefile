# Docker and general settings
COMPOSE_FILE = docker-compose.yaml
DATABASE_FOLDER = database  # save dump and other database files
# Load environment variables from .env file
ifneq ("$(wildcard .env)","")
    include .env
    export
endif

# General commands
.PHONY: build run start stop down clean restart logs prune

# ------DOCKER------
# build docker images
build:
	docker-compose -f $(COMPOSE_FILE) build

# Starting a project with logs
run:
	docker-compose -f $(COMPOSE_FILE) up

# Starting a project in the background (without logs)
start:
	docker-compose -f $(COMPOSE_FILE) up -d

# Stop the project
stop:
	docker-compose -f $(COMPOSE_FILE) stop

# Stop and remove containers
down:
	docker-compose -f $(COMPOSE_FILE) down

# Stop and delete containers, volumes, and networks
clean:
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans

# Restart the project
restart: stop start

# Show logs
logs:
	docker-compose -f $(COMPOSE_FILE) logs

# Remove old images
prune:
	docker system prune -f



# ------DJANGO MIGRATIONS------
.PHONY: makemigrations migrate migrations
# Create a new migration
makemigrations:
	docker-compose -f $(COMPOSE_FILE) exec web poetry run python manage.py makemigrations

# Apply migrations
migrate:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_CONTAINER) poetry run python manage.py migrate

# Creating and using database migrations
migrations: makemigrations migrate

# ------DATABASE------
.PHONY: db-dump db-restore db-shell db-clear

# Create a database dump
db-dump:
	docker-compose -f $(COMPOSE_FILE) exec db pg_dump -U $(DB_USER) -d $(DB_NAME) > database/dump.sql

# Restore the database from the dump
db-restore:
	docker-compose -f $(COMPOSE_FILE) exec -T $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) < $(DATABASE_FOLDER)/dump.sql

# Clear database
db-clear:
	docker-compose -f $(COMPOSE_FILE) exec $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Connect to the terminals
.PHONY: db-shell django-shell
# Connect to the database terminal
db-shell:
	docker-compose -f $(COMPOSE_FILE) exec $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

# Connect to the Django terminal
django-shell:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_CONTAINER) poetry run python manage.py shell

# ------DJANGO TESTS------
.PHONY: test
# Run tests
test:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_CONTAINER) poetry run python manage.py test