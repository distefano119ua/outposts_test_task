# Project name
PROJECT_NAME=outposts

# Docker Compose
DC=docker-compose

.PHONY: help build up down restart logs ps clean

help:
	@echo "Available commands:"
	@echo "  make build     Build docker images"
	@echo "  make up        Start services"
	@echo "  make down      Stop services"
	@echo "  make restart   Restart services"
	@echo "  make logs      Show logs"
	@echo "  make ps        Show containers status"
	@echo "  make clean     Remove containers, networks and images"

build:
	$(DC) build

up:
	$(DC) up -d

down:
	$(DC) down

restart: down up

logs:
	$(DC) logs -f

ps:
	$(DC) ps

clean:
	$(DC) down -v --rmi local --remove-orphans