# Deploying to Cloud Run

Now deploy the MCP server to Cloud Run directly from the source code.

## Create the Dockerfile

Create and open a new `Dockerfile` for deploying to Cloud Run:

```bash
cloudshell edit ~/mpesa-mcp-server/Dockerfile
```

Include the following code in the Dockerfile to use the `uv` tool for running the `server.py` file:

```dockerfile
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN uv sync

EXPOSE 8080

CMD ["uv", "run", "server.py"]
```

## Create a Service Account

Create a service account named `mcp-server-sa`:

```bash
gcloud iam service-accounts create mcp-server-sa --display-name="MCP Server Service Account"
```

## Return to the Project Directory

The `gcloud iam` command may leave you at the `~` home directory. Before deploying from source, return to the MCP server project folder and confirm the expected files are present:

```bash
cd ~/mpesa-mcp-server
pwd
ls
```

You should see output similar to:

```text
/home/<your-username>/mpesa-mcp-server
Dockerfile
pyproject.toml
server.py
uv.lock
```

## Deploy to Cloud Run

Run the `gcloud` command to deploy the application to Cloud Run:

```bash
cd ~/mpesa-mcp-server
gcloud run deploy safaricom-mpesa-mcp-server \
    --service-account=mcp-server-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=. \
    --labels=dev-tutorial=codelab-mcp
```

> **Important:** The `--no-allow-unauthenticated` flag requires authentication. This is critical for security.

## Confirm Artifact Registry Creation

Since this is your first time deploying to Cloud Run from source code, you will see:

```text
Deploying from source requires an Artifact Registry Docker repository to store built containers. A repository named
[cloud-run-source-deploy] in region [europe-west1] will be created.

Do you want to continue (Y/n)?
```

Type `Y` and press `Enter`.

## Verify Deployment

After a few minutes, you will see a message like:

```text
OK Building and deploying new service... Done.
  OK Creating Container Repository...
  OK Validating Service...
  OK Uploading sources...
  OK Building Container...
  OK Creating Revision...
  OK Routing traffic...
Done.
Service [safaricom-mpesa-mcp-server] revision [safaricom-mpesa-mcp-server-00001-74h] has been deployed and is serving 100 percent of traffic.
Service URL: https://safaricom-mpesa-mcp-server-683099143523.europe-west1.run.app
```

> **Note:** If you try to visit the Service URL directly in your browser, you will see **"Error Forbidden"** because your MCP server requires authentication.

You have deployed your Safaricom M-PESA Express MCP server. Next, you will connect to it from Gemini CLI.
