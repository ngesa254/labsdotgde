# Lesson 3.5: Agentic Workflows with Gemini (Prep Lab)

📓 `Kisumu_buildwithai_agentic_workflows_with_gemini.ipynb`  
**Colab:** https://colab.research.google.com/drive/1LkY6OG9H7R2NvsgzdCYVJ7QKIfStYgSr

## Challenge: Build a DevFest Agent with Tools 🦜️🔗

Create an agent that can fetch schedules, search images, and generate social posts for DevFest events.

## Prerequisites
* Python + Colab (notebook-ready).
* Google Gemini API key configured.
* Familiarity with `llama-index` and function calling (covered in earlier lessons).

## Concept
Realistic agents combine **multiple external tools** with **LLM reasoning**. In this lab, you'll extend Gemini with a set of practical tools:
* Scrapers for DevFest Lagos & Nairobi schedules
* An image search helper
* A social media post generator

Your agent will decide when to use each, and synthesize results into one coherent answer.

## Task

### 1. Implement the tools:
* `get_devfest_lagos_schedule()`
* `get_devfest_nairobi_schedule()`
* `search_for_devfest_images(location)`
* `generate_social_media_post(event_name, summary)`

### 2. Register tools with a **ReAct-style agent** (via LlamaIndex).

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

agent = ReActAgent.from_tools(
    [tool1, tool2, tool3, tool4], 
    llm=Settings.llm,
    verbose=True
)
```

### 3. Try these prompts:
* "Who is speaking about AI in Lagos?"
* "Show me pictures of DevFest Nairobi."
* "Find all AI sessions in Nairobi and generate a tweet to promote them."

## Outcome
You'll see **tool calls** in action, with Gemini chaining data → reasoning → output. In the interactive chat loop, the agent will even **remember context** for follow-up questions.

## Question
How do tool descriptions influence whether the LLM chooses the correct tool? What happens when tool scopes overlap?