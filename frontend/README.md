# AgentForge Marketplace Frontend

React and Vite interface for browsing the AgentForge catalogue and running tools through the local API.

```bash
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite development server proxies `/api` to `http://127.0.0.1:8000`.

For a production build:

```bash
npm run build
```

Set `VITE_API_URL` before building if the API is hosted on another origin.
