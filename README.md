# collab-ai


Collaborative multi-agent system for agile software development



## Quick start

### 1. Install dependencies
poetry install

### 2. Run the app
poetry run uvicorn app.main:app --reload --port 8000

### 3. Test health endpoint
curl http://localhost:8000/v1/health

### 4. Test db (Create database tables as well)
poetry run python -m src.scripts.test_db

### 5. Run tests
poetry run pytest
