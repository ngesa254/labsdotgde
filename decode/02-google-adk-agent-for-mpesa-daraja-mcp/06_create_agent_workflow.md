# Create Agent Workflow

## Create `__init__.py`

Create the `__init__.py` file:

```bash
cloudshell edit __init__.py
```

Add:

```python
from . import agent
```

## Create `agent.py`

```bash
cloudshell edit agent.py
```

Add the following code:

```python
import logging
import os

import google.cloud.logging
import google.auth.transport.requests
import google.oauth2.id_token
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.tools.tool_context import ToolContext

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")
mcp_server_url = os.getenv("MCP_SERVER_URL")

if not mcp_server_url:
    raise ValueError("The environment variable MCP_SERVER_URL is not set.")


def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    tool_context.state["PROMPT"] = prompt
    logging.info("[State updated] Added to PROMPT: %s", prompt)
    return {"status": "success"}


def get_id_token():
    audience = mcp_server_url.split("/mcp")[0]
    request = google.auth.transport.requests.Request()
    return google.oauth2.id_token.fetch_id_token(request, audience)


mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=mcp_server_url,
        headers={
            "Authorization": f"Bearer {get_id_token()}",
        },
    )
)


checkout_planner = Agent(
    name="checkout_planner",
    model=model_name,
    description="Determines how to fulfill product and payment requests using MCP tools.",
    instruction="""
    You are an operations assistant with Safaricom MCP access.

    Use the MCP tools to help with:
    - listing products
    - getting product details
    - calculating order totals
    - validating MPESA Express payloads
    - preparing STK Push requests
    - parsing callback payloads
    - explaining known error codes

    Always prefer MCP tools over guessing.

    PROMPT:
    {{ PROMPT }}
    """,
    tools=[mcp_tools],
    output_key="checkout_data",
)


response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Formats product, order, and payment results for a merchant operator.",
    instruction="""
    You are a helpful merchant operations assistant.

    Take the CHECKOUT_DATA and produce a concise, operationally useful response.
    If there is product information, present it clearly.
    If there is payment information, present the amount, request IDs, and next steps.
    If there is an error, explain it in plain language and suggest what to do next.

    CHECKOUT_DATA:
    {{ checkout_data }}
    """,
)


checkout_workflow = SequentialAgent(
    name="checkout_workflow",
    description="Runs checkout planning and response formatting in sequence.",
    sub_agents=[checkout_planner, response_formatter],
)


root_agent = Agent(
    name="safaricom_mcp_access_greeter",
    model=model_name,
    description="Main entry point for the Google ADK agent with Safaricom MCP access.",
    instruction="""
    Greet the user as a Google ADK agent with Safaricom MCP access.
    Tell them you can help with products, totals, MPESA Express requests, callbacks, and payment errors.
    When they respond, save their prompt with add_prompt_to_state and then hand off to checkout_workflow.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[checkout_workflow],
)
```

## Architecture Overview

This agent has one job: orchestrate the Safaricom M-PESA Express MCP server and its product tools.

- `safaricom_mcp_access_greeter` handles the first interaction
- `checkout_planner` decides which MCP tools to call
- `response_formatter` turns raw tool output into merchant-friendly responses

This is intentionally cleaner than the inherited zoo example because it keeps the entire workflow inside one business domain.
