# Prepare Data and Call the Model

## Overview

You will now prepare the content to send to the model, and make a call to the Gemini model.

## Step-by-Step Instructions

### 1. Locate the Call Model Function

Find the `--- Call the Model ---` section where the `call_model` function is defined.

### 2. Define Contents

Under `# TODO: Prepare the content for the model`, define the input content that will be sent to the model. For a basic prompt, this will be the user's input message.

```python
        contents = [prompt]
```

### 3. Define the Response

Paste this code under `# TODO: Define response`:

```python
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
        )
```

### 4. Return the Response

Uncomment the following line:

```python
        return response.text
```

### 5. Examine the Function Call

Examine the line where the `call_model` function is being called, towards the bottom of the file in the `with` block. If you don't understand what is happening here, highlight the line and ask Gemini Code Assist to explain.

---

## A More Explicit Way to Define `contents`

The above way of defining `contents` works because the SDK is smart enough to understand that a list containing strings represents user text input. It automatically formats it correctly for the model API.

However, the more explicit and fundamental way to structure input involves using `types.Part` and `types.Content` objects, like this:

```python
user_message_parts = [types.Part.from_text(text=prompt)]
contents = [
    types.Content(
        role="user", # Indicates the content is from the user
        parts=user_message_parts, # A list, allowing multiple types of content
    ),
]
```

### Why Use This More Verbose Method?

The explicit `types.Part` and `types.Content` structure becomes necessary when your input is more complex than just simple text. The most common scenario is when you need to send **multi-modal prompts**, such as combining text with an image. 

Read more about `contents` and `parts` in [this Vertex AI doc](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini).

---

## Updated `call_model` Function

At this point, the `call_model` function should look like this:

```python
def call_model(prompt: str, model_name: str) -> str:
    """
    This function interacts with a large language model (LLM) to generate text based on a given prompt and system instructions. 
    It will be replaced in a later step with a more advanced version that handles tooling.
    """
    try:

        contents = [prompt]

        # TODO: Define generate_content configuration (needed later for system instructions and parameters)

        response = client.models.generate_content(
            model=model_name,
            contents=contents,
        )
        logging.info(f"[call_model_response] LLM Response: \"{response.text}\"")

        return response.text
    except Exception as e:
        return f"Error: {e}"
```

---

> **✅ Checkpoint**  
> After completing this step, your application will be able to send prompts to the Gemini model and receive responses. The basic chat functionality should now work!

---

**Next Steps:** You can now test your chatbot by sending messages and receiving AI-generated responses. In the following steps, you'll enhance the application with system instructions and parameters.