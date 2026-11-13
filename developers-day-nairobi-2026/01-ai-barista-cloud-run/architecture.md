# Barista architecture and request flow

[Open the HTML architecture guide](BARISTA_CLOUD_RUN_ARCHITECTURE.html) for a browser presentation with navigation, expandable diagrams, and print support.

These diagrams follow the supplied architecture and sequence references and the workshop's Python code. The base application runs Streamlit, the ADK runner, the agent definition, and the menu tool in the same Cloud Run container. Gemini inference is an external API call from that container through Vertex AI.

## Base architecture: Gemini and local menu retrieval

```mermaid
flowchart LR
    browser["Customer browser"]
    subgraph cloud["Google Cloud project"]
        subgraph run["Cloud Run container"]
            ui["Streamlit web interface · app.py"]
            subgraph runtime["Agent runtime"]
                runner["ADK InMemoryRunner"]
                agent["LlmAgent · barista_agent"]
                tool["Python tool · get_menu()"]
            end
            menu[("Local menu.json · 8 items")]
            ui -->|"Chat message"| runner
            runner -->|"Run agent with session history"| agent
            agent -.->|"Tool request handled by ADK"| tool
            tool -->|"Read menu"| menu
            menu -->|"Menu records"| tool
            tool -.->|"Tool result"| runner
            runner -->|"Answer for display"| ui
            ui -->|"Separate sidebar read"| menu
        end
        gemini["Gemini · Vertex AI endpoint"]
        runner -->|"Message, instructions, tool definition / result"| gemini
        gemini -->|"Tool request or answer"| runner
    end
    browser -->|"HTTPS · customer query"| ui
    ui -->|"Menu and chat response"| browser
    style cloud fill:#eef5ff,stroke:#4285f4,stroke-width:2px,color:#17365d
    style run fill:#f8fafc,stroke:#64748b,color:#0f172a
    style runtime fill:#dbeafe,stroke:#3b82f6,color:#0f172a
```

`agent.py` defines the agent and menu tool. `app.py` creates the runner, manages the Streamlit session, reads the sidebar menu, and displays responses. ADK executes the Python function when Gemini requests a tool call. The diagram separates these responsibilities; they run inside one Python application.

The runtime service account provides the application's cloud identity. Cloud Build and Artifact Registry support deployment, as shown below.

## Chat sequence: menu question

```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant UI as Streamlit
    participant ADK as ADK runner
    participant Gemini as Gemini via Vertex AI
    participant Tool as Python get_menu()
    participant Menu as Local menu.json

    Customer->>UI: Recommend something strong and warm
    UI->>ADK: Submit message with the current session ID
    ADK->>Gemini: Send message, history, instructions, and tool definition
    Gemini-->>ADK: Request get_menu()
    ADK->>Tool: Execute get_menu()
    Tool->>Menu: Read packaged JSON file
    Menu-->>Tool: Eight menu records
    Tool-->>ADK: Return menu records as JSON
    ADK->>Gemini: Send tool result
    Gemini-->>ADK: Generate recommendation using menu facts
    ADK-->>UI: Return response events
    UI-->>Customer: Display the answer and save chat history
```

This sequence illustrates a menu lookup. A greeting can produce a response without a tool call. ADK handles the model/tool loop; the model requests the function and the runner executes it. The sidebar loads menu data independently, so a visible sidebar alone does not verify the chat path.

The base tool reads the entire menu. Embeddings and nearest-neighbor search are introduced in the optional extension.

## Optional Firestore retrieval flow

```mermaid
flowchart TD
    subgraph seed["Preparation · Cloud Shell"]
        source["menu.json or Matcha demo item"]
        script["seed.py"]
        seedembed["Embed item name and description · 768 dimensions"]
        source --> script --> seedembed
    end
    model["Vertex AI embedding endpoint · us-central1"]
    seedembed -->|"Embedding request"| model
    model -->|"Item vector"| seedembed
    db[("Named Firestore database · menu collection and vector index")]
    seedembed -->|"Write item fields and embedding"| db

    subgraph runtime["Cloud Run · vector service"]
        runner["ADK runner"]
        tool["get_menu(query) → search_menu(query)"]
        queryembed["Embed customer query · same model and 768 dimensions"]
        nearest["Cosine nearest-neighbor query · limit 3"]
        result["Return menu fields without stored embeddings"]
        sidebar["Streamlit sidebar · list_menu()"]
        runner -->|"Execute requested tool"| tool
        tool --> queryembed
        queryembed --> nearest
        nearest --> result
        result -->|"Tool result"| runner
    end
    queryembed -->|"Embedding request"| model
    model -->|"Query vector"| queryembed
    nearest -->|"Search embedding index"| db
    db -->|"Up to 3 matching documents"| nearest
    sidebar -->|"List all menu documents"| db
    db -->|"Menu records for display"| sidebar
    chat["Gemini chat endpoint · global"]
    runner -->|"Message or tool result"| chat
    chat -->|"Tool request or grounded answer"| runner
```

Seed writes and runtime queries use the same database, embedding model, and vector length. Menu tags, prices, and allergen fields accompany retrieved candidates and support factual checks. Similarity ranks candidates; a top-three result is not an exhaustive availability check.

The Matcha demo writes a new document and embedding to Firestore. Subsequent tool calls can retrieve it without rebuilding the Cloud Run service. Refresh the page to reload the sidebar. See [step 8](08_firestore_vector_search.md) for the seed, index, and verification commands.

## Source deployment flow

```mermaid
flowchart LR
    shell["Cloud Shell · source files"]
    deploy["gcloud run deploy --source ."]
    build["Cloud Build · Python buildpacks"]
    registry[("Artifact Registry · container image")]
    run["Cloud Run revision · Streamlit application"]
    url["Service HTTPS URL"]
    identity["Dedicated runtime service account"]
    vertex["Vertex AI · Gemini and optional embeddings"]
    firestore[("Firestore · optional menu database")]

    shell --> deploy --> build
    build -->|"Push built image"| registry
    registry -->|"Deploy image"| run
    run --> url
    identity -.->|"Attached runtime identity"| run
    run -->|"Vertex AI permission"| vertex
    run -->|"Firestore read permission for extension"| firestore
```

The deployer, build identity, and runtime service account have separate responsibilities. [Step 6](06_deploy_cloud_run.md) covers the deployment and runtime role; [step 8](08_firestore_vector_search.md) adds Firestore read access. Deployment creates the URL, while the browser/chat checks in [step 7](07_test_barista.md) confirm application behavior.

[Lab overview](README.md) · [Step 1](01_overview.md) · [Event overview](../README.md)
