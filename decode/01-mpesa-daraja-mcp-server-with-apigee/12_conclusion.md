# Conclusion

🎉 **Congratulations!** You have successfully deployed and connected to a secure Safaricom M-PESA Express MCP server.

## What You Accomplished

In this lab, you:

- Created a Python MCP server using FastMCP with async httpx for non-blocking API calls
- Added token caching to reduce latency on repeated Daraja API calls
- Added static catalog tools for product discovery and order totals with quantity validation
- Added MPESA Express tools for payload validation, request construction, callback parsing, and error explanation
- Deployed the MCP server to Cloud Run as a secure, authenticated service
- Connected to the remote MCP server from Gemini CLI
- Verified tool calls in the server logs
- Tested the full end-to-end flow: product listing → purchase → dynamic phone number prompt → STK Push

## Key Improvements Applied

Your deployed MCP server includes production-ready improvements:

1. **Async httpx** — Non-blocking HTTP calls prevent event loop blocking during slow Safaricom API responses
2. **Token caching** — Daraja access tokens cached for ~3540s (with 60s safety margin) to eliminate redundant token requests
3. **Input validation** — Quantity validation and Pydantic `extra="forbid"` catch errors early
4. **Updated callback URL** — Points to your webhook.site instance for real-time callback monitoring

## Continue to the Next Lab

In Lab 2, you will build a Google ADK agent with Safaricom MCP access that uses the MCP server you created in this lab.

**Next:** [Build the Google ADK agent for MPESA + DARAJA MCP](../02-google-adk-agent-for-mpesa-daraja-mcp/readme.md)

---

**Need to clean up?** See [Step 11.5: Clean Up Lab Resources](./11.5_cleanup.md) if you want to reset and start over.
