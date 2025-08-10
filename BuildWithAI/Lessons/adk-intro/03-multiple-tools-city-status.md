# Challenge: Multiple Tools — "City Status"
Add **two tools** and let the model route between them (or call both) to answer a combined query.

## Prerequisites
- A working ADK project with one tool (e.g., `get_weather`) from the previous challenge.

## Concept
Real agents often need **multiple tools**. The LLM chooses which to call (and in what order) based on your instructions and tool descriptions. Here, you'll add a second tool and respond to prompts like:  
> "Tell me a fact about Cairo **and** today's weather."

## Task

### 1. Keep your existing `get_weather(city, date?)` tool

### 2. Add a `get_city_fact(city)` tool

**Tool 2: City Facts**

```python
from typing import Dict

def get_city_fact(city: str) -> Dict[str, str]:
    """
    Return a short, workshop-friendly fact for an African city.
    """
    facts = {
        "Nairobi": "Nairobi is the 'Green City in the Sun' and hosts Nairobi National Park.",
        "Lagos": "Lagos is one of Africa's largest cities and Nigeria's commercial hub.",
        "Cairo": "Cairo, on the Nile, is near the ancient Pyramids of Giza.",
        "Cape Town": "Cape Town is famous for Table Mountain and the Cape Winelands.",
        "Accra": "Accra is Ghana's coastal capital, known for its art and beaches.",
        "Kampala": "Kampala spans several hills near Lake Victoria, Uganda's cultural center.",
    }
    city_t = city.strip().title()
    return {"city": city_t, "fact": facts.get(city_t, f"{city_t} is a vibrant African city with rich culture.")}
```

### 3. Update the agent to register both tools

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-2.5-flash",
    name="AfricaWorkshopAgent",
    description="Answers questions with mock weather and city facts.",
    instruction=(
        "Use get_weather(city, date?) for weather. "
        "Use get_city_fact(city) for city facts. "
        "If the user asks for both (e.g., 'fact and weather'), call both tools and synthesize a single answer."
    ),
    tools=[get_weather, get_city_fact],
)
```

## Prompts to try
- "Give me a quick fact about Nairobi."
- "What's the weather in Accra on 2025-08-12?"
- "Tell me a fact about Cairo and today's weather."

## Outcome
You'll see multiple tool calls in the Trace view and a merged response in chat (a concise "city status").

## Question
What guidelines help the LLM reliably choose between overlapping tools? How can you improve routing with clearer names, argument schemas, and examples?