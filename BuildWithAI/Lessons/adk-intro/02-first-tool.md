<!-- # Challenge: Your First Tool
Define a tool and register it with your agent.

## Prerequisites
*   The [uv](https://github.com/astral-sh/uv) Python package manager installed.
*   An [ADK project]([ADK](https://google.github.io/adk-docs/getting-started/installation)) with a sample agent.

## Concept
As powerful as they are, LLMs used in *isolation* have some key limitations. For example, their knowledge is frozen at the time they were trained - and they cannot interact directly with the outside world.

A key development that enables a more dynamic approach is 'tool calling'. Here's how it works:

*   With each request, you provide the LLM with a list of available tools and their descriptions.
*   The LLM uses these descriptions to decide which tool (if any) can help fulfill the request.
*   Instead of running the tool itself, the LLM generates a structured output that specifies which tool it wants to use and what information to pass to it.
*   Your application code receives this output, executes the actual tool, and then calls the LLM a second time, providing the tool's result as part of the new request.
*   The LLM then uses the tool's output to generate its final response to you.

## Task
Create a simple Python function that accepts a number of sides, `roll_dice(sides: int)`, and add it to the `tools` list of your `Agent`. Test it in the web UI.

## Outcome
The agent will call your Python function and reply with its result. You will see the function call and response in the web UI.

## Question
The description of a tool is very important for getting good results. Can you explain why? What are common failure modes with tool descriptions? -->





# Challenge: Your First Tool
Define a tool and register it with your agent.

## Prerequisites
- The [uv](https://github.com/astral-sh/uv) Python package manager installed.
- An [ADK project](https://google.github.io/adk-docs/getting-started/installation) with a sample agent (`adk create demo`).

## Concept
LLMs in isolation can't access fresh data or perform actions. **Tool calling** lets models request your functions:
- You provide a set of tools (functions) and descriptions.
- The LLM decides when and what to call.
- Your app executes the tool and feeds the result back to the model.

In this challenge, we'll replace the typical "roll a dice" example with a more useful **mock weather tool**.

## Task

### 1. Create a Python function called `get_weather` in your agent file:

```python
from typing import Dict, Any, Optional
import random

def get_weather(city: str, date: Optional[str] = None) -> Dict[str, Any]:
    """
    Return a mock weather report (deterministic per city/date).
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy", "Windy"]
    base_temps = {
        "Nairobi": 23,
        "Lagos": 28,
        "Cairo": 30,
        "Cape Town": 20,
        "Accra": 27,
        "Kampala": 24,
    }
    
    key = f"{city.strip().title()}|{date or 'today'}"
    rng = random.Random(key)
    city_t = city.strip().title()
    base = base_temps.get(city_t, 25)
    temp = base + rng.randint(-3, 3)
    condition = rng.choice(conditions)
    is_sunny = condition in {"Sunny", "Partly Cloudy"}
    
    return {
        "city": city_t,
        "date": date or "today",
        "condition": condition,
        "temperature_celsius": temp,
        "is_sunny": is_sunny
    }
```

### 2. Register it in your agent definition:

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-2.5-flash",
    name="AfricaWorkshopAgent",
    description="Answers general questions and can look up mock city weather.",
    instruction="When asked about weather, call get_weather(city, date?). Use 'is_sunny' for yes/no answers.",
    tools=[get_weather],
)
```

### 3. Start the Developer UI:

```bash
adk web
```

### 4. Try in the UI:
- "What's the weather in Nairobi?"
- "Is it sunny in Lagos today?"

## Outcome
You'll see the `get_weather` function being called by your agent when you ask weather-related questions, and the Dev UI will display the function call details in the Trace view.

## Question
Why does the tool description (name, purpose, arguments, constraints) affect tool selection and argument quality?

List 2–3 common failure modes, such as:
- Vague or overly broad descriptions
- Overlapping scopes between tools
- Missing input format details
