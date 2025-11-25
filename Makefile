# Makefile para Telegram Automation Bot
# Simplifica comandos comunes del proyecto

.PHONY: help install setup run docker-build docker-up docker-down docker-logs clean test lint

# Variables
PYTHON := python
PIP := pip
DOCKER_COMPOSE := docker-compose

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias Python
	$(PIP) install -r requirements.txt

setup: ## Configura el proyecto (crea .env y venv)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ .env creado. Por favor editalo con tus credenciales."; \
	fi
	@if [ ! -d venv ]; then \
		$(PYTHON) -m venv venv; \
		echo "✅ Virtual environment creado."; \
	fi

run: ## Ejecuta la aplicación en modo desarrollo
	$(PYTHON) run.py

run-prod: ## Ejecuta la aplicación con gunicorn
	gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app

docker-build: ## Construye la imagen Docker
	$(DOCKER_COMPOSE) build

docker-up: ## Levanta los contenedores
	$(DOCKER_COMPOSE) up -d

docker-up-build: ## Construye y levanta los contenedores
	$(DOCKER_COMPOSE) up -d --build

docker-down: ## Detiene y elimina los contenedores
	$(DOCKER_COMPOSE) down

docker-logs: ## Muestra los logs de los contenedores
	$(DOCKER_COMPOSE) logs -f

docker-restart: ## Reinicia los contenedores
	$(DOCKER_COMPOSE) restart

docker-shell: ## Abre una shell en el contenedor
	$(DOCKER_COMPOSE) exec telegram-bot /bin/bash

clean: ## Limpia archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

clean-all: clean ## Limpia todo incluyendo venv y Docker
	rm -rf venv
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

test: ## Ejecuta los tests (cuando se implementen)
	pytest

test-cov: ## Ejecuta los tests con cobertura
	pytest --cov=app --cov-report=html

lint: ## Ejecuta el linter (flake8)
	flake8 app/

format: ## Formatea el código con black
	black app/

check: lint test ## Ejecuta linter y tests

env-dev: ## Copia configuración de desarrollo
	cp .env.development .env

env-example: ## Copia configuración de ejemplo
	cp .env.example .env

status: ## Muestra el estado de los contenedores
	$(DOCKER_COMPOSE) ps

logs-error: ## Muestra solo los logs de error
	$(DOCKER_COMPOSE) logs --tail=100 | grep -i error

health: ## Verifica el health check
	@curl -f http://localhost:5000/health && echo "✅ Servicio saludable" || echo "❌ Servicio no responde"

.DEFAULT_GOAL := help
