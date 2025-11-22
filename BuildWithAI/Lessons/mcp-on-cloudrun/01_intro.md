# How to Deploy a Secure MCP Server on Cloud Run

## Introduction

### Overview

In this lab, you will build and deploy a Model Context Protocol (MCP) server. MCP servers are useful for providing LLMs with access to external tools and services. You will configure it as a secure, production-ready service on Cloud Run that can be accessed from multiple clients. Then you will connect to the remote MCP server from Gemini CLI.

### What You'll Do

We will use [FastMCP](https://github.com/jlowin/fastmcp) to create a zoo MCP server that has two tools:

- `get_animals_by_species` — Retrieve animals filtered by species
- `get_animal_details` — Get detailed information about a specific animal

FastMCP provides a quick, Pythonic way to build MCP servers and clients.

### What You'll Learn

- Deploy the MCP server to Cloud Run
- Secure your server's endpoint by requiring authentication for all requests, ensuring only authorized clients and agents can communicate with it
- Connect to your secure MCP server endpoint from Gemini CLI