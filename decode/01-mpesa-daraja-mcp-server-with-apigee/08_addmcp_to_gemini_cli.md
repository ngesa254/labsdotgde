# Add the Remote MCP Server to Gemini CLI

Now that you've successfully deployed a remote MCP server, you can connect to it using various applications like Google Code Assist or Gemini CLI. In this section, we will establish a connection to your new remote MCP server using Gemini CLI.

> **Note:** Gemini CLI comes pre-installed in Cloud Shell.

## Grant Permissions to Call the MCP Server

Give your user account permission to call the remote MCP server:

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="user:$(gcloud config get-value account)" \
    --role="roles/run.invoker"
```

## Set Environment Variables

Save your Google Cloud credentials and project number in environment variables:

```bash
export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
export ID_TOKEN=$(gcloud auth print-identity-token)
```

Verify the values are set:

```bash
echo $PROJECT_NUMBER
echo $ID_TOKEN
```

You should see your project number (e.g., `683099143523`) and a long JWT token string.

## Configure Gemini CLI

Create the `.gemini` folder if it doesn't already exist:

```bash
mkdir -p ~/.gemini
```

### Option A: Generate settings.json with a command (Recommended)

Run this command to create the settings file with your actual values substituted:

```bash
cat > ~/.gemini/settings.json << EOF
{
  "ide": {
    "hasSeenNudge": true
  },
  "mcpServers": {
    "zoo-remote": {
      "httpUrl": "https://zoo-mcp-server-${PROJECT_NUMBER}.europe-west1.run.app/mcp",
      "headers": {
        "Authorization": "Bearer ${ID_TOKEN}"
      }
    }
  },
  "security": {
    "auth": {
      "selectedType": "cloud-shell"
    }
  }
}
EOF
```

Verify the file was created correctly:

```bash
cat ~/.gemini/settings.json
```

The output should show your actual project number and token values (not `${PROJECT_NUMBER}` or `${ID_TOKEN}`).

### Option B: Edit manually

If you prefer to edit manually:

```bash
cloudshell edit ~/.gemini/settings.json
```

> **⚠️ Important:** JSON files do NOT interpret bash variables. You must replace `${PROJECT_NUMBER}` and `${ID_TOKEN}` with the actual values. Copy the values from `echo $PROJECT_NUMBER` and `echo $ID_TOKEN` and paste them directly into the file.

Example with actual values:

```json
{
  "ide": {
    "hasSeenNudge": true
  },
  "mcpServers": {
    "zoo-remote": {
      "httpUrl": "https://zoo-mcp-server-683099143523.europe-west1.run.app/mcp",
      "headers": {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImt..."
      }
    }
  },
  "security": {
    "auth": {
      "selectedType": "cloud-shell"
    }
  }
}
```

## Start Gemini CLI

Start the Gemini CLI in Cloud Shell:

```bash
gemini
```

You may need to press `Enter` to accept some default settings.

## Verify MCP Connection

Have Gemini list the MCP tools available to it:

```
/mcp
```

You should see output similar to:

```
Configured MCP servers:

🟢 zoo-remote - Ready (2 tools)
  Tools:
  - get_animal_details
  - get_animals_by_species
```

## Test the MCP Server

Ask Gemini to find something in the zoo:

```
Where can I find penguins?
```

The Gemini CLI should know to use the `zoo-remote` MCP Server and will ask if you would like to allow execution of MCP.

Use the down arrow, then press `Enter` to select:

```
Yes, always allow all tools from server "zoo-remote"
```

The output should show the correct answer and a display box showing that the MCP server was used.

**Congratulations!** You have successfully deployed a remote MCP server to Cloud Run and tested it using Gemini CLI.

When you are ready to end your session, type `/quit` and press `Enter` to exit Gemini CLI.

---

## Troubleshooting

### Authentication Error (401 Unauthorized)

If you see an error like this when calling MCP tools:

```
Error POSTing to endpoint (HTTP 401):
<h1>Error: Unauthorized</h1>
<h2>Your client does not have permission to the requested URL</h2>
```

**This is likely because the ID Token has expired.** ID tokens are short-lived (typically 1 hour) and need to be refreshed.

**To fix this:**

1. Type `/quit` and press `Enter` to exit Gemini CLI.

2. Regenerate the ID token:

   ```bash
   export ID_TOKEN=$(gcloud auth print-identity-token)
   ```

3. Regenerate the settings file:

   ```bash
   cat > ~/.gemini/settings.json << EOF
   {
     "ide": {
       "hasSeenNudge": true
     },
     "mcpServers": {
       "zoo-remote": {
         "httpUrl": "https://zoo-mcp-server-${PROJECT_NUMBER}.europe-west1.run.app/mcp",
         "headers": {
           "Authorization": "Bearer ${ID_TOKEN}"
         }
       }
     },
     "security": {
       "auth": {
         "selectedType": "cloud-shell"
       }
     }
   }
   EOF
   ```

4. Restart Gemini CLI:

   ```bash
   gemini
   ```

### OAuth Discovery Error

If you see:

```
🔍 Attempting OAuth discovery for 'zoo-remote'...
❌ 'zoo-remote' requires authentication but no OAuth configuration found
```

This usually means the settings.json file has `${PROJECT_NUMBER}` or `${ID_TOKEN}` as literal strings instead of actual values. Follow **Option A** above to regenerate the file correctly.

### Service Account Already Exists

If you see an error when creating the service account:

```
ERROR: (gcloud.iam.service-accounts.create) Service account mcp-server-sa already exists
```

This is fine — the service account was already created previously. You can continue with the deployment.

### Bash Syntax Errors When Pasting JSON

If you accidentally paste JSON into the terminal and see errors like:

```
bash: ide:: command not found
bash: hasSeenNudge:: command not found
```

This happens when JSON is pasted directly into bash instead of into a file. Use **Option A** above or make sure you're editing the file in the Cloud Shell Editor, not pasting into the terminal.