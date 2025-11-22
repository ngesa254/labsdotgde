# MCP Fundamentals: Build Rich-Context AI Apps

## Introduction

### Overview

In this Lab, you'll learn the core concepts of the **Model Context Protocol (MCP)** and how to implement it in your AI applications.

Connecting AI applications to external systems to bring rich context to LLMs has often meant writing custom integrations for each use case. This has fragmented AI development between teams within a company and across the industry.

MCP is an open protocol that standardizes how LLMs access tools, data, and prompts from external sources, simplifying how new context is integrated into AI applications. Developed by Anthropic, MCP is based on a client-server architecture that defines the communication details between an MCP client (hosted inside the AI application) and an MCP server (which exposes tools, resources, and prompt templates).

## The Problem: Fragmented AI Development

Connecting AI applications to external systems to bring rich context to LLMs has often meant **writing custom integrations for each use case**. This has fragmented AI development:

- Between teams within a company
- Across the industry

Every new tool, database, or API required custom code, making it difficult to reuse integrations and slowing down development.

## What is MCP?

The **Model Context Protocol (MCP)** is an open protocol that standardizes how LLMs access:

- **Tools** — Functions your LLM can call
- **Data Resources** — External data your LLM can access
- **Prompt Templates** — Reusable prompt patterns

MCP, developed by Anthropic, is based on a **client-server architecture**. It defines the communication details between:

| Component | Description |
|-----------|-------------|
| **MCP Client** | Hosted inside your AI application |
| **MCP Server** | Exposes tools, resources, and prompt templates |

The server can be:
- A **subprocess** launched by the client and running locally
- An **independent process** running remotely

> **Note:** Anthropic launched MCP in November 2024, and the ecosystem has been growing rapidly since then.

### What You'll Do

In this hands-on course, you'll:

- **Make a chatbot MCP-compatible** — Build a chatbot with custom tools for searching academic papers, and transform it into an MCP-compatible application
- **Build an MCP server** — Create a local MCP server that exposes tools, resources, and prompt templates using [FastMCP](https://github.com/jlowin/fastmcp), and test it using MCP Inspector
- **Create an MCP client** — Build an MCP client inside your chatbot to dynamically connect to your server
- **Connect to reference servers** — Connect your chatbot to servers built by Anthropic's MCP team such as `filesystem` (implements filesystem operations) and `fetch` (extracts contents from the web as markdown)
- **Configure Claude Desktop** — Connect to your server and explore how it abstracts away the low-level logic of MCP clients
- **Deploy remotely** — Deploy your MCP server remotely and test it with the Inspector or other MCP-compatible applications

### What You'll Learn

- Understand why MCP makes AI development less fragmented and how it standardizes connections between AI applications and external data sources
- Learn the core components of the client-server architecture of MCP and the underlying communication mechanism
- Build and test MCP servers using FastMCP and MCP Inspector
- Connect MCP clients to multiple servers (your own and third-party)
- Configure Claude Desktop to work with MCP servers
- Deploy MCP servers remotely for production use
- Understand the roadmap for future MCP development: multi-agent architecture, MCP registry API, server discovery, authorization, and authentication

## The MCP Ecosystem

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your LLM Application                         │
│                   (Research Assistant Agent)                    │
│                                                                 │
│                      ┌─────────────┐                            │
│                      │ MCP Client  │                            │
│                      └──────┬──────┘                            │
└─────────────────────────────┼───────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌───────────┐       ┌───────────┐       ┌───────────┐
    │  GitHub   │       │  Google   │       │   File    │
    │   MCP     │       │   Drive   │       │  System   │
    │  Server   │       │   MCP     │       │   MCP     │
    │           │       │  Server   │       │  Server   │
    └───────────┘       └───────────┘       └───────────┘
```

The MCP ecosystem includes a growing number of MCP servers developed by:
- The open source community
- Anthropic's MCP team

## Reference Servers You'll Use

| Server | Purpose |
|--------|---------|
| **filesystem** | Implements filesystem operations (read, write, list files) |
| **fetch** | Extracts contents from the web as markdown |

By the end of the Lab, you'll be able to build **rich-context AI applications** that can connect to a growing ecosystem of MCP servers, with minimal integration work.