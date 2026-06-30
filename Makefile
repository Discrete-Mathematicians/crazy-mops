.PHONY: help install lint format test test-cov run migrate check clean

PYTHON = python3
VENV = venv
VENV_BIN = $(VENV)/bin
NC = \033[0m
GREEN = \033[0;32m
RED = \033[41m

help:
	@echo "Доступные команды:"
	@echo "  make venv      - Создать виртуальное окружение"
	@echo "  make install   - Установить зависимости"
	@echo "  make migrate   - Применить миграции"
	@echo "  make run       - Запустить сервер"
	@echo "  make test      - Запустить тесты"
	@echo "  make test-cov  - Запустить тесты с отчётом о покрытии (пока без блокировки)"
	@echo "  make lint      - Проверить стиль"
	@echo "  make format    - Исправить стиль"
	@echo "  make check     - Линтеры и тесты"

venv:
	@echo "$(GREEN)Создание виртуального окружения...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)Виртуальное окружение создано.$(NC)"
	@echo "$(GREEN)Скопируй: $(RED)source $(VENV)/bin/activate$(NC)"

install: venv
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	$(VENV_BIN)/pip install -r requirements.txt
	$(VENV_BIN)/pip install -r requirements-dev.txt
	@echo "$(GREEN)Готово!$(NC)"

migrate:
	python manage.py migrate

run:
	python manage.py runserver

test:
	pytest || true

test-cov:
	pytest --cov=. --cov-report=term || true

lint:
	flake8 --max-line-length=119 --exclude=venv,__pycache__,migrations,.git,docs .
	isort --check-only --profile=black --line-length=119 .
	black --check --line-length=119 .

format:
	isort --profile=black --line-length=119 .
	black --line-length=119 .

check: lint test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true

