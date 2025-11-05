# Create Starter Files for Wanderbot

## Step-by-Step Instructions

### 1. Create and Open the Application File

Create and open a new `app.py` file for the application. Run the following code in the terminal:

```shell
cloudshell edit app.py
```

The `cloudshell edit` command will open the `app.py` file in the editor above the terminal.

### 2. Add the Application Starter Code

Paste the following app starter code into `app.py`:

```python
import streamlit as st
from google import genai
from google.genai import types
import requests
import logging

# --- Defining variables and parameters  ---
REGION = "global"
PROJECT_ID = None # TO DO: Insert Project ID
GEMINI_MODEL_NAME = "gemini-2.5-flash"

temperature = .2
top_p = 0.95

system_instructions = None

# --- Tooling ---
# TODO: Define the weather tool function declaration

# TODO: Define the get_current_temperature function


# --- Initialize the Vertex AI Client ---
try:
    # TODO: Initialize the Vertex AI client

    print(f"VertexAI Client initialized successfully with model {GEMINI_MODEL_NAME}")
except Exception as e:
    st.error(f"Error initializing VertexAI client: {e}")
    st.stop()


# TODO: Add the get_chat function here in Task 15.


# --- Call the Model ---
def call_model(prompt: str, model_name: str) -> str:
    """
    This function interacts with a large language model (LLM) to generate text based on a given prompt and system instructions. 
    It will be replaced in a later step with a more advanced version that handles tooling.
    """
    try:

        # TODO: Prepare the content for the model

        # TODO: Define generate_content configuration (needed for system instructions and parameters)

        # TODO: Define response

        logging.info(f"[call_model_response] LLM Response: \"{response.text}\"")
        # TODO: Uncomment the below "return response.text" line
        # return response.text

    except Exception as e:
        return f"Error: {e}"


# --- Presentation Tier (Streamlit) ---
# Set the title of the Streamlit application
st.title("Travel Chat Bot")

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    # Initialize the chat history with a welcome message
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Display the chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Get user input
if prompt := st.chat_input():
    # Add the user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user's message
    st.chat_message("user").write(prompt)

    # Show a spinner while waiting for the model's response
    with st.spinner("Thinking..."):
        # Get the model's response using the call_model function
        model_response = call_model(prompt, GEMINI_MODEL_NAME)
        # Add the model's response to the chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": model_response}
        )
        # Display the model's response
        st.chat_message("assistant").write(model_response)
```

### 3. Create and Open the Requirements File

Create and open a new `requirements.txt` file for the application code. Run the following code in the terminal:

```shell
cloudshell edit requirements.txt
```

The `cloudshell edit` command will open the `requirements.txt` file in the editor above the terminal.

### 4. Add the Dependencies

Paste the following app starter code into `requirements.txt`:

```txt
google-genai
streamlit
requests
```

### 5. Install the Required Dependencies

Install the required Python dependencies for this project. Run the following code in the terminal:

```shell
uv pip install -r requirements.txt
```

---

> **📝 Note**  
> The starter code contains several `TODO` comments. These will be completed in subsequent steps as you build out the travel assistant chatbot functionality.

---

**Next Steps:** With your starter files created and dependencies installed, you're ready to begin implementing the chatbot features.