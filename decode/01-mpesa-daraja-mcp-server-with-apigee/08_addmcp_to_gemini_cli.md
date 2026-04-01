# Connect the Remote MCP Server to Gemini CLI

Now that you've successfully deployed a remote MCP server, connect to it using Gemini CLI.

## Generate an ID Token

```bash
export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
export ID_TOKEN=$(gcloud auth print-identity-token)
mkdir -p ~/.gemini
```

## Create the Gemini Settings File

Create `~/.gemini/settings.json` with your MCP server configuration:

```bash
cat > ~/.gemini/settings.json << EOF
{
  "ide": {
    "hasSeenNudge": true
  },
  "mcpServers": {
    "safaricom-mpesa-remote": {
      "httpUrl": "https://safaricom-mpesa-mcp-server-${PROJECT_NUMBER}.europe-west1.run.app/mcp",
      "headers": {
        "Authorization": "Bearer ${ID_TOKEN}"
      }
    }
  },
  "security": {
    "auth": {
      "selectedType": "cloud-shell"
    }
  }
}
EOF
```

## Start Gemini CLI

```bash
gemini
```

## Verify MCP Connection

Run:

```text
/mcp
```

You should see output similar to:

```text
Configured MCP servers:

🟢 safaricom-mpesa-remote - Ready
  Tools:
  - list_products
  - get_product
  - calculate_order_total
  - generate_access_token_request
  - validate_stk_push_payload
  - initiate_stk_push
  - parse_stk_callback
  - explain_stk_error
```

## Test the MCP Server

Ask Gemini:

```text
List the products in the catalog and tell me which one costs 2,500 KES.
```

Then try:

```text
Build an STK Push request for two conference passes using the catalog total.
```

Gemini should use the MCP server tools to:

- inspect the product catalog
- calculate the order total
- construct the MPESA Express request payload

When you are ready to end your session, type `/quit` and press `Enter`.
