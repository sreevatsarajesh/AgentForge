import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server = StdioServerParameters(command=str(Path(".venv/bin/agentforge-mcp").resolve()), args=[])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            tools = result.tools
            print("MCP tools exposed:", len(tools))
            print("Sample tools:", [tool.name for tool in tools[:10]])
            assert len(tools) == 100
            test = await session.call_tool("productivity_compound_interest", arguments={"payload": {"principal": 1000, "annual_rate": 5, "years": 1, "compounds_per_year": 1}})
            print("Test tool error:", test.isError)
            print("Test tool result:", test.content)
            assert not test.isError
            print("ALL MCP CHECKS PASSED")

asyncio.run(main())
