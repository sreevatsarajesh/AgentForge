import json
from pathlib import Path
_DATA=Path(__file__).resolve().parent/"data"/"plugins.json"
with _DATA.open(encoding="utf-8") as f: _REGISTRY=json.load(f)
TOOLS={x["tool_name"]:x for x in _REGISTRY["tools"]}
CATEGORIES=_REGISTRY["categories"]
