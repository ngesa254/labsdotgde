# (Optional) Add MCP Prompt to Server

An MCP prompt can speed up your workflow for prompts you run often by creating a shorthand for a longer prompt.

For this lab, add a prompt that prepares a payment request for a product checkout flow.

## Add the Prompt to Your Server

Add this code to your `server.py` file above the main guard:

```python
@mcp.prompt()
def checkout(product_id: str, quantity: int) -> str:
    return (
        f"Use the catalog tools to find product {product_id}, "
        f"calculate the order total for quantity {quantity}, "
        f"and then prepare an MPESA Express STK Push request summary."
    )
```

## Re-deploy to Cloud Run

```bash
cd ~/mpesa-mcp-server
gcloud run deploy safaricom-mpesa-mcp-server \
    --region=europe-west1 \
    --source=. \
    --labels=dev-tutorial=codelab-mcp
```

## Refresh Your ID Token

```bash
export ID_TOKEN=$(gcloud auth print-identity-token)
```

## Test the Custom Command

Start Gemini CLI:

```bash
gemini
```

Then run:

```text
/checkout conf-pass-001 2
```

You should see Gemini use the catalog and payment tools together in one workflow.
