
#01-local
# from google.adk.agents.llm_agent import Agent

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )


# # # 02
# ## Add Tools


# from typing import Dict, Any, Optional
# import random
# from google.adk.agents.llm_agent import Agent

# # ---- Tool --------------------------------------------------------------------
# def get_weather(city: str, date: Optional[str] = None) -> Dict[str, Any]:
#     """
#     Tool: get_weather
#     Returns a mock weather report for a city (deterministic per city/date).

#     Args:
#       city: City name, e.g., "Nairobi".
#       date: Optional date string (YYYY-MM-DD). If omitted, assume today.

#     Returns:
#       {
#         "city": "<City>",
#         "date": "<YYYY-MM-DD or 'today'>",
#         "condition": "<Sunny|Cloudy|Rainy|Partly Cloudy|Stormy|Windy>",
#         "temperature_celsius": <int>,
#         "is_sunny": <bool>
#       }
#     """
#     conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy", "Windy"]
#     base_temps = {
#         "Nairobi": 23, "Lagos": 28, "Cairo": 30,
#         "Cape Town": 20, "Accra": 27, "Kampala": 24,
#     }

#     # Seed for stable outputs per (city, date)
#     seed = f"{city.strip().title()}|{date or 'today'}"
#     rng = random.Random(seed)

#     city_t = city.strip().title()
#     base = base_temps.get(city_t, 25)
#     temp = base + rng.randint(-3, 3)
#     condition = rng.choice(conditions)

#     # Simple rule: “Sunny” or “Partly Cloudy” => sunny
#     is_sunny = condition in {"Sunny", "Partly Cloudy"}

#     return {
#         "city": city_t,
#         "date": date or "today",
#         "condition": condition,
#         "temperature_celsius": temp,
#         "is_sunny": is_sunny,
#     }

# # ---- Agent -------------------------------------------------------------------
# root_agent = Agent(
#     model="gemini-2.5-flash",
#     name="AfricaWorkshopAgent",
#     description="Answers general questions and can look up (mock) city weather.",
#     instruction=(
#         "You can call the get_weather tool to answer weather questions. "
#         "If the user asks yes/no (e.g., 'Is it sunny in Lagos today?'), "
#         "use the tool and base the answer on the 'is_sunny' boolean."
#     ),
#     tools=[get_weather],
# )


## 03
## Multiple-tools

from typing import Dict, Any, Optional
import random
from google.adk.agents.llm_agent import Agent

# ---- Tool 1: Weather ---------------------------------------------------------
def get_weather(city: str, date: Optional[str] = None) -> Dict[str, Any]:
    """
    Return a mock weather report (deterministic per city/date).
    Use for questions like "What's the weather in Nairobi?" or "Is it sunny in Lagos today?"
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy", "Windy"]
    base_temps = {
        "Nairobi": 23, "Lagos": 28, "Cairo": 30,
        "Cape Town": 20, "Accra": 27, "Kampala": 24,
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
        "is_sunny": is_sunny,
    }

# ---- Tool 2: City Facts ------------------------------------------------------
def get_city_fact(city: str) -> Dict[str, str]:
    """
    Return a short, workshop-friendly fact for an African city.
    Use for: 'Tell me something about Accra' or 'Give me a quick fact about Cairo'.
    """
    facts = {
        "Nairobi": "Nairobi is known as the 'Green City in the Sun' and hosts Nairobi National Park.",
        "Lagos": "Lagos is one of Africa’s largest cities and Nigeria’s commercial hub.",
        "Cairo": "Cairo, on the Nile, is near the ancient Pyramids of Giza.",
        "Cape Town": "Cape Town is famous for Table Mountain and the Cape Winelands.",
        "Accra": "Accra is Ghana’s coastal capital, known for its art, markets, and beaches.",
        "Kampala": "Kampala is built on hills near Lake Victoria and is Uganda’s cultural center.",
    }
    city_t = city.strip().title()
    return {
        "city": city_t,
        "fact": facts.get(city_t, f"{city_t} is a vibrant African city with rich culture and history.")
    }

# ---- Agent -------------------------------------------------------------------
root_agent = Agent(
    model="gemini-2.5-flash",
    name="AfricaWorkshopAgent",
    description=(
        "Answers general questions and can look up mock city weather or quick city facts for African cities."
    ),
    instruction=(
        "You have two tools: "
        "1) get_weather(city, date?) for weather queries (including yes/no like 'Is it sunny in Lagos today?'). "
        "2) get_city_fact(city) for short city facts. "
        "Decide which tool to call based on the user's request. "
        "If the user mentions both fact and weather, call get_weather first, then enrich with get_city_fact."
    ),
    tools=[get_weather, get_city_fact],
)
