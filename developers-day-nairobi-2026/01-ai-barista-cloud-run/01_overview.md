## 1. What you are building

A customer asks for a drink in Streamlit. The ADK runner sends the question, barista instructions, and tool definition to Gemini. Gemini can request the tool. ADK executes the Python function and returns the result to Gemini, which uses it to generate a reply. The Streamlit sidebar has its own menu read path. A populated sidebar proves the UI can read the menu. A correct recommendation tests the chat path.

| Component | Role |
|---|---|
| Streamlit | Browser interface and per-session chat display |
| Google ADK | Runs the agent loop and executes tool requests |
| Gemini 3.5 Flash | Interprets requests and writes answers |
| Cloud Run | Hosts the Python application and serves its HTTPS URL |
| Local JSON | Supplies all eight menu records when the base tool runs |
| Firestore, optional | Stores menu documents and returns up to three semantic matches to the agent |

In the base lab, retrieval means loading the whole file at runtime. The tool call can be skipped for a greeting. A menu lookup still returns all eight records. In the optional extension, the tool embeds a query and retrieves candidates using cosine distance. Similarity ranks candidates. Tags, prices, and allergen fields supply factual constraints. Chat history lives in memory and can reset on refresh or a new connection.

### Architecture and flow diagrams

See the [architecture guide](architecture.md) for the Cloud Run container layout, a numbered chat sequence, the optional Firestore retrieval flow, and the source deployment pipeline.

---

[Lab overview](README.md) · [Next](02_project_setup.md)
