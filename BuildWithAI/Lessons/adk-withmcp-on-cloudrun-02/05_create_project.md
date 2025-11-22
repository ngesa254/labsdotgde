# Create the Project Folder

## Create the Project Directory

This command creates a main folder for the lab and the agent's source code:

```bash
cd && mkdir zoo_guide_agent && cd zoo_guide_agent
```

## Create the Requirements File

Create the `requirements.txt` file. This file lists the Python libraries your agent needs.

```bash
cloudshell edit requirements.txt
```

The editor will open above the terminal. Add the following dependencies and save:

```
google-adk==1.14.0
langchain-community==0.3.27
wikipedia==1.4.0
```

> ⚠️ **Note:** Make sure to add these lines in the editor, not in the terminal. If you accidentally paste them in the terminal, you'll see errors like `bash: google-adk==1.14.0: command not found`.

| Package | Purpose |
|---------|---------|
| `google-adk` | Google Agent Development Kit for building AI agents |
| `langchain-community` | Community integrations for LangChain |
| `wikipedia` | Wikipedia API wrapper for accessing Wikipedia content |

---

## Set Environment Variables

Set variables for your current project ID, project number, and create a dedicated service account:

```bash
export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export SA_NAME=lab2-cr-service
export SERVICE_ACCOUNT="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
```

## Create the Service Account

Create a dedicated service account for your project:

```bash
gcloud iam service-accounts create ${SA_NAME} \
    --display-name="Service Account for lab 2"
```

You should see:

```
Created service account [lab2-cr-service].
```

---

## Configure the Agent Environment

Create and open a `.env` file to configure the agent:

```bash
cloudshell edit .env
```

The `cloudshell edit` command will open the `.env` file in the editor above the terminal.

Add the following to specify the model:

```
MODEL="gemini-2.5-flash"
```

---

## Add the MCP Server URL

### Option A: Using the MCP Server from Lab 1 (Recommended)

If you completed Lab 1, follow these steps to use the MCP server you created:

**1. Grant the service account permission to call the MCP server:**

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/run.invoker"
```

You should see output confirming the IAM policy was updated:

```
Updated IAM policy for project [your-project-id].
bindings:
...
- members:
  - serviceAccount:lab2-cr-service@your-project-id.iam.gserviceaccount.com
  - user:your-email@gmail.com
  role: roles/run.invoker
...
```

**2. Add the MCP server URL to your `.env` file:**

```bash
echo -e "\nMCP_SERVER_URL=https://zoo-mcp-server-${PROJECT_NUMBER}.europe-west1.run.app/mcp" >> .env
```

### Option B: Using a Public MCP Server

If you are using a public MCP server link provided during a live event, run the following command and replace `PROJECT_NUMBER` with the value provided:

```bash
echo -e "\nMCP_SERVER_URL=https://zoo-mcp-server-PROJECT_NUMBER.europe-west1.run.app/mcp" >> .env
```

---

## Verify Your Configuration

Your `.env` file should now contain:

```
MODEL="gemini-2.5-flash"
MCP_SERVER_URL=https://zoo-mcp-server-683099143523.europe-west1.run.app/mcp
```

Where `683099143523` is your project number (yours will be different).

You can verify by running:

```bash
cat .env
```