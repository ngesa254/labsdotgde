# Verify Logs

To verify that your Cloud Run MCP server was called, check the service logs.

```bash
gcloud run services logs read safaricom-mpesa-mcp-server --region europe-west1 --limit=10
```

You should see entries similar to:

```text
POST 200 https://safaricom-mpesa-mcp-server-683099143523.europe-west1.run.app/mcp
[INFO]: >>> Tool called: list_products
[INFO]: >>> Tool called: calculate_order_total
[INFO]: >>> Tool called: initiate_stk_push
```

This confirms that your MCP server is receiving and processing requests from Gemini CLI.
