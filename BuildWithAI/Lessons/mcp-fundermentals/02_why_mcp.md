# Why MCP?

## Overview

In this lesson, we'll explore why the Model Context Protocol makes AI development less fragmented and how it standardizes connections between AI applications and external data sources.

## The Core Principle

**Models are only as good as the context provided to them.**

You can have an incredibly intelligent model at the frontier, but if it doesn't have the ability to connect to the outside world and pull in the data and context necessary, it's not as useful as it can possibly be.

## What MCP Does

The **Model Context Protocol** is an open-source protocol that standardizes how your large language model connects and works with your tools and data sources.

### The Goal: Build Once, Use Everywhere

Instead of reinventing the wheel for each integration, MCP standardizes the way AI applications connect with data sources—the same way **REST** standardizes how web applications communicate with backends and other systems.

| Without MCP | With MCP |
|-------------|----------|
| Build custom integration for each model + data source combination | Build integration once, use across all models and applications |
| Repeated work across teams | Reusable servers across organization |
| Fragmented development | Standardized protocol |

## Everything Can Be Done Without MCP, But...

As we think about a world in which many different models communicate with many different data sources (and even with each other), we want to make sure we're speaking the same language.

### The Problem Without MCP

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Model A   │────▶│  Custom     │────▶│   GitHub    │
└─────────────┘     │  Code 1     │     └─────────────┘
                    └─────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Model B   │────▶│  Custom     │────▶│   GitHub    │
└─────────────┘     │  Code 2     │     └─────────────┘
                    └─────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Model A   │────▶│  Custom     │────▶│   Asana     │
└─────────────┘     │  Code 3     │     └─────────────┘
                    └─────────────┘
```

**Problem:** Building the same integration over and over again for different models and data sources.

### The Solution With MCP

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Model A   │────▶│             │     │   GitHub    │
└─────────────┘     │             │────▶│     MCP     │
                    │             │     │   Server    │
┌─────────────┐     │  Standard   │     └─────────────┘
│   Model B   │────▶│     MCP     │
└─────────────┘     │  Protocol   │     ┌─────────────┐
                    │             │────▶│    Asana    │
┌─────────────┐     │             │     │     MCP     │
│   Model C   │────▶│             │     │   Server    │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Solution:** Build once, connect anywhere.

## Inspired by Proven Protocols

MCP stands on the shoulders of other successful protocols:

### Language Server Protocol (LSP)

Developed by Microsoft in 2016, **LSP** standardizes how Integrated Development Environments (IDEs) interact with language-specific tools.

**Before LSP:** Write extensions for each language × each IDE combination
**After LSP:** Write once per language, works across all IDEs

MCP applies this same principle to AI applications and data sources.

## Demo: MCP in Action

### Scenario: Triaging GitHub Issues to Asana

With just a few lines of code, you can:

1. **Connect to GitHub MCP Server** — Read issues from a repository
2. **Connect to Asana MCP Server** — Create and assign tasks
3. **Use natural language** — "Triage these issues and create Asana tickets"

**What's happening:**
- Reading from one data source (GitHub)
- Writing to another data source (Asana)
- Human-in-the-loop verification for actions
- All through natural language interface

This is the power of MCP—seamless integration with external data sources with minimal code.

## The Traditional Approach (Without MCP)

When building AI applications that connect to external data, you typically need to manage:

| Concern | Questions |
|---------|-----------|
| **Tool Storage** | Where do you store your tools? |
| **Prompts** | Where do you store custom prompts? |
| **Data Access** | Where do you store the data access layer? |
| **Authentication** | How do you handle authentication logic? |

**Result:** Repeating the wheel over and over again—many different AI applications talking to similar data sources but written in different ways.

## The MCP Approach

### Separation of Concerns

With MCP, we shift the burden of responsibility and separate concerns in a clean fashion:

```
┌─────────────────────────────────────────────────────────────────┐
│                  MCP-Compatible Applications                    │
│         (AI Assistants, Agents, Desktop Apps, etc.)             │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌───────────┐       ┌───────────┐       ┌───────────┐
    │ Data      │       │   CRM     │       │  Version  │
    │ Stores    │       │ (HubSpot, │       │  Control  │
    │  MCP      │       │Salesforce)│       │   (Git)   │
    │ Server    │       │    MCP    │       │    MCP    │
    │           │       │  Server   │       │  Server   │
    └───────────┘       └───────────┘       └───────────┘
```

### Key Benefits

- **Model Agnostic** — Works with any LLM
- **Open Source** — Tools and data connectivity provided by the community
- **Reusable** — Build or use servers across multiple applications
- **Natural Language Interface** — Talk to data stores without writing custom logic

---

## Benefits for Different Audiences

| Audience | Benefits |
|----------|----------|
| **Application Developers** | Connect to an MCP server with very little work |
| **API Developers** | Build the MCP server once, adopt it everywhere |
| **End Users** | MCP abstracted away—just provide a URL to access data |
| **Enterprises** | Separate concerns, build standalone integrations different teams can use |

---

## The Growing MCP Ecosystem

The MCP ecosystem is growing rapidly:

- **Large Companies** — Building MCP servers for their platforms
- **Startups** — Developing MCP integrations at the frontier
- **Open Source Community** — Creating servers for popular tools and APIs
- **Private Development** — Internal servers for enterprise use cases

### MCP SDKs

Software Development Kits available across multiple languages:
- Python
- TypeScript/JavaScript
- And more, developed by the open source community

### MCP-Compatible Applications

- Web applications
- Desktop applications (like Claude Desktop)
- Agentic products

## Common Questions About MCP

### Who writes MCP servers?

**Anyone can!**

- You can build your own MCP servers
- Use community-adopted servers
- Download reference servers from Anthropic

In upcoming lessons, you'll learn how to build your own MCP servers.

### How are MCP servers different from APIs?

Think of an MCP server as a **gateway or wrapper** on top of an API:

| APIs | MCP Servers |
|------|-------------|
| Call endpoints directly | Use natural language |
| Handle request/response formatting | MCP server handles formatting |
| Manage authentication yourself | MCP server manages auth |

**MCP servers let you use natural language instead of direct API calls.**

### Do MCP servers only support tool use?

**No!** While MCP servers do provide functions and schemas (tools), they also provide:

- **Resources** — Access to data
- **Prompts** — Reusable prompt templates

We'll explore all of these in the next lesson.

## Summary

**Why MCP?**

- **Standardization** — One protocol for connecting AI apps to external data
- **Reusability** — Build once, use everywhere
- **Separation of Concerns** — Clean architecture
- **Model Agnostic** — Works with any LLM
- **Open Source** — Growing ecosystem of servers and clients

With very little code, you can bring rich context into your AI applications by connecting to a growing ecosystem of MCP servers.

## Next Steps

In the next lesson, we'll explore **how MCP works** under the hood and introduce:

- Hosts
- Clients
- Servers
- Underlying primitives: Resources, Tools, and Prompts

**Continue to the next lesson →**