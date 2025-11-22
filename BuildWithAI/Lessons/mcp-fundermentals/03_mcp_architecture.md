# MCP Architecture

## Overview

MCP is based on a **client-server architecture**. In this lesson, we'll explore the features that MCP can provide and how communication between the client and the server takes place.

## Client-Server Architecture

MCP follows the classic **client-server architecture**, similar to other protocols.

### Components

```
┌─────────────────────────────────────────────────────────────────┐
│                          Host                                   │
│              (Claude Desktop, Claude AI, etc.)                  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ MCP Client 1 │  │ MCP Client 2 │  │ MCP Client 3 │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │   MCP    │       │   MCP    │       │   MCP    │
    │ Server 1 │       │ Server 2 │       │ Server 3 │
    └──────────┘       └──────────┘       └──────────┘
```

| Component | Description |
|-----------|-------------|
| **Host** | LLM application that wants to access data through MCP (e.g., Claude Desktop, Cursor, Windsurf) |
| **MCP Client** | Lives inside the host, maintains a 1:1 connection with an MCP server |
| **MCP Server** | Lightweight program that exposes specific capabilities through the protocol |

### Key Points

- **1:1 Connection** — Each MCP client maintains exactly one connection with one MCP server
- **Hosts manage clients** — The host is responsible for storing and maintaining all clients and connections to MCP servers
- **Message-based communication** — Clients and servers communicate through messages defined by MCP

## MCP Primitives

MCP provides three fundamental primitives (building blocks) that servers can expose to clients:

### 1. Tools 🛠️

**Tools** are functions that can be invoked by the client.

**Purpose:** Allow for actions that modify data or state

**Use cases:**
- Retrieving data
- Searching
- Sending messages
- Updating database records
- POST-like operations

**Think of tools as:** Functions the LLM can call to perform actions

### 2. Resources 📚

**Resources** are read-only data or context exposed by the server.

**Purpose:** Provide data that applications can consume

**Characteristics:**
- Read-only
- Similar to GET requests
- Application chooses whether to use the resource

**Examples:**
- Database records
- API responses
- Files
- PDFs
- Dynamic data that updates

### 3. Prompt Templates 📝

**Prompt Templates** are predefined prompts that live on the server.

**Purpose:** Remove the burden of prompt engineering from the user

**How it works:**
- User provides dynamic data
- Server provides the optimized prompt template
- User doesn't need to figure out best practices

**Example:** Instead of the user writing "Query Google Drive and summarize documents with the following criteria...", they select a template and just provide the search terms.


## Roles and Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **Server** | Exposes tools, resources, and prompts |
| **Client** | Finds and requests tools, resources, and prompts |
| **Host** | Manages multiple clients and provides the UI |


## Demo: SQLite MCP Server with Claude Desktop

Let's see MCP in action with a real example.

### Setup

- **Host:** Claude Desktop
- **MCP Server:** SQLite MCP server
- **Capabilities:** Exposes tools, resources, and prompts for working with SQLite databases

### Example 1: Using Tools

**User prompt:** "What tables do I have and how many records are in each table?"

**What happens:**
1. Client uses the `list_tables` tool from the SQLite server
2. Server executes the tool (no dynamic data needed)
3. Returns: 30 products, 30 users, 0 orders

**Human-in-the-loop:** The host (Claude Desktop) can require user approval before executing tools

### Example 2: Generating Visualizations

**User prompt:** "Generate an interesting visualization based on the data in the products table"

**What happens:**
1. Client queries the products table
2. Client analyzes the data (price distribution, quantity, etc.)
3. Client uses Claude's Artifacts feature to create visualization
4. Returns: Interactive charts showing price vs. quantity

**Key insight:** By bringing external data into the AI application through MCP, we can create much more powerful and interesting applications.

### Example 3: Using Prompt Templates

**User prompt:** Select the "MCP demo" prompt template and add dynamic data: "planets"

**What happens:**
1. Server provides a pre-written, optimized prompt template
2. User only provides the dynamic data (topic: "planets")
3. Template automatically:
   - Sets up database tables
   - Populates with sample data
   - Analyzes business problems
   - Generates insights

**Benefit:** Users get battle-tested, evaluated prompts without doing prompt engineering themselves

### Example 4: Using Resources

**What's happening:**
- A "Business Insights Memo" resource is dynamically updated as data changes
- No need for tools to fetch this information
- Data constantly refreshed based on database state
- Client can access the memo at any time

## Building MCP Components with Python SDK

MCP provides Software Development Kits (SDKs) for building servers and clients. In this course, we'll use the **Python MCP SDK**.

![Defining a Tool](img_defining_tool.png)

### Creating a Tool

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Args:
        a: First number to add
        b: Second number to add
    
    Returns:
        The sum of the two numbers
    """
    return a + b
```

**What's happening:**
- Decorate a function with `@mcp.tool()`
- Specify arguments with type hints
- Add docstring to describe the tool (becomes part of the schema)
- Tool schema is automatically generated
- Return the result when the tool is executed

### Creating a Resource

![Resources Overview](img_resources.png)

Resources allow the MCP Server to expose data to the client. They are:
- Similar to GET request handlers in a typical HTTP server
- Can return any type of data (strings, JSON, binary, etc.)
- Read-only by design

#### Direct Resource

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs():
    # Return a list of document names
    return json.dumps(get_all_documents())
```

**What's happening:**
- Specify a URI (Uniform Resource Identifier)
- Decorate a function that returns the data
- Optionally specify MIME type to hint at data format

#### Templated Resource

```python
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str):
    # Return the contents of a doc
    return get_document_by_id(doc_id)
```

**What's happening:**
- Use templating syntax like Python f-strings
- Dynamic URIs based on parameters
- Client can reference specific resources: `@docs://documents/report.pdf`

![Resources Usage](img_resources_usage.png)

**Direct resources** — Server provides a list of all documents  
**Templated resources** — Server provides contents of a single, specific document

### Creating a Prompt Template

![Prompts Overview](img_prompts.png)

Prompts define a set of User and Assistant messages that can be used by the client. These prompts should be **high quality and well-tested**.

```python
@mcp.prompt(
    name="format",
    description="Rewrites the contents of a document in Markdown format",
)
def format_document(
    doc_id: str,
) -> list[base.Message]:
    # Return a list of messages
    return [
        base.Message(
            role="user",
            content=f"Please convert document {doc_id} to Markdown"
        )
    ]
```

**What's happening:**
- Decorate a function with `@mcp.prompt()`
- Return a list of messages (user/assistant format)
- User provides dynamic data (doc_id)
- Server provides the optimized prompt structure

![Prompt Engineering Comparison](img_prompt_engineering.png)

**The value of prompt templates:**

**Basic user prompt:**
```
Convert report.pdf to markdown
```
*This works, but might not get the best results*

**Optimized prompt template:**
```
You are a document conversion specialist tasked with rewriting documents in Markdown format. 
Your goal is to take the content of a given document and convert it into well-structured Markdown, 
preserving the original meaning and enhancing readability.

Here is the identifier of the document you need to convert:
<document_id>
{{doc_id}}
</document_id>

Instructions:
1. Retrieve the content of the document associated with the given document_id
2. Analyze the structure and content of the document
3. Convert the document to Markdown format, following these guidelines:
   - Use appropriate header levels (# for main titles, ## for subtitles, etc.)
   - Properly format lists (both ordered and unordered)
   - Use emphasis (*italic* or **bold**) where appropriate
   - Add links and images using Markdown syntax if present in the original document
   - Preserve any special formatting or structure that's important to the document's meaning

[...detailed instructions continue...]
```
*This gives much better, more consistent results!*

Users benefit from thoroughly evaluated prompts without having to do the prompt engineering themselves.


## Communication Lifecycle

![Communication Lifecycle](img_communication_lifecycle.png)

### 1. Initialization

```
Client                    Server
  │                         │
  ├──── Initialize Request ──▶
  │                         │
  ◀──── Initialize Response ─┤
  │                         │
  ├──── Initialized Notification ──▶
  │                         │
```

**Steps:**
1. Client opens connection to server
2. Client sends initialization request
3. Server sends response
4. Client sends notification to confirm initialization

**Connection is established**

### 2. Message Exchange

Once initialized, clients and servers exchange messages:

| Direction | Type | Purpose |
|-----------|------|---------|
| Client → Server | Request | Ask for tools, resources, prompts |
| Server → Client | Request | Sampling (ask LLM for completion) |
| Both directions | Notification | Send information without expecting response |

### 3. Termination

When communication is complete, the connection is terminated.

## Transports: How Messages Travel

A **transport** handles the mechanics of how messages are sent between client and server.

### Transport Types

| Transport | Use Case |
|-----------|----------|
| **Standard I/O (stdio)** | Local servers (subprocess) |
| **HTTP + Server-Sent Events (SSE)** | Remote servers (stateful) |
| **Streamable HTTP** | Remote servers (stateful or stateless) |

## Standard I/O Transport (Local Servers)

### How it Works

![Standard I/O Transport](img_stdio_transport.png)

When running servers locally, stdio (Standard I/O) is most commonly used.

**Process:**

1. **Launch** — Client launches the server as a subprocess and initializes communication
2. **Message Exchange** — Ongoing bidirectional communication:
   - Client writes to the server's **stdin** (standard input) stream
   - Server writes to its **stdout** (standard output) stream
3. **Termination** — Close stdin, terminate subprocess

**Key characteristics:**
- Server runs as a subprocess of the client
- Communication happens through stdin/stdout pipes
- All message exchange is abstracted away by the SDK
- Most common for running servers locally on your machine

**Example use cases:**
- Development and testing
- Claude Desktop connecting to local MCP servers
- Command-line tools that need MCP capabilities


## HTTP + Server-Sent Events (Stateful Remote Servers)

### How it Works

```
Client                         Server
  │                              │
  ├──── HTTP POST /mcp ──────────▶ Initialize
  │                              │
  ◀──── HTTP Response ───────────┤
  │                              │
  ├──── GET /sse ────────────────▶ Upgrade to SSE
  │                              │
  ◀──── Server-Sent Events ──────┤ Ongoing messages
  │                              │
  ├──── HTTP POST (requests) ────▶
  │                              │
```

**Characteristics:**
- **Stateful connection** — Connection remains open between requests
- **Data is remembered** — Server maintains state across requests
- **Server can push** — Server-sent events allow server to send messages to client

**Use case:** Applications that need to maintain conversation state or session data

## Streamable HTTP Transport (Recommended)

### Why Streamable HTTP?

Many deployed applications are **stateless** (each request is independent) for better scaling. The original HTTP+SSE transport only supported stateful connections.

**Streamable HTTP** supports both:
- ✅ Stateful connections (with SSE)
- ✅ Stateless connections (pure HTTP)

![Streamable HTTP Transport](img_streamable_http_transport.png)

For remote MCP servers, the **Streamable HTTP transport** is used. This supports:
- **Stateless connections** — Each request is independent
- **Stateful connections** — With the ability to opt into Server-Sent Events

### How it Works

**1. Initialize the connection:**
```
POST /mcp to initialize request
  ↓
Initialize response
```

**2. (Optional) Upgrade to Server-Sent Events:**
```
optional GET /mcp with Accept: text/event-stream
  ↓
Server can now send messages to client
```
*If you skip this step, you have a stateless connection*

**3. Exchange messages:**
```
POST /mcp with request
  ↓
HTTP Response
```

**4. Terminate (optional):**
```
optional DELETE /mcp to terminate session
  ↓
Session terminated
```

### Stateless vs. Stateful Mode

| Mode | When to Use | How it Works |
|------|-------------|--------------|
| **Stateless** | Scalable deployments, serverless functions | Just POST requests, no SSE upgrade |
| **Stateful** | Applications needing conversation state | POST + GET with SSE for server messages |

**Going forward:** Streamable HTTP is the recommended transport for remote servers.

> **Note:** As of this recording, Streamable HTTP is not yet supported across all SDKs, so we'll use HTTP+SSE in our examples.


## Summary

In this lesson, you learned:

- ✅ **Client-server architecture** — Hosts, clients, and servers
- ✅ **Three primitives** — Tools, Resources, Prompt Templates
- ✅ **Building MCP components** — Using the Python SDK
- ✅ **Communication lifecycle** — Initialization, messages, termination
- ✅ **Transports** — Standard I/O (local), HTTP+SSE (stateful), Streamable HTTP (both)
- ✅ **Stateful vs. Stateless** — When to use each approach

### Key Takeaways

| Concept | Key Point |
|---------|-----------|
| **Tools** | Functions that modify data (like POST requests) |
| **Resources** | Read-only data (like GET requests) |
| **Prompts** | Pre-written, optimized prompt templates |
| **Standard I/O** | For local servers (subprocess) |
| **HTTP+SSE** | For remote stateful servers |
| **Streamable HTTP** | For remote servers (stateful or stateless) |

## Next Steps

Now it's time to get your hands on some code! In the next lesson, we'll:

- Take a look at the tools we'll be using
- Start building our own MCP servers
- Eventually build clients and hosts

**Continue to the next lesson →**