# Lab 1: Build the MPESA Express MCP Server with Apigee on Cloud Run

> **DECODE Builders Lab Part 1: Safaricom APIs with Google Cloud MCP infrastructure**

<p align="center">
  <img src="https://img.shields.io/badge/Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Cloud Run">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13">
  <img src="https://img.shields.io/badge/FastMCP-2.12.4-00ADD8?style=for-the-badge" alt="FastMCP">
  <img src="https://img.shields.io/badge/Apigee-API%20Management-FF6D00?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Apigee">
  <img src="https://img.shields.io/badge/Safaricom-MPESA%20%2B%20DARAJA-1B5E20?style=for-the-badge" alt="Safaricom MPESA and DARAJA">
  <img src="https://img.shields.io/badge/Gemini%20CLI-Ready-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini CLI">
</p>

---

## Overview

In this hands-on lab, you will build and deploy a **Model Context Protocol (MCP) server** as a secure, production-ready service on Google Cloud Run. MCP servers enable LLMs to access external tools and services, extending their capabilities beyond their training data.

You will adapt the workshop pattern to a **Safaricom M-PESA Express MCP server** that also includes a static product catalog, deploy it securely with authentication, and connect to it using **Gemini CLI**. You will also prepare the service for an **Apigee** front door so developers and agents can consume Safaricom payment capabilities and product lookup tools through a governed API layer.

## Duration

| Experience Level | Estimated Time |
|-----------------|----------------|
| Beginner | 45-60 minutes |
| Intermediate | 30-45 minutes |
| Experienced | 20-30 minutes |

## What You'll Learn

- ✅ Create an MCP server using **FastMCP** (Python)
- ✅ Deploy to **Cloud Run** with authentication
- ✅ Secure endpoints with IAM-based access control
- ✅ Connect **Gemini CLI** to remote MCP servers
- ✅ Create custom MCP prompts for faster workflows
- ✅ Verify tool calls via Cloud Run logs

## Prerequisites

- A Google Account (personal account recommended)
- Basic familiarity with Python and command line
- Access to Google Cloud Console
- ~$1 USD in Cloud resources (new users get $300 free trial)

---

## Lab Structure

| Step | Title | Description |
|------|-------|-------------|
| 01 | [Introduction](01_intro.md) | Lab overview and learning objectives |
| 02 | [Project Setup](02_setup.md) | GCP account, Cloud Shell, authentication |
| 03 | [Cloud Shell](03_cloudshell.md) | Activate and configure Cloud Shell |
| 04 | [Enable APIs](04_enabling_apis.md) | Enable Cloud Run, Artifact Registry, Cloud Build |
| 05 | [Prepare Python Project](05_prep_project.md) | Initialize project with `uv` |
| 06 | [Create MCP Server](06_create_mcp_server.md) | Build the MPESA Express MCP server with FastMCP |
| 07 | [Deploy to Cloud Run](07_deploy_on_cloudrun.md) | Containerize and deploy |
| 08 | [Connect Gemini CLI](08_addmcp_to_gemini_cli.md) | Configure and test MCP connection |
| 09 | [Verify Logs](09_verify_logs.md) | *(Optional)* Check server logs |
| 10 | [Add MCP Prompt](10_add_mcp_prompt.md) | *(Optional)* Create custom prompt workflow |
| 11 | [Use Flash Lite](11_gemini_flash_lite.md) | *(Optional)* Faster responses with Flash Lite |
| 11.5 | [Clean Up Resources](11.5_cleanup.md) | *(Optional)* Reset lab or redeploy changes |
| 12 | [Conclusion](12_conclusion.md) | Summary and next steps |

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
                            │ Safaricom       │
                            │ M-PESA Express  │
                            │ MCP Server      │
                            │                 │
                            │ Product Catalog │
                            │ Order Totals    │
                            │ OAuth Token     │
                            │ STK Push        │
                            │ Callback Parse  │
                            │ Error Explain   │
                            └─────────────────┘
```

## MCP Tools You'll Build

| Tool | Description |
|------|-------------|
| `list_products()` | List products from the merchant catalog |
| `get_product(product_id)` | Fetch a specific product by ID |
| `calculate_order_total(items)` | Compute the order total in KES |
| `generate_access_token_request()` | Get the OAuth token request details for Safaricom DARAJA API calls |
| `validate_stk_push_payload(...)` | Validate an MPESA Express request payload before submission |
| `initiate_stk_push(...)` | Start an MPESA Express payment request |
| `parse_stk_callback(callback_payload)` | Normalize callback payloads for agents and developers |
| `explain_stk_error(code)` | Translate common API or transaction errors into action guidance |

---

## Quick Start

**Already familiar with GCP?** Here's the speed run:

```bash
# 1. Enable APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

# 2. Create project
mkdir mpesa-mcp-server && cd mpesa-mcp-server
uv init --description "Safaricom M-PESA Express MCP server on Cloud Run" --bare --python 3.13
uv add fastmcp==2.12.4 httpx==0.28.1 --no-sync

# 3. Create server.py and Dockerfile (see step 06 & 07)

# 4. Deploy
export MPESA_CONSUMER_KEY="your_consumer_key"
export MPESA_CONSUMER_SECRET="your_consumer_secret"
gcloud run deploy safaricom-mpesa-mcp-server \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=. \
    --set-env-vars="MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY},MPESA_CONSUMER_SECRET=${MPESA_CONSUMER_SECRET}" \
    --labels=dev-tutorial=codelab-mcp

# 5. Configure Gemini CLI (see step 08)
```

---

## Related Labs

This lab is part of a series:

| Lab | Description |
|-----|-------------|
| **→ This Lab** | Deploy a Secure MCP Server on Cloud Run |
| Lab 2 | Build a Google ADK agent that uses the Safaricom MCP server |
| Lab 3 | Multi-Agent Systems with ADK and MCP |

---

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub Repository](https://github.com/PrefectHQ/FastMCP)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Apigee Documentation](https://cloud.google.com/apigee)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [Google Agent Development Kit (ADK)](https://github.com/google/adk-python)

---

## Getting Help

- **Stuck for more than 20 seconds?** Raise your hand — we're here to help!
- Check the troubleshooting sections in each step
- Common issues are usually related to expired ID tokens or IAM permissions

---

##  Cleanup

When you're done, clean up to avoid charges:

```bash
# Delete the Cloud Run service
gcloud run services delete safaricom-mpesa-mcp-server --region=europe-west1

# Or delete the entire project
gcloud projects delete $GOOGLE_CLOUD_PROJECT

# Clean up local files
rm -rf ~/mpesa-mcp-server ~/.gemini
```

---

<p align="center">
  <strong>Happy Building! 🚀</strong>
</p>
