"""Read-only MCP network check. Start server locally, or set remote URL and token."""
import asyncio
import os
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def main():
    headers = {}
    if os.getenv("ID_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["ID_TOKEN"]
    transport = StreamableHttpTransport(os.getenv("MCP_ENDPOINT", "http://127.0.0.1:8080/mcp"), headers=headers)
    async with Client(transport) as client:
        tools = await client.list_tools()
        print("Tools:", ", ".join(t.name for t in tools))
        result = await client.call_tool("calculate_order_total", {"items": [{"product_id": "conf-pass-001", "quantity": 2}]})
        print(result.data)

if __name__ == "__main__":
    asyncio.run(main())
