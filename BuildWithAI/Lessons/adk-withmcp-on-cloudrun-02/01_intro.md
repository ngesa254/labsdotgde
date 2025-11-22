# Introduction

This lab focuses on the implementation and deployment of a client agent service. You will use **Agent Development Kit (ADK)** to build an AI agent that uses remote tools such as the MCP server created in Lab 1.

The key architectural principle demonstrated is the **separation of concerns**, with a distinct reasoning layer (the agent) communicating with a distinct tooling layer (the MCP server) via a secure API.

## Background

In Lab 1, you created an MCP server that provides data about the animals in a fictional zoo to LLMs, for example when using the Gemini CLI.

In this lab, we are building a **tour guide agent** for the fictional zoo. The agent will:

- Use the same MCP server from Lab 1 to access details about the zoo animals
- Use Wikipedia to create the best tour guide experience
- Be deployed to Cloud Run for access by all zoo visitors

## Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│                     │  HTTPS  │                      │
│   Zoo Tour Guide    │────────▶│   Zoo MCP Server     │
│   (ADK Agent)       │◀────────│   (from Lab 1)       │
│                     │         │                      │
└─────────────────────┘         └──────────────────────┘
          │
          │ Wikipedia
          ▼
    ┌───────────┐
    │ Wikipedia │
    │    API    │
    └───────────┘
```

---

## Prerequisites

- ✅ A running MCP server on Cloud Run (from Lab 1) or its associated Service URL
- ✅ A Google Cloud project with billing enabled

---

## What You'll Learn

- How to structure a Python project for ADK deployment
- How to implement a tool-using agent with `google-adk`
- How to connect an agent to a remote MCP server for its toolset
- How to deploy a Python application as a serverless container to Cloud Run
- How to configure secure, service-to-service authentication using IAM roles
- How to delete Cloud resources to avoid incurring future costs

---

## What You'll Need

- A Google Cloud Account and Google Cloud Project
- A web browser such as Chrome
- The MCP Server Service URL from Lab 1