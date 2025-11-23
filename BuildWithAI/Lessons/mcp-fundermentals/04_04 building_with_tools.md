# Build a Chatbot with Tools

## Overview

In this lesson, you'll build a chatbot and code its tools. Before working with MCP, it's important to have a good foundation with tool use and prompting large language models.

> **Note:** If you're already familiar with tool use and the Anthropic SDK, feel free to skip this lesson and jump to building your first MCP server.

---

## What You'll Build

A chatbot that can:
- Search for academic papers on arXiv
- Extract detailed information about specific papers
- Summarize findings for the user

This chatbot uses **tool use** (function calling) to extend the model's capabilities beyond its training data.

---

## Setup: Import Libraries

First, import the necessary libraries:

```python
import arxiv
import json
import os
from typing import Any
import anthropic

# Define where we'll save paper information
PAPER_DIRECTORY = "papers"
```

**What we're importing:**
- `arxiv` — SDK for searching academic papers
- `json` — For formatting data
- `os` — For environment variables and file operations
- `anthropic` — SDK for Claude

---

## Function 1: Search Papers

Create a function to search for papers on arXiv:

```python
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
```

**Test it:**

```python
# Search for papers about "quantum computing"
paper_ids = search_papers("quantum computing")
print(f"Found {len(paper_ids)} papers")
print(f"First ID: {paper_ids[0]}")
```

**Output:**
```
Found 5 papers
First ID: http://arxiv.org/abs/2401.12345v1
```

The information is saved locally to `papers/papers_info.json`.

---

## Function 2: Extract Paper Info

Create a function to extract detailed information about a specific paper:

```python
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

**Test it:**

```python
# Get details about the first paper
paper_info = extract_info(paper_ids[0])
print(paper_info)
```

**Output:**
```json
{
  "title": "Quantum Computing: A Gentle Introduction",
  "authors": ["John Doe", "Jane Smith"],
  "summary": "This paper provides an overview of quantum computing...",
  "pdf_url": "http://arxiv.org/pdf/2401.12345v1",
  "published": "2024-01-15 10:30:00"
}
```

---

## Define Tools for the LLM

Now we'll define these functions as **tools** that Claude can use.

### Tool Definitions

```python
tools = [
    {
        "name": "search_papers",
        "description": "Search for academic papers on arXiv by topic. Returns a list of paper IDs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to search for (e.g., 'quantum computing', 'machine learning')"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5
                }
            },
            "required": ["topic"]
        }
    },
    {
        "name": "extract_info",
        "description": "Extract detailed information about a specific paper using its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "paper_id": {
                    "type": "string",
                    "description": "The arXiv paper ID"
                }
            },
            "required": ["paper_id"]
        }
    }
]
```

**What's happening:**
- Each tool has a `name`, `description`, and `input_schema`
- The schema defines what parameters the tool accepts
- The model uses this information to decide when and how to call tools

> **Important:** The model doesn't actually execute the functions. We need to write code to call the functions and return results to the model.

---

## Tool Execution Helper

Create a helper function to map tool names to actual functions:

```python
def execute_tool(tool_name: str, tool_input: dict[str, Any]) -> str:
    """
    Execute a tool function and return the result.
    
    Args:
        tool_name: Name of the tool to execute
        tool_input: Dictionary of input parameters
        
    Returns:
        String result from the tool execution
    """
    # Map tool names to functions
    tool_functions = {
        "search_papers": search_papers,
        "extract_info": extract_info
    }
    
    if tool_name not in tool_functions:
        return f"Error: Unknown tool '{tool_name}'"
    
    try:
        # Call the function with the provided inputs
        result = tool_functions[tool_name](**tool_input)
        
        # Convert result to string if it's not already
        if isinstance(result, list):
            return json.dumps(result)
        return str(result)
    
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"
```

---

## Build the Chatbot

### Initialize the Client

```python
# Load API key from environment
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
```

### Create the Chat Loop

```python
def chat_loop(user_query: str, messages: list = None) -> str:
    """
    Run a conversation with Claude, handling tool use.
    
    Args:
        user_query: The user's message
        messages: Conversation history (optional)
        
    Returns:
        Claude's final response
    """
    # Initialize messages if not provided
    if messages is None:
        messages = []
    
    # Add user message
    messages.append({
        "role": "user",
        "content": user_query
    })
    
    # Start conversation loop
    while True:
        # Call Claude
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
        
        # Add assistant response to messages
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        
        # Check if we need to execute tools
        if response.stop_reason == "tool_use":
            # Find tool use blocks in the response
            tool_results = []
            
            for content_block in response.content:
                if content_block.type == "tool_use":
                    # Execute the tool
                    tool_result = execute_tool(
                        content_block.name,
                        content_block.input
                    )
                    
                    # Add tool result to messages
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": tool_result
                    })
            
            # Add tool results to messages
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
            # Continue the loop to get Claude's response to the tool results
            continue
        
        # If no more tool use, extract final response
        final_response = ""
        for content_block in response.content:
            if hasattr(content_block, "text"):
                final_response += content_block.text
        
        return final_response
```

---

## Test the Chatbot

### Simple Interactive Loop

```python
def interactive_chat():
    """Run an interactive chat session."""
    messages = []
    
    print("Chat started! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        
        response = chat_loop(user_input, messages)
        print(f"\nClaude: {response}")

# Start the chat
interactive_chat()
```

---

## Example Conversation

```
You: Hi

Claude: Hello! I'm an AI assistant. I can help you search for academic 
papers on arXiv and extract detailed information about them. I have two 
main tools available:

1. search_papers - Search for papers by topic
2. extract_info - Get detailed information about a specific paper

How can I help you today?

---

You: Search for recent papers on algebra

Claude: [Tool use: search_papers with topic="algebra"]

I found 5 papers on algebra. Here are the IDs:
- http://arxiv.org/abs/2401.12345v1
- http://arxiv.org/abs/2401.12346v1
- http://arxiv.org/abs/2401.12347v1
- http://arxiv.org/abs/2401.12348v1
- http://arxiv.org/abs/2401.12349v1

Would you like me to extract more detailed information about any of these?

---

You: Yes please extract information on the first two you found and 
summarize them both for me

Claude: [Tool use: extract_info with paper_id="http://arxiv.org/abs/2401.12345v1"]
[Tool use: extract_info with paper_id="http://arxiv.org/abs/2401.12346v1"]

Here's a summary of both papers:

**Paper 1: Invariant Algebras and Their Applications**
This paper explores the theory of invariant algebras...

**Paper 2: Deformation of Algebras in Modern Mathematics**
This paper discusses the deformation theory of algebras...

---

You: quit
Goodbye!
```

---

## Key Concepts

### Tool Use Flow

```
1. User sends message
   ↓
2. Claude decides a tool is needed
   ↓
3. Claude returns tool_use block with:
   - Tool name
   - Tool inputs
   ↓
4. We execute the actual function
   ↓
5. We send tool result back to Claude
   ↓
6. Claude processes result and responds
```

### Important Notes

| Concept | Details |
|---------|---------|
| **No Persistent Memory** | Each conversation starts fresh unless you maintain message history |
| **Tool Execution** | The model doesn't call functions—we do |
| **Error Handling** | Always handle errors when executing tools |
| **Message History** | Pass the full conversation to maintain context |

---

## What's Next?

In this lesson, you learned:
- ✅ How to build a chatbot with the Anthropic SDK
- ✅ How to implement tool use (function calling)
- ✅ How to execute tools and return results to the model
- ✅ How to maintain conversation state

**Next:** You'll refactor this code to use MCP! Instead of defining tools directly in your chatbot, you'll:
- Build an MCP server that exposes these tools
- Test the server with MCP Inspector
- Connect your chatbot to the server as an MCP client

This will make your tools reusable across any MCP-compatible application.

**Continue to the next lesson →**