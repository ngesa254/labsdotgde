# Build the MPESA Express MCP Server with FastMCP

In this step, you will build an MCP server that exposes both a **merchant product catalog** and **Safaricom M-PESA Express** capabilities as structured tools for developers, Gemini CLI, and Google ADK agents.

Instead of calling raw APIs directly every time, the MCP server provides a reusable tool layer for:

- listing products from a static catalog
- fetching product details
- calculating order totals
- generating access tokens
- validating MPESA Express request payloads
- initiating STK Push requests
- interpreting callback payloads
- explaining common API and transaction errors

This is a much better fit for agentic systems than a toy in-memory example because **MPESA Express is asynchronous by design**:

1. The merchant system sends a request
2. Safaricom acknowledges the request
3. The customer receives an STK Push prompt on their phone
4. The customer enters their M-PESA PIN
5. Safaricom sends the final result to the merchant callback URL

In production, this pattern can sit behind **Apigee** to add policy enforcement, quotas, spike arrest, observability, and governed API exposure.

## Why One MCP Server

For this workshop, we are intentionally using **one MCP server** instead of splitting into separate catalog and payments MCP services.

That design keeps the workshop simpler while still preserving a clean separation inside the code:

- `catalog` tools for product data
- `payments` tools for MPESA Express

The ADK agent in Lab 2 will then orchestrate both domains through a single `MCPToolset`.

## Product Catalog Model

The merchant catalog is static JSON for workshop simplicity. Each product contains:

- `id`
- `name`
- `category`
- `price_kes`
- `currency`
- `inventory_status`

This gives the agent enough context to:

- search products
- retrieve prices
- build an order
- pass the total into an MPESA Express request

## What We Are Wrapping

For this lab, the MCP server is modeling the **LIPA NA M-PESA ONLINE API**, also known as **M-PESA Express / STK Push**.

Core request concepts:

- `BusinessShortCode`
- `Password`
- `Timestamp`
- `TransactionType`
- `Amount`
- `PartyA`
- `PartyB`
- `PhoneNumber`
- `CallBackURL`
- `AccountReference`
- `TransactionDesc`

Core response concepts:

- `MerchantRequestID`
- `CheckoutRequestID`
- `ResponseCode`
- `ResponseDescription`
- `CustomerMessage`

Core callback concepts:

- `ResultCode`
- `ResultDesc`
- `CallbackMetadata`

## Test the APIs Before Coding

Before writing any server code, confirm that the Safaricom sandbox APIs work from your Cloud Shell. This builds confidence that the credentials, endpoints, and payload structure are correct.

### Set Your Daraja Credentials

Export the Consumer Key and Consumer Secret from your Daraja sandbox app:

```bash
export MPESA_CONSUMER_KEY="your_consumer_key_here"
export MPESA_CONSUMER_SECRET="your_consumer_secret_here"
```

> **Where do I get these?** Go to [developer.safaricom.co.ke/dashboard/myapps](https://developer.safaricom.co.ke/dashboard/myapps), find your sandbox app (or create one — select **M-PESA EXPRESS Sandbox** as the product), and copy the **Consumer Key** and **Consumer Secret**. See [Step 07](./07_deploy_on_cloudrun.md) for a detailed walkthrough with screenshots.

### Step 1: Generate an Access Token

The DARAJA API uses OAuth 2.0 client credentials. Send your Consumer Key and Secret via HTTP Basic Auth:

```bash
ACCESS_TOKEN=$(curl -s -u "$MPESA_CONSUMER_KEY:$MPESA_CONSUMER_SECRET" \
  "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Access Token: $ACCESS_TOKEN"
```

You should see a token like:

```text
Access Token: 8vpffLWLY6txqb3xxLqWqA2XSCeT
```

> **What's happening:** You're exchanging your app credentials for a short-lived bearer token. This token is required for all subsequent API calls.

### Step 2: Compute the Password and Timestamp

The STK Push API requires a `Password` field that is the Base64 encoding of `BusinessShortCode + Passkey + Timestamp`. The `Timestamp` must match the current UTC time:

```bash
TIMESTAMP=$(date -u +%Y%m%d%H%M%S)
PASSKEY="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
PASSWORD=$(echo -n "174379${PASSKEY}${TIMESTAMP}" | base64)

echo "Timestamp: $TIMESTAMP"
echo "Password: $PASSWORD"
```

> **Why this matters:** A missing or stale Password is the #1 cause of `400.002.02` errors. The MCP server code will auto-compute this using a Pydantic model so it is **never** missing.

### Why You Need a Callback URL (webhook.site)

MPESA Express is **asynchronous**. When you send an STK Push request, Safaricom immediately returns a `ResponseCode: 0` ("accepted for processing"), but the **actual payment result** (success, cancelled, wrong PIN, timeout) arrives later as a POST request to your `CallBackURL`.

In production, this would be your backend server. For this workshop, we use [webhook.site](https://webhook.site) — a free service that gives you a temporary HTTPS URL and shows every request it receives in real time.

**Get your own callback URL:**

1. Open [https://webhook.site](https://webhook.site) in a new browser tab
2. You will see a unique URL like `https://webhook.site/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
3. Copy the full URL — this is your callback URL
4. Keep the tab open so you can see the callback payload after the payment

> **What you'll see there:** After you enter your M-PESA PIN, Safaricom sends a JSON payload to your webhook.site URL containing the `ResultCode`, `MpesaReceiptNumber`, `Amount`, `PhoneNumber`, and `TransactionDate`. This is the data that the `parse_stk_callback` MCP tool is designed to process.

For this workshop, a shared callback URL is provided in the code. Replace it with your own if you want to see the callbacks in your own webhook.site dashboard.

### Step 3: Send an STK Push Request

Replace `YOUR_PHONE_NUMBER` with your own Safaricom M-PESA registered number in the format `2547XXXXXXXX`:

```bash
curl -s -X POST "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"BusinessShortCode\": \"174379\",
    \"Password\": \"${PASSWORD}\",
    \"Timestamp\": \"${TIMESTAMP}\",
    \"TransactionType\": \"CustomerPayBillOnline\",
    \"Amount\": \"1\",
    \"PartyA\": \"YOUR_PHONE_NUMBER\",
    \"PartyB\": \"174379\",
    \"PhoneNumber\": \"YOUR_PHONE_NUMBER\",
    \"CallBackURL\": \"https://webhook.site/945572f7-298f-4173-afb2-f0392f1a8cd3\",
    \"AccountReference\": \"DECODE2026\",
    \"TransactionDesc\": \"decode pay\"
  }"
```

Expected response:

```json
{
  "MerchantRequestID": "59b5-44b3-a37b-3dad8b1200e34702",
  "CheckoutRequestID": "ws_CO_01042026184420639727668102",
  "ResponseCode": "0",
  "ResponseDescription": "Success. Request accepted for processing",
  "CustomerMessage": "Success. Request accepted for processing"
}
```

A `ResponseCode` of `0` means the request was **accepted for processing**. Your phone will receive an M-PESA PIN prompt. Enter your PIN to complete the simulated payment.

> **No real money will be deducted.** The sandbox simulates the full flow without debiting your M-PESA wallet.

### Step 4: Check the Callback

After you enter your M-PESA PIN, Safaricom posts the transaction result to the callback URL. Open your webhook.site URL in a browser:

```text
https://webhook.site/945572f7-298f-4173-afb2-f0392f1a8cd3
```

> **Tip:** Visit [webhook.site](https://webhook.site) to get your own unique callback URL.

## How This Maps to the MCP Server Code

Now that you've tested the APIs manually, here's how each curl step becomes an MCP tool in the server code:

| Manual curl step | MCP tool | What the tool adds |
|---|---|---|
| Generate access token (Step 1) | `generate_access_token_request()` | Reads credentials from environment variables instead of hardcoding |
| Compute Password + Timestamp (Step 2) | `STKPushRequest` Pydantic model | **Auto-computes** Password and Timestamp — they are never missing |
| Send STK Push (Step 3) | `initiate_stk_push()` | Validates all fields via Pydantic, then sends the request |
| Check callback (Step 4) | `parse_stk_callback()` | Extracts receipt number, amount, and status from the callback JSON |
| Debug errors | `explain_stk_error()` | Maps error codes to plain-language guidance |
| Browse products | `list_products()`, `get_product()` | Returns catalog data so the agent can look up prices |
| Calculate total | `calculate_order_total()` | Sums product prices × quantities for the Amount field |

The key insight: **the MCP server wraps the exact same API calls you just tested**, but adds validation, auto-computation, and error handling so an AI agent can use them reliably without constructing raw HTTP requests.

## Add FastMCP and HTTP Client Dependencies

Run the following command to add FastMCP and `httpx` as dependencies in the `pyproject.toml` file:

```bash
uv add fastmcp==2.12.4 httpx==0.28.1 --no-sync
```

You should see output similar to:

```text
Using CPython 3.13.2
Resolved 65 packages in 933ms
```

This will also add `httpx` to your dependencies and create a `uv.lock` file for the project.

## Create the Server File

Create and open a new `server.py` file for the MCP server source code:

```bash
cloudshell edit ~/mpesa-mcp-server/server.py
```

The `cloudshell edit` command will open the `server.py` file in the editor above the terminal.

If the command fails with an error like:

```text
Exception: Cannot send messages to client. Please try again later
```

your Cloud Shell terminal is running, but the browser editor client is not ready to receive the request. Use this fallback:

1. Create the file manually:

   ```bash
   touch ~/mpesa-mcp-server/server.py
   ```

2. Open the `mpesa-mcp-server` folder from the Cloud Shell Editor file explorer.
3. Click `server.py` in the editor.
4. Paste the server code from this step and save the file.

To confirm the project files are in place, run:

```bash
ls ~/mpesa-mcp-server
```

You should see:

```text
pyproject.toml
server.py
uv.lock
```

## Add the Server Code

Add the following MPESA Express MCP server source code in the `server.py` file:

```python
import asyncio
import base64
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict

from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
import httpx

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("MPESA Express MCP Server")

SANDBOX_BASE_URL = "https://sandbox.safaricom.co.ke"
TOKEN_PATH = "/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_PATH = "/mpesa/stkpush/v1/processrequest"
DEFAULT_TIMEOUT_SECONDS = 30.0

_cached_token: str | None = None
_token_expiry: float = 0.0

PRODUCTS = [
    {
        "id": "conf-pass-001",
        "name": "Build With AI Conference Pass",
        "category": "event",
        "price_kes": 5,
        "currency": "KES",
        "inventory_status": "in_stock",
    },
    {
        "id": "tee-001",
        "name": "DECODE Workshop T-Shirt",
        "category": "merch",
        "price_kes": 3,
        "currency": "KES",
        "inventory_status": "in_stock",
    },
    {
        "id": "coffee-001",
        "name": "Single Origin Coffee Beans",
        "category": "retail",
        "price_kes": 1,
        "currency": "KES",
        "inventory_status": "low_stock",
    },
]


def current_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def build_password(shortcode: str, passkey: str, timestamp: str) -> str:
    raw_value = f"{shortcode}{passkey}{timestamp}".encode("utf-8")
    return base64.b64encode(raw_value).decode("utf-8")


def get_env_value(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    raise ValueError(f"Missing required environment variable. Expected one of: {', '.join(names)}")


def get_http_timeout() -> float:
    return float(os.getenv("MPESA_HTTP_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS))


class STKPushRequest(BaseModel):
    """
    Pydantic model for Safaricom MPESA Express STK Push request.
    Validates inputs AND auto-computes Password and Timestamp so they are NEVER missing.
    """

    phone_number: str = Field(..., description="Safaricom number in 2547XXXXXXXX format")
    amount: int = Field(..., ge=1, description="Amount in KES (minimum 1)")
    business_shortcode: str = Field(default="174379")
    passkey: str = Field(default="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919")
    transaction_type: str = Field(default="CustomerPayBillOnline")
    party_a: str = Field(default="")
    party_b: str = Field(default="174379")
    callback_url: str = Field(default="https://webhook.site/945572f7-298f-4173-afb2-f0392f1a8cd3")
    account_reference: str = Field(default="DECODE2026", max_length=12)
    transaction_desc: str = Field(default="decode pay", max_length=13)
    timestamp: str = Field(default="", description="Auto-computed")
    password: str = Field(default="", description="Auto-computed")

    model_config = {"extra": "forbid"}

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v.startswith("2547") or len(v) != 12:
            raise ValueError("phone_number must be in format 2547XXXXXXXX")
        return v

    @field_validator("transaction_type")
    @classmethod
    def validate_tx_type(cls, v: str) -> str:
        if v not in {"CustomerPayBillOnline", "CustomerBuyGoodsOnline"}:
            raise ValueError("Must be CustomerPayBillOnline or CustomerBuyGoodsOnline")
        return v

    @field_validator("callback_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError("callback_url must use https")
        return v

    @model_validator(mode="after")
    def compute_derived(self):
        """Auto-compute party_a, timestamp, and password. These are NEVER missing."""
        if not self.party_a:
            self.party_a = self.phone_number
        self.timestamp = current_timestamp()
        self.password = build_password(self.business_shortcode, self.passkey, self.timestamp)
        return self

    def to_safaricom_payload(self) -> Dict[str, Any]:
        """Export the exact JSON body Safaricom expects — Password and Timestamp included."""
        return {
            "BusinessShortCode": self.business_shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": self.transaction_type,
            "Amount": str(self.amount),
            "PartyA": self.party_a,
            "PartyB": self.party_b,
            "PhoneNumber": self.phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": self.account_reference,
            "TransactionDesc": self.transaction_desc,
        }


@mcp.tool()
def list_products() -> Dict[str, Any]:
    """Returns the full static merchant product catalog."""
    logger.info(">>> Tool called: list_products")
    return {"products": PRODUCTS}


@mcp.tool()
def get_product(product_id: str) -> Dict[str, Any]:
    """Returns a specific product by product_id."""
    logger.info(">>> Tool called: get_product")
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return {"error": f"Product '{product_id}' not found"}


@mcp.tool()
def calculate_order_total(items: list[dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates an order total from product IDs and quantities.

    Example items:
    [{"product_id": "conf-pass-001", "quantity": 2}]
    """
    logger.info(">>> Tool called: calculate_order_total")

    lines = []
    total = 0
    for item in items:
        product = next((p for p in PRODUCTS if p["id"] == item["product_id"]), None)
        if not product:
            return {"error": f"Product '{item['product_id']}' not found"}
        quantity = int(item["quantity"])
        if quantity < 1:
            return {"error": f"Quantity must be at least 1, got {quantity} for '{product['name']}'"}
        line_total = product["price_kes"] * quantity
        total += line_total
        lines.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "quantity": quantity,
                "unit_price_kes": product["price_kes"],
                "line_total_kes": line_total,
            }
        )

    return {
        "currency": "KES",
        "line_items": lines,
        "order_total_kes": total,
    }


async def _fetch_access_token() -> Dict[str, Any]:
    """Private helper: fetches a DARAJA access token with caching. Called by both the MCP tool and initiate_stk_push."""
    global _cached_token, _token_expiry

    if _cached_token and time.time() < _token_expiry:
        logger.info("Reusing cached DARAJA token (expires in %ds)", int(_token_expiry - time.time()))
        return {
            "environment": "sandbox",
            "access_token": _cached_token,
            "cached": True,
        }

    try:
        consumer_key = get_env_value("MPESA_CONSUMER_KEY", "CONSUMER_KEY")
        consumer_secret = get_env_value("MPESA_CONSUMER_SECRET", "CONSUMER_SECRET")
    except ValueError as exc:
        logger.error("Missing credentials: %s", exc)
        return {"error": str(exc)}

    token_url = f"{SANDBOX_BASE_URL}{TOKEN_PATH}"

    try:
        async with httpx.AsyncClient(timeout=get_http_timeout()) as client:
            response = await client.get(
                token_url,
                auth=(consumer_key, consumer_secret),
            )
        response.raise_for_status()
        token_payload = response.json()
    except httpx.TimeoutException:
        logger.error("Token request timed out")
        return {"error": "Token request timed out. Safaricom sandbox may be slow - retry."}
    except httpx.HTTPStatusError as exc:
        logger.error("Token request failed: %s %s", exc.response.status_code, exc.response.text)
        return {"error": f"Token request failed with HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.HTTPError as exc:
        logger.error("Token request error: %s", exc)
        return {"error": f"Token request network error: {exc}"}

    _cached_token = token_payload["access_token"]
    expires_in = int(token_payload.get("expires_in", 3600))
    _token_expiry = time.time() + expires_in - 60
    logger.info("Cached new DARAJA token (expires in %ds)", expires_in - 60)

    return {
        "environment": "sandbox",
        "token_url": token_url,
        "auth_mode": "basic_auth",
        "access_token": _cached_token,
        "expires_in": expires_in,
        "next_step": "Use the generated token as a Bearer token for MPESA Express requests.",
    }


@mcp.tool()
async def generate_access_token_request() -> Dict[str, Any]:
    """
    Generates a DARAJA access token using environment-provided consumer credentials.
    """
    logger.info(">>> Tool called: generate_access_token_request")
    return await _fetch_access_token()


@mcp.tool()
def validate_stk_push_payload(
    phone_number: str,
    amount: int,
    business_shortcode: str = "174379",
    transaction_type: str = "CustomerPayBillOnline",
    party_a: str = "",
    party_b: str = "174379",
    callback_url: str = "https://webhook.site/945572f7-298f-4173-afb2-f0392f1a8cd3",
    account_reference: str = "DECODE2026",
    transaction_desc: str = "decode pay",
) -> Dict[str, Any]:
    """
    Validates an MPESA Express STK Push payload using Pydantic.

    IMPORTANT: Before calling this tool, you MUST ask the user for their
    Safaricom M-PESA phone number in the format 2547XXXXXXXX.
    Do NOT assume, guess, or hardcode a phone number.

    Only phone_number and amount are required - all other fields have sandbox defaults.
    Returns the COMPLETE Safaricom payload including auto-computed Password and Timestamp.
    This is a VALIDATION-ONLY tool. To actually send the payment, call initiate_stk_push.
    Do NOT use Shell or curl to send the request yourself.
    """
    logger.info(">>> Tool called: validate_stk_push_payload")

    try:
        request = STKPushRequest(
            phone_number=phone_number,
            amount=amount,
            business_shortcode=business_shortcode,
            transaction_type=transaction_type,
            party_a=party_a,
            party_b=party_b,
            callback_url=callback_url,
            account_reference=account_reference,
            transaction_desc=transaction_desc,
        )
    except ValidationError as exc:
        return {
            "valid": False,
            "errors": [e["msg"] for e in exc.errors()],
        }

    return {
        "valid": True,
        "errors": [],
        "normalized_payload": request.to_safaricom_payload(),
    }


@mcp.tool()
async def initiate_stk_push(
    phone_number: str,
    amount: int,
    business_shortcode: str = "174379",
    passkey: str = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
    transaction_type: str = "CustomerPayBillOnline",
    party_a: str = "",
    party_b: str = "174379",
    callback_url: str = "https://webhook.site/945572f7-298f-4173-afb2-f0392f1a8cd3",
    account_reference: str = "DECODE2026",
    transaction_desc: str = "decode pay",
) -> Dict[str, Any]:
    """
    Initiates a Safaricom MPESA Express STK Push payment.

    IMPORTANT: Before calling this tool, you MUST ask the user for their
    Safaricom M-PESA phone number in the format 2547XXXXXXXX.
    Do NOT assume, guess, or hardcode a phone number.

    Only phone_number and amount are required.
    All other parameters have sandbox defaults built in.
    Password and Timestamp are auto-computed by the Pydantic model.
    """
    logger.info(">>> Tool called: initiate_stk_push")

    try:
        request = STKPushRequest(
            phone_number=phone_number,
            amount=amount,
            business_shortcode=business_shortcode,
            passkey=passkey,
            transaction_type=transaction_type,
            party_a=party_a,
            party_b=party_b,
            callback_url=callback_url,
            account_reference=account_reference,
            transaction_desc=transaction_desc,
        )
    except ValidationError as exc:
        return {"valid": False, "errors": [e["msg"] for e in exc.errors()]}

    token_info = await _fetch_access_token()
    if "error" in token_info:
        return {"error": f"Could not get access token: {token_info['error']}"}

    access_token = token_info["access_token"]
    request_body = request.to_safaricom_payload()

    try:
        async with httpx.AsyncClient(timeout=get_http_timeout()) as client:
            response = await client.post(
                f"{SANDBOX_BASE_URL}{STK_PUSH_PATH}",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json=request_body,
            )
        response.raise_for_status()
        response_payload = response.json()
    except httpx.TimeoutException:
        logger.error("STK Push request timed out")
        return {"error": "STK Push request timed out. Safaricom sandbox may be slow - retry."}
    except httpx.HTTPStatusError as exc:
        logger.error("STK Push failed: %s %s", exc.response.status_code, exc.response.text)
        return {"error": f"STK Push failed with HTTP {exc.response.status_code}: {exc.response.text}"}
    except httpx.HTTPError as exc:
        logger.error("STK Push network error: %s", exc)
        return {"error": f"STK Push network error: {exc}"}

    return {
        "environment": "sandbox",
        "endpoint": f"{SANDBOX_BASE_URL}{STK_PUSH_PATH}",
        "request_body": request_body,
        "response": response_payload,
        "accepted_for_processing": response_payload.get("ResponseCode") == "0",
        "checkout_request_id": response_payload.get("CheckoutRequestID"),
        "merchant_request_id": response_payload.get("MerchantRequestID"),
        "notes": [
            "This API is asynchronous.",
            "A ResponseCode of 0 means the request was accepted for processing.",
            "Final transaction outcome arrives on the callback URL.",
        ],
    }


@mcp.tool()
def parse_stk_callback(callback_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a Safaricom callback payload into a compact, agent-friendly structure.
    """
    logger.info(">>> Tool called: parse_stk_callback")

    stk_callback = callback_payload.get("Body", {}).get("stkCallback", {})
    metadata_items = stk_callback.get("CallbackMetadata", {}).get("Item", [])
    metadata = {item.get("Name"): item.get("Value") for item in metadata_items if "Name" in item}

    return {
        "merchant_request_id": stk_callback.get("MerchantRequestID"),
        "checkout_request_id": stk_callback.get("CheckoutRequestID"),
        "result_code": stk_callback.get("ResultCode"),
        "result_description": stk_callback.get("ResultDesc"),
        "successful": stk_callback.get("ResultCode") == 0,
        "amount": metadata.get("Amount"),
        "mpesa_receipt_number": metadata.get("MpesaReceiptNumber"),
        "transaction_date": metadata.get("TransactionDate"),
        "phone_number": metadata.get("PhoneNumber"),
    }


@mcp.tool()
def explain_stk_error(code: str) -> Dict[str, str]:
    """
    Maps common DARAJA and MPESA Express error codes to plain-language guidance.
    """
    logger.info(">>> Tool called: explain_stk_error")

    errors = {
        # Result codes (transaction outcome)
        "0": "Success. The transaction was processed successfully on M-PESA.",
        "1": "Insufficient balance. The customer does not have enough money in their M-PESA account.",
        "2": "Declined: amount is below the minimum C2B transaction limit (currently KES 1).",
        "3": "Declined: amount exceeds the maximum C2B transaction limit.",
        "4": "Declined: would exceed the customer's daily transfer limit (currently KES 500,000).",
        "8": "Declined: would exceed the Pay Bill or Till Number account balance limit.",
        "17": "Rule limited. Duplicate transaction - same amount to same customer within 2 minutes. Wait and retry.",
        "1019": "Transaction expired. The customer did not respond in time.",
        "1025": "Push request failed. The USSD prompt may be too long (over 182 chars). Shorten the AccountReference.",
        "1032": "Request cancelled by the customer.",
        "1037": "Customer unreachable. Phone may be offline, busy, or in another M-PESA session.",
        "2001": "Invalid M-PESA PIN entered by the customer. Advise them to retry with the correct PIN.",
        "2028": "Request not permitted. Check TransactionType and PartyB: use CustomerPayBillOnline for PayBill, CustomerBuyGoodsOnline for Till.",
        "8006": "Security credential locked. Customer should contact Safaricom Care (call 100 or 200).",
        "SFC_IC0003": "Operator does not exist. Verify TransactionType and PartyB match your short code type.",
        # API error codes (request-level)
        "400.002.02": "Invalid request payload. Check required fields, data types, and Content-Type: application/json header.",
        "404.001.01": "Resource not found. Verify you are calling the correct API endpoint.",
        "404.001.03": "Invalid access token. Generate a fresh token - tokens expire every hour.",
        "405.001": "Method not allowed. Ensure you are sending a POST request, not GET.",
        "500.001.1001": "Server error. Could be: merchant does not exist, wrong Password encoding, or subscriber locked in another session.",
        "500.003.02": "System busy or spike arrest violation. Retry with backoff and reduce request rate.",
        "500.003.03": "Quota violation. Too many requests - reduce your request volume.",
        "500.003.1001": "Internal server error. Verify your setup matches the API documentation.",
    }

    return {
        "code": code,
        "meaning": errors.get(code, "Unknown error code. Check the Safaricom DARAJA documentation."),
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info("🚀 MPESA Express MCP server started on port %s", port)
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=port,
        )
    )
```

After saving the file, verify that `server.py` is no longer empty:

```bash
cat ~/mpesa-mcp-server/server.py
```

If the file prints the Python source code you just pasted, you are ready for the next step.

## What to Customize

The server code works **out of the box** for this workshop with the shared sandbox credentials. If you want to use your own setup, here's exactly what to change:

| What | Where in `server.py` | Default (works for workshop) | Change to |
|---|---|---|---|
| **Callback URL** | `STKPushRequest.callback_url` field default (line ~35 of the class) | `https://webhook.site/945572f7-298f-4173-afb2-f0392f1a8cd3` | Your own [webhook.site](https://webhook.site) URL |
| **Product catalog** | `PRODUCTS` list | 3 workshop items at KES 5, 3, 1 | Your own products and prices |
| **Account reference** | `STKPushRequest.account_reference` field default | `DECODE2026` | Your own reference (max 12 chars) |

### What You Do NOT Change in server.py

These values are either **auto-computed** or **set at deploy time**, not in the source code:

| What | Why you don't touch it |
|---|---|
| **Consumer Key / Secret** | Passed as environment variables at deploy time (`MPESA_CONSUMER_KEY`, `MPESA_CONSUMER_SECRET`). Never hardcode credentials in source files. |
| **Password** | Auto-computed by the `STKPushRequest` Pydantic model from `BusinessShortCode + Passkey + Timestamp`. It is **never** missing. |
| **Timestamp** | Auto-computed at request time using UTC. Always fresh. |
| **Phone number** | Passed as a tool parameter when calling `initiate_stk_push`. The agent or user provides it at runtime. |
| **BusinessShortCode / Passkey** | Sandbox defaults (`174379` / standard sandbox passkey). Only change these when moving to production Go Live. |

> **For this workshop:** You can paste the code exactly as-is and proceed to the next step. No changes are required.

## Understanding the Code

The server defines eight MCP tools:

| Tool | Description |
|------|-------------|
| `list_products()` | Returns the full workshop product catalog |
| `get_product(product_id)` | Fetches one product and its price |
| `calculate_order_total(items)` | Totals a basket in KES |
| `generate_access_token_request()` | Generates a live DARAJA access token from environment-provided credentials |
| `validate_stk_push_payload(...)` | Checks required fields and normalizes the request payload |
| `initiate_stk_push(...)` | Validates the payload, fetches a token, and sends a real STK Push request |
| `parse_stk_callback(callback_payload)` | Converts callback payloads into a smaller, agent-friendly structure |
| `explain_stk_error(code)` | Explains common transaction and API errors with mitigation hints |

This structure is deliberate:

- **validation** is separate from **execution**
- **request submission** is separate from **callback interpretation**
- **error explanation** is separate from the raw API payload
- **credentials** stay in environment variables instead of source code

That separation makes the MCP tools easier for both humans and agents to use correctly.

## Why This Matters for the Rest of the Lab

In the next steps, you will deploy this MCP server to Cloud Run and connect to it from Gemini CLI. Later, in Lab 2, a Google ADK agent will use these tools to reason about payment workflows without needing to speak directly to raw DARAJA APIs every time.
