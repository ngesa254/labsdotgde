<!-- # Challenge: Local Setup & "Hello, Agent!"
Set up your local development environment and run the basic agent.

## Concept
The first step is to set up your local development environment and run the basic, pre-generated agent to understand the core workflow.

## Prerequisites
*   Optional: The [uv](https://github.com/astral-sh/uv) Python package manager.

## Task
Use `adk create demo` to generate agent source code and `adk web` to launch the local web UI. If you're using `uv`, getting started with a project is two steps: run `uv init` and `uv add google-adk`.

## Outcome
You have the ADK web UI running on your machine, allowing you to chat with your first, simple agent.

## Question
The `adk web` command starts a server. Explore the UI and find out what all the tabs do. -->



# Challenge: Local Setup & "Hello, Agent!"
Set up your local development environment and run the basic agent.

## Concept
The first step is to prepare your local environment and run a pre-generated agent to understand the **Agent Development Kit (ADK)** workflow and explore the Developer UI.

ADK makes it easy to create AI agents that can reason, call tools, and be deployed locally or in the cloud. Before you start building custom tools, you'll get hands-on experience with a simple, working agent.

## Prerequisites
- Python 3.10+ installed
- Optional: The [uv](https://github.com/astral-sh/uv) Python package manager for faster installs and simplified project setup.

## Task

### If you're **not** using `uv`:
1. Create a new ADK project:
   ```bash
   adk create demo
   ```

2. Start the Developer UI:
   ```bash
   adk web
   ```

### If you are using `uv`:
1. Initialize a new project:
   ```bash
   uv init
   ```

2. Add ADK to your project:
   ```bash
   uv add google-adk
   ```

3. Create the demo agent:
   ```bash
   adk create demo
   ```

4. Start the Developer UI:
   ```bash
   adk web
   ```

## Outcome
You should now have the ADK Developer UI running locally at:
```
http://localhost:8000
```

From here you can:
- Chat with your first agent
- Explore how it responds to prompts
- See the request/response flow in the Trace view

## Question
The `adk web` command starts a local web server.

Explore the UI tabs and answer:
- What does each of these tabs do? **Trace, Events, State, Artifacts, Sessions, Eval**
- Which one would be most useful for debugging tool calls?