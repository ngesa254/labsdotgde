# (Optional) Verify Tool Calls in Server Logs

To verify that your Cloud Run MCP server was called, check the service logs.

```bash
gcloud run services logs read zoo-mcp-server --region europe-west1 --limit=5
```

You should see an output log that confirms a tool call was made. 🛠️

```
2025-11-22 06:34:05 [INFO]: Processing request of type ListToolsRequest
2025-11-22 06:35:28 POST 200 https://zoo-mcp-server-683099143523.europe-west1.run.app/mcp
2025-11-22 06:35:28 INFO:     169.254.169.126:32866 - "POST /mcp HTTP/1.1" 200 OK
2025-11-22 06:35:28 [INFO]: Processing request of type CallToolRequest
2025-11-22 06:35:28 [INFO]: >>> 🛠️ Tool: 'get_animals_by_species' called for 'penguin'
```

## Understanding the Logs

| Log Entry | Meaning |
|-----------|---------|
| `Processing request of type ListToolsRequest` | Gemini CLI queried the server for available tools |
| `POST /mcp HTTP/1.1" 200 OK` | The MCP endpoint received a successful request |
| `Processing request of type CallToolRequest` | A tool was invoked |
| `Tool: 'get_animals_by_species' called for 'penguin'` | The specific tool and parameter that was called |

This confirms that your MCP server is receiving and processing requests from the Gemini CLI client.