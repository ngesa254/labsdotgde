# Deploy the Agent

Deploy the agent to Cloud Run:

```bash
uvx --from google-adk \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=europe-west1 \
  --service_name=adk-agent-safaricom-mcp-access \
  --with_ui \
  . \
  -- \
  --labels=dev-tutorial=codelab-adk \
  --service-account=$SERVICE_ACCOUNT
```

For this lab, allow unauthenticated invocations for testing if prompted.

After deployment, you will see a URL similar to:

```text
https://adk-agent-safaricom-mcp-access-XXXXXXXXXXXX.europe-west1.run.app
```

Copy this URL for the next task.
