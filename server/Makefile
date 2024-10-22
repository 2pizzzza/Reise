# Variables
PYTHON = python3
PIP = pip3
ENV = venv
APP = app.main:app
HOST = 127.0.0.1
PORT = 8000

# Create virtual environment
venv:
	$(PYTHON) -m venv $(ENV)

# Install dependencies
install:
	$(ENV)/bin/$(PIP) install -r requirements.txt

# Run the FastAPI app
run:
	uvicorn app.main:app --host $(HOST) --port $(PORT) --reload

# Run tests
test:
	$(ENV)/bin/pytest

# Format code with black
format:
	$(ENV)/bin/black .

# Lint code with flake8
lint:
	$(ENV)/bin/flake8 .

# Clean up __pycache__ and other unnecessary files
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type d -name '*.egg-info' -exec rm -r {} +

.PHONY: venv install run test format lint clean
