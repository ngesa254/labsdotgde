# Adding Resources and Prompts

## Overview

So far, your MCP server only provided **tools** to your chatbot. You'll now update your server to also provide **resources** and **prompt templates**. On the chatbot side, you'll expose these features to the user.

This lesson completes the implementation of all three MCP primitives!

---

## Recap: MCP Primitives

| Primitive | Purpose | Direction | Example |
|-----------|---------|-----------|---------|
| **Tools** | Execute actions | Client calls → Server executes | `search_papers()` |
| **Resources** | Read-only data | Client requests → Server provides | List of papers |
| **Prompts** | Pre-built prompt templates | Client requests → Server provides | Optimized search prompt |

---

## Part 1: Adding Resources to the Server

### What Are Resources?

**Resources** are read-only data that applications can choose to use or provide to the model. Think of them as **GET requests** in HTTP—they retrieve data without modifying anything.

**When to use resources instead of tools:**
- Data that doesn't require modification (read-only)
- Content that updates dynamically
- Information the model might need in its context

### Resource URIs

Resources are identified by **URIs** (Uniform Resource Identifiers):

```
papers://folders           → List all folders
papers://computers         → Get papers about computers
papers://math              → Get papers about math
```

### Adding Resources to research_server.py

Update your `research_server.py` to include resources:

```python
from mcp.server.fastmcp import FastMCP
import arxiv
import json
import os

PAPER_DIRECTORY = "papers"
mcp = FastMCP("research")

# ... existing tool definitions ...

@mcp.resource("papers://folders")
def list_folders() -> str:
    """List all available paper folders (topics)."""
    try:
        # Check if directory exists
        if not os.path.exists(PAPER_DIRECTORY):
            return "No papers directory found"
        
        # List all subdirectories (topics)
        folders = [
            f for f in os.listdir(PAPER_DIRECTORY)
            if os.path.isdir(os.path.join(PAPER_DIRECTORY, f))
        ]
        
        if not folders:
            return "No paper folders found"
        
        return json.dumps({
            "folders": folders,
            "count": len(folders)
        }, indent=2)
    
    except Exception as e:
        return f"Error listing folders: {str(e)}"


@mcp.resource("papers://{topic}")
def get_papers_by_topic(topic: str) -> str:
    """Get all papers for a specific topic."""
    try:
        # Read from papers_info.json
        papers_file = f"{PAPER_DIRECTORY}/papers_info.json"
        
        if not os.path.exists(papers_file):
            return f"No papers found. Please search for papers first."
        
        with open(papers_file, "r") as f:
            all_papers = json.load(f)
        
        # Filter papers by topic (this is a simple implementation)
        # In a real app, you'd have better topic tracking
        topic_papers = []
        for paper_id, paper_data in all_papers.items():
            # Check if topic appears in title or summary
            if (topic.lower() in paper_data.get("title", "").lower() or
                topic.lower() in paper_data.get("summary", "").lower()):
                topic_papers.append({
                    "id": paper_id,
                    "title": paper_data.get("title"),
                    "authors": paper_data.get("authors"),
                    "summary": paper_data.get("summary")[:200] + "..."
                })
        
        if not topic_papers:
            return f"No papers found for topic: {topic}"
        
        return json.dumps({
            "topic": topic,
            "count": len(topic_papers),
            "papers": topic_papers
        }, indent=2)
    
    except Exception as e:
        return f"Error fetching papers for topic '{topic}': {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**What's happening:**

1. **`@mcp.resource("papers://folders")`** — Direct resource (no parameters)
   - Lists all available paper topics/folders

2. **`@mcp.resource("papers://{topic}")`** — Templated resource (with parameter)
   - Gets papers for a specific topic
   - URI includes `{topic}` placeholder

**Key differences from tools:**
- No parameters in function signature for direct resources
- Template parameter becomes function argument
- Returns data as string (usually JSON)
- No side effects—only reads data

---

## Part 2: Adding Prompts to the Server

### What Are Prompt Templates?

**Prompt templates** remove the burden of prompt engineering from users. Instead of users crafting complex prompts, the server provides battle-tested, optimized prompts with placeholders for dynamic data.

**Benefits:**
- Users don't need prompt engineering expertise
- Consistent, high-quality prompts
- Easy to update and improve centrally
- Can include complex instructions

### The Purpose of Prompts

| Without Prompt Template | With Prompt Template |
|-------------------------|----------------------|
| User: "search for math papers" | Server: *"You are an academic research assistant. Your task is to search arXiv for papers on [topic]. Return exactly [num_papers] results. Format the response as..."* |
| ❌ Vague, inconsistent results | ✅ Consistent, high-quality results |

### Adding Prompts to research_server.py

Add a prompt template to your server:

```python
from mcp.types import TextContent, PromptMessage

@mcp.prompt()
def generate_search_prompt(topic: str, num_papers: int = 5) -> list[PromptMessage]:
    """
    Generate an optimized prompt for searching academic papers.
    
    Args:
        topic: The research topic to search for
        num_papers: Number of papers to retrieve (optional, default: 5)
    """
    
    prompt_text = f"""You are an academic research assistant helping to find relevant papers.

Your task:
1. Search for papers on the topic: "{topic}"
2. Find exactly {num_papers} relevant papers
3. For each paper, provide:
   - Title
   - Authors
   - Brief summary
   - Why it's relevant to the topic

Guidelines:
- Prioritize recent papers (published within the last 3 years)
- Focus on papers with high citation counts
- Ensure papers are directly relevant to the topic
- Provide a brief analysis of the research landscape

Begin your search now."""

    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=prompt_text
            )
        )
    ]
```

**What's happening:**

1. **`@mcp.prompt()`** — Registers function as a prompt template
2. **Function parameters** — Become prompt arguments
   - `topic` (required) — Must be provided by user
   - `num_papers` (optional) — Has default value
3. **Return value** — List of `PromptMessage` objects
   - Contains the full prompt text
   - Can include multiple messages (user/assistant turns)

**Why this is powerful:**
- Users just provide `topic="machine learning"` and `num_papers=3`
- Server generates the complex, optimized prompt
- Easy to improve prompt quality without updating clients

---

## Part 3: Updating the Chatbot to Use Resources and Prompts

### Updated Chatbot State

Add tracking for resources and prompts:

```python
class MCPChatbot:
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic(...)
        self.sessions = []
        self.tools = []
        self.tool_to_session = {}
        
        # NEW: Track resources and prompts
        self.resource_uris = []          # List of available resource URIs
        self.prompts = []                # List of available prompts
        self.prompt_to_session = {}      # Map prompt name → session
        self.exit_stack = None
```

### Listing Resources and Prompts

Update `connect_to_server()` to list all primitives:

```python
async def connect_to_server(self, server_name: str, server_config: dict):
    """Connect to a server and list tools, resources, and prompts."""
    
    # ... existing connection code ...
    
    await session.initialize()
    
    # List tools
    try:
        tools_response = await session.list_tools()
        for tool in tools_response.tools:
            # ... add tools ...
    except Exception as e:
        print(f"  ! No tools available: {e}")
    
    # List resources
    try:
        resources_response = await session.list_resources()
        for resource in resources_response.resources:
            self.resource_uris.append({
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "session": session
            })
        print(f"  ✓ Resources: {len(resources_response.resources)}")
    except Exception as e:
        print(f"  ! No resources available: {e}")
    
    # List prompts
    try:
        prompts_response = await session.list_prompts()
        for prompt in prompts_response.prompts:
            prompt_dict = {
                "name": prompt.name,
                "description": prompt.description,
                "arguments": [
                    {
                        "name": arg.name,
                        "description": arg.description,
                        "required": arg.required
                    }
                    for arg in (prompt.arguments or [])
                ]
            }
            self.prompts.append(prompt_dict)
            self.prompt_to_session[prompt.name] = session
        print(f"  ✓ Prompts: {len(prompts_response.prompts)}")
    except Exception as e:
        print(f"  ! No prompts available: {e}")
```

**What's happening:**
- `session.list_resources()` — Gets available resource URIs
- `session.list_prompts()` — Gets available prompt templates
- Track which session each prompt belongs to
- Store resource URIs with metadata

---

## Part 4: Creating the User Interface

### UI Design Choices

**Remember:** MCP doesn't mandate how interfaces should look. The presentation is up to the client/host to create!

**Our design:**
- `@` prefix for resources: `@folders`, `@computers`
- `/` prefix for prompts: `/prompts`, `/prompt generate_search_prompt`

### Fetching Resources

Add a method to fetch resource content:

```python
async def get_resource(self, uri: str) -> str:
    """Fetch a resource by URI."""
    
    # Find the session that has this resource
    for resource in self.resource_uris:
        if resource["uri"] == uri:
            session = resource["session"]
            
            # Read the resource
            result = await session.read_resource(uri)
            
            # Extract content
            if result.contents:
                return result.contents[0].text
            return "No content available"
    
    return f"Resource not found: {uri}"
```

### Listing Prompts

Add a method to list available prompts:

```python
def list_available_prompts(self):
    """Display all available prompts."""
    if not self.prompts:
        print("No prompts available")
        return
    
    print("\nAvailable Prompts:")
    print("-" * 60)
    
    for prompt in self.prompts:
        print(f"\n📝 {prompt['name']}")
        print(f"   {prompt['description']}")
        
        if prompt['arguments']:
            print("   Arguments:")
            for arg in prompt['arguments']:
                required = "required" if arg['required'] else "optional"
                print(f"     - {arg['name']} ({required}): {arg['description']}")
    
    print("\nUsage: /prompt <name> key=value key=value")
    print("-" * 60)
```

### Executing Prompts

Add a method to execute a prompt template:

```python
async def execute_prompt(self, prompt_name: str, arguments: dict):
    """Execute a prompt template with given arguments."""
    
    # Find the session for this prompt
    session = self.prompt_to_session.get(prompt_name)
    
    if not session:
        print(f"Prompt not found: {prompt_name}")
        return
    
    # Get the prompt with arguments
    result = await session.get_prompt(prompt_name, arguments)
    
    # Extract the prompt messages
    if result.messages:
        # Use the prompt as the query
        prompt_content = result.messages[0].content.text
        
        # Process the prompt as if it were a user query
        await self.process_query(prompt_content)
```

---

## Part 5: Updated Chat Loop

Add special commands for resources and prompts:

```python
async def chat_loop(self):
    """Interactive chat loop with resource and prompt support."""
    
    print("\nCommands:")
    print("  @<resource>     - Fetch a resource (e.g., @folders)")
    print("  /prompts        - List available prompts")
    print("  /prompt <name>  - Execute a prompt (e.g., /prompt generate_search_prompt topic=ai)")
    print("  quit            - Exit")
    print()
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if query.lower() == 'quit':
                print("Goodbye!")
                break
            
            # Handle resources
            if query.startswith('@'):
                await self.handle_resource_command(query)
            
            # Handle prompt listing
            elif query == '/prompts':
                self.list_available_prompts()
            
            # Handle prompt execution
            elif query.startswith('/prompt '):
                await self.handle_prompt_command(query)
            
            # Handle regular queries
            else:
                await self.process_query(query)
            
            print()
            
        except Exception as e:
            print(f"\nError: {str(e)}\n")
```

### Handling Resource Commands

```python
async def handle_resource_command(self, query: str):
    """Handle resource fetch commands (e.g., @folders, @computers)."""
    
    # Remove @ prefix
    resource_name = query[1:]
    
    # Build URI
    # For our server, resources are "papers://folders" or "papers://{topic}"
    if resource_name == "folders":
        uri = "papers://folders"
    else:
        uri = f"papers://{resource_name}"
    
    # Fetch resource
    print(f"\n📚 Fetching resource: {uri}")
    content = await self.get_resource(uri)
    print(content)
```

### Handling Prompt Commands

```python
async def handle_prompt_command(self, query: str):
    """Handle prompt execution commands (e.g., /prompt generate_search_prompt topic=ai)."""
    
    # Remove '/prompt ' prefix
    parts = query[8:].strip().split(maxsplit=1)
    
    if not parts:
        print("Usage: /prompt <name> key=value key=value")
        return
    
    prompt_name = parts[0]
    
    # Parse arguments (key=value pairs)
    arguments = {}
    if len(parts) > 1:
        arg_string = parts[1]
        # Split by spaces, then by =
        for pair in arg_string.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                # Try to convert to int if possible
                try:
                    arguments[key] = int(value)
                except ValueError:
                    arguments[key] = value
    
    # Execute prompt
    print(f"\n🚀 Executing prompt: {prompt_name}")
    print(f"   Arguments: {arguments}")
    await self.execute_prompt(prompt_name, arguments)
```

---

## Complete Updated Chatbot

The full `mcp_chatbot.py` with all features:

```python
#!/usr/bin/env python3
"""MCP chatbot with tools, resources, and prompts."""

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
        self.anthropic_client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.sessions = []
        self.tools = []
        self.tool_to_session = {}
        self.resource_uris = []
        self.prompts = []
        self.prompt_to_session = {}
        self.exit_stack = None

    async def connect_to_server(self, server_name: str, server_config: dict):
        """Connect to a server and list all primitives."""
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
        self.sessions.append(session)
        
        print(f"\n🔗 Connecting to: {server_name}")
        
        # List tools
        try:
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                tool_dict = {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                self.tools.append(tool_dict)
                self.tool_to_session[tool.name] = session
            print(f"  ✓ Tools: {len(tools_response.tools)}")
        except Exception as e:
            print(f"  ! No tools: {e}")
        
        # List resources
        try:
            resources_response = await session.list_resources()
            for resource in resources_response.resources:
                self.resource_uris.append({
                    "uri": resource.uri,
                    "name": resource.name,
                    "description": resource.description,
                    "session": session
                })
            print(f"  ✓ Resources: {len(resources_response.resources)}")
        except Exception as e:
            print(f"  ! No resources: {e}")
        
        # List prompts
        try:
            prompts_response = await session.list_prompts()
            for prompt in prompts_response.prompts:
                prompt_dict = {
                    "name": prompt.name,
                    "description": prompt.description,
                    "arguments": [
                        {
                            "name": arg.name,
                            "description": arg.description,
                            "required": arg.required
                        }
                        for arg in (prompt.arguments or [])
                    ]
                }
                self.prompts.append(prompt_dict)
                self.prompt_to_session[prompt.name] = session
            print(f"  ✓ Prompts: {len(prompts_response.prompts)}")
        except Exception as e:
            print(f"  ! No prompts: {e}")

    async def connect_to_all_servers(self):
        """Connect to all servers."""
        with open("server_config.json", "r") as f:
            config = json.load(f)
        
        self.exit_stack = AsyncExitStack()
        await self.exit_stack.__aenter__()
        
        for server_name, server_config in config["mcpServers"].items():
            await self.connect_to_server(server_name, server_config)
        
        print(f"\n✅ Connected to {len(self.sessions)} servers")
        print(f"   Total tools: {len(self.tools)}")
        print(f"   Total resources: {len(self.resource_uris)}")
        print(f"   Total prompts: {len(self.prompts)}\n")

    async def execute_tool(self, tool_name: str, tool_args: dict):
        """Execute a tool."""
        session = self.tool_to_session.get(tool_name)
        if not session:
            return f"Tool not found: {tool_name}"
        
        result = await session.call_tool(tool_name, tool_args)
        if result.content:
            return result.content[0].text
        return ""

    async def get_resource(self, uri: str) -> str:
        """Fetch a resource."""
        for resource in self.resource_uris:
            if resource["uri"] == uri:
                session = resource["session"]
                result = await session.read_resource(uri)
                if result.contents:
                    return result.contents[0].text
                return "No content"
        return f"Resource not found: {uri}"

    def list_available_prompts(self):
        """List all prompts."""
        if not self.prompts:
            print("No prompts available")
            return
        
        print("\n📝 Available Prompts:")
        print("-" * 60)
        
        for prompt in self.prompts:
            print(f"\n{prompt['name']}")
            print(f"  {prompt['description']}")
            
            if prompt['arguments']:
                print("  Arguments:")
                for arg in prompt['arguments']:
                    req = "required" if arg['required'] else "optional"
                    print(f"    - {arg['name']} ({req})")
        
        print("\nUsage: /prompt <name> key=value")
        print("-" * 60)

    async def execute_prompt(self, prompt_name: str, arguments: dict):
        """Execute a prompt."""
        session = self.prompt_to_session.get(prompt_name)
        if not session:
            print(f"Prompt not found: {prompt_name}")
            return
        
        result = await session.get_prompt(prompt_name, arguments)
        
        if result.messages:
            prompt_content = result.messages[0].content.text
            await self.process_query(prompt_content)

    async def process_query(self, query):
        """Process a query."""
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
                    
                    print(f"\n[Tool: {tool_name}]")
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

    async def handle_resource_command(self, query: str):
        """Handle @resource commands."""
        resource_name = query[1:]
        
        if resource_name == "folders":
            uri = "papers://folders"
        else:
            uri = f"papers://{resource_name}"
        
        print(f"\n📚 Resource: {uri}")
        content = await self.get_resource(uri)
        print(content)

    async def handle_prompt_command(self, query: str):
        """Handle /prompt commands."""
        parts = query[8:].strip().split(maxsplit=1)
        
        if not parts:
            print("Usage: /prompt <name> key=value")
            return
        
        prompt_name = parts[0]
        arguments = {}
        
        if len(parts) > 1:
            for pair in parts[1].split():
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    try:
                        arguments[key] = int(value)
                    except ValueError:
                        arguments[key] = value
        
        print(f"\n🚀 Prompt: {prompt_name}")
        await self.execute_prompt(prompt_name, arguments)

    async def chat_loop(self):
        """Chat loop."""
        print("\n" + "="*60)
        print("Commands:")
        print("  @<resource>     - Fetch resource (e.g., @folders)")
        print("  /prompts        - List prompts")
        print("  /prompt <name>  - Execute prompt")
        print("  quit            - Exit")
        print("="*60 + "\n")
        
        while True:
            try:
                query = input("Query: ").strip()
                
                if query.lower() == 'quit':
                    print("Goodbye!")
                    break
                
                if query.startswith('@'):
                    await self.handle_resource_command(query)
                elif query == '/prompts':
                    self.list_available_prompts()
                elif query.startswith('/prompt '):
                    await self.handle_prompt_command(query)
                else:
                    await self.process_query(query)
                
                print()
                
            except Exception as e:
                print(f"\nError: {str(e)}\n")

    async def cleanup(self):
        """Cleanup connections."""
        if self.exit_stack:
            await self.exit_stack.__aexit__(None, None, None)


async def main():
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

## Running the Complete System

### Start the Chatbot

```bash
cd mcp_project
source .venv/bin/activate
uv run mcp_chatbot.py
```

### Expected Output

```
🔗 Connecting to: research
  ✓ Tools: 2
  ✓ Resources: 2
  ✓ Prompts: 1

🔗 Connecting to: fetch
  ✓ Tools: 2
  ✓ Prompts: 1

🔗 Connecting to: filesystem
  ✓ Tools: 7
  ! No resources
  ! No prompts

✅ Connected to 3 servers
   Total tools: 11
   Total resources: 2
   Total prompts: 2

============================================================
Commands:
  @<resource>     - Fetch resource (e.g., @folders)
  /prompts        - List prompts
  /prompt <name>  - Execute prompt
  quit            - Exit
============================================================

Query: _
```

---

## Example Usage

### Example 1: List Available Folders

```
Query: @folders

📚 Resource: papers://folders
{
  "folders": ["computers", "math", "physics"],
  "count": 3
}
```

**What happened:**
1. User typed `@folders`
2. Chatbot constructed URI: `papers://folders`
3. Called `session.read_resource("papers://folders")`
4. Server returned list of folders

---

### Example 2: Get Papers on a Topic

```
Query: @computers

📚 Resource: papers://computers
{
  "topic": "computers",
  "count": 5,
  "papers": [
    {
      "id": "http://arxiv.org/abs/2401.12345v1",
      "title": "Advances in Computer Architecture",
      "authors": ["John Doe", "Jane Smith"],
      "summary": "This paper explores recent developments..."
    },
    ...
  ]
}
```

**What happened:**
1. User typed `@computers`
2. Chatbot constructed URI: `papers://computers`
3. Server filtered papers related to "computers"
4. Returned JSON with matching papers

---

### Example 3: List Available Prompts

```
Query: /prompts

📝 Available Prompts:
------------------------------------------------------------

generate_search_prompt
  Generate an optimized prompt for searching academic papers
  Arguments:
    - topic (required)
    - num_papers (optional)

fetch_url
  Fetch an URL and extract its contents as markdown
  Arguments:
    - url (required)

Usage: /prompt <name> key=value
------------------------------------------------------------
```

---

### Example 4: Execute a Prompt

```
Query: /prompt generate_search_prompt topic=algebra num_papers=3

🚀 Prompt: generate_search_prompt

[Tool: search_papers]
[Tool: extract_info]
[Tool: extract_info]
[Tool: extract_info]

I found 3 papers on algebra:

1. **Algebraic Structures in Modern Mathematics**
   - Authors: Alice Johnson, Bob Williams
   - Summary: This paper explores fundamental algebraic structures...
   
2. **Linear Algebra Applications**
   ...

Papers saved to papers/algebra/
```

**What happened:**
1. User executed prompt with arguments
2. Chatbot called `session.get_prompt("generate_search_prompt", {topic: "algebra", num_papers: 3})`
3. Server returned optimized prompt text
4. Chatbot sent prompt to Claude
5. Claude used tools to search and extract papers
6. Results displayed to user

---

### Example 5: Combining All Primitives

```
Query: /prompt generate_search_prompt topic=history num_papers=2

🚀 Prompt: generate_search_prompt

[Tool: search_papers]
[Tool: extract_info]
[Tool: extract_info]

Found 2 papers on history...

Query: @folders

📚 Resource: papers://folders
{
  "folders": ["computers", "math", "physics", "algebra", "history"],
  "count": 5
}

Query: @history

📚 Resource: papers://history
{
  "topic": "history",
  "count": 2,
  "papers": [...]
}
```

**Workflow:**
1. ✅ **Prompt** — Used optimized search prompt
2. ✅ **Tools** — Searched and extracted papers
3. ✅ **Resource** — Listed available topics
4. ✅ **Resource** — Fetched history papers

All three primitives working together! 🎉

---

## Key Concepts

### Resources vs. Tools

| Aspect | Resources | Tools |
|--------|-----------|-------|
| **Purpose** | Read-only data | Execute actions |
| **Side effects** | None | May modify state |
| **HTTP analogy** | GET | POST/PUT/DELETE |
| **When to use** | Fetching data | Performing operations |
| **Example** | List papers | Search for papers |

### Prompt Design Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Task framing** | Explain the role | "You are an academic research assistant..." |
| **Step-by-step** | Break down the task | "1. Search for papers 2. Analyze relevance..." |
| **Output format** | Specify how to respond | "For each paper, provide: title, authors..." |
| **Guidelines** | Add constraints | "Prioritize recent papers..." |

---

## UI Design Considerations

### Why @ and / Prefixes?

These are **arbitrary choices** for our chatbot. You could use:
- `resource:folders` instead of `@folders`
- `!prompt search` instead of `/prompt search`
- GUI buttons instead of text commands

**MCP doesn't mandate UI patterns** — design what works for your users!

### Alternative UI Designs

| Design | Example |
|--------|---------|
| **Natural language** | "Show me folders" → chatbot detects intent |
| **Dropdown menus** | GUI with selectable resources |
| **Autocomplete** | Type `@` and see available resources |
| **Voice commands** | "Alexa, use the search prompt for AI" |

---

## Production Considerations

### Error Handling

```python
try:
    content = await self.get_resource(uri)
    print(content)
except Exception as e:
    print(f"Error fetching resource: {e}")
    # Log error, show user-friendly message
```

### Resource Caching

```python
# Cache frequently-accessed resources
self.resource_cache = {}

async def get_resource(self, uri: str) -> str:
    if uri in self.resource_cache:
        return self.resource_cache[uri]
    
    content = await self._fetch_resource(uri)
    self.resource_cache[uri] = content
    return content
```

### Prompt Validation

```python
def validate_prompt_arguments(self, prompt_name: str, arguments: dict):
    """Ensure required arguments are provided."""
    prompt = next(p for p in self.prompts if p['name'] == prompt_name)
    
    for arg in prompt['arguments']:
        if arg['required'] and arg['name'] not in arguments:
            raise ValueError(f"Missing required argument: {arg['name']}")
```

---

## Troubleshooting

### Issue: "Resource not found"

**Solution:**
- Check that the URI is correct
- Verify the server exposes this resource
- Use `session.list_resources()` to see available URIs

### Issue: "Prompt execution fails"

**Solution:**
- Verify required arguments are provided
- Check argument names match prompt definition
- Test the prompt in MCP Inspector first

### Issue: "Resources return empty content"

**Solution:**
- Check that data exists on the server
- Verify file paths in server code
- Add logging to server resource functions

---

## Summary

In this lesson, you learned:

- ✅ How to add **resources** to an MCP server
- ✅ How to add **prompt templates** to an MCP server
- ✅ The difference between direct and templated resources
- ✅ How to list resources and prompts from the client
- ✅ How to create a UI for accessing resources and prompts
- ✅ How to execute prompt templates with arguments
- ✅ How all three primitives (tools, resources, prompts) work together

### The Complete MCP Picture

| Primitive | Server Side | Client Side |
|-----------|-------------|-------------|
| **Tools** | `@mcp.tool()` | `call_tool(name, args)` |
| **Resources** | `@mcp.resource(uri)` | `read_resource(uri)` |
| **Prompts** | `@mcp.prompt()` | `get_prompt(name, args)` |

You've now built a **complete MCP system** with all three primitives! 🎉

---

## What's Next?

You've built:
1. ✅ MCP Server with tools, resources, and prompts
2. ✅ MCP Client that uses all three primitives
3. ✅ Multi-server chatbot with custom UI

In the next lessons, you'll:
- Use **Claude Desktop** as a ready-made MCP host
- **Deploy servers remotely** for production
- Explore **advanced MCP patterns**

**Continue to the next lesson →**