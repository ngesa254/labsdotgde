# Deploying to Cloud Run

Now deploy the MCP server to Cloud Run directly from the source code.

## Create the Dockerfile

Create and open a new `Dockerfile` for deploying to Cloud Run:

```bash
cloudshell edit ~/mcp-on-cloudrun/Dockerfile
```

Include the following code in the Dockerfile to use the `uv` tool for running the `server.py` file:

```dockerfile
# Use the official Python image
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project into /app
COPY . /app
WORKDIR /app

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN uv sync

EXPOSE $PORT

# Run the FastMCP server
CMD ["uv", "run", "server.py"]
```

## Create a Service Account

Create a service account named `mcp-server-sa`:

```bash
gcloud iam service-accounts create mcp-server-sa --display-name="MCP Server Service Account"
```

You should see:

```
Created service account [mcp-server-sa].
```

## Deploy to Cloud Run

Run the `gcloud` command to deploy the application to Cloud Run:

```bash
cd ~/mcp-on-cloudrun
gcloud run deploy zoo-mcp-server \
    --service-account=mcp-server-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=. \
    --labels=dev-tutorial=codelab-mcp
```

> **Important:** The `--no-allow-unauthenticated` flag requires authentication. This is critical for security — without it, anyone could call your MCP server and potentially cause damage to your system.

## Confirm Artifact Registry Creation

Since this is your first time deploying to Cloud Run from source code, you will see:

```
Deploying from source requires an Artifact Registry Docker repository to store built containers. A repository named
[cloud-run-source-deploy] in region [europe-west1] will be created.

Do you want to continue (Y/n)?
```

Type `Y` and press `Enter`. This creates an Artifact Registry repository for storing the MCP server Docker container for the Cloud Run service.

## Verify Deployment

After a few minutes, you will see a message like:

```
OK Building and deploying new service... Done.
  OK Creating Container Repository...
  OK Validating Service...
  OK Uploading sources...
  OK Building Container...
  OK Creating Revision...
  OK Routing traffic...
Done.
Service [zoo-mcp-server] revision [zoo-mcp-server-00001-74h] has been deployed and is serving 100 percent of traffic.
Service URL: https://zoo-mcp-server-683099143523.europe-west1.run.app
```

> **Note:** If you try to visit the Service URL directly in your browser, you will see **"Error Forbidden"** because your MCP server requires authentication. This is expected behavior.

You have deployed your MCP server! Now you can connect to it from a client.