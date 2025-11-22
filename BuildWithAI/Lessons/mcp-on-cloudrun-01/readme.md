# Lab: Deploy a Secure MCP Server on Cloud Run

> **Part of Lesson 3: Multi-Agent Systems with ADK and MCP**

<p align="center">
  <img src="https://img.shields.io/badge/Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Cloud Run">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13">
  <img src="https://img.shields.io/badge/FastMCP-2.12.4-00ADD8?style=for-the-badge" alt="FastMCP">
  <img src="https://img.shields.io/badge/Gemini%20CLI-Ready-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini CLI">
</p>

---

## 🎯 Overview

In this hands-on lab, you will build and deploy a **Model Context Protocol (MCP) server** as a secure, production-ready service on Google Cloud Run. MCP servers enable LLMs to access external tools and services, extending their capabilities beyond their training data.

You'll create a "Zoo MCP Server" with tools to query animal information, deploy it securely with authentication, and connect to it using **Gemini CLI**.

## ⏱️ Duration

| Experience Level | Estimated Time |
|-----------------|----------------|
| Beginner | 45-60 minutes |
| Intermediate | 30-45 minutes |
| Experienced | 20-30 minutes |

## 🎓 What You'll Learn

- ✅ Create an MCP server using **FastMCP** (Python)
- ✅ Deploy to **Cloud Run** with authentication
- ✅ Secure endpoints with IAM-based access control
- ✅ Connect **Gemini CLI** to remote MCP servers
- ✅ Create custom MCP prompts for faster workflows
- ✅ Verify tool calls via Cloud Run logs

## 📋 Prerequisites

- A Google Account (personal account recommended)
- Basic familiarity with Python and command line
- Access to Google Cloud Console
- ~$1 USD in Cloud resources (new users get $300 free trial)

---

## 📚 Lab Structure

| Step | Title | Description |
|------|-------|-------------|
| 01 | [Introduction](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/01_intro.md) | Lab overview and learning objectives |
| 02 | [Project Setup](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/02_setup.md) | GCP account, Cloud Shell, authentication |
| 03 | [Cloud Shell](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/03_cloudshell.md) | Activate and configure Cloud Shell |
| 04 | [Enable APIs](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/04_enabling_apis.md) | Enable Cloud Run, Artifact Registry, Cloud Build |
| 05 | [Prepare Python Project](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/05_prep_project.md) | Initialize project with `uv` |
| 06 | [Create MCP Server](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/06_create_mcp_server.md) | Build the Zoo MCP server with FastMCP |
| 07 | [Deploy to Cloud Run](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/07_deploy_on_cloudrun.md) | Containerize and deploy |
| 08 | [Connect Gemini CLI](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/08_addmcp_to_gemini_cli.md) | Configure and test MCP connection |
| 09 | [Verify Logs](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/09_verify_logs.md) | *(Optional)* Check server logs |
| 10 | [Add MCP Prompt](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/10_add_mcp_prompt.md) | *(Optional)* Create custom `/find` command |
| 11 | [Use Flash Lite](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/11_gemini_flash_lite.md) | *(Optional)* Faster responses with Flash Lite |
| 12 | [Conclusion](https://github.com/ngesa254/labsdotgde/blob/main/BuildWithAI/Lessons/mcp-on-cloudrun-01/12_conclusion.md) | Summary and cleanup |

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────────┐
│                 │  HTTPS  │                      │
│   Gemini CLI    │────────▶│  Cloud Run Service   │
│  (MCP Client)   │◀────────│   (MCP Server)       │
│                 │   JSON  │                      │
└─────────────────┘         └──────────────────────┘
                                     │
                            ┌────────┴────────┐
                            │   FastMCP       │
                            │   Zoo Server    │
                            │                 │
                            │  🦁 Lions       │
                            │  🐧 Penguins    │
                            │  🐘 Elephants   │
                            │  🐻 Bears       │
                            └─────────────────┘
```

## 🛠️ MCP Tools You'll Build

| Tool | Description |
|------|-------------|
| `get_animals_by_species(species)` | Get all animals of a specific species |
| `get_animal_details(name)` | Get details about a specific animal by name |

---

## 🚀 Quick Start

**Already familiar with GCP?** Here's the speed run:

```bash
# 1. Enable APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

# 2. Create project
mkdir mcp-on-cloudrun && cd mcp-on-cloudrun
uv init --description "MCP server on Cloud Run" --bare --python 3.13
uv add fastmcp==2.12.4 --no-sync

# 3. Create server.py and Dockerfile (see step 06 & 07)

# 4. Deploy
gcloud iam service-accounts create mcp-server-sa --display-name="MCP Server Service Account"
gcloud run deploy zoo-mcp-server \
    --service-account=mcp-server-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=.

# 5. Configure Gemini CLI (see step 08)
```

---

## 🔗 Related Labs

This lab is part of a series:

| Lab | Description |
|-----|-------------|
| **→ This Lab** | Deploy a Secure MCP Server on Cloud Run |
| Lab 2 | Use an MCP Server on Cloud Run with an ADK Agent |
| Lab 3 | Multi-Agent Systems with ADK and MCP |

---

## 📖 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [Google Agent Development Kit (ADK)](https://github.com/google/adk-python)

---

## 🆘 Getting Help

- **Stuck for more than 20 seconds?** Raise your hand — we're here to help!
- Check the troubleshooting sections in each step
- Common issues are usually related to expired ID tokens or IAM permissions

---

## 🧹 Cleanup

When you're done, clean up to avoid charges:

```bash
# Delete the Cloud Run service
gcloud run services delete zoo-mcp-server --region=europe-west1

# Or delete the entire project
gcloud projects delete $GOOGLE_CLOUD_PROJECT

# Clean up local files
rm -rf ~/mcp-on-cloudrun ~/.gemini
```

---

<p align="center">
  <strong>Happy Building! 🚀</strong>
</p>