# Create the Project Folder

## Create the Project Directory

```bash
cd && mkdir adk_agent_safaricom_mcp_access && cd adk_agent_safaricom_mcp_access
```

## Create the Requirements File

Create the `requirements.txt` file:

```bash
cloudshell edit requirements.txt
```

Add:

```text
google-adk==1.14.0
python-dotenv==1.0.1
google-cloud-logging==3.11.0
```

> **Tip:** If `cloudshell edit` fails with a "Cannot send messages to client" error, use `cat` instead:
>
> ```bash
> cat > requirements.txt << 'EOF'
> google-adk==1.14.0
> python-dotenv==1.0.1
> google-cloud-logging==3.11.0
> EOF
> ```

## Set Environment Variables

```bash
export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export SA_NAME=lab2-cr-service
export SERVICE_ACCOUNT="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
```

## Create the Service Account

```bash
gcloud iam service-accounts create ${SA_NAME} \
    --display-name="Service Account for lab 2"
```

## Configure the Agent Environment

Create the `.env` file with your project's MCP server URL. This uses shell variable expansion to bake the correct URL into the file:

```bash
cat > .env << EOF
MODEL="gemini-2.5-flash"
MCP_SERVER_URL=https://safaricom-mpesa-mcp-server-${PROJECT_NUMBER}.europe-west1.run.app/mcp
EOF
```

Verify the `.env` file was written with the correct URL (the project number should be a real number, not a variable):

```bash
cat .env
```

You should see output like:

```text
MODEL="gemini-2.5-flash"
MCP_SERVER_URL=https://safaricom-mpesa-mcp-server-123456789012.europe-west1.run.app/mcp
```

> **Important:** If the URL still shows `${PROJECT_NUMBER}`, run `echo $PROJECT_NUMBER` to verify the variable is set, then re-run the `cat > .env` command above.

If you are using a shared workshop deployment, replace the URL with the value provided to you.
