# (Optional) Add MCP Prompt to Server

An MCP prompt can speed up your workflow for prompts you run often by creating a shorthand for a longer prompt.

For this lab, add a prompt that prepares a payment request for a product checkout flow.

## Add the Prompt to Your Server

Add this code to your `server.py` file above the main guard:

```python
@mcp.prompt()
def checkout(product_id: str, quantity: int, phone_number: str) -> str:
    return (
        f"Use the catalog tools to find product {product_id}, "
        f"calculate the order total for quantity {quantity}, "
        f"then initiate an MPESA Express STK Push payment using these sandbox defaults: "
        f"BusinessShortCode 174379, PartyB 174379, "
        f"passkey bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919, "
        f"TransactionType CustomerPayBillOnline, "
        f"CallBackURL https://webhook.site/75b593ff-ae70-45a0-a569-3efe2ff58b59, "
        f"AccountReference DECODE2026, TransactionDesc decode pay, "
        f"PhoneNumber {phone_number}, PartyA {phone_number}."
    )
```

## Re-deploy to Cloud Run

```bash
cd ~/mpesa-mcp-server
gcloud run deploy safaricom-mpesa-mcp-server \
    --region=europe-west1 \
    --source=. \
    --set-env-vars="MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY},MPESA_CONSUMER_SECRET=${MPESA_CONSUMER_SECRET}" \
    --labels=dev-tutorial=codelab-mcp
```

> **Note:** If your terminal session has expired and you no longer have `MPESA_CONSUMER_KEY` and `MPESA_CONSUMER_SECRET` set, re-export them first (see Step 07).

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
