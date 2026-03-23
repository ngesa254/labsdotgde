# Build the MPESA Express MCP Server with FastMCP

In this step, you will build an MCP server that exposes **Safaricom M-PESA Express** capabilities as structured tools for developers, Gemini CLI, and Google ADK agents.

Instead of calling raw DARAJA endpoints directly every time, the MCP server provides a reusable tool layer for:

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

## Add FastMCP Dependency

Run the following command to add FastMCP as a dependency in the `pyproject.toml` file:

```bash
uv add fastmcp==2.12.4 --no-sync
```

You should see output similar to:

```text
Using CPython 3.13.2
Resolved 65 packages in 933ms
```

This will also add a `uv.lock` file to your project.

## Create the Server File

Create and open a new `server.py` file for the MCP server source code:

```bash
cloudshell edit ~/mcp-on-cloudrun/server.py
```

The `cloudshell edit` command will open the `server.py` file in the editor above the terminal.

## Add the Server Code

Add the following MPESA Express MCP server source code in the `server.py` file:

```python
import asyncio
import base64
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("MPESA Express MCP Server")

SANDBOX_BASE_URL = "https://sandbox.safaricom.co.ke"
STK_PUSH_PATH = "/mpesa/stkpush/v1/processrequest"


def current_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def build_password(shortcode: str, passkey: str, timestamp: str) -> str:
    raw_value = f"{shortcode}{passkey}{timestamp}".encode("utf-8")
    return base64.b64encode(raw_value).decode("utf-8")


@mcp.tool()
def generate_access_token_request() -> Dict[str, Any]:
    """
    Returns the OAuth endpoint and auth mode required to obtain a DARAJA access token.

    In a production implementation, this tool would make the outbound token request
    using the consumer key and consumer secret stored in Secret Manager.
    """
    logger.info(">>> Tool called: generate_access_token_request")
    return {
        "environment": "sandbox",
        "token_url": f"{SANDBOX_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
        "auth_mode": "basic_auth",
        "required_secrets": ["consumer_key", "consumer_secret"],
        "next_step": "Use the generated token as a Bearer token for MPESA Express requests.",
    }


@mcp.tool()
def validate_stk_push_payload(
    business_shortcode: str,
    transaction_type: str,
    amount: int,
    party_a: str,
    party_b: str,
    phone_number: str,
    callback_url: str,
    account_reference: str,
    transaction_desc: str,
) -> Dict[str, Any]:
    """
    Performs basic validation for an MPESA Express request before it is sent.
    """
    logger.info(">>> Tool called: validate_stk_push_payload")

    errors = []

    if transaction_type not in {"CustomerPayBillOnline", "CustomerBuyGoodsOnline"}:
        errors.append("transaction_type must be CustomerPayBillOnline or CustomerBuyGoodsOnline")
    if amount < 1:
        errors.append("amount must be at least 1")
    if not party_a.startswith("2547") or len(party_a) != 12:
        errors.append("party_a must be in the format 2547XXXXXXXX")
    if not phone_number.startswith("2547") or len(phone_number) != 12:
        errors.append("phone_number must be in the format 2547XXXXXXXX")
    if len(account_reference) > 12:
        errors.append("account_reference must be 12 characters or fewer")
    if len(transaction_desc) > 13:
        errors.append("transaction_desc must be 13 characters or fewer")
    if not callback_url.startswith("https://"):
        errors.append("callback_url should use https")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "normalized_payload": {
            "BusinessShortCode": business_shortcode,
            "TransactionType": transaction_type,
            "Amount": str(amount),
            "PartyA": party_a,
            "PartyB": party_b,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
        },
    }


@mcp.tool()
def initiate_stk_push(
    business_shortcode: str,
    passkey: str,
    transaction_type: str,
    amount: int,
    party_a: str,
    party_b: str,
    phone_number: str,
    callback_url: str,
    account_reference: str,
    transaction_desc: str,
) -> Dict[str, Any]:
    """
    Builds the MPESA Express request body and returns the target endpoint.

    In production, this tool would:
    1. fetch an access token
    2. call the DARAJA STK Push endpoint
    3. return the live API response
    """
    logger.info(">>> Tool called: initiate_stk_push")

    timestamp = current_timestamp()
    password = build_password(business_shortcode, passkey, timestamp)

    request_body = {
        "BusinessShortCode": business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": transaction_type,
        "Amount": str(amount),
        "PartyA": party_a,
        "PartyB": party_b,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }

    return {
        "environment": "sandbox",
        "endpoint": f"{SANDBOX_BASE_URL}{STK_PUSH_PATH}",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer <access_token>",
        },
        "request_body": request_body,
        "notes": [
            "This API is asynchronous.",
            "A successful submission only means the request was accepted for processing.",
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
        "0": "Success. The request was processed successfully.",
        "1032": "The customer canceled the STK Push request.",
        "1037": "The customer could not be reached. Their phone may be offline, busy, or in another session.",
        "2001": "The customer entered an invalid M-PESA PIN.",
        "404.001.03": "Invalid access token. Generate a fresh token and retry before expiry.",
        "400.002.02": "Invalid request payload. Check required fields and formatting.",
        "500.003.02": "System busy or request rate too high. Retry with backoff and review throttling.",
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

## Understanding the Code

The server defines five MCP tools:

| Tool | Description |
|------|-------------|
| `generate_access_token_request()` | Returns the token endpoint and auth model needed to request a DARAJA access token |
| `validate_stk_push_payload(...)` | Checks required fields and normalizes the request payload |
| `initiate_stk_push(...)` | Builds the MPESA Express request body and shows how it should be sent |
| `parse_stk_callback(callback_payload)` | Converts callback payloads into a smaller, agent-friendly structure |
| `explain_stk_error(code)` | Explains common transaction and API errors with mitigation hints |

This structure is deliberate:

- **validation** is separate from **execution**
- **request submission** is separate from **callback interpretation**
- **error explanation** is separate from the raw API payload

That separation makes the MCP tools easier for both humans and agents to use correctly.

## Why This Is Better Than a Raw REST Wrapper

The point of MCP is not to mirror every HTTP endpoint 1:1. The point is to expose the **useful capabilities** of a system as composable tools.

For MPESA Express, the most useful capabilities are:

- understanding what a valid request looks like
- constructing a correct STK Push payload
- interpreting asynchronous results
- explaining failures quickly

That is what the tools above are designed to do.

## Where Apigee Fits

You are building the MCP server on Cloud Run in this lab, but the production pattern should assume **Apigee** in front of the service for:

- quota enforcement
- spike arrest
- authentication and policy mediation
- observability
- partner-facing API productization

For the workshop, think of the architecture like this:

```text
Gemini CLI / ADK Agent
        |
        v
Apigee
        |
        v
Cloud Run MCP Server
        |
        v
Safaricom DARAJA APIs
```

## Sample MPESA Express Request

Here is a clean example of the request body your MCP server is helping to build:

```json
{
  "BusinessShortCode": "174379",
  "Password": "<base64_shortcode_passkey_timestamp>",
  "Timestamp": "20210628092408",
  "TransactionType": "CustomerPayBillOnline",
  "Amount": "1",
  "PartyA": "254722000000",
  "PartyB": "174379",
  "PhoneNumber": "254722111111",
  "CallBackURL": "https://example.com/mpesa/callback",
  "AccountReference": "acct-ref",
  "TransactionDesc": "payment"
}
```

## Sample Submission Response

```json
{
  "MerchantRequestID": "2654-4b64-97ff-b827b542881d3130",
  "CheckoutRequestID": "ws_CO_1007202409152617172396192",
  "ResponseCode": "0",
  "ResponseDescription": "Success. Request accepted for processing",
  "CustomerMessage": "Success. Request accepted for processing"
}
```

## Sample Successful Callback

```json
{
  "Body": {
    "stkCallback": {
      "MerchantRequestID": "29115-34620561-1",
      "CheckoutRequestID": "ws_CO_191220191020363925",
      "ResultCode": 0,
      "ResultDesc": "The service request is processed successfully.",
      "CallbackMetadata": {
        "Item": [
          { "Name": "Amount", "Value": 1.0 },
          { "Name": "MpesaReceiptNumber", "Value": "NLJ7RT61SV" },
          { "Name": "TransactionDate", "Value": 20191219102115 },
          { "Name": "PhoneNumber", "Value": 254708374149 }
        ]
      }
    }
  }
}
```

## Common Errors Worth Explaining Well

| Code | Meaning | What to do |
|------|---------|------------|
| `400.002.02` | Invalid request payload | Recheck request body fields and formatting |
| `404.001.03` | Invalid access token | Generate a fresh token and retry |
| `1032` | Request canceled by user | Ask the customer to retry the payment |
| `1037` | Customer device unreachable | Retry later when the phone is reachable |
| `2001` | Invalid PIN | Ask the customer to enter the correct M-PESA PIN |
| `500.003.02` | System busy or rate-limited | Retry with backoff and review throttling rules |

## Why This Matters for the Rest of the Lab

In the next steps, you will deploy this MCP server to Cloud Run and connect to it from Gemini CLI. Later, in Lab 2, a Google ADK agent will use these tools to reason about payment workflows without needing to speak directly to raw DARAJA APIs every time.
