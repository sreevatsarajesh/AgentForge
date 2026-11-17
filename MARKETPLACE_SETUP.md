# AgentForge Marketplace

This package adds a React/Vite marketplace frontend and a FastAPI backend to the AgentForge repository. The backend reads the existing 100-tool registry and invokes the existing local execution engine. The frontend supports browsing, category filtering, text search, tool details, JSON payload editing and local execution.

## Backend

From the AgentForge repository root:

```bash
python -m pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation: `http://127.0.0.1:8000/docs`

## Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Production build

```bash
cd frontend
npm run build
```

The production output is written to `frontend/dist`. Configure your production web server to serve that directory and proxy `/api` requests to the FastAPI service. Set `VITE_API_URL` at build time if the API is hosted on a different origin.

## API endpoints

- `GET /api/health`
- `GET /api/overview`
- `GET /api/categories`
- `GET /api/tools?category=all&q=&limit=100&offset=0`
- `GET /api/tools/{tool_name}`
- `POST /api/tools/{tool_name}/execute` with `{"payload": {}}`

The API executes tools using the existing AgentForge engine. It does not add external model calls or change the MCP stdio server.
