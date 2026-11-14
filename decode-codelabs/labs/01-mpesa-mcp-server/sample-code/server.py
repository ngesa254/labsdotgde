"""Cloud Run IAM protects deployed requests; local listener is for development."""
import os
from fastmcp import FastMCP
from domain import (list_products, get_product, calculate_order_total,
                    validate_stk_push_payload, parse_stk_callback, explain_stk_error)
from payments import initiate_stk_push

mcp = FastMCP("DECODE merchant tools", mask_error_details=True)
for tool in (list_products, get_product, calculate_order_total,
             validate_stk_push_payload, parse_stk_callback, explain_stk_error):
    mcp.tool()(tool)
# No model can enable the tool through a prompt or tool argument.
if os.getenv("ENABLE_SANDBOX_INITIATION") == "true":
    mcp.tool()(initiate_stk_push)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.getenv("PORT", "8080")),
            path="/mcp", stateless_http=True)
