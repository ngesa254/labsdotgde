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

## Set Daraja Sandbox Credentials

The MCP server reads consumer credentials from environment variables at runtime. Before deploying, you need to get your **Consumer Key** and **Consumer Secret** from the Safaricom Daraja developer portal.

### How to Get Your Credentials

1. Go to [developer.safaricom.co.ke/dashboard/myapps](https://developer.safaricom.co.ke/dashboard/myapps)
2. Log in with your Daraja account (or create one if you haven't already)
3. You will see your sandbox apps listed under **My Apps**

![Daraja My Apps Dashboard](image-daraja-myapps.png)

4. Find your sandbox app (for this workshop, use the shared app **decodegemini**)
5. Click the copy icon next to **Consumer Key** and **Consumer Secret** to copy them

### Export Your Credentials

Replace the values below with the Consumer Key and Consumer Secret from your Daraja app:

```bash
export MPESA_CONSUMER_KEY="your_consumer_key_here"
export MPESA_CONSUMER_SECRET="your_consumer_secret_here"
```

For this workshop, we are sharing the **decodegemini** sandbox app. Use these credentials:

```bash
export MPESA_CONSUMER_KEY="7WS02XptTqkWBUl1mPWn4Vj0tMxjyWF1MwAneRRGxwl2d2lq"
export MPESA_CONSUMER_SECRET="2oNVkVPDebg0NiBteUUbjRlLEtnbHHkGKDyqLDbuAxHJ8Ax5M9K2NWrwzBH5zwDH"
```

> **Want to use your own app?** Click **Create Sandbox App** on the Daraja portal, select **M-PESA EXPRESS Sandbox** as the product, and copy the generated Consumer Key and Consumer Secret.

> **Will I be charged real money?** No. The sandbox environment does not process real M-PESA transactions. However, when you move to **production Go Live**, real money is involved. **Any test transactions made against a live short code will be reversed** — but always use the sandbox for development and testing.

## Deploy to Cloud Run

Run the `gcloud` command to deploy the application to Cloud Run, passing the Daraja credentials as environment variables:

```bash
cd ~/mpesa-mcp-server
gcloud run deploy safaricom-mpesa-mcp-server \
    --service-account=mcp-server-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=. \
    --set-env-vars="MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY},MPESA_CONSUMER_SECRET=${MPESA_CONSUMER_SECRET}" \
    --labels=dev-tutorial=codelab-mcp
```

> **Important:** The `--no-allow-unauthenticated` flag requires authentication. This is critical for security.
> The `--set-env-vars` flag passes your Daraja credentials to the running container. In production, use **Secret Manager** instead of plain environment variables.

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
