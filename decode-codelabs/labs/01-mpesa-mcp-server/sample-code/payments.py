"""Optional sandbox-only integration. No network occurs at import time."""
import base64
import os
from datetime import datetime, timezone
from urllib.parse import urlparse
import httpx
from domain import PaymentInput
from pydantic import StrictInt

SANDBOX_BASE_URL = "https://sandbox.safaricom.co.ke"

async def initiate_stk_push(phone_number: str, amount: StrictInt, account_reference: str = "DECODE") -> dict:
    """Submit once only when operator enabled sandbox mode. Acceptance is not payment."""
    if os.getenv("ENABLE_SANDBOX_INITIATION") != "true":
        return {"error": "initiation_disabled", "payment_verified": False}
    try:
        p = PaymentInput(phone_number=phone_number, amount=amount, account_reference=account_reference)
        key = os.environ["DARAJA_CONSUMER_KEY"]
        secret = os.environ["DARAJA_CONSUMER_SECRET"]
        shortcode = os.environ["DARAJA_BUSINESS_SHORTCODE"]
        passkey = os.environ["DARAJA_PASSKEY"]
        callback = os.environ["DARAJA_CALLBACK_URL"]
        parsed = urlparse(callback)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.hostname.endswith(".invalid"):
            raise ValueError("invalid callback configuration")
        if not shortcode.isdigit():
            raise ValueError("invalid shortcode")
    except (KeyError, ValueError):
        return {"error": "invalid_input_or_configuration", "payment_verified": False}
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
    body = {"BusinessShortCode": shortcode, "Password": password, "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline", "Amount": str(p.amount),
            "PartyA": p.phone_number, "PartyB": shortcode, "PhoneNumber": p.phone_number,
            "CallBackURL": callback, "AccountReference": p.account_reference, "TransactionDesc": "decode pay"}
    # Explicitly no retries. Credentials and request body are never returned or logged.
    async with httpx.AsyncClient(timeout=20, follow_redirects=False) as client:
        try:
            token_response = await client.get(SANDBOX_BASE_URL + "/oauth/v1/generate?grant_type=client_credentials", auth=(key, secret))
            token_response.raise_for_status()
            token = token_response.json()["access_token"]
        except (httpx.HTTPError, ValueError, KeyError):
            return {"error": "oauth_failed", "payment_verified": False}
        try:
            response = await client.post(SANDBOX_BASE_URL + "/mpesa/stkpush/v1/processrequest",
                                         headers={"Authorization": f"Bearer {token}"}, json=body)
            response.raise_for_status()
            result = response.json()
        except (httpx.HTTPError, ValueError):
            return {"status": "outcome_unknown", "payment_verified": False,
                    "next_step": "Reconcile externally before any resubmission; request may have reached Daraja."}
    return {"accepted_for_processing": result.get("ResponseCode") == "0",
            "checkout_request_id": result.get("CheckoutRequestID"),
            "merchant_request_id": result.get("MerchantRequestID"), "payment_verified": False}
