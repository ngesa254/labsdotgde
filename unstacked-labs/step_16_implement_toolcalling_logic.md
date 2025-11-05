# Implement the Tool-Calling Logic

## Overview

Now, let's fill in the TODOs to make our tool-calling logic fully functional.

---

## Implement `get_chat`

### 1. Define the Tools Configuration

In the `get_chat` function under `# TODO: Define the tools configuration...` comment, define the `tools` object by creating a `types.Tool` instance from our `weather_function` declaration:

```python
        tools = types.Tool(function_declarations=[weather_function])
```

### 2. Define the Generate Content Configuration

Under `# TODO: Define the generate_content configuration...`, define `generate_content_config`, making sure to pass the `tools` object to the model. This is how the model learns about the tools it can use:

```python
        generate_content_config = types.GenerateContentConfig(
            system_instruction=[types.Part.from_text(text=system_instructions)],
            tools=[tools] # Pass the tool definition here
        )
```

### 3. Create a New Chat Session

Under `# TODO: Create a new chat session`, create the `chat` object using `client.chats.create()`, passing in our model name and config:

```python
        chat = client.chats.create(
            model=model_name,
            config=generate_content_config,
        )
```

---

## Implement `call_model`

### 1. Get the Chat Session

Under `# TODO: Get the existing chat session...` in the `call_model` function, call our new `get_chat` helper function:

```python
        chat = get_chat(model_name)
```

### 2. Send the Message to the Model

Next, find `# TODO: Send the message to the model.` Send the user's message using the `chat.send_message()` method:

```python
            response = chat.send_message(message_content)
```

### 3. Call the Appropriate Function

Find `# TODO: Call the appropriate function....` This is where we check which function the model wants and execute it:

```python
                    if function_call.name == "get_current_temperature":
                      result = get_current_temperature(**function_call.args)
                    function_response_part = types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": result},
                    )
                    message_content = [function_response_part]
```

### 4. Return the Final Response

Lastly, find `# TODO: Return the model's final text response` and add the return statement:

```python
        return response.text
```

---

## Updated `get_chat` Function

The updated `get_chat` function should now look like this:

```python
def get_chat(model_name: str):
    if f"chat-{model_name}" not in st.session_state:
        #Tools
        tools = types.Tool(function_declarations=[weather_function])

        # Initialize a configuration object
        generate_content_config = types.GenerateContentConfig(
            system_instruction=[types.Part.from_text(text=system_instructions)],
            tools=[tools]
        )
        chat = client.chats.create(
            model=model_name,
            config=generate_content_config,
        )
        st.session_state[f"chat-{model_name}"] = chat
    return st.session_state[f"chat-{model_name}"]
```

---

## Updated `call_model` Function

The updated `call_model` function should now look like this:

```python
def call_model(prompt: str, model_name: str) -> str:
    try:
        chat = get_chat(model_name)
        message_content = prompt
        
        while True:
            response = chat.send_message(message_content)
            has_tool_calls = False
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    has_tool_calls = True
                    function_call = part.function_call
                    logging.info(f"Function to call: {function_call.name}")
                    logging.info(f"Arguments: {function_call.args}")
                    if function_call.name == "get_current_temperature":
                        result = get_current_temperature(**function_call.args)
                        function_response_part = types.Part.from_function_response(
                            name=function_call.name,
                            response={"result": result},
                        )
                        message_content = [function_response_part]
                elif part.text:
                    logging.info("No function call found in the response.")
                    logging.info(response.text)

            if not has_tool_calls:
                break

        return response.text

    except Exception as e:
        return f"Error: {e}"
```

---

## Understanding the Implementation

### The Tool-Calling Flow

1. **Tool Registration**: The `get_chat` function creates a `types.Tool` object containing our weather function declaration and passes it to the model configuration.

2. **Chat Session Creation**: A new chat session is created with both system instructions and tool definitions.

3. **Message Handling**: When a user sends a message, `call_model` sends it to the chat session.

4. **Function Call Detection**: The model analyzes the message and decides if it needs to call a tool. If so, it returns a `function_call` object instead of text.

5. **Function Execution**: Our code detects the function call, executes the actual Python function (`get_current_temperature`), and packages the result.

6. **Result Return**: The function result is sent back to the model as a `function_response_part`.

7. **Final Response**: The model receives the function result and generates a natural language response incorporating that data.

8. **Loop Termination**: The loop continues until the model no longer requests any function calls.

---

> **✅ Checkpoint**  
> After completing this step, your chatbot will be able to call external functions to fetch real-time data like weather information!

---

**Next Steps:** Test your application with weather-related queries to see the tool-calling functionality in action.