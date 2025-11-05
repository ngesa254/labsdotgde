# Define a Weather Tool

## Understanding the Need for Tools

So far, our chatbot is knowledgeable, but its knowledge is limited to the data it was trained on. It can't access real-time information. For a travel bot, being able to fetch live data like weather forecasts is a huge advantage.

This is where **tooling**, also known as **function calling**, comes in. We can define a set of tools (Python functions) that the LLM can choose to call to get external information.

---

## How Tooling Works

The function calling process follows these steps:

1. **We describe our tools** to the model, including what they do and what parameters they take.

2. **The user sends a prompt** (e.g., "What's the weather in London?").

3. **The model receives the prompt** and sees that the user is asking about something it can find out using one of its tools.

4. **Instead of responding with text**, the model responds with a special `function_call` object, indicating which tool it wants to call and with which arguments.

5. **Our Python code receives this `function_call`**, executes our actual `get_current_temperature` function with the provided arguments, and gets the result (e.g., 15°C).

6. **We send this result back to the model**.

7. **The model receives the result** and generates a natural language response for the user (e.g., "The current temperature in London is 15°C.").

This process allows the model to answer questions far beyond its training data, making it a much more powerful and useful assistant.

---

## Define a Weather Tool

If a traveler is looking for advice on what to do, and is choosing between activities affected by the weather, a weather tool could come in handy! Let's create a tool for our model to get the current weather. 

We need two parts:
1. **A function declaration** that describes the tool to the model
2. **The actual Python function** that implements it

### Step-by-Step Instructions

#### 1. Locate the Weather Tool Comment

In `app.py`, find the comment:

```python
# TODO: Define the weather tool function declaration
```

#### 2. Add the Function Declaration

Under this comment, add the `weather_function` variable. This is a dictionary that tells the model everything it needs to know about the function's purpose, parameters, and required arguments:

```python
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}
```

#### 3. Locate the Function Implementation Comment

Next, find the comment:

```python
# TODO: Define the get_current_temperature function
```

#### 4. Add the Python Function

Under it, add the following Python code. This function will:
- Call a geocoding API to get coordinates for the location
- Use those coordinates to call a weather API
- Return a simple string with the temperature and unit

```python
def get_current_temperature(location: str) -> str:
    """Gets the current temperature for a given location."""

    try:
        # --- Get Latitude and Longitude for the location ---
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if not geocode_data.get("results"):
            return f"Could not find coordinates for {location}."

        lat = geocode_data["results"][0]["latitude"]
        lon = geocode_data["results"][0]["longitude"]

        # --- Get Weather for the coordinates ---
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        temperature = weather_data["current_weather"]["temperature"]
        unit = "°C"

        return f"{temperature}{unit}"

    except Exception as e:
        return f"Error fetching weather: {e}"
```

---

## Understanding the Components

### Function Declaration (`weather_function`)

- **`name`**: The identifier the model will use to call this function
- **`description`**: Tells the model what this function does (crucial for the model to decide when to use it)
- **`parameters`**: Defines what inputs the function expects
  - **`type`**: Specifies this is an object with properties
  - **`properties`**: Defines each parameter (in this case, just `location`)
  - **`required`**: Lists which parameters are mandatory

### Python Function (`get_current_temperature`)

This is the actual implementation that:
1. Takes a location string as input
2. Calls the Open-Meteo geocoding API to get latitude/longitude
3. Calls the Open-Meteo weather API with those coordinates
4. Extracts and returns the current temperature

---

> **📝 Note**  
> We've defined the tool, but we haven't yet told the model about it or handled the function calling workflow. That will come in the next steps.

---

**Next Steps:** You'll integrate this tool into your model configuration and implement the logic to handle function calls from the model.