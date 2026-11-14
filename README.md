# LabsDotGDE™ — Google AI, Agentic Systems, MCP & Cloud Run Workshops

**[Launch DECODE labs — From Code to Cash](https://ngesa254.github.io/labsdotgde/codelabs/index.html)**

Build an M-Pesa MCP server and a Google ADK payment agent with guided, step-by-step labs.

[Start Lab 1: M-Pesa MCP server](https://ngesa254.github.io/labsdotgde/codelabs/codelabs/decode-mpesa-mcp/) · [Start Lab 2: ADK agent](https://ngesa254.github.io/labsdotgde/codelabs/codelabs/decode-adk-payment-agent/)

**[View the rendered AI Barista architecture guide](https://ngesa254.github.io/labsdotgde/)**

<p align="center">
  <img src="https://img.shields.io/badge/Google%20ADK-Agent%20Development%20Kit-EA4335?style=for-the-badge&logo=google&logoColor=white" alt="Google ADK">
  <img src="https://img.shields.io/badge/Gemini%202.5-Live%20API%20%26%20Vertex%20AI-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Gemini & Vertex AI">
  <img src="https://img.shields.io/badge/MCP-Model%20Context%20Protocol-00ADD8?style=for-the-badge" alt="MCP">
  <img src="https://img.shields.io/badge/Cloud%20Run-Serverless%20Containers-34A853?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Cloud Run">
  <img src="https://img.shields.io/badge/Apigee-API%20Management-FF6D00?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Apigee">
  <img src="https://img.shields.io/badge/Keras%203%20%26%20Gemma%202-Open%20Models-D00000?style=for-the-badge&logo=keras&logoColor=white" alt="Keras & Gemma">
</p>

Welcome to **LabsDotGDE™** (`labsdotgde`) — a comprehensive, production-inspired collection of hands-on Developer Relations (DevRel) codelabs, architectural blueprints, reference implementations, and interactive notebooks.

This monorepo powers developer workshops across Africa and globally—spanning **DevFest**, **PyCON Africa**, **Deep Learning Indaba** **Build With AI (Nairobi, Kisumu, Cape Town, Kigali, Accra, JHB,)**, **Safaricom DECODE**, **Open Digital Health Summit (OSDH)**, **AMLD Africa**, and **GDSC / Campus Connect** bootcamps.

---

## Google for Developers Day: Nairobi — November 13, 2026

The [Nairobi workshop folder](developers-day-nairobi-2026/README.md) contains the event details and a [step-by-step AI Barista lab](developers-day-nairobi-2026/01-ai-barista-cloud-run/README.md) using Google ADK, Streamlit, Gemini, and Cloud Run, with an optional Firestore vector search extension.

**Event:** 8:00 AM–5:00 PM EAT (GMT+3), Sarit Expo Center, Westlands, Nairobi.

## Table of Contents

1. [Repository Overview & Core Pillars](#-repository-overview--core-pillars)
2. [System Architecture & Learning Progression](#-system-architecture--learning-progression)
3. [Repository Directory Map](#-repository-directory-map)
4. [Track 1: `decode/` — Agentic Fintech Systems with M-Pesa Daraja, MCP, Apigee & ADK](#-track-1-decode--agentic-fintech-systems-with-m-pesa-daraja-mcp-apigee--adk)
5. [Track 2: `BuildWithAI/` — Google Agent Development Kit (ADK), MCP & Gemini Live API](#-track-2-buildwithai--google-agent-development-kit-adk-mcp--gemini-live-api)
6. [Track 3: `unstacked-labs/` — Building GenAI Solutions with Vertex AI SDK ("WanderBot")](#-track-3-unstacked-labs--building-genai-solutions-with-vertex-ai-sdk-wanderbot)
7. [Track 4: Regional Build With AI Chapters (Nairobi, Kisumu, Cape Town)](#-track-4-regional-build-with-ai-chapters-nairobi-kisumu-cape-town)
8. [Track 5: `OSDH/` — Open Digital Health Summit (FHIR Prompting & Gemma 2 with Keras 3)](#-track-5-osdh--open-digital-health-summit-fhir-prompting--gemma-2-with-keras-3)
9. [Track 6: Community Bootcamps & Polyglot Starters (`devfestnairobi24`, `gdsc_bootcamp`, `capetown`)](#-track-6-community-bootcamps--polyglot-starters)
10. [Hosted Google Colab Notebooks & Global Workshops](#-hosted-google-colab-notebooks--global-workshops)
11. [Prerequisites & Environment Setup](#-prerequisites--environment-setup)
12. [Cloud Deployment & Cost Cleanup](#-cloud-deployment--cost-cleanup)

---

## Repository Overview & Core Pillars

Modern AI engineering has evolved from single-turn prompt completions to **stateful, tool-augmented, multi-agent systems** governed by enterprise API gateways and deployed on serverless cloud infrastructure. This repository is structured around five core technical pillars:

1. **Google Agent Development Kit (ADK):** Designing single-agent and hierarchical multi-agent systems with deterministic tool routing, session state management, Dev UI tracing, and one-command Cloud Run deployments (`adk deploy cloud_run --with_ui`).
2. **Model Context Protocol (MCP):** Building local (`stdio`) and remote (`SSE` / HTTP) MCP servers using **FastMCP**, securing them on **Google Cloud Run** with IAM authentication, governing them behind **Apigee API Management**, and consuming them from **Gemini CLI** and **ADK Agents**.
3. **Multimodal Real-Time Streaming (Gemini Live API):** Low-latency bidirectional text, native audio (`.wav`), tool execution, and video frame understanding powered by **Gemini 2.5 Flash**.
4. **RAG & ReAct Agentic Workflows (LlamaIndex + Vertex AI / Gemini API):** Scraping live conference schedules (DevFest Lagos & DevFest Nairobi), indexing into vector stores with HuggingFace embeddings (`BAAI/bge-small-en-v1.5`), and orchestrating **ReAct** reasoning loops.
5. **Domain-Specific & Open-Weight AI:** Healthcare interoperability (**HL7 FHIR** & SMART Guidelines) using structured Chain-of-Thought prompting, and fine-tuning / running **Gemma 2** open models on **Keras 3** (`keras_nlp`).

---

##  System Architecture & Learning Progression

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                        LABSDOTGDE LEARNING & ARCHITECTURE PATH                     │
└────────────────────────────────────────────────────────────────────────────────────┘

  [Stage 1: Foundations]              [Stage 2: RAG & ReAct]
  ├─ Prompt Engineering (R.O.D.E.S)   ├─ LlamaIndex + HuggingFace Embeddings
  ├─ Polyglot SDKs (Py / KT / JS)     ├─ Web Scrapers & QueryEngineTools
  ├─ Vertex AI Studio & Streamlit     └─ Autonomous ReAct Agents
  └─ Gemma 2 + Keras 3 Quickstarts
                 │                                      │
                 ▼                                      ▼
  [Stage 3: Google ADK & Live API]    [Stage 4: Enterprise MCP & Fintech (DECODE)]
  ├─ ADK Local Dev UI & Tooling       ├─ Gemini CLI / ADK Agent Client
  ├─ Multi-Agent Session State        ├─ IAM Service-to-Service Auth
  ├─ Gemini 2.5 Live Audio & Video    ├─ Apigee API Gateway & Policy Layer
  └─ Cloud Run Serverless Deploy      └─ Cloud Run FastMCP Server ──► Safaricom Daraja
```

---

## Repository Directory Map

```text
labsdotgde/
├── developers-day-nairobi-2026/                 # Google for Developers Day: Nairobi (November 13, 2026)
│   ├── README.md                                # Event details and workshop entry point
│   └── 01-ai-barista-cloud-run/                 # ADK + Streamlit + Cloud Run; optional Firestore RAG
│
├── decode/                                      # Safaricom DECODE Fintech Agentic Workshop
│   ├── README.md                                # End-to-end "From Code to Cash" workshop guide
│   ├── artifacts/                               # Architecture & lab overview diagrams
│   ├── 01-mpesa-daraja-mcp-server-with-apigee/  # Lab 1: FastMCP + Daraja STK Push + Cloud Run + Apigee
│   └── 02-google-adk-agent-for-mpesa-daraja-mcp/# Lab 2: ADK Agent consuming remote M-Pesa MCP tools
│
├── BuildWithAI/                                 # Flagship ADK, MCP & Gemini Live API Curriculum
│   ├── README.md                                # Workshop curriculum & hands-on challenge guide
│   ├── gcp_cost_clean_up.md                     # GCP billing & resource teardown instructions
│   ├── Lessons/
│   │   ├── adk-intro/                           # Lesson 1: Local setup, first tool, multi-tool, Cloud Run
│   │   ├── mcp-fundermentals/                   # Lesson 2: MCP architecture, servers, clients, prompts
│   │   ├── adk-mcp/                             # Lesson 3: Extending ADK agents with MCP
│   │   ├── mcp-on-cloudrun-01/                  # Codelab: Deploying secure MCP servers on Cloud Run
│   │   ├── adk-withmcp-on-cloudrun-02/          # Codelab: Connecting ADK agents on Cloud Run to MCP
│   │   └── adk-gemini-live/                     # Lesson 4: Gemini 2.5 Live API, audio, tools & video
│   └── Samples/
│       ├── adk_into/                            # Working ADK demo agent (Weather + City Facts)
│       ├── multi-agents/                        # Multi-tool ADK agent (dice, coin, random generator)
│       ├── adk-gemini-live/                     # Live API text & native audio streaming scripts
│       ├── adk_mcp/                             # ADK + MCP sample notes
│       └── L4/ L5/ L6/ L7/ L9/                  # Progressive ArXiv Research MCP Server & Chatbot labs
│
├── unstacked-labs/                              # 20-Step Vertex AI SDK + Streamlit Codelab ("WanderBot")
│   ├── README.md                                # Lab overview & learning objectives
│   ├── step_2_project_setup.md ... step_20_Congratulations!.md
│   └── troubleshooting.md                       # Common Vertex AI & Cloud Shell fixes
│
├── BuildWithAIKisumu/                           # Build With AI Kisumu ("DevFest Dala")
│   ├── check_list.md                            # 725-line Production Cloud Run Deployment Checklist
│   ├── lesson_1_prompts/                        # R.O.D.E.S Prompt Engineering lab
│   └── lesson_2_agents/                         # DevFest ReAct Agent & Scraper (Gemini API + LlamaIndex)
│
├── buildWithAINairobi/                          # Build With AI Nairobi
│   ├── lesson_1_prompt_engineering/             # Prompt engineering fundamentals
│   └── lesson_3_agents/                         # DevFest ReAct Agent & Scraper
│
├── BwAICapeTown/                                # Build With AI Cape Town
│   ├── lesson_1_prompt_engineering/             # Prompt engineering labs (0 & 1) + prompt templates
│   └── lesson_3_agents/                         # Vertex AI + LlamaIndex DevFest ReAct Agent
│
├── OSDH/                                        # Open Digital Health Summit (Healthcare AI Track)
│   ├── lesson_1_prompt_engineering/             # Prompting for HL7 FHIR & African rural clinics
│   ├── lesson-2_advanced_prompting/             # Advanced Prompting Techniques Jupyter Notebook
│   └── lesson_3_gemma_with_keras/               # Keras 3 + Gemma 2 Quickstart & Chat Notebooks
│
├── devfestnairobi24/                            # DevFest Nairobi 2024 Multilingual Assistant ("Jess")
│   ├── multilingual_assistant.py                # Python SDK implementation (EN/SW/FR/PT routing)
│   ├── multilingual_assistant.kt                # Android Kotlin SDK implementation
│   └── multilingual_assistant.txt               # System instruction & few-shot prompt specification
│
├── gdsc_bootcamp/                               # GDSC Bootcamp Starter
│   └── gdsc_gemini.py                           # Python Gemini SDK + safety settings starter (CUEA)
│
├── capetown/                                    # Node.js Starter
│   └── gemini_starts.js                         # @google/generative-ai JavaScript quickstart
│
└── jess_demo.kt                                 # Standalone Kotlin Chain-of-Thought multilingual demo
```

---

## Track 1: `decode/` — Agentic Fintech Systems with M-Pesa Daraja, MCP, Apigee & ADK

> **Title:** *From Code to Cash: Building Agentic Payment Systems with M-Pesa, Apigee, and Google Cloud*  
> **Entry Point:** [`decode/README.md`](decode/README.md)  
> **Estimated Duration:** 2–3 Hours

Designed for the **Safaricom DECODE Builders Lab**, this two-part production workshop guides engineers through building secure, IAM-authenticated fintech payment agents on Google Cloud that integrate with **Safaricom DARAJA (M-Pesa Express / STK Push)**.

### Architecture Flow
```text
Developer / Gemini CLI ──(Authenticated MCP)──► Apigee API Gateway
                                                       │
Cloud Run: Google ADK Agent ──(IAM S2S Auth)───────────▼
                                         Cloud Run: FastMCP Server
                                                       │
                                                       ▼
                                         Safaricom DARAJA / M-Pesa Express APIs
```

### Labs Included
| Lab | Directory | Key Steps & Deliverables |
| :--- | :--- | :--- |
| **Lab 1: M-Pesa Daraja MCP Server with Apigee** | [`decode/01-mpesa-daraja-mcp-server-with-apigee/`](decode/01-mpesa-daraja-mcp-server-with-apigee/readme.md) | 12 guided modules (`01_intro.md` → `12_conclusion.md`): Setup GCP & Cloud Shell, enable Cloud Run / Artifact Registry / Cloud Build APIs, build a **FastMCP** server wrapping M-Pesa Express STK Push tools, deploy to Cloud Run with `--no-allow-unauthenticated`, proxy with **Apigee**, connect via **Gemini CLI**, verify Cloud Logging, and test with **Gemini Flash-Lite**. |
| **Lab 2: Google ADK Agent for M-Pesa MCP** | [`decode/02-google-adk-agent-for-mpesa-daraja-mcp/`](decode/02-google-adk-agent-for-mpesa-daraja-mcp/readme.md) | 11 guided modules (`01_intro.md` → `11_congratulations.md`): Architect a Python `google-adk` project, connect the ADK agent to the remote Cloud Run MCP endpoint from Lab 1, configure least-privilege IAM service-to-service bindings (`roles/run.invoker`), deploy the agent UI to Cloud Run, and validate end-to-end payment workflows. |

---

## Track 2: `BuildWithAI/` — Google Agent Development Kit (ADK), MCP & Gemini Live API

> **Title:** *ADK LABS: Building AI Agents with Google's Agent Development Kit (ADK)*  
> **Entry Point:** [`BuildWithAI/README.md`](BuildWithAI/README.md)

The flagship curriculum for mastering Google's **Agent Development Kit (ADK)**, the **Model Context Protocol (MCP)**, and **Gemini 2.5 Multimodal Live API**.

### Curriculum Breakdown (`BuildWithAI/Lessons/`)

1. **Lesson 1 — ADK Fundamentals (`Lessons/adk-intro/`):**
   - [`01-local-setup.md`](BuildWithAI/Lessons/adk-intro/01-local-setup.md): Virtual environment setup, project scaffolding, and launching the ADK Dev UI (`adk web`).
   - [`02-first-tool.md`](BuildWithAI/Lessons/adk-intro/02-first-tool.md): Empowering an `Agent` (`gemini-2.5-flash`) with deterministic Python function tools (`get_weather`) and inspecting tool execution traces.
   - [`03-multiple-tools-city-status.md`](BuildWithAI/Lessons/adk-intro/03-multiple-tools-city-status.md): Combining multiple tools (`get_weather` + `get_city_fact`) across African cities (Nairobi, Lagos, Cairo, Cape Town, Accra, Kampala).
   - [`04-first-cloud-deployment.md`](BuildWithAI/Lessons/adk-intro/04-first-cloud-deployment.md): Serverless deployment to Cloud Run via `adk deploy cloud_run --with_ui`.

2. **Lesson 2 — Model Context Protocol Fundamentals (`Lessons/mcp-fundermentals/`):**
   - 8 comprehensive modules (`01_intro.md` → `08_add_resources_prompts.md`) covering why MCP matters, Host-Client-Server architecture, building an ArXiv research tool server (`search_papers`, `extract_info`), building an MCP client, connecting to reference servers (Filesystem & Fetch), and adding MCP Resources & Prompts.

3. **Lesson 3 — Multi-Agent Systems with ADK & Remote MCP (`Lessons/adk-mcp/`, `mcp-on-cloudrun-01/`, `adk-withmcp-on-cloudrun-02/`):**
   - [`035-agentic-workflows-prep.md`](BuildWithAI/Lessons/adk-mcp/035-agentic-workflows-prep.md): Preparatory lab building a DevFest Assistant with Gemini + LlamaIndex.
   - [`mcp-on-cloudrun-01/`](BuildWithAI/Lessons/mcp-on-cloudrun-01/readme.md): 12-step codelab deploying a FastMCP server (`add`, `subtract` & custom prompts) to Cloud Run and invoking it via Gemini CLI.
   - [`adk-withmcp-on-cloudrun-02/`](BuildWithAI/Lessons/adk-withmcp-on-cloudrun-02/readme.md): 11-step codelab deploying a `google-adk` agent on Cloud Run that authenticates to the remote MCP server.

4. **Lesson 4 — Multimodal Streaming Agents with Gemini Live API (`Lessons/adk-gemini-live/`):**
   - [`036-gemini-liveapi-fundamentals.md`](BuildWithAI/Lessons/adk-gemini-live/036-gemini-liveapi-fundamentals.md): Turn-based text-to-text and text-to-native-audio (`.wav`) streaming with Gemini 2.5 Flash Live API, including resumable sessions.
   - [`037-gemini-liveapi-tools.md`](BuildWithAI/Lessons/adk-gemini-live/037-gemini-liveapi-tools.md): Real-time blocking vs. non-blocking tool execution, code execution, and interruptible responses.
   - [`038-gemini-liveapi-video-understanding.md`](BuildWithAI/Lessons/adk-gemini-live/038-gemini-liveapi-video-understanding.md): Video stream captioning, object detection, frame text extraction, and YouTube timeline analysis.

### Progressive Code Samples (`BuildWithAI/Samples/`)
- **`Samples/adk_into/`**: Complete `uv`-managed ADK package (`google-adk>=1.14.1`) featuring `AfricaWorkshopAgent` with `get_weather` and `get_city_fact` tools.
- **`Samples/multi-agents/`**: ADK `root_agent` (`gemini-2.0-flash-001`) equipped with utility tools (`roll_dice`, `flip_coin`, `choose_one`, `generate_random_number`).
- **`Samples/adk-gemini-live/`**: Standalone async Live API scripts (`gemini_live_01.py` for streaming text and `gemini_live_audio_02.py` for generating and saving 24kHz PCM audio to `.wav`).
- **`Samples/L4/` → `Samples/L9/`**: Step-by-step evolution of an ArXiv Research MCP Server (`research_server.py`) and interactive `mcp_chatbot.py`:
  - **L4:** FastMCP server exposing `search_papers` and `extract_info` over `stdio`.
  - **L5:** Interactive MCP client (`ClientSession`, `stdio_client`) with Gemini tool calling.
  - **L6:** Multi-server MCP chatbot (`server_config.json`) connecting simultaneously to `filesystem`, `research`, and `fetch` MCP servers.
  - **L7:** Extending the server with `@mcp.resource("papers://folders")` and `@mcp.prompt` (`generate_search_prompt`).
  - **L9:** Containerized (`Dockerfile`) remote MCP server running over **SSE (`transport="sse"`)** on port `8001` for cloud deployment.

---

## Track 3: `unstacked-labs/` — Building GenAI Solutions with Vertex AI SDK ("WanderBot")

> **Title:** *Building Gen AI Solutions with the Vertex AI SDK*  
> **Entry Point:** [`unstacked-labs/README.md`](unstacked-labs/README.md)

A 20-step guided codelab (`step_2_project_setup.md` through `step_20_Congratulations!.md` + [`troubleshooting.md`](unstacked-labs/troubleshooting.md)) where developers act as engineers at a travel marketing company building **WanderBot**—an interactive travel assistant powered by **Gemini 2.5 Flash** on **Vertex AI** and **Streamlit**.

### Key Learning Milestones
- **Steps 2–8:** Google Cloud project configuration, Cloud Shell Editor workflow, API enablement, Python virtual environment setup, exploring the Streamlit starter app, and launching the web UI.
- **Steps 9–13:** Initializing the Vertex AI client (`vertexai.init`), preparing multimodal/text payloads, calling Gemini, and engineering system instructions to shape persona and constraints.
- **Steps 14–17:** Defining a real-time weather function tool (`step_14_define_weather_tool.md`), refactoring to a stateful chat session (`step_15_refactor_chat_tooling.md`), implementing tool-calling dispatch logic (`step_16_implement_toolcalling_logic.md`), and testing live tool invocations.
- **Steps 18–20:** Iterative prompt refinement and tuning generation parameters (`temperature`, `top_p`, `max_output_tokens`).

---

## Track 4: Regional Build With AI Chapters (Nairobi, Kisumu, Cape Town)

Hands-on regional workshop tracks tailored for developer communities across East and Southern Africa:

| Chapter Directory | Key Files & Highlights |
| :--- | :--- |
| **`BuildWithAIKisumu/`** (*DevFest Dala*) | • [`check_list.md`](BuildWithAIKisumu/check_list.md): A comprehensive **725-line Cloud Run Deployment Runbook & Checklist** covering GCP auth, billing verification, API enablement, IAM roles (`roles/run.admin`, `roles/iam.serviceAccountUser`, `roles/storage.admin`), local `adk web` verification, deployment commands, and troubleshooting.<br>• [`lesson_1_prompts/lab_0_prompt_engineering.md`](BuildWithAIKisumu/lesson_1_prompts/lab_0_prompt_engineering.md): Mastering the **R.O.D.E.S.** framework (*Role, Objective, Details, Examples, Sense Check*) with Google AI Studio & Vertex AI Studio.<br>• [`lesson_2_agents/`](BuildWithAIKisumu/lesson_2_agents/): Complete **DevFest Lagos & Nairobi Schedule Scraper + LlamaIndex ReAct Agent** (`app_bwn.py` & `app_bwn_ReAct.py`) using `BAAI/bge-small-en-v1.5` embeddings and Gemini 1.5 Pro. |
| **`buildWithAINairobi/`** | • [`lesson_1_prompt_engineering/lab_0_prompt_engineering.md`](buildWithAINairobi/lesson_1_prompt_engineering/lab_0_prompt_engineering.md): Foundational prompt engineering codelab.<br>• [`lesson_3_agents/`](buildWithAINairobi/lesson_3_agents/): Nairobi edition of the LlamaIndex + Gemini ReAct agent and live conference schedule scraper (`app_bwn.py`, `app_bwn_ReAct.py`). |
| **`BwAICapeTown/`** | • [`lesson_1_prompt_engineering/`](BwAICapeTown/lesson_1_prompt_engineering/): Progressive prompt engineering labs (`lab_0_prompt_engineering.md`, `lab_1_prompt_engineering.md`, `prompt.md`).<br>• [`lesson_3_agents/agents_react.py`](BwAICapeTown/lesson_3_agents/agents_react.py): **Vertex AI** (`llama_index.llms.vertex.Vertex` with `gemini-2.5-pro-preview-03-25` and automatic fallbacks) ReAct Agent with web scraping and DuckDuckGo image search tools. |

---

## 🏥 Track 5: `OSDH/` — Open Digital Health Summit (FHIR Prompting & Gemma 2 with Keras 3)

Created for the **Open Digital Health Summit '24: Building with FHIR Track**, focusing on AI for healthcare interoperability in low-resource settings across Africa:

1. **[`OSDH/lesson_1_prompt_engineering/lab_prompt_engineering.md`](OSDH/lesson_1_prompt_engineering/lab_prompt_engineering.md):**
   - A 6-step structured prompting guide for **HL7 FHIR Architects** designing offline-capable immunization tracking and Android FHIR SDK solutions aligned with WHO SMART Guidelines.
   - Covers persona definition, ideation for rural clinics with unstable connectivity, XML `<example>` and `<thinking>` Chain-of-Thought tags, and Ministry of Health technical specification generation.
2. **[`OSDH/lesson-2_advanced_prompting/Lesson_2_Advanced_Prompting_Techniques.ipynb`](OSDH/lesson-2_advanced_prompting/Lesson_2_Advanced_Prompting_Techniques.ipynb):**
   - Interactive Jupyter notebook exploring few-shot prompting, Chain-of-Thought (CoT), and structured output generation.
3. **[`OSDH/lesson_3_gemma_with_keras/`](OSDH/lesson_3_gemma_with_keras/):**
   - [`lesson_3_1_Keras_Gemma_2_Quickstart.ipynb`](OSDH/lesson_3_gemma_with_keras/lesson_3_1_Keras_Gemma_2_Quickstart.ipynb): Installing `keras-nlp` and `keras>=3`, configuring the JAX backend, loading `gemma2_2b_en`, and running single/batch text generation.
   - [`Lesson_3_2_Keras_Gemma_2_Quickstart_Chat.ipynb`](OSDH/lesson_3_gemma_with_keras/Lesson_3_2_Keras_Gemma_2_Quickstart_Chat.ipynb): Building multi-turn conversational chat workflows with Gemma 2 and Keras 3.

---

## Track 6: Community Bootcamps & Polyglot Starters

Ready-to-run reference implementations demonstrating Gemini integration across **Python**, **Kotlin (Android)**, and **JavaScript (Node.js)**:

- **[`devfestnairobi24/`](devfestnairobi24/) & [`jess_demo.kt`](jess_demo.kt) — "Jess" Multilingual Assistant:**
  - Demonstrates deterministic language routing and Chain-of-Thought (`<thought process="Chain-of-Thought">`) across **English, Kiswahili, French, and Portuguese** (with automatic fallback to Kiswahili for mixed or unsupported languages and M-Pesa billing domain examples).
  - Provided in both Python ([`multilingual_assistant.py`](devfestnairobi24/multilingual_assistant.py)) and Android Kotlin ([`multilingual_assistant.kt`](devfestnairobi24/multilingual_assistant.kt), [`jess_demo.kt`](jess_demo.kt)).
- **[`gdsc_bootcamp/gdsc_gemini.py`](gdsc_bootcamp/gdsc_gemini.py):**
  - Clean Python starter for GDSC Campus Connect (Catholic University of Eastern Africa — CUEA) demonstrating `.env` key management, `generation_config`, and explicit `safety_settings` thresholds.
- **[`capetown/gemini_starts.js`](capetown/gemini_starts.js):**
  - Minimalist Node.js quickstart using `@google/generative-ai` and `dotenv`.

---

## Hosted Google Colab Notebooks & Global Workshops

Launch these interactive notebooks directly in **Google Colab**:

| Workshop / Session | Event / Community | Topics Covered | Colab Link |
| :--- | :--- | :--- | :---: |
| **Agentic Workflows with Gemini & ReAct** | Build With AI / Kisumu & Nairobi | Function calling, web scraping (DevFest Lagos/Nairobi), LlamaIndex `ReActAgent`, social post generation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1LkY6OG9H7R2NvsgzdCYVJ7QKIfStYgSr) |
| **Multimodal Live API Fundamentals** | Build With AI (Lesson 3.6) | Gemini 2.5 Flash Live API, turn-based text-to-audio, native `.wav` playback, resumable sessions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1v6JnpWr3xDBFip6HRxBHiQWxe6-N9jMc) |
| **Multimodal Live API with Tools** | Build With AI (Lesson 3.7) | Real-time tool registration, code execution, blocking vs. non-blocking async function calling | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Rn6SM4yKCKftM6zz2EN0P5uNw98vtKmO) |
| **Video Understanding with Gemini Live API** | Build With AI (Lesson 3.8) | Scene captioning, object detection, OCR from video frames, YouTube timeline querying | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uIsAzF5dKUs-6Jdnaa7FGnCJobme6rDA) |
| **Unlocking Generative AI with Gemini** | Campus Connect — CUEA | Deep learning foundations, LLMs, Google AI Studio, and Gemini Python SDK | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1lnjeo-pk4XHp1ZBwm7DTV2mXnt_lBN23) |
| **Keras 3 — A Spectrum of Workflows & Gemma** | Zindi Africa | Multi-backend Keras 3 (JAX, PyTorch, TensorFlow) and managing Gemma LLMs | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1T8LA5bygK4p2L5GyR8V1xSF9tu6KxFxJ) |
| **Working with Gemini Pro and LangChain** | Build With AI | Document loading, vector storage, and Retrieval-Augmented Generation (RAG) Q&A bots | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1q2TcaoXqxNz92bAQaBisomZUUk1VRqY6) |
| **Creating Art with Stable Diffusion (Labs 1–3)** | AMLD Africa — Nairobi | Generative image synthesis and diffusion workflows | [Lab 1](https://colab.research.google.com/drive/1aYlso-T-9DkswERrGl3omrR-n2zvczOs) · [Lab 2](https://colab.research.google.com/drive/1Uulic4so-RHJfpFaCzbnc1cs1QymtRkv) · [Lab 3](https://colab.research.google.com/drive/1jN-AksZQr7lBDJi5Q7Y5ah9fTY1vMv2q) |

---

## Prerequisites & Environment Setup

### 1. System Requirements
- **Python:** `3.11+` or `3.12+` (`uv` or `venv` recommended)
- **Google Cloud SDK:** `gcloud` CLI installed and authenticated (or use **Google Cloud Shell**)
- **API Keys / Credentials:**
  - A **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/) (`GOOGLE_API_KEY` or `GEMINI_API_KEY`)
  - A **Google Cloud Project** with Billing, Vertex AI, Cloud Run, Cloud Build, and Artifact Registry APIs enabled
  - *(For `decode/` only)* Safaricom [Daraja Developer Portal](https://daraja.safaricom.co.ke/) credentials

### 2. Quickstart: Clone & Run an ADK Agent Locally

```bash
# 1. Clone the repository
git clone https://github.com/ngesa254/labsdotgde.git
cd labsdotgde

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Google ADK and core dependencies
pip install google-adk google-genai mcp fastmcp python-dotenv

# 4. Configure your API key
export GOOGLE_API_KEY="your-gemini-api-key"

# 5. Launch the ADK Interactive Dev UI on the sample agent
cd BuildWithAI/Samples/adk_into
adk web
```
Then open `http://127.0.0.1:8000` in your browser to chat with `AfricaWorkshopAgent` and inspect live tool-call traces.

---

## Cloud Deployment & Cost Cleanup

When deploying MCP servers or ADK agents to **Google Cloud Run** (in `decode/` or `BuildWithAI/`):

- **Pre-Deployment Verification:** Follow [`BuildWithAIKisumu/check_list.md`](BuildWithAIKisumu/check_list.md) to verify your IAM roles, active project, and container readiness.
- **Avoid Unexpected Charges:** Always clean up Cloud Run services, Artifact Registry container images, and temporary GCP projects after completing a workshop. Step-by-step teardown commands are documented in:
  - [`BuildWithAI/gcp_cost_clean_up.md`](BuildWithAI/gcp_cost_clean_up.md)
  - [`decode/01-mpesa-daraja-mcp-server-with-apigee/11.5_cleanup.md`](decode/01-mpesa-daraja-mcp-server-with-apigee/11.5_cleanup.md)
  - [`decode/02-google-adk-agent-for-mpesa-daraja-mcp/10_cleanup.md`](decode/02-google-adk-agent-for-mpesa-daraja-mcp/10_cleanup.md)

---

## 🤝 Author & Community

Curated and maintained by **[Ngesa Marvin](https://github.com/ngesa254)** (*[@Ngesa254](https://twitter.com/Ngesa254)*) — **AI/ML Lead**,  **Google Developer Expert (GDE) in AI/ML**.

**Happy Building!** 🚀
