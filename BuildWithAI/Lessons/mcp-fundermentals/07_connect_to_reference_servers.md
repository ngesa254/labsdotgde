# Connecting to Reference Servers

## Overview

In the previous lesson, you connected your chatbot to one server that you built. Now you'll update your chatbot so that it can connect to **any server**. You'll learn about the reference servers developed by the Anthropic team and how to download and use them.

---

## The MCP Ecosystem

So far, you've built MCP servers and clients that connect on a **1:1 basis**. Now it's time to:

- Connect to **multiple servers** simultaneously
- Use **reference servers** built by Anthropic
- Explore the **ecosystem** of available MCP servers

---

## Discovering Reference Servers

### The MCP Servers Repository

Anthropic maintains a GitHub repository of reference servers:

🔗 **https://github.com/modelcontextprotocol/servers**

**What you'll find:**
- **Reference servers** — Built and maintained by Anthropic
- **Third-party servers** — Community contributions
- **Official integrations** — Partnerships with companies

> Any data source you can imagine probably has an MCP server!

### Categories of Servers

| Category | Examples |
|----------|----------|
| **Web & APIs** | Fetch, Brave Search, Google Maps |
| **File Systems** | File system, Git, Memory |
| **Databases** | PostgreSQL, SQLite, MongoDB |
| **Development** | GitHub, GitLab, Sentry |
| **Communication** | Slack, Email |
| **Productivity** | Google Drive, Notion, Linear |

---

## Reference Servers We'll Use

### 1. Fetch Server

**Purpose:** Retrieve content from web pages and convert HTML to Markdown

**GitHub:** https://github.com/modelcontextprotocol/servers/tree/main/src/fetch

**What it exposes:**
- **Tools:**
  - `fetch` — Retrieve webpage content
  - `fetch_multiple` — Retrieve multiple pages
- **Prompt:**
  - `fetch_url` — Template for fetching and processing URLs

**Installation:**
```bash
# No installation needed! Use uvx to run directly
uvx mcp-server-fetch
```

**Language:** Python

**Use cases:**
- Fetching documentation
- Web scraping for research
- Converting HTML to LLM-friendly format

---

### 2. File System Server

**Purpose:** Access your local file system—read, write, search files

**GitHub:** https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

**What it exposes:**
- **Resources:**
  - `file://` URIs for files
- **Tools:**
  - `read_file` — Read file contents
  - `write_file` — Write to files
  - `list_directory` — List directory contents
  - `create_directory` — Create directories
  - `move_file` — Move/rename files
  - `search_files` — Search for files
  - `get_file_info` — Get file metadata

**Installation:**
```bash
# No installation needed! Use npx to run directly
npx -y @modelcontextprotocol/server-filesystem <allowed-directory>
```

**Language:** TypeScript

**Use cases:**
- File management automation
- Documentation generation
- Log file analysis

---

### 3. Your Research Server

**Purpose:** Search and extract information from arXiv papers

**What it exposes:**
- **Tools:**
  - `search_papers` — Search arXiv
  - `extract_info` — Get paper details

**Installation:**
```bash
uv run research_server.py
```

**Language:** Python

---

## Understanding Server Commands

Different servers use different package managers:

### Python Servers (uvx)

```bash
# Run Python server without installing
uvx mcp-server-fetch
```

**What's happening:**
- `uvx` — UV's command for running packages without installation
- Downloads dependencies on-the-fly
- Executes the server

### TypeScript/JavaScript Servers (npx)

```bash
# Run Node.js server without installing
npx -y @modelcontextprotocol/server-filesystem /path/to/directory
```

**What's happening:**
- `npx` — npm's package runner
- `-y` — Auto-accept installation prompts
- Downloads and executes the server

### Local Servers (uv run)

```bash
# Run local Python server
uv run research_server.py
```

**What's happening:**
- Runs a local Python file
- Uses your virtual environment
- Server must exist locally

---

## Server Configuration File

Instead of hardcoding server parameters, create a **server configuration file** that your chatbot can read.

### Create `server_config.json`

```json
{
  "mcpServers": {
    "research": {
      "command": "uv",
      "args": ["run", "research_server.py"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
      ]
    }
  }
}
```

**What each field means:**

| Field | Description | Example |
|-------|-------------|---------|
| **Key** | Server name | `"research"`, `"fetch"` |
| **command** | Executable to run | `"uv"`, `"uvx"`, `"npx"` |
| **args** | Arguments for command | `["run", "research_server.py"]` |

**Note on File System paths:**
- `.` means current directory
- The server can only access this directory and subdirectories
- Security feature to prevent unauthorized file access

---

## Updated MCP Chatbot Architecture

### Before (Lesson 06)

```
┌─────────────────────────┐
│    MCP Chatbot Host     │
│                         │
│   ┌─────────────────┐   │
│   │   MCP Client    │   │
│   └────────┬────────┘   │
└────────────┼────────────┘
             │
             ▼
      ┌──────────────┐
      │ Research     │
      │ Server       │
      └──────────────┘
```

### After (Lesson 07)

```
┌─────────────────────────────────────────────────┐
│          MCP Chatbot Host                       │
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ Client  │  │ Client  │  │ Client  │         │
│  │    1    │  │    2    │  │    3    │         │
│  └────┬────┘  └────┬────┘  └────┬────┘         │
└───────┼────────────┼─────────────┼──────────────┘
        │            │             │
        ▼            ▼             ▼
   ┌─────────┐  ┌────────┐  ┌──────────┐
   │Research │  │ Fetch  │  │Filesystem│
   │ Server  │  │ Server │  │  Server  │
   └─────────┘  └────────┘  └──────────┘
```

---

## Building the Multi-Server Chatbot

### Key Challenges

| Challenge | Solution |
|-----------|----------|
| Managing multiple sessions | List of active sessions |
| Mapping tools to servers | Dictionary: tool name → session |
| Multiple async connections | `AsyncExitStack` context manager |
| Reading config file | Parse JSON and iterate over servers |

### Updated Chatbot Structure

```python
class MCPChatbot:
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic(...)
        
        # NEW: Track multiple sessions and tools
        self.sessions = []           # List of active server sessions
        self.tools = []              # All tools from all servers
        self.tool_to_session = {}    # Map tool name → session
        self.exit_stack = None       # Manage multiple connections
```

---

## Step 1: Connect to a Single Server

Update the connection logic to be reusable:

```python
async def connect_to_server(self, server_name: str, server_config: dict):
    """Connect to a single MCP server and list its tools."""
    
    # Create server parameters
    server_params = StdioServerParameters(
        command=server_config["command"],
        args=server_config.get("args", []),
        env=server_config.get("env")
    )
    
    # Connect to server
    read, write = await self.exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    
    # Create session
    session = await self.exit_stack.enter_async_context(
        ClientSession(read, write)
    )
    
    # Initialize
    await session.initialize()
    
    # List tools
    tools_response = await session.list_tools()
    
    # Add session to list
    self.sessions.append(session)
    
    # Process tools
    for tool in tools_response.tools:
        tool_dict = {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        }
        self.tools.append(tool_dict)
        
        # Map tool to session
        self.tool_to_session[tool.name] = session
    
    print(f"✓ Connected to {server_name} ({len(tools_response.tools)} tools)")
```

**Key points:**
- `exit_stack` manages multiple async context managers
- Each tool is mapped to its corresponding session
- All tools are collected in a single list for Claude

---

## Step 2: Connect to Multiple Servers

Read the config file and connect to all servers:

```python
async def connect_to_all_servers(self):
    """Connect to all servers defined in server_config.json."""
    
    # Read configuration
    with open("server_config.json", "r") as f:
        config = json.load(f)
    
    # Create exit stack for managing connections
    self.exit_stack = AsyncExitStack()
    await self.exit_stack.__aenter__()
    
    # Connect to each server
    for server_name, server_config in config["mcpServers"].items():
        await self.connect_to_server(server_name, server_config)
    
    print(f"\n✓ Connected to {len(self.sessions)} servers")
    print(f"✓ Total tools available: {len(self.tools)}")
```

**Important note:** This code is **blocking** (sequential). For better performance, you could use `asyncio.gather()` to connect to servers in parallel.

---

## Step 3: Execute Tools from the Correct Server

When Claude calls a tool, execute it on the correct server:

```python
async def execute_tool(self, tool_name: str, tool_args: dict):
    """Execute a tool on the appropriate server."""
    
    # Find which session this tool belongs to
    session = self.tool_to_session.get(tool_name)
    
    if not session:
        return f"Error: Tool '{tool_name}' not found"
    
    # Call the tool through MCP
    result = await session.call_tool(tool_name, tool_args)
    
    # Extract result content
    if result.content:
        return result.content[0].text
    return ""
```

---

## Step 4: Updated Process Query

Update query processing to use the tool-to-session mapping:

```python
async def process_query(self, query):
    """Process a single query with Claude and MCP tools."""
    messages = [{'role': 'user', 'content': query}]
    
    processing = True
    
    while processing:
        response = self.anthropic_client.messages.create(
            max_tokens=4096,
            model='claude-3-7-sonnet-20250219',
            tools=self.tools,  # All tools from all servers
            messages=messages
        )
        
        assistant_content = []
        
        for content in response.content:
            if content.type == 'text':
                print(content.text)
                assistant_content.append(content)
                
            elif content.type == 'tool_use':
                assistant_content.append(content)
                
                messages.append({
                    'role': 'assistant',
                    'content': assistant_content
                })
                
                # Execute tool on correct server
                tool_name = content.name
                tool_args = content.input
                tool_id = content.id
                
                print(f"\n[Calling '{tool_name}' via MCP...]")
                
                # NEW: Use execute_tool which finds the right session
                result = await self.execute_tool(tool_name, tool_args)
                
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": result
                    }]
                })
                
                break
        
        if len(response.content) == 1 and response.content[0].type == "text":
            processing = False
```

---

## Step 5: Clean Up Connections

Properly close all connections when done:

```python
async def cleanup(self):
    """Clean up all server connections."""
    if self.exit_stack:
        await self.exit_stack.__aexit__(None, None, None)
```

---

## Complete Multi-Server Chatbot

Save as `mcp_chatbot.py`:

```python
#!/usr/bin/env python3
"""MCP-enabled chatbot that connects to multiple servers."""

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from contextlib import AsyncExitStack

import asyncio
import nest_asyncio
import anthropic
from dotenv import load_dotenv
import os
import json

nest_asyncio.apply()
load_dotenv()


class MCPChatbot:
    def __init__(self):
        """Initialize the MCP chatbot."""
        self.anthropic_client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.sessions = []
        self.tools = []
        self.tool_to_session = {}
        self.exit_stack = None

    async def connect_to_server(self, server_name: str, server_config: dict):
        """Connect to a single MCP server."""
        server_params = StdioServerParameters(
            command=server_config["command"],
            args=server_config.get("args", []),
            env=server_config.get("env")
        )
        
        read, write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        
        session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        
        await session.initialize()
        tools_response = await session.list_tools()
        
        self.sessions.append(session)
        
        for tool in tools_response.tools:
            tool_dict = {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            self.tools.append(tool_dict)
            self.tool_to_session[tool.name] = session
        
        print(f"✓ Connected to {server_name} ({len(tools_response.tools)} tools)")

    async def connect_to_all_servers(self):
        """Connect to all servers in server_config.json."""
        with open("server_config.json", "r") as f:
            config = json.load(f)
        
        self.exit_stack = AsyncExitStack()
        await self.exit_stack.__aenter__()
        
        for server_name, server_config in config["mcpServers"].items():
            await self.connect_to_server(server_name, server_config)
        
        print(f"\n✓ Connected to {len(self.sessions)} servers")
        print(f"✓ Total tools: {len(self.tools)}\n")

    async def execute_tool(self, tool_name: str, tool_args: dict):
        """Execute a tool on the appropriate server."""
        session = self.tool_to_session.get(tool_name)
        
        if not session:
            return f"Error: Tool '{tool_name}' not found"
        
        result = await session.call_tool(tool_name, tool_args)
        
        if result.content:
            return result.content[0].text
        return ""

    async def process_query(self, query):
        """Process a query with Claude and MCP tools."""
        messages = [{'role': 'user', 'content': query}]
        
        processing = True
        
        while processing:
            response = self.anthropic_client.messages.create(
                max_tokens=4096,
                model='claude-3-7-sonnet-20250219',
                tools=self.tools,
                messages=messages
            )
            
            assistant_content = []
            
            for content in response.content:
                if content.type == 'text':
                    print(content.text)
                    assistant_content.append(content)
                    
                elif content.type == 'tool_use':
                    assistant_content.append(content)
                    
                    messages.append({
                        'role': 'assistant',
                        'content': assistant_content
                    })
                    
                    tool_name = content.name
                    tool_args = content.input
                    tool_id = content.id
                    
                    print(f"\n[Calling '{tool_name}' via MCP...]")
                    
                    result = await self.execute_tool(tool_name, tool_args)
                    
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result
                        }]
                    })
                    
                    break
            
            if len(response.content) == 1 and response.content[0].type == "text":
                processing = False

    async def chat_loop(self):
        """Run the interactive chat loop."""
        print("Type your queries or 'quit' to exit.\n")
        
        while True:
            try:
                query = input("Query: ").strip()
                
                if query.lower() == 'quit':
                    print("Goodbye!")
                    break
                
                await self.process_query(query)
                print()
                
            except Exception as e:
                print(f"\nError: {str(e)}\n")

    async def cleanup(self):
        """Clean up all connections."""
        if self.exit_stack:
            await self.exit_stack.__aexit__(None, None, None)


async def main():
    """Main entry point."""
    chatbot = MCPChatbot()
    
    try:
        await chatbot.connect_to_all_servers()
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Running the Multi-Server Chatbot

### Setup

```bash
# Navigate to project directory
cd mcp_project

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Ensure server_config.json exists
ls server_config.json

# Run the chatbot
uv run mcp_chatbot.py
```

### Expected Output

```
✓ Connected to research (2 tools)
✓ Connected to fetch (2 tools)
✓ Connected to filesystem (7 tools)

✓ Connected to 3 servers
✓ Total tools: 11

Type your queries or 'quit' to exit.

Query: _
```

---

## Example Usage: Complex Workflows

### Example 1: Fetch, Summarize, Save

**Query:**
```
Fetch the content of https://modelcontextprotocol.io/docs/concepts/architecture 
and save the content to a file called "mcp_summary.md", then create a visual 
diagram that summarizes the content.
```

**What happens:**

1. **fetch tool** (Fetch Server)
   - Retrieves webpage content
   - Converts HTML to Markdown

2. **write_file tool** (File System Server)
   - Saves content to `mcp_summary.md`

3. **Claude processes** the content
   - Creates a text-based diagram
   - Returns result to user

**Result:**
```
✓ Content fetched and saved to mcp_summary.md
✓ Created visual diagram summarizing MCP architecture
```

---

### Example 2: Research Pipeline

**Query:**
```
Fetch deeplearning.ai and find an interesting term. Search for 2 papers 
around that term and summarize your findings. Write them to a file called 
results.txt.
```

**What happens:**

1. **fetch tool** (Fetch Server)
   - Fetches deeplearning.ai homepage
   - Extracts content

2. **Claude identifies** interesting term
   - Example: "multi-concept pre-training"

3. **search_papers tool** (Research Server)
   - Searches arXiv for papers
   - Returns paper IDs

4. **extract_info tool** (Research Server)
   - Gets details for each paper

5. **Claude summarizes** findings

6. **write_file tool** (File System Server)
   - Saves summary to `results.txt`

**Result:**
```
✓ Found papers on "multi-concept pre-training"
✓ Summarized findings
✓ Written to results.txt
```

---

### Example 3: File Management

**Query:**
```
List all markdown files in the current directory, read the first one, 
and create a summary.
```

**What happens:**

1. **list_directory tool** (File System Server)
   - Lists files in current directory
   - Filters for `.md` files

2. **read_file tool** (File System Server)
   - Reads first markdown file

3. **Claude summarizes** content

---

## Understanding AsyncExitStack

### Why We Need It

Managing multiple async context managers is tricky:

**Problem:**
```python
# This doesn't work well
async with stdio_client(params1) as (r1, w1):
    async with stdio_client(params2) as (r2, w2):
        async with stdio_client(params3) as (r3, w3):
            # Too nested!
```

**Solution:**
```python
# AsyncExitStack manages all of them
exit_stack = AsyncExitStack()
await exit_stack.__aenter__()

read1, write1 = await exit_stack.enter_async_context(stdio_client(params1))
read2, write2 = await exit_stack.enter_async_context(stdio_client(params2))
read3, write3 = await exit_stack.enter_async_context(stdio_client(params3))

# Cleanup all at once
await exit_stack.__aexit__(None, None, None)
```

---

## Key Concepts

### Server Discovery

| Method | Description |
|--------|-------------|
| **GitHub Repository** | Browse available servers |
| **Server Registry** | Search by category or feature |
| **Documentation** | Read installation and usage guides |

### Configuration Best Practices

| Practice | Benefit |
|----------|---------|
| **JSON config file** | Easy to add/remove servers |
| **Environment variables** | Keep secrets secure |
| **Allowed directories** | Security for file system access |
| **Server naming** | Clear identification in logs |

### Tool Name Conflicts

**Problem:** What if two servers have tools with the same name?

**Solution:** In production, you'd want to:
- Namespace tools: `fetch.fetch_url` vs `research.fetch_paper`
- Track server name with each tool
- Allow users to specify which server to use

**Current approach:** Last server wins (tool gets overwritten)

---

## Comparison: Single vs. Multiple Servers

### Single Server (Lesson 06)

```python
# One session
session = await ClientSession(read, write)

# One server's tools
tools = [tool for tool in session.list_tools()]

# Execute tool
result = await session.call_tool(name, args)
```

**Limitations:**
- Only one server's capabilities
- Limited functionality
- Not scalable

### Multiple Servers (Lesson 07)

```python
# Multiple sessions
sessions = [session1, session2, session3]

# All tools from all servers
tools = []
for session in sessions:
    tools.extend(session.list_tools())

# Execute tool on correct server
session = tool_to_session[tool_name]
result = await session.call_tool(name, args)
```

**Benefits:**
- ✅ Combine capabilities from multiple servers
- ✅ Richer functionality
- ✅ Scalable architecture
- ✅ Use ecosystem servers

---

## Important Notes

### Production Considerations

This code is **not production-ready**. For real applications, consider:

| Improvement | Description |
|-------------|-------------|
| **Error handling** | Gracefully handle server failures |
| **Connection pooling** | Reuse connections efficiently |
| **Parallel connections** | Use `asyncio.gather()` to connect faster |
| **Tool namespacing** | Avoid name conflicts |
| **Health checks** | Verify servers are responsive |
| **Retry logic** | Handle transient failures |

### Performance Optimization

```python
# Sequential (current approach)
for server in servers:
    await connect_to_server(server)  # Slow

# Parallel (better approach)
await asyncio.gather(*[
    connect_to_server(server)
    for server in servers
])  # Fast!
```

---

## Troubleshooting

### Issue: "Server not found"

**Solution:**
- Check that the command is in your PATH
- For `uvx`/`npx`, ensure internet connection for first download
- Verify server name in config matches actual package name

### Issue: "Permission denied" (File System)

**Solution:**
- Check that the directory in config exists
- Verify you have read/write permissions
- Try using an absolute path instead of `.`

### Issue: "Tool not found"

**Solution:**
- Check that the server initialized successfully
- Verify the tool name matches what the server exposes
- Use MCP Inspector to test the server individually

---

## Summary

In this lesson, you learned:

- ✅ How to discover reference servers in the MCP ecosystem
- ✅ How to use `uvx` and `npx` to run servers without installation
- ✅ How to create a server configuration file
- ✅ How to manage multiple MCP client sessions
- ✅ How to map tools to their corresponding servers
- ✅ How to execute tools from the correct server
- ✅ How to build complex workflows combining multiple servers

### The Power of Multiple Servers

| Single Server | Multiple Servers |
|---------------|------------------|
| Limited functionality | Rich, combined capabilities |
| One data source | Many data sources |
| Simple use cases | Complex workflows |
| Manual integration | Standard protocol |

---

## What's Next?

You've now built a fully functional MCP chatbot that can:
- ✅ Connect to any MCP server
- ✅ Use tools from multiple servers
- ✅ Build complex workflows

In the next lessons, you'll:
- Add **resources** for read-only data
- Add **prompt templates** to help users
- Use **Claude Desktop** as a ready-made MCP host
- **Deploy servers remotely** for production use

**Continue to the next lesson →**