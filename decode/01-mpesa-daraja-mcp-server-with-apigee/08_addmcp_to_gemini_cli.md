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

> **Token expiry:** The ID token expires after **1 hour**. If you get authentication errors later, regenerate it:
> ```bash
> export ID_TOKEN=$(gcloud auth print-identity-token)
> ```
> Then recreate the `settings.json` file (re-run the `cat > ~/.gemini/settings.json` command above).

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


![alt text](image-5.png)

## Test the MCP Server

### Step 1: Browse the Catalog

Ask Gemini:

```text
List the products in the catalog and their prices.
```

### Step 2: Build an Order

```text
I want to buy 1 coffee. Send the STK Push to 254727668102.
```

Gemini should use the MCP server tools to inspect the product catalog and calculate the order total.

### Step 3: Initiate a Real STK Push (Sandbox)

Now test the full payment flow. The sandbox defaults (BusinessShortCode, passkey, PartyB, CallBackURL, etc.) are already embedded in the tool descriptions — you don't need to type them.

> **Important:** Use your own Safaricom M-PESA registered phone number in the format `2547XXXXXXXX` (e.g. `254727668102`). You will receive an M-PESA PIN prompt on your phone. This is the sandbox — **no real money will be deducted. Any amount shown is simulated and will be automatically reversed.**

Ask Gemini:

```text
I want to buy 1 coffee. Send the STK Push to 254727668102.
```

Replace `254727668102` with **your own** Safaricom M-PESA number.

The agent already knows the sandbox shortcode, passkey, callback URL, and other defaults from the tool descriptions — you only need to say **what to buy** and **your phone number**.

The agent should:

1. Look up the product price from the catalog
2. Validate the STK Push payload
3. Initiate the STK Push request
4. Return a `ResponseCode: 0` confirmation

You will see the M-PESA PIN prompt appear on your phone. Enter your PIN to complete the payment.

### Step 4: Verify Payment via Callback

After you enter your M-PESA PIN, Safaricom sends the transaction result to the callback URL. Open your webhook.site URL in a browser to see the callback payload:

```text
https://webhook.site/75b593ff-ae70-45a0-a569-3efe2ff58b59
```

> **Tip:** If you want your own unique callback URL, visit [webhook.site](https://webhook.site) and copy the generated URL. Replace the CallBackURL in the prompt above with yours.

You can then ask Gemini to interpret the callback:

```text
Parse this STK callback payload and tell me if the payment was successful:
```

Paste the JSON payload from webhook.site into the Gemini CLI prompt. The agent will use the `parse_stk_callback` tool to extract the receipt number, amount, and transaction status.

### Money Reversal Notice

> **For sandbox:** No real money is moved. The sandbox simulates the full flow without debiting your M-PESA wallet.
>
> **For production (Go Live):** Real money is debited from the customer's M-PESA account. If you are testing against a live short code, **any money paid during testing will be reversed**. Contact [apisupport@safaricom.co.ke](mailto:apisupport@safaricom.co.ke) if you need a reversal processed.

When you are ready to end your session, type `/quit` and press `Enter`.
