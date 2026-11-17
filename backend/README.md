# AgentForge Marketplace Backend

FastAPI service backed by the existing AgentForge registry and execution engine.

Run these commands from the AgentForge repository root:

```bash
python -m pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation is available at `http://127.0.0.1:8000/docs`.
