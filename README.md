# Collab AI

**Collaborative multi-agent system for software development**
Backend built with FastAPI, LangGraph, SQLAlchemy, and an OpenAI-compatible LLM.



## Quick start

### **1. Install dependencies**

```sh
poetry install
```

### **2. Set environment variables**

Create `.env` in project root:

```
LLM_BASE_URL=https://openai-compatible-endpoint
LLM_API_KEY=api-key
LLM_MODEL=model-name

LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=
```

### **3. Run the API**

```sh
poetry run uvicorn app.main:app --reload --port 8000
```

API will be available at:

```
http://localhost:8000
```


### **4. Health Check**

```sh
curl http://localhost:8000/v1/health
```


### **5. Test DB connectivity**

Creates tables + inserts test record.

```sh
poetry run python -m src.scripts.test_db
```


### **6. Run tests**

```sh
poetry run pytest
```

---

## Core API Endpoints

###  Create a new execution

```
POST /v1/executions
```

Example:

```json
{
  "requirement": "Add a health check endpoint.",
  "orchestrator": "langgraph",
  "human_approval_after": []
}
```

Response:

* `id` — execution ID
* `status` — initial `PENDING`
* `orchestrator` — engine used


### Get execution result

```
GET /v1/executions/{execution_id}
```

Response includes:

* execution metadata
* `result` containing:

  * requirement
  * ProductOwner agent output
  * Developer agent output
  * current step



##  Architecture 

* **ProductOwner agent**: LLM-based agent (story, acceptance criteria, tasks).
* **Developer agent**: minimal stub (static summary).
* **Orchestrator**: LangGraph 1.x (dict-based state machine).
* **Storage**: SQLite via SQLAlchemy.
* **Tracing**: Langfuse spans


## Notes

* Designed for Python **3.12+**
* Built for **OpenAI-compatible** endpoints (Cerit, local models, etc.)
