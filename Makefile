.PHONY: help venv install lint lint-py lint-front format format-py format-front test test-cov run migrate check clean

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
	@echo "  make test-cov  - Запустить тесты с отчётом о покрытии (порог 70%)"
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
	@command -v npm >/dev/null && npm ci || echo "$(RED)npm не найден - фронт-линтеры работать не будут$(NC)"
	@echo "$(GREEN)Готово!$(NC)"

migrate:
	$(VENV_BIN)/python manage.py migrate

run:
	$(VENV_BIN)/python manage.py runserver

test:
	$(VENV_BIN)/pytest

test-cov:
	$(VENV_BIN)/pytest --cov=. --cov-report=term --cov-fail-under=70

lint: lint-py lint-front

lint-py:
	$(VENV_BIN)/flake8 .
	$(VENV_BIN)/isort --check-only .
	$(VENV_BIN)/black --check .

lint-front:
	$(VENV_BIN)/djlint templates/ --check
	npx stylelint "static/css/*.css"

format: format-py format-front

format-front:
	$(VENV_BIN)/djlint templates/ --reformat
	npx stylelint "static/css/*.css" --fix

format-py:
	$(VENV_BIN)/isort .
	$(VENV_BIN)/black .

check: lint test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	