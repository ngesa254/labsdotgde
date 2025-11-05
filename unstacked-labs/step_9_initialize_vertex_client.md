# Initialize the Vertex AI Client

## Explore Available Models in Vertex AI

Google Cloud's Vertex AI platform provides access to a variety of generative AI models. Before you integrate one, you can explore the available options in the Google Cloud Console.

### Browse the Model Garden

1. From the Google Cloud Console, navigate to **Model Garden**. You can do this by searching for "Model Garden" in the search bar at the top of the screen and selecting **Vertex AI**.

2. Browse the available models. You can filter by things like:
   - Modalities
   - Task types
   - Features

For the purposes of this lab, you will be using the **Gemini 2.5 Flash** model, which is a good choice for building responsive chat applications due to its speed.

---

## Initialize the Vertex AI Client

Now you will modify the `--- Initialize the Vertex AI Client ---` section in `app.py` to initialize the Vertex AI client. This client object will be used to send prompts to the model.

### Step-by-Step Instructions

#### 1. Open the Application File

Open `app.py` in the Cloud Shell Editor.

#### 2. Set Your Project ID

In `app.py`, find the line:

```python
PROJECT_ID = None
```

Replace `None` with your Google Cloud Project ID in quotes.

**Example:**

```python
PROJECT_ID = "google-cloud-labs"
```

**If you can't remember your project ID**, you can list all your project IDs with:

```shell
gcloud projects list | awk '/PROJECT_ID/{print $2}'
```

#### 3. Define the Client

Inside the `try` block, initialize the Vertex AI client:

```python
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=REGION,
    )
```

---

## Updated Vertex AI Client Initialization

At this point, the **Initialize the Vertex AI Client** section would look like this:

```python
# --- Initialize the Vertex AI Client ---
try:
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=REGION,
    )
    print(f"VertexAI Client initialized successfully with model {GEMINI_MODEL_NAME}")
except Exception as e:
    st.error(f"Error initializing VertexAI client: {e}")
    st.stop()
```

---

> **✅ Checkpoint**  
> After completing this step, your Vertex AI client will be properly initialized and ready to communicate with the Gemini model.

---

**Next Steps:** With the client initialized, you'll be able to start sending prompts to the Gemini model and receiving responses.