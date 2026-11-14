"""Pure catalog and preparation functions: no network or credential access."""
from copy import deepcopy
from pydantic import BaseModel, ConfigDict, Field, StrictInt, ValidationError

PRODUCTS = [
    {"id": "conf-pass-001", "name": "Build With AI Conference Pass", "category": "event", "price_kes": 5, "currency": "KES", "inventory_status": "in_stock"},
    {"id": "tee-001", "name": "DECODE Workshop T-Shirt", "category": "merch", "price_kes": 3, "currency": "KES", "inventory_status": "in_stock"},
    {"id": "coffee-001", "name": "Single Origin Coffee Beans", "category": "retail", "price_kes": 1, "currency": "KES", "inventory_status": "low_stock"},
]
class BasketItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    product_id: str = Field(min_length=1)
    quantity: StrictInt = Field(ge=1, le=100)

class PaymentInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    phone_number: str = Field(pattern=r"^254[17][0-9]{8}$")
    amount: StrictInt = Field(ge=1, le=1000)
    account_reference: str = Field(default="DECODE", pattern=r"^[A-Za-z0-9-]{1,12}$")

def list_products() -> dict:
    """List the fictional workshop catalog; prices are teaching fixtures in KES."""
    return {"products": deepcopy(PRODUCTS)}

def get_product(product_id: str) -> dict:
    """Fetch one catalog product, or an explicit error."""
    return next((dict(p) for p in PRODUCTS if p["id"] == product_id), {"error": "unknown_product"})

def calculate_order_total(items: list[dict]) -> dict:
    """Compute KES totals from server prices. No order is created or stock reserved."""
    if not 1 <= len(items) <= 20:
        return {"error": "basket_requires_1_to_20_lines"}
    lines = []
    for raw in items:
        try:
            item = BasketItem.model_validate(raw)
        except ValidationError:
            return {"error": "invalid_basket_item"}
        product = get_product(item.product_id)
        if "error" in product:
            return product
        lines.append({"product_id": item.product_id, "quantity": item.quantity,
                      "unit_price_kes": product["price_kes"],
                      "line_total_kes": item.quantity * product["price_kes"]})
    return {"currency": "KES", "line_items": lines,
            "order_total_kes": sum(line["line_total_kes"] for line in lines)}

def validate_stk_push_payload(phone_number: str, amount: StrictInt, account_reference: str = "DECODE") -> dict:
    """Validate and prepare an illustrative request. Never initiates payment."""
    try:
        p = PaymentInput(phone_number=phone_number, amount=amount, account_reference=account_reference)
    except ValidationError:
        return {"valid": False, "error": "invalid_payment_input"}
    return {"valid": True, "status": "prepared_only", "payment_verified": False,
            "example_payload": {"BusinessShortCode": "BUSINESS_SHORTCODE",
              "Password": "SERVER_GENERATED_AT_SEND_TIME", "Timestamp": "SERVER_GENERATED_AT_SEND_TIME",
              "TransactionType": "CustomerPayBillOnline", "Amount": str(p.amount),
              "PartyA": p.phone_number, "PartyB": "BUSINESS_SHORTCODE", "PhoneNumber": p.phone_number,
              "CallBackURL": "https://callback.example.invalid/stk", "AccountReference": p.account_reference,
              "TransactionDesc": "decode pay"}}

def parse_stk_callback(callback_payload: dict) -> dict:
    """Interpret supplied JSON only. This is not a webhook receiver or trusted evidence."""
    try:
        callback = callback_payload["Body"]["stkCallback"]
        code = callback["ResultCode"]
        if type(code) is not int or not callback.get("CheckoutRequestID"):
            raise ValueError("invalid callback")
        return {"reported_result_code": code, "reported_success": code == 0,
                "checkout_request_id": callback["CheckoutRequestID"],
                "payment_verified": False, "evidence": "untrusted_supplied_json"}
    except (KeyError, TypeError, ValueError, AttributeError):
        return {"error": "invalid_callback", "payment_verified": False}

def explain_stk_error(code: str) -> dict:
    """Explain a source example; confirm current meanings in your Daraja portal."""
    return {"code": code, "meaning": {"0": "Reported success; provenance and correlation still required.",
        "1032": "Customer cancelled.", "1037": "Customer unreachable or timed out."}.get(code,
        "Consult current Daraja documentation; do not infer an outcome or retry automatically.")}
