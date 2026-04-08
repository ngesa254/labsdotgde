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

The MCP server reads consumer credentials from environment variables at runtime. Before deploying, you need a **Consumer Key** and **Consumer Secret** from the Safaricom Daraja developer portal.

### How to Get Your Credentials

1. **Create an account** at [developer.safaricom.co.ke](https://developer.safaricom.co.ke/) if you don't have one
2. **Sign in** and navigate to [My Apps](https://developer.safaricom.co.ke/dashboard/myapps)
3. Click the green **Create Sandbox App** button in the top right
4. Give your app a name (e.g. `my-decode-app`)
5. Select **M-PESA EXPRESS Sandbox** as the product and submit
6. Your new app will appear on the My Apps page with a **Consumer Key** and **Consumer Secret**

![Daraja My Apps Dashboard — each sandbox app shows a Consumer Key and Consumer Secret with copy buttons](image-daraja-myapps.png)

7. Click the **copy icon** next to **Consumer Key** and **Consumer Secret** to copy each value

### Export Your Credentials

Paste the values you copied from the Daraja portal into these export commands:

```bash
export MPESA_CONSUMER_KEY="paste_your_consumer_key_here"
export MPESA_CONSUMER_SECRET="paste_your_consumer_secret_here"
```

> **Important:** These must be the credentials from **your own** Daraja sandbox app. Do not share your credentials with others or commit them to version control.

### About the Sandbox

| Question | Answer |
|----------|--------|
| **Will I be charged real money?** | No. The sandbox simulates M-PESA transactions without debiting your wallet. |
| **What short code does the sandbox use?** | `174379` — a shared test short code provided by Safaricom. |
| **What passkey do I use?** | The sandbox passkey is public: `bfb279f9aa9b...` (already hardcoded in the MCP server). |
| **How do I go to production?** | Complete the [Go Live](https://developer.safaricom.co.ke/go-live) process on the Daraja portal with a real pay bill or till number. |

> **More info:** Visit the [M-PESA Express API documentation](https://developer.safaricom.co.ke/apis/MpesaExpressSimulate) for the full request/response reference, error codes, and integration steps.

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

### Troubleshooting: Service Account Permission Error

If the deploy command fails with:

```text
Permission 'iam.serviceaccounts.actAs' denied on service account mcp-server-sa@...
```

This means your user account cannot impersonate the service account. Deploy **without** the `--service-account` flag to use the default Compute Engine service account instead:

```bash
gcloud run deploy safaricom-mpesa-mcp-server \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=. \
    --set-env-vars="MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY},MPESA_CONSUMER_SECRET=${MPESA_CONSUMER_SECRET}" \
    --labels=dev-tutorial=codelab-mcp
```

This works for the workshop. In production, always use a dedicated service account with the minimum required permissions.

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
