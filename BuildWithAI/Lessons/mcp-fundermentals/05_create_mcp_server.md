# Creating an MCP Server

## Overview

In this lesson, you'll take the tools you implemented for the chatbot and wrap them in an MCP server using the **Standard I/O transport**. You'll use **FastMCP**, which provides a high-level interface to build an MCP server. Finally, you'll use the **MCP Inspector** to test your server.

---

## Two Approaches to Building MCP Servers

When creating an MCP server that exposes tools, the server needs to handle two main requests from the client:

1. **Listing all the tools** (`ListToolsRequest`)
2. **Executing a particular tool** (`CallToolRequest`)

There are two ways to create an MCP server:

| Approach | Description | When to Use |
|----------|-------------|-------------|
| **Low-level implementation** | Directly define and handle various request types | When you need to customize every aspect of your server |
| **High-level with FastMCP** | Focus on defining tools as functions; FastMCP handles protocol details | For faster, simpler server development (recommended) |

In this lesson, we'll use **FastMCP** for its simplicity and speed.

---

## From Chatbot Tools to MCP Server

In the previous lesson, you created two functions:
- `search_papers()` — Search for papers on arXiv
- `extract_info()` — Get details about a specific paper

You then defined these as tools with schemas and passed them to Claude.

**Now**, instead of defining tools directly in your chatbot, you'll:
1. Create an MCP server that exposes these tools
2. Let the server handle the tool definitions and schemas
3. Test the server before connecting any client

---

## Setup: Import FastMCP

Add the FastMCP import to your code:

```python
from mcp.server.fastmcp import FastMCP

# Keep your existing imports
import arxiv
import json
import os
from typing import Any
```

---

## Initialize the MCP Server

Create an instance of FastMCP:

```python
# Initialize FastMCP server
mcp = FastMCP("research")
```

**What's happening:**
- `FastMCP("research")` creates a server named "research"
- This server will expose tools, resources, and prompts
- We'll use the `@mcp.tool()` decorator to register functions as tools

---

## Convert Functions to MCP Tools

Take your existing functions and decorate them with `@mcp.tool()`:

```python
@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> list[str]:
    """
    Search for papers on arXiv and save results locally.
    
    Args:
        topic: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of paper IDs
    """
    # Initialize the arXiv client
    client = arxiv.Client()
    
    # Search for relevant articles
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    results = list(client.results(search))
    
    # Create directory if it doesn't exist
    os.makedirs(PAPER_DIRECTORY, exist_ok=True)
    
    # Save paper information to a JSON file
    papers_data = {}
    for paper in results:
        papers_data[paper.entry_id] = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "pdf_url": paper.pdf_url,
            "published": str(paper.published)
        }
    
    # Write to file
    with open(f"{PAPER_DIRECTORY}/papers_info.json", "w") as f:
        json.dump(papers_data, f, indent=2)
    
    # Return list of paper IDs
    return list(papers_data.keys())


@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Extract detailed information about a paper from saved data.
    
    Args:
        paper_id: The arXiv paper ID
        
    Returns:
        Formatted string with paper details
    """
    try:
        with open(f"{PAPER_DIRECTORY}/papers_info.json", "r") as f:
            papers = json.load(f)
        
        if paper_id in papers:
            paper = papers[paper_id]
            return json.dumps(paper, indent=2)
        else:
            return f"No saved information for paper: {paper_id}"
    
    except FileNotFoundError:
        return "No papers have been searched yet. Please search first."
```

**What's different:**
- ✅ Added `@mcp.tool()` decorator to both functions
- ✅ Kept the docstrings (FastMCP uses them to generate tool descriptions)
- ✅ No need to manually define tool schemas—FastMCP infers them from type hints!

---

## Add Server Entry Point

Add the code to run the server:

```python
if __name__ == "__main__":
    # Run the server with stdio transport
    mcp.run(transport="stdio")
```

**What's happening:**
- `if __name__ == "__main__":` ensures this only runs when the file is executed directly
- `mcp.run(transport="stdio")` starts the server using Standard I/O transport
- This is perfect for local development and testing

---

## Complete Server File

Save your complete server as `research_server.py`:

```python
from mcp.server.fastmcp import FastMCP
import arxiv
import json
import os

# Define where we'll save paper information
PAPER_DIRECTORY = "papers"

# Initialize FastMCP server
mcp = FastMCP("research")

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> list[str]:
    """
    Search for papers on arXiv and save results locally.
    
    Args:
        topic: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of paper IDs
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = list(client.results(search))
    
    os.makedirs(PAPER_DIRECTORY, exist_ok=True)
    
    papers_data = {}
    for paper in results:
        papers_data[paper.entry_id] = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "pdf_url": paper.pdf_url,
            "published": str(paper.published)
        }
    
    with open(f"{PAPER_DIRECTORY}/papers_info.json", "w") as f:
        json.dump(papers_data, f, indent=2)
    
    return list(papers_data.keys())


@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Extract detailed information about a paper from saved data.
    
    Args:
        paper_id: The arXiv paper ID
        
    Returns:
        Formatted string with paper details
    """
    try:
        with open(f"{PAPER_DIRECTORY}/papers_info.json", "r") as f:
            papers = json.load(f)
        
        if paper_id in papers:
            paper = papers[paper_id]
            return json.dumps(paper, indent=2)
        else:
            return f"No saved information for paper: {paper_id}"
    
    except FileNotFoundError:
        return "No papers have been searched yet. Please search first."


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Setup Your Environment

### Prerequisites

Before running your server, ensure you have:

| Tool | Purpose | Installation |
|------|---------|--------------|
| **uv** | Fast Python package manager | [Installation guide](https://github.com/astral-sh/uv) |
| **Node.js** | Required for MCP Inspector | [Installation guide](https://nodejs.org/) |

### Create Project Structure

```bash
# Create project directory
mkdir mcp_project
cd mcp_project

# Your research_server.py should be in this directory
```

### Initialize UV Project

```bash
# Initialize uv project
uv init
```

**Output:**
```
Initialized project `mcp_project`
```

### Create Virtual Environment

```bash
# Create virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

**You should see:**
```
(mcp_project) your-username@machine:~/mcp_project$
```

### Install Dependencies

```bash
# Install required packages
uv pip install mcp arxiv
```

**What's installed:**
- `mcp` — Model Context Protocol SDK
- `arxiv` — arXiv API wrapper

---

## Test Your Server with MCP Inspector

The **MCP Inspector** is a browser-based tool for testing MCP servers without building a client.

### Start the Inspector

```bash
# Clear terminal for visibility (optional)
clear

# Run the inspector
npx @modelcontextprotocol/inspector uv run research_server.py
```

**What's happening:**
- `npx` runs the inspector without installing it globally
- `@modelcontextprotocol/inspector` is the MCP Inspector package
- `uv run research_server.py` is the command to start your server

**Output:**
```
Starting MCP Inspector...
Inspector running at http://localhost:5173
```

### Open the Inspector

Navigate to `http://localhost:5173` in your browser.

---

## Using the MCP Inspector

### 1. Select Transport

The Inspector interface shows three transport options:

| Transport | Use Case |
|-----------|----------|
| **stdio** | Local servers (like ours) |
| **Server-Sent Events (SSE)** | Remote servers (stateful) |
| **Streamable HTTP** | Remote servers (stateful or stateless) |

✅ Keep **stdio** selected (default for local development)

### 2. Verify Command

The command field should show:
```
uv run research_server.py
```

This matches the command we used to start the Inspector.

> **Note:** If running in a cloud environment, you may need to paste in a proxy address. For local development, this isn't necessary.

### 3. Connect to Server

Click **"Connect"**

**What happens:**
1. Inspector launches your server as a subprocess
2. **Initialization handshake** occurs (remember this from lesson 03!)
3. Inspector and server establish communication

You should see:
```
✓ Connected to research server
```

### 4. View Initialization

Click on the **"Initialize"** tab to see the initialization request/response:

```json
Request:
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "mcp-inspector",
      "version": "1.0.0"
    }
  }
}

Response:
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "research",
      "version": "1.0.0"
    }
  }
}
```

This is the **initialization process** from the MCP architecture lesson!

### 5. List Available Tools

Click on the **"Tools"** tab.

You'll see a **"List Tools"** button. Click it to see available tools:

```
✓ Found 2 tools:
  - search_papers
  - extract_info
```

The Inspector sends a `ListToolsRequest` and your server responds with the tool definitions.

### 6. Test a Tool

Let's test the `search_papers` tool:

**Click on "search_papers"**

You'll see the tool schema:

```json
{
  "name": "search_papers",
  "description": "Search for papers on arXiv and save results locally.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "topic": {
        "type": "string",
        "description": "The search query"
      },
      "max_results": {
        "type": "integer",
        "description": "Maximum number of results to return",
        "default": 5
      }
    },
    "required": ["topic"]
  }
}
```

**Notice:**
- ✅ Description comes from the docstring
- ✅ Parameters inferred from type hints
- ✅ `max_results` has a default value

**Fill in the parameters:**
```
topic: "quantum computing"
max_results: 3
```

**Click "Run Tool"**

**Result:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "[\"http://arxiv.org/abs/2401.12345v1\", \"http://arxiv.org/abs/2401.12346v1\", \"http://arxiv.org/abs/2401.12347v1\"]"
    }
  ]
}
```

You just tested your MCP server without building a client! 🎉

### 7. Test the Second Tool

Click on **"extract_info"**

**Fill in a paper ID** (use one from the previous result):
```
paper_id: "http://arxiv.org/abs/2401.12345v1"
```

**Click "Run Tool"**

**Result:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"title\": \"Quantum Computing: A Gentle Introduction\",\n  \"authors\": [\"John Doe\", \"Jane Smith\"],\n  \"summary\": \"This paper provides...\",\n  \"pdf_url\": \"http://arxiv.org/pdf/2401.12345v1\",\n  \"published\": \"2024-01-15 10:30:00\"\n}"
    }
  ]
}
```

Perfect! Your tool returned detailed paper information.

---

## What Makes MCP Inspector Valuable?

| Benefit | Description |
|---------|-------------|
| **Sandbox Testing** | Test tools without building a client or host |
| **Schema Validation** | Verify your tool schemas are correctly inferred |
| **Quick Iteration** | Make changes to your server and test immediately |
| **Debugging** | See exactly what requests and responses look like |
| **Third-Party Servers** | Test servers built by others before integrating |

---

## Stop the Inspector

When you're done testing:

1. Return to your terminal
2. Press **Ctrl+C** to stop the server

```
^C
Shutting down MCP Inspector...
Server stopped.
```

**To restart:**
```bash
# Press Up Arrow to get the previous command
npx @modelcontextprotocol/inspector uv run research_server.py
```

---

## Key Concepts

### FastMCP Benefits

| Feature | Benefit |
|---------|---------|
| **Type Inference** | Automatically generates schemas from type hints |
| **Docstring Parsing** | Uses docstrings for tool descriptions |
| **Decorator Pattern** | Simple `@mcp.tool()` decorator to register tools |
| **Transport Handling** | Manages stdio, SSE, or HTTP transports automatically |

### The Testing Flow

```
1. Write server code (research_server.py)
   ↓
2. Start Inspector with server command
   ↓
3. Inspector launches server as subprocess
   ↓
4. Initialization handshake occurs
   ↓
5. Test tools in browser interface
   ↓
6. Verify tool execution and responses
   ↓
7. Iterate: Make changes → Restart → Test again
```

---

## Comparison: Before and After MCP

### Before MCP (Lesson 04)

```python
# Define tool schema manually
tools = [
    {
        "name": "search_papers",
        "description": "Search for academic papers...",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", ...},
                "max_results": {"type": "integer", ...}
            },
            "required": ["topic"]
        }
    }
]

# Execute tools manually in your chatbot
def execute_tool(tool_name, tool_input):
    if tool_name == "search_papers":
        return search_papers(**tool_input)
    # ... more tool mappings
```

**Problems:**
- ❌ Tool definitions tied to specific chatbot
- ❌ Manual schema writing (error-prone)
- ❌ Tools not reusable across applications

### After MCP (Lesson 05)

```python
# Just decorate your functions
@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> list[str]:
    """Search for papers on arXiv..."""
    # Implementation

@mcp.tool()
def extract_info(paper_id: str) -> str:
    """Extract detailed information..."""
    # Implementation

# Run the server
mcp.run(transport="stdio")
```

**Benefits:**
- ✅ Tools exposed through standard protocol
- ✅ Automatic schema generation
- ✅ Reusable across any MCP-compatible application
- ✅ Can test independently with Inspector

---

## Troubleshooting

### Issue: "Module 'mcp' not found"

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall dependencies
uv pip install mcp arxiv
```

### Issue: "Port already in use"

**Solution:**
```bash
# Kill any existing Inspector processes
# Then restart
npx @modelcontextprotocol/inspector uv run research_server.py
```

### Issue: Inspector shows "Connection Failed"

**Solution:**
- Verify your `research_server.py` has no syntax errors
- Check that `mcp.run(transport="stdio")` is in the `if __name__ == "__main__"` block
- Try running the server directly: `uv run research_server.py` (should hang, waiting for input)

---

## Summary

In this lesson, you learned:

- ✅ How to convert functions to MCP tools using `@mcp.tool()`
- ✅ How FastMCP infers tool schemas from type hints and docstrings
- ✅ How to run an MCP server with stdio transport
- ✅ How to use MCP Inspector to test your server
- ✅ The initialization handshake in action
- ✅ How to test tools without building a client

### What's Different from Lesson 04?

| Aspect | Lesson 04 (Direct Tools) | Lesson 05 (MCP Server) |
|--------|--------------------------|------------------------|
| **Tool Definition** | Manual JSON schemas | Automatic from decorators |
| **Reusability** | Tied to one chatbot | Reusable across applications |
| **Testing** | Need full chatbot | Test with Inspector |
| **Schema Maintenance** | Manual updates | Auto-generated from code |

---

## Next Steps

In the next lesson, you'll:
- Build an MCP **client** inside your chatbot
- Connect your chatbot to the research server
- Create an MCP **host** that manages multiple servers
- See the complete MCP architecture in action

**Continue to the next lesson →**