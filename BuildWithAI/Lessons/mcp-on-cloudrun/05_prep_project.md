# Prepare Your Python Project

## Create the Project Folder

Create a folder named `mcp-on-cloudrun` to store the source code for deployment:

```bash
mkdir mcp-on-cloudrun && cd mcp-on-cloudrun
```

## Initialize the Python Project

Create a Python project with the `uv` tool to generate a `pyproject.toml` file:

```bash
uv init --description "Example of deploying an MCP server on Cloud Run" --bare --python 3.13
```

You should see:

```
Initialized project `mcp-on-cloudrun`
```

## Verify the Project Configuration

The `uv init` command creates a `pyproject.toml` file for your project. To view the contents of the file, run:

```bash
cat pyproject.toml
```

The output should look like the following:

```toml
[project]
name = "mcp-on-cloudrun"
version = "0.1.0"
description = "Example of deploying an MCP server on Cloud Run"
requires-python = ">=3.13"
dependencies = []
```