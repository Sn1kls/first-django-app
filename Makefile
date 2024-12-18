# Docker and general settings
ENV = dev
COMPOSE_FILE = docker-compose.$(ENV).yml
ENV_FILE = ./environment/$(ENV).env
DATABASE_FOLDER = database  # save dump and other database files

# Load environment variables from .env file
ifneq ("$(wildcard $(ENV_FILE))","")
    include $(ENV_FILE)
    export
endif

# General commands
.PHONY: build run start stop down clean restart logs prune makemigrations migrate migrations \
        db-dump db-restore db-shell db-clear django-shell test dev_runbuild

# ------DOCKER------
# Build docker images
dev_build:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build
prod_build:
	$(MAKE) ENV=prod dev_build

# Starting a project with logs
dev_run:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up
prod_run:
	$(MAKE) ENV=prod dev_run

dev_runbuild:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up --build
prod_runbuild:
	$(MAKE) ENV=prod dev_runbuild

# Starting a project in the background (without logs)
dev_start:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d
prod_start:
	$(MAKE) ENV=prod dev_start

# Stop the project
dev_stop:
	docker-compose -f $(COMPOSE_FILE) stop
prod_stop:
	$(MAKE) ENV=prod dev_stop

# Stop and remove containers
dev_down:
	docker-compose -f $(COMPOSE_FILE) down
prod_down:
	$(MAKE) ENV=prod dev_down

# Stop and delete containers, volumes, and networks
dev_clean:
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans
prod_clean:
	$(MAKE) ENV=prod dev_clean

# Restart the project
dev_restart: dev_stop dev_start
prod_restart:
	$(MAKE) ENV=prod dev_restart

# Show logs
dev_logs:
	docker-compose -f $(COMPOSE_FILE) logs
prod_logs:
	$(MAKE) ENV=prod dev_logs

# ------DJANGO MIGRATIONS------
dev_makemigrations:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec web poetry run python manage.py makemigrations
prod_makemigrations:
	$(MAKE) ENV=prod dev_makemigrations

dev_migrate:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec $(WEB_CONTAINER) poetry run python manage.py migrate
prod_migrate:
	$(MAKE) ENV=prod dev_migrate

dev_migrations: dev_makemigrations dev_migrate
prod_migrations: prod_makemigrations prod_migrate

# ------DATABASE------
dev_db-dump:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec db pg_dump -U $(DB_USER) -d $(DB_NAME) > $(DATABASE_FOLDER)/dump.sql
prod_db-dump:
	$(MAKE) ENV=prod dev_db-dump

dev_db-restore:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec -T $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) < $(DATABASE_FOLDER)/dump.sql
prod_db-restore:
	$(MAKE) ENV=prod dev_db-restore

dev_db-clear:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
prod_db-clear:
	$(MAKE) ENV=prod dev_db-clear

# Connect to the terminals
dev_db-shell:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)
prod_db-shell:
	$(MAKE) ENV=prod dev_db-shell

dev_django-shell:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec $(WEB_CONTAINER) poetry run python manage.py shell
prod_django-shell:
	$(MAKE) ENV=prod dev_django-shell

# ------DJANGO TESTS------
dev_test:
	docker-compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec $(WEB_CONTAINER) poetry run python manage.py test
prod_test:
	$(MAKE) ENV=prod dev_test