# Lab 2: Google ADK Agent with Safaricom MPESA + DARAJA MCP and Apigee on Cloud Run

> **DECODE Builders Lab Part 2: Google ADK agent integration with Safaricom and Google Cloud tooling**

<p align="center">
  <img src="https://img.shields.io/badge/Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Cloud Run">
  <img src="https://img.shields.io/badge/Google%20ADK-1.14.0-EA4335?style=for-the-badge&logo=google&logoColor=white" alt="Google ADK">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/MCP-Protocol-00ADD8?style=for-the-badge" alt="MCP">
  <img src="https://img.shields.io/badge/Apigee-API%20Management-FF6D00?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Apigee">
  <img src="https://img.shields.io/badge/Safaricom-MPESA%20%2B%20DARAJA-1B5E20?style=for-the-badge" alt="Safaricom MPESA and DARAJA">
</p>

---

## Overview

In this hands-on lab, you will build and deploy a **Google ADK fintech agent** using Google's **Agent Development Kit (ADK)**. The agent uses a multi-agent architecture to answer fintech workflow requests by combining:

- **Internal data and actions** from the Safaricom MCP server created in Lab 1
- **Google Cloud infrastructure** for deployment, identity, and runtime
- **Optional Apigee exposure** for governed API access patterns

The key architectural principle demonstrated is **separation of concerns** — a distinct reasoning layer (the agent) communicating with a distinct tooling layer (the MCP server) via a secure API.

## Duration

| Experience Level | Estimated Time |
|-----------------|----------------|
| Beginner | 60-75 minutes |
| Intermediate | 45-60 minutes |
| Experienced | 30-45 minutes |

## What You'll Learn

- ✅ Structure a Python project for ADK deployment
- ✅ Implement a multi-agent workflow using `SequentialAgent`
- ✅ Connect to a remote MCP server using `MCPToolset`
- ✅ Integrate external tools like the Wikipedia API
- ✅ Deploy an agent to Cloud Run using `adk deploy`
- ✅ Configure secure service-to-service authentication with IAM

## Prerequisites

- **Completed Lab 1** (or have access to a running MCP server URL)
- A Google Cloud project with billing enabled
- Basic familiarity with Python

---

## Lab Structure

| Step | Title | Description |
|------|-------|-------------|
| 01 | [Introduction](01_intro.md) | Lab overview and architecture |
| 02 | [Why Cloud Run?](02_why_cloudrun.md) | Benefits of serverless for ADK agents |
| 03 | [Setup](03_setup.md) | Project setup and Cloud Shell |
| 04 | [Enable APIs](04_enable_apis.md) | Enable required GCP APIs |
| 05 | [Create Project](05_create_project.md) | Set up folder, requirements, environment |
| 06 | [Create Agent Workflow](06_create_agent_workflow.md) | Build the multi-agent system |
| 07 | [Prepare Deployment](07_prepare_deployment.md) | Configure IAM for Vertex AI |
| 08 | [Deploy Agent](08_deploy_agent.md) | Deploy with `adk deploy cloud_run` |
| 09 | [Test Agent](09_test_agent.md) | Test the deployed agent |
| 10 | [Cleanup](10_cleanup.md) | Clean up resources |
| 11 | [Congratulations](11_congratulations.md) | Summary and next steps |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Zoo Tour Guide Agent                         │
│                    (Deployed on Cloud Run)                      │
│                                                                 │
│  ┌──────────┐   ┌─────────────────────┐   ┌──────────────────┐ │
│  │ Greeter  │──▶│ Comprehensive       │──▶│ Response         │ │
│  │  Agent   │   │ Researcher          │   │ Formatter        │ │
│  │          │   │                     │   │                  │ │
│  │ Welcomes │   │ Tools:              │   │ Formats output   │ │
│  │ user     │   │ • MCP Server 🦁     │   │ for user         │ │
│  │          │   │ • Wikipedia 📚      │   │                  │ │
│  └──────────┘   └─────────────────────┘   └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│     Zoo MCP Server      │     │     Wikipedia API       │
│     (from Lab 1)        │     │                         │
│                         │     │  General knowledge      │
│  🦁 Lions    🐧 Penguins│     │  about animals          │
│  🐘 Elephants 🐻 Bears  │     │                         │
└─────────────────────────┘     └─────────────────────────┘
```

## Agent Components

| Component | Type | Purpose |
|-----------|------|---------|
| `greeter` | Root Agent | Welcomes users and saves their prompt |
| `comprehensive_researcher` | Agent | Queries MCP server and Wikipedia |
| `response_formatter` | Agent | Formats findings into friendly response |
| `tour_guide_workflow` | SequentialAgent | Orchestrates the research → format flow |

---

## Quick Start

**Already familiar with ADK?** Here's the speed run:

```bash
# 1. Enable APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
    cloudbuild.googleapis.com aiplatform.googleapis.com compute.googleapis.com

# 2. Create project
cd && mkdir zoo_guide_agent && cd zoo_guide_agent

# 3. Set up environment
export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export SA_NAME=lab2-cr-service
export SERVICE_ACCOUNT="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# 4. Create service account and grant permissions
gcloud iam service-accounts create ${SA_NAME} --display-name="Service Account for lab 2"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/run.invoker"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/aiplatform.user"

# 5. Create files (requirements.txt, .env, __init__.py, agent.py)

# 6. Deploy
uvx --from google-adk adk deploy cloud_run \
  --project=$PROJECT_ID --region=europe-west1 \
  --service_name=zoo-tour-guide --with_ui . \
  -- --service-account=$SERVICE_ACCOUNT
```

---

## Related Labs

| Lab | Description | Status |
|-----|-------------|--------|
| [Lab 1](../01-mpesa-daraja-mcp-server-with-apigee/readme.md) | Deploy the Safaricom MPESA + DARAJA MCP server | Required |
| **Lab 2** | Build the Google ADK agent with Safaricom MCP access | **You are here** |
| Lab 3 | Multi-Agent Systems with ADK and MCP | Coming soon |

---

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Samples Repository](https://github.com/google/adk-samples)
- [Building Custom Tools](https://google.github.io/adk-docs/tools/)
- [MCP Tools Guide](https://google.github.io/adk-docs/tools/mcp-tools/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Apigee Documentation](https://cloud.google.com/apigee)

---

## Getting Help

- **Stuck for more than 20 seconds?** Raise your hand — we're here to help!
- Common issues are usually related to:
  - Missing IAM permissions
  - Incorrect MCP server URL
  - Environment variables not loaded

---

## Cleanup

When you're done, clean up to avoid charges:

```bash
# Delete the agent service
gcloud run services delete zoo-tour-guide --region=europe-west1 --quiet

# Delete Artifact Registry
gcloud artifacts repositories delete cloud-run-source-deploy --location=europe-west1 --quiet

# (Optional) Delete the entire project
gcloud projects delete $PROJECT_ID
```

---

<p align="center">
  <strong>Happy Building! 🚀</strong>
</p>
