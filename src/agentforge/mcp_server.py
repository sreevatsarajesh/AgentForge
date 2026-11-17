from typing import Any
from mcp.server.fastmcp import FastMCP
from .engine import execute_tool
from .registry import TOOLS
mcp=FastMCP("AgentForge")
def _register(spec):
    async def handler(payload: dict[str,Any]) -> dict[str,Any]:
        return execute_tool(spec["tool_name"],payload)
    handler.__name__=spec["tool_name"]
    handler.__doc__=spec["description"]+" Input: payload JSON object. Output: structured result."
    mcp.tool(name=spec["tool_name"],description=handler.__doc__)(handler)
for item in TOOLS.values(): _register(item)
def main():
    mcp.run(transport="stdio")
if __name__=="__main__": main()
