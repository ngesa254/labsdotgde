# ADK LABS: Building AI Agents with Google's Agent Development Kit (ADK)

Welcome! In this workshop, we’ll guide you from the fundamentals of agent development to creating and deploying powerful, intelligent AI agents on Google Cloud.

## How to Make the Most of This Workshop

- **Pair up:** Collaboration makes the challenges faster and more fun.
- **Learn at your own pace:** Pick the challenges that interest you. It's fine not to finish all of them.
- **Celebrate progress:** Completing even one challenge is a win.
- **Ask for help:** In-person? Stuck for more than 20 seconds—raise your hand and we'll help.

These challenges are designed for exploration rather than step-by-step instructions. You’re encouraged to use all available resources to figure things out:

- Search the [ADK documentation](https://google.github.io/adk-docs/) and explore the [adk-samples](https://github.com/google/adk-samples) repository.
- I also have another repository with example solutions to some of the challenges — resist the temptation to peek until you’ve tried solving them yourself!
- Most challenges will require a Google Cloud Project.  
  - In our in-person workshops, you can use the free $5 credit on the Google Cloud free tier (no credit card needed).  
  - Be aware of rate limits and quotas.

## Lesson 1: ADK Fundermentals

### 1. Local Setup & "Hello, Agent!"
📁 `Lessons/adk-intro/01-local-setup.md`  
Set up your environment and run the Dev UI.

### 2. Your First Tool // Empower ADK agents with tools.

📁 `Lessons/adk-intro/02-first-tool.md`  
Add a practical tool (`get_weather`) and see tool calls in the Trace view.

### 3. Multiple Tools — "City Status"
📁 `Lessons/adk-intro/03-multiple-tools-city-status.md`  
Add `get_city_fact` and learn routing / combining outputs.

### 4. Your First Cloud Deployment
📁 `Lessons/adk-intro/04-first-cloud-deployment.md`  
Publish to Cloud Run with `adk deploy cloud_run --with_ui`.

## Lesson 2: Multi Agent Systems with ADK and MCP

## Repo Structure (suggested)

```
/solutions
  /demo
    agent.py        # your agent + tools
/Lessons
  /adk-intro
    01-local-setup.md
    02-first-tool.md
    03-multiple-tools-city-status.md
    04-first-cloud-deployment.md
readme.md
```

**Happy building!** 🚀