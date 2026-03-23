# From Code to Cash: Building Agentic Payment Systems with M-Pesa, Apigee, and Google Cloud

> **Build a secure MPESA Express MCP server and a Google ADK agent on Cloud Run**

<p align="center">
  <img src="https://img.shields.io/badge/Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Cloud Run">
  <img src="https://img.shields.io/badge/Google%20ADK-Agent%20Development-EA4335?style=for-the-badge&logo=google&logoColor=white" alt="Google ADK">
  <img src="https://img.shields.io/badge/MCP-Remote%20Tools-00ADD8?style=for-the-badge" alt="MCP">
  <img src="https://img.shields.io/badge/Apigee-API%20Management-FF6D00?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Apigee">
  <img src="https://img.shields.io/badge/Safaricom-DARAJA%20%2B%20DECODE-1B5E20?style=for-the-badge" alt="Safaricom DARAJA and DECODE">
</p>

---

## Overview

This repository contains the **DECODE Builders Lab** for building secure fintech agents on Google Cloud with Safaricom APIs and Google tooling. The workshop is organized into **two connected labs**:

- **Lab 1:** Deploy a secure **MPESA Express MCP server** on Cloud Run with an **Apigee-ready** edge
- **Lab 2:** Build and deploy a **Google ADK agent** that calls that MCP server securely on Google Cloud

The intended flow is simple:

1. Complete the MCP server lab first
2. Use the deployed MCP service in the ADK agent lab
3. Validate the full agent-to-tool workflow end to end

## Duration

| Segment | Estimated Time |
|--------|----------------|
| Lab 1: MCP Server | 45-60 minutes |
| Lab 2: ADK Agent | 60-75 minutes |
| Validation + cleanup | 20-30 minutes |
| Total workshop time | 2-3 hours |

## How to Use This Workshop

Use this workshop like a guided build, not a reference dump.

- Start with **Lab 1** unless you already have a deployed MCP endpoint for MPESA Express and DARAJA
- Use the copied lab files as working material and adapt them to the DECODE fintech use case as you go
- If you get stuck for more than 20 seconds in a live session, ask for help and keep moving
- Use the official docs when you need answers: ADK, MCP, Cloud Run, Apigee, Gemini CLI, and Safaricom DARAJA
- Complete the core path first, then take optional extensions such as Apigee hardening, observability, or marketplace discovery

## What You'll Build

- A secure Cloud Run MCP server that exposes MPESA Express and DARAJA capabilities as tools
- An Apigee-ready API surface in front of the MCP workflow for governance and future production controls
- A Cloud Run ADK agent that connects to the MCP server over authenticated service-to-service calls
- A reusable reference architecture for fintech agents on Google Cloud

## What You'll Learn

- ✅ How to structure a remote MCP server for fintech APIs
- ✅ How to secure Cloud Run services with IAM authentication
- ✅ How to position Apigee as an API management and security layer for the MCP service
- ✅ How to connect Gemini CLI to a protected MCP endpoint
- ✅ How to build an ADK agent that uses remote MCP tools
- ✅ How to deploy the agent on Cloud Run with the right IAM roles
- ✅ How to test and clean up the full solution safely

## Prerequisites

- A Google Cloud project with billing enabled
- Access to Cloud Shell or a local `gcloud` environment
- Python 3.11+ and either `uv` or `pip`
- Gemini CLI installed and authenticated
- Safaricom DARAJA developer credentials and app setup
- Working knowledge of Python, APIs, IAM, and Cloud Run

## Core References

- Safaricom DECODE: `https://decode.safaricom.co.ke/`
- Safaricom DARAJA: `https://daraja.safaricom.co.ke/`
- Google ADK docs: `https://google.github.io/adk-docs/`
- MCP docs: `https://modelcontextprotocol.io/`
- Cloud Run docs: `https://cloud.google.com/run/docs`
- Apigee docs: `https://cloud.google.com/apigee`

---

## Workshop Structure

| Lab | Folder | Purpose | Start Here |
|-----|--------|---------|------------|
| Lab 1 | `01-mpesa-daraja-mcp-server-with-apigee` | Build and deploy the secure MCP layer for Safaricom APIs on Google Cloud | `01-mpesa-daraja-mcp-server-with-apigee/readme.md` |
| Lab 2 | `02-google-adk-agent-for-mpesa-daraja-mcp` | Build and deploy the Google ADK agent that uses the MCP layer | `02-google-adk-agent-for-mpesa-daraja-mcp/readme.md` |

## Recommended Navigation

If you are landing in this folder for the first time, use this sequence:

1. Read `01-mpesa-daraja-mcp-server-with-apigee/readme.md`
2. Complete the setup and deployment steps for the MCP server
3. Keep the deployed MCP service URL and authentication setup ready
4. Move to `02-google-adk-agent-for-mpesa-daraja-mcp/readme.md`
5. Build the ADK agent and point it to the MCP server from Lab 1
6. Test the end-to-end flow and then clean up resources
7. Use Apigee as an optional extension layer for security, governance, and productization

## Architecture

```text
Developer / Gemini CLI
        |
        | Authenticated MCP calls
        v
Apigee
        |
        | Managed API gateway and policy layer
        v
Cloud Run: Safaricom MPESA + DARAJA MCP Server
        |
        | Tool wrappers for Safaricom APIs
        v
Safaricom DARAJA / DECODE APIs

Cloud Run: Google ADK Agent Service
        |
        | IAM-authenticated service-to-service MCP access
        v
Apigee / Cloud Run MCP endpoint
```

## Lab 1 Summary

In `01-mpesa-daraja-mcp-server-with-apigee`, developers will:

- Create an MCP server using Python and FastMCP
- Wrap MPESA/DARAJA capabilities as MCP tools
- Deploy the service to Cloud Run
- Require authentication for all requests
- Connect to the secure endpoint from Gemini CLI
- Prepare the design for Apigee-based governance and policy enforcement

## Lab 2 Summary

In `02-google-adk-agent-for-mpesa-daraja-mcp`, developers will:

- Structure a Python project for ADK deployment
- Build a tool-using agent with `google-adk`
- Connect the agent to the remote MCP server from Lab 1
- Configure IAM for secure service-to-service access
- Deploy and test the agent on Cloud Run

---

## Quick Start

Already familiar with the architecture? Use this workshop path:

```bash
cd decode

# Start with the MCP server lab
cd 01-mpesa-daraja-mcp-server-with-apigee

# After Lab 1 is deployed, return and continue with the ADK agent lab
cd ../02-google-adk-agent-for-mpesa-daraja-mcp
```

## Expected Outcomes

By the end of the workshop, developers should have:

- A deployed MCP server exposing MPESA/DARAJA tools
- A documented Apigee integration point for security and governance
- A deployed ADK agent connected to that MCP server
- IAM bindings configured for least-privilege access
- A tested Gemini CLI and agent workflow
- A clear cleanup path to avoid future charges

## Cleanup

When the workshop is complete:

- Delete the MCP server Cloud Run service
- Delete the ADK agent Cloud Run service
- Delete Artifact Registry repositories created for deployment
- Remove unneeded service accounts and IAM bindings
- Delete the project if it was created only for the workshop
- Remove local env files containing credentials or secrets
- Remove Apigee resources if you provisioned them as an extension

---

## Notes for Developers

- Treat **Lab 1** as the foundation for **Lab 2**
- Do not start the ADK lab until the MCP server endpoint is deployed and reachable
- Keep your service URL, project ID, region, and service account details available between the two labs
- Keep your Apigee environment details available if you decide to expose the MCP service through an API gateway
- Adapt the sample implementations from the copied labs to the DECODE fintech use case as you build

---

**Build secure fintech agents. Start with Lab 1, then move to Lab 2.**
