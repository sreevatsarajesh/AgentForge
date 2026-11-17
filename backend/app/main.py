import json
import sys
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agentforge.engine import execute_tool
from agentforge.registry import TOOLS

with (SRC / "agentforge" / "data" / "categories.json").open(encoding="utf-8") as category_file:
    CATEGORIES = json.load(category_file)

app = FastAPI(title="AgentForge Marketplace API", version="1.1.0", description="Discovery and execution API for the AgentForge tool ecosystem")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["*"])

class ExecuteRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


def public_tool(spec: dict[str, Any]) -> dict[str, Any]:
    return {"name": spec["name"], "tool_name": spec["tool_name"], "title": spec["title"], "category": spec["category"], "description": spec["description"], "skill_path": spec.get("skill_path", "")}

@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "service": "AgentForge Marketplace API", "version": "1.1.0", "tools": len(TOOLS), "categories": len(CATEGORIES)}

@app.get("/api/overview")
def overview() -> dict[str, Any]:
    counts = {category: len(names) for category, names in CATEGORIES.items()}
    return {"tool_count": len(TOOLS), "category_count": len(CATEGORIES), "categories": counts}

@app.get("/api/categories")
def categories() -> list[dict[str, Any]]:
    return [{"name": name, "count": len(names)} for name, names in CATEGORIES.items()]

@app.get("/api/tools")
def list_tools(category: str | None = None, q: str | None = None, limit: int = Query(100, ge=1, le=250), offset: int = Query(0, ge=0)) -> dict[str, Any]:
    items = [public_tool(spec) for spec in TOOLS.values()]
    if category and category != "all":
        items = [item for item in items if item["category"] == category]
    if q:
        term = q.casefold().strip()
        items = [item for item in items if term in item["title"].casefold() or term in item["description"].casefold() or term in item["tool_name"].casefold() or term in item["category"].casefold()]
    total = len(items)
    return {"items": items[offset:offset + limit], "total": total, "limit": limit, "offset": offset}

@app.get("/api/tools/{tool_name}")
def get_tool(tool_name: str) -> dict[str, Any]:
    spec = TOOLS.get(tool_name)
    if not spec:
        raise HTTPException(status_code=404, detail="Tool not found")
    return public_tool(spec)

@app.post("/api/tools/{tool_name}/execute")
def run_tool(tool_name: str, request: ExecuteRequest) -> dict[str, Any]:
    if tool_name not in TOOLS:
        raise HTTPException(status_code=404, detail="Tool not found")
    try:
        return execute_tool(tool_name, request.payload)
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Tool execution failed") from exc
