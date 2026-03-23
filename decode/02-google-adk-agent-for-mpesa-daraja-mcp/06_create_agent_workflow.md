# Create Agent Workflow

## Create `__init__.py` File

Create the `__init__.py` file. This file tells Python that the `zoo_guide_agent` directory is a package.

```bash
cloudshell edit __init__.py
```

The above command opens up the code editor. Add the following code to `__init__.py`:

```python
from . import agent
```

---

## Create Main `agent.py` File

Create the main `agent.py` file. This command creates the Python file for your multi-agent system.

```bash
cloudshell edit agent.py
```

We'll build the agent step by step.

---

## Step 1: Imports and Initial Setup

This first block brings in all the necessary libraries from the ADK and Google Cloud. It also sets up logging and loads the environment variables from your `.env` file, which is crucial for accessing your model and server URL.

Add the following code to your `agent.py` file:

```python
import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")
```

---

## Step 2: Defining the Tools (The Agent's Capabilities)

An agent is only as good as the tools it can use. In this section, we define all the capabilities our agent will have, including a custom function to save data, an MCP Tool that connects to our secure MCP server, and a Wikipedia Tool.

Add the following code to the bottom of `agent.py`:

```python
# Greet user and save their prompt

def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict[str, str]:
    """Saves the user's initial prompt to the state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] Added to PROMPT: {prompt}")
    return {"status": "success"}


# Configuring the MCP Tool to connect to the Zoo MCP server

mcp_server_url = os.getenv("MCP_SERVER_URL")
if not mcp_server_url:
    raise ValueError("The environment variable MCP_SERVER_URL is not set.")

def get_id_token():
    """Get an ID token to authenticate with the MCP server."""
    target_url = os.getenv("MCP_SERVER_URL")
    audience = target_url.split('/mcp/')[0]
    request = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(request, audience)
    return id_token

"""
# Use this code if you are using the public MCP Server and comment out the code below defining mcp_tools
mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=mcp_server_url
    )
)
"""

mcp_tools = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=mcp_server_url,
                headers={
                    "Authorization": f"Bearer {get_id_token()}",
                },
            ),
        )

# Configuring the Wikipedia Tool
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)
```

### The Three Tools Explained

| Tool | Purpose | How It Works |
|------|---------|--------------|
| 📝 `add_prompt_to_state` | Remembers what a zoo visitor asks | A Python function that writes the visitor's prompt into the shared `tool_context.state` dictionary. This tool context represents the agent's short-term memory for a single conversation. Data saved to the state by one agent can be read by the next agent in the workflow. |
| 🦁 `MCPToolset` | Connects to the zoo MCP server from Lab 1 | Securely connects to the zoo's private server URL. Uses `get_id_token` to automatically get a secure "keycard" (a service account ID token) to prove its identity and gain access. |
| 🌍 `LangchainTool` | Gives the agent general world knowledge | Acts as an adapter, allowing our agent to use the pre-built `WikipediaQueryRun` tool from the LangChain library. |

**Resources:**
- [MCP Toolset](https://google.github.io/adk-docs/tools/mcp-tools/)
- [Function Tools](https://google.github.io/adk-docs/tools/function-tools/)
- [State](https://google.github.io/adk-docs/sessions/state/)

---

## Step 3: Defining the Specialist Agents

Next we will define the **Researcher Agent** and **Response Formatter Agent**.

- **Researcher Agent**: The "brain" of our operation. This agent takes the user's prompt from the shared State, examines its powerful tools (the Zoo's MCP Server Tool and the Wikipedia Tool), and decides which ones to use to find the answer.

- **Response Formatter Agent**: Handles presentation. It doesn't use any tools to find new information. Instead, it takes the raw data gathered by the Researcher agent (passed via the State) and uses the LLM's language skills to transform it into a friendly, conversational response.

Add the following code to the bottom of `agent.py`:

```python
# 1. Researcher Agent
comprehensive_researcher = Agent(
    name="comprehensive_researcher",
    model=model_name,
    description="The primary researcher that can access both internal zoo data and external knowledge from Wikipedia.",
    instruction="""
    You are a helpful research assistant. Your goal is to fully answer the user's PROMPT.
    You have access to two tools:
    1. A tool for getting specific data about animals AT OUR ZOO (names, ages, locations).
    2. A tool for searching Wikipedia for general knowledge (facts, lifespan, diet, habitat).

    First, analyze the user's PROMPT.
    - If the prompt can be answered by only one tool, use that tool.
    - If the prompt is complex and requires information from both the zoo's database AND Wikipedia,
      you MUST use both tools to gather all necessary information.
    - Synthesize the results from the tool(s) you use into preliminary data outputs.

    PROMPT:
    {{ PROMPT }}
    """,
    tools=[
        mcp_tools,
        wikipedia_tool
    ],
    output_key="research_data" # A key to store the combined findings
)

# 2. Response Formatter Agent
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Synthesizes all information into a friendly, readable response.",
    instruction="""
    You are the friendly voice of the Zoo Tour Guide. Your task is to take the
    RESEARCH_DATA and present it to the user in a complete and helpful answer.

    - First, present the specific information from the zoo (like names, ages, and where to find them).
    - Then, add the interesting general facts from the research.
    - If some information is missing, just present the information you have.
    - Be conversational and engaging.

    RESEARCH_DATA:
    {{ research_data }}
    """
)
```

---

## Step 4: The Workflow Agent

The **Workflow Agent** acts as the 'back-office' manager for the zoo tour. It takes the research request and ensures the two agents we defined above perform their jobs in the correct order: first research, then formatting. This creates a predictable and reliable process for answering a visitor's question.

**How:** It's a `SequentialAgent`, a special type of agent that doesn't think for itself. Its only job is to run a list of `sub_agents` (the researcher and formatter) in a fixed sequence, automatically passing the shared memory from one to the next.

Add this block of code to the bottom of `agent.py`:

```python
tour_guide_workflow = SequentialAgent(
    name="tour_guide_workflow",
    description="The main workflow for handling a user's request about an animal.",
    sub_agents=[
        comprehensive_researcher, # Step 1: Gather all data
        response_formatter,       # Step 2: Format the final response
    ]
)
```

---

## Final Step: Assemble the Main Workflow

This Agent is designated as the `root_agent`, which the ADK framework uses as the starting point for all new conversations. Its primary role is to orchestrate the overall process. It acts as the initial controller, managing the first turn of the conversation.

Add this final block of code to the bottom of `agent.py`:

```python
root_agent = Agent(
    name="greeter",
    model=model_name,
    description="The main entry point for the Zoo Tour Guide.",
    instruction="""
    - Let the user know you will help them learn about the animals we have in the zoo.
    - When the user responds, use the 'add_prompt_to_state' tool to save their response.
    After using the tool, transfer control to the 'tour_guide_workflow' agent.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[tour_guide_workflow]
)
```

---

## Agent Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        root_agent (greeter)                     │
│                    "Welcome to the Zoo!"                        │
│                   Tools: add_prompt_to_state                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   tour_guide_workflow                           │
│                    (SequentialAgent)                            │
│                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │ comprehensive_      │ ──▶│ response_formatter  │            │
│  │ researcher          │    │                     │            │
│  │                     │    │ "Present findings   │            │
│  │ Tools:              │    │  in friendly way"   │            │
│  │ • MCP (Zoo data)    │    │                     │            │
│  │ • Wikipedia         │    │ No tools            │            │
│  └─────────────────────┘    └─────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

Your `agent.py` file is now complete! By building it this way, you can see how each component—tools, worker agents, and manager agents—has a specific role in creating the final, intelligent system.

**Next up: Deployment!**