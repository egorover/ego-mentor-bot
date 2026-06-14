# Makefile for EgoMentor Bot

.PHONY: help install run test lint clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run Telegram bot"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean cache files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

run:
	python -m src.presentation.telegram.bot

test:
	pytest tests/ -v --cov=src --cov-report=html

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

lint:
	ruff check src/
	black --check src/
	mypy src/

format:
	black src/
	ruff check --fix src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

docker-build:
	docker build -t ego-mentor-bot .

docker-run:
	docker run -d --name ego-mentor-bot \
		--env-file .env \
		-v $(PWD)/knowledge_base.xlsx:/app/knowledge_base.xlsx \
		ego-mentor-bot

docker-stop:
	docker stop ego-mentor-bot || true
	docker rm ego-mentor-bot || true

docker-logs:
	docker logs -f ego-mentor-bot
