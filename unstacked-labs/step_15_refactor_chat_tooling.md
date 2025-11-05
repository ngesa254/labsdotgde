# Refactor for Chat and Tooling

## Why Refactor?

Our current `call_model` function uses a simple, one-shot `generate_content` call. This is great for single questions but isn't ideal for a multi-turn conversation, especially one that involves back-and-forth for tooling.

A better practice is to use a **chat session**, which maintains the context of the conversation. We will now refactor our code to use a chat session, which is necessary to correctly implement tooling.

---

## Refactoring Instructions

### 1. Delete the Existing `call_model` Function

Delete the existing `call_model` function. We will replace it with a more advanced version.

### 2. Add the New `call_model` Function

In its place, add the new `call_model` function from the code block below. This new function contains the logic to handle the tool-calling loop we discussed earlier. 

Notice it has several `TODO` comments that we will complete in the next steps:

```python
# --- Call the Model ---
def call_model(prompt: str, model_name: str) -> str:
    """
    This function interacts with a large language model (LLM) to generate text based on a given prompt.
    It maintains a chat session and handles function calls from the model to external tools.
    """
    try:
        # TODO: Get the existing chat session or create a new one.

        message_content = prompt

        # Start the tool-calling loop
        while True:
            # TODO: Send the message to the model.

            # Check if the model wants to call a tool
            has_tool_calls = False
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    has_tool_calls = True
                    function_call = part.function_call
                    logging.info(f"Function to call: {function_call.name}")
                    logging.info(f"Arguments: {function_call.args}")

                    # TODO: Call the appropriate function if the model requests it.

            # If no tool call was made, break the loop
            if not has_tool_calls:
                break

        # TODO: Return the model's final text response.

    except Exception as e:
        return f"Error: {e}"
```

### 3. Add the `get_chat` Helper Function

Now, let's add a helper function to manage the chat session. **Above** the new `call_model` function, find the comment:

```python
# TODO: Add the get_chat function here in Task 15.
```

Replace this comment with the `get_chat` function. This function will create a new chat session with our system instructions and tool definitions, or retrieve the existing one. This is a good practice for organizing code:

```python
def get_chat(model_name: str):
    if f"chat-{model_name}" not in st.session_state:

        # TODO: Define the tools configuration for the model

        # TODO: Define the generate_content configuration, including tools

        # TODO: Create a new chat session

        st.session_state[f"chat-{model_name}"] = chat
    return st.session_state[f"chat-{model_name}"]
```

---

## Understanding the Refactored Structure

### The `get_chat` Function

This function manages the chat session lifecycle:
- **Checks if a chat session exists** for the current model in Streamlit's session state
- **Creates a new chat session** if one doesn't exist (with TODOs to be filled in)
- **Returns the chat session** to be used by `call_model`

### The New `call_model` Function

This function now includes:
- **Chat session management**: Gets or creates a chat session
- **Tool-calling loop**: A `while True` loop that handles the back-and-forth with the model
- **Function call detection**: Checks if the model wants to call a tool
- **Tool execution logic**: (To be implemented) Calls the actual Python function
- **Response handling**: Returns the final text response after all tool calls are complete

### The Tool-Calling Loop

The loop works as follows:
1. Send a message to the model
2. Check if the model's response contains a function call
3. If yes, execute the function and send the result back to the model
4. If no, break the loop and return the final response

---

## What We've Set Up

You have now set up the scaffolding for our advanced, tool-enabled chat logic!

The structure is in place, but we still have several `TODO` items to complete:
- Define the tools configuration
- Define the generate_content configuration with tools
- Create the chat session
- Send messages to the model
- Execute function calls
- Return the final response

---

> **📝 Note**  
> This refactoring is essential for implementing function calling. The chat session maintains conversation context and enables the multi-turn interaction required for the model to request tool calls and receive results.

---

**Next Steps:** In the following steps, you'll fill in the `TODO` comments to complete the chat session setup and tool-calling implementation.