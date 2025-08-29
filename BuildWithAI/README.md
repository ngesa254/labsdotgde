# ADK LABS: Building AI Agents with Google's Agent Development Kit (ADK)

Welcome! In this workshop, we'll guide you from the fundamentals of agent development to creating and deploying powerful AI agents on Google Cloud.

## How to Make the Most of This Workshop

- **Pair up:** Collaboration makes the challenges faster and more fun.
- **Learn at your own pace:** Pick the challenges that interest you. It's fine not to finish all of them.
- **Celebrate progress:** Completing even one challenge is a win.
- **Ask for help:** In-person? Stuck for more than 20 seconds—raise your hand and we'll help.

These challenges are designed for exploration rather than step-by-step instructions. You're encouraged to use all available resources to figure things out:

- Search the [ADK documentation](https://google.github.io/adk-docs/) and explore the [adk-samples](https://github.com/google/adk-samples) repository.
- I also have another repository with example solutions to some of the challenges — resist the temptation to peek until you've tried solving them yourself!
- Most challenges will require a Google Cloud Project.  
  - In our in-person workshops, you can use the free $5 credit on the Google Cloud free tier (no credit card needed).  
  - Be aware of rate limits and quotas.

## Lesson 1: ADK Fundamentals

Get started with Google Agent Development Kit (ADK)
Empower ADK agents with tools

### 1.1 Local Setup & "Hello, Agent!"
📁 `Lessons/adk-intro/01-local-setup.md`  
Set up your environment and run the Dev UI.

### 1.2 Your First Tool // Empower ADK agents with tools.

📁 `Lessons/adk-intro/02-first-tool.md`  
Add a practical tool (`get_weather`) and see tool calls in the Trace view.

### 1.3 Multiple Tools — "City Status"
📁 `Lessons/adk-intro/03-multiple-tools-city-status.md`  
Add `get_city_fact` and learn routing / combining outputs.

### 1.4 Your First Cloud Deployment
📁 `Lessons/adk-intro/04-first-cloud-deployment.md`  
Publish to Cloud Run with `adk deploy cloud_run --with_ui`.

## Lesson 2: Build multi-agent systems with ADK

This workshop covers orchestrating multi-agent systems within the Google Agent Development Kit (Google ADK).

This workshop assumes that you are familiar with the basics of ADK and tool use as covered in the lesson 1.

In this workshop, you will:

- Create multiple agents and relate them to one another with parent to sub-agent relationships
- Build content across multiple turns of conversation and multiple agents by writing to a session's state dictionary
- Instruct agents to read values from the session state to use as context for their responses
- Use workflow agents to pass the conversation between agents directly

### 2.1. Convert function calling agents into ADK Tools...

## Lesson 3: Multi-Agent Systems with ADK and MCP

📁 `Lessons/adk-mcp/`  
Extend ADK agents with Model Context Protocol (MCP) integrations.

### 3.5 Agentic Workflows with Gemini (Prep Lab)

📁 `Lessons/adk-mcp/035-agentic-workflows-prep.md`  
📓 `Kisumu_buildwithai_agentic_workflows_with_gemini.ipynb`  
**Colab:** https://colab.research.google.com/drive/1LkY6OG9H7R2NvsgzdCYVJ7QKIfStYgSr

Hands-on codelab to build a DevFest Assistant using Gemini + LlamaIndex:

- Scrape schedules (Lagos/Nairobi)
- Search images
- Generate social media posts
- Assemble a ReAct-style agent with tool use

### 3.6 Multimodal Live API Quickstart (Prep Lab)

📁 `Lessons/adk-mcp/036-gemini-liveapi-fundamentals.md`  
📓 `Kisumu_buildwithai_liveapi_fundermentals.ipynb`  
**Colab:** https://colab.research.google.com/drive/1v6JnpWr3xDBFip6HRxBHiQWxe6-N9jMc

Experiment with Gemini 2.5 Flash Live API (preview) in Colab:

- Turn-based text→text and text→audio chat
- Save and play back native audio (.wav)
- Resumable sessions to continue later
- Path toward async, real-time streaming

**Outcome:** You'll understand Live API basics and have a working Colab demo before moving to full ADK integration.

## Lesson 4: Multimodal Streaming Agents with ADK and Gemini Live API

📁 `Lessons/adk-gemini-live/`  
Bring it all together: build a real-time, multimodal chat application with ADK + Gemini Live API.

Learn to:

- Stream text, images, and audio into/out of your ADK agent
- Deploy multimodal workflows locally and to the cloud
- Extend your ADK agent with low-latency voice/video streaming

**Outcome:** A fully functional multimodal ADK agent that can interact via text and speech, and be deployed to Cloud Run.

## Hands-On Projects

### Project A: DevFest Assistant Agent

Build a comprehensive agent that can:

- Fetch real-time conference schedules (DevFest Lagos & Nairobi)
- Provide personalized session recommendations
- Generate social media content
- Handle multi-turn conversations with memory

Use the tech covered in Lessons 1–4 and the prep labs (3.5 & 3.6)

## Repo Structure

```
BuildWithAI/
├── .venv/                           # Python virtual environment
├── Lessons/
│   ├── adk-gemini-live/            # Lesson 4: Multimodal streaming agents
│   ├── adk-intro/                  # Lesson 1: ADK fundamentals
│   │   ├── 01-local-setup.md
│   │   ├── 02-first-tool.md
│   │   ├── 03-multiple-tools-city-status.md
│   │   └── 04-first-cloud-deployment.md
│   └── adk-mcp/                    # Lesson 3: MCP integrations & prep labs
│       ├── 035-agentic-workflows-prep.md
│       └── 036-gemini-liveapi-fundamentals.md
├── Samples/
│   ├── adk_intro/                  # Sample code for intro lessons
│   └── adk_mcp/                    # Sample MCP implementations
├── notebooks/
│   ├── Kisumu_buildwithai_agentic_workflows_with_gemini.ipynb
│   └── Kisumu_buildwithai_liveapi_fundamentals.ipynb
└── README.md
```
source .venv/bin/activate

**Happy building!** 🚀