# Refine the Model's Output with Parameters

## Overview

Great work! Your travel assistant can now use tools to fetch live, external data, making it significantly more powerful.

Now that we've enhanced what our model can do, let's fine-tune **how** it responds. Model parameters allow you to control the style and randomness of the LLM's generated text. By adjusting these settings, you can make the bot's output more focused and deterministic or more creative and varied.

---

## Understanding Model Parameters

For this lab, we will be focusing on `temperature` and `top_p`. 

> **📚 Reference**  
> Refer to the [`GenerateContentConfig`](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini) in our API reference for a complete list of configurable parameters and their descriptions.

### `temperature`

Controls the randomness of the output. 

- **Lower value (closer to 0)**: Makes the output more deterministic and focused
- **Higher value (closer to 2)**: Increases randomness and creativity

For a Q&A or assistant bot, a lower temperature is usually preferred for more consistent and factual responses.

### `top_p`

The maximum cumulative probability of tokens to consider when sampling. Tokens are sorted based on their assigned probabilities so that only the most likely tokens are considered. The model considers the most likely tokens whose probabilities sum up to the `top_p` value. 

- **Lower value**: Restricts the token choices, resulting in less varied output
- **Higher value**: Allows more token choices, resulting in more varied output

---

## Call Parameters

### 1. Locate the Parameter Variables

Find the variables `temperature` and `top_p`, defined at the top of `app.py`. Notice that they haven't yet been called anywhere.

```python
temperature = .2
top_p = 0.95
```

### 2. Add Parameters to GenerateContentConfig

Add `temperature` and `top_p` to the parameters defined within `GenerateContentConfig` in the `get_chat` function:

```python
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            top_p=top_p,
            system_instruction=[types.Part.from_text(text=system_instructions)],
            tools=[tools] # Pass the tool definition here
        )
```

---

## Updated `get_chat` Function

The `get_chat` function now looks like this:

```python
def get_chat(model_name: str):
    if f"chat-{model_name}" not in st.session_state:
        #Tools
        tools = types.Tool(function_declarations=[weather_function])

        # Initialize a configuration object
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            top_p=top_p,
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

## Understanding the Parameter Values

With the current settings:

- **`temperature = 0.2`**: This low temperature makes the model's responses more focused and deterministic, which is ideal for a travel assistant where accuracy and consistency are important.

- **`top_p = 0.95`**: This high value allows the model to consider a wide range of likely tokens, providing some variety in responses while still maintaining quality.

---

## Experimenting with Parameters

You can experiment with different parameter values to see how they affect the model's behavior:

### For More Deterministic Responses
```python
temperature = 0.1
top_p = 0.8
```

### For More Creative Responses
```python
temperature = 0.8
top_p = 0.95
```

### For Highly Creative/Random Responses
```python
temperature = 1.5
top_p = 1.0
```

> **⚠️ Note**  
> After changing parameter values, you'll need to restart the application and potentially clear your browser's session state (refresh the page) to see the effects, as the chat session is cached in Streamlit's session state.

---

> **✅ Checkpoint**  
> After completing this step, your chatbot will have fine-tuned response generation, balancing consistency with appropriate variation for a professional travel assistant experience.

---

**Next Steps:** Test your application with the new parameters to observe how they affect the quality and style of responses.