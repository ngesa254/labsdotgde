# Prepare the Application for Deployment

With your local environment ready, the next step is to prepare your Google Cloud project for the deployment.

This involves:
1. A final check of your agent's file structure to ensure it's compatible with the deployment command
2. Configuring a critical IAM permission that allows your deployed Cloud Run service to act on your behalf and call the Vertex AI models

Completing this step ensures the cloud environment is ready to run your agent successfully.

---

## Load Environment Variables

Load the variables into your shell session by running the `source` command:

```bash
source .env
```

---

## Grant Vertex AI Permissions

Grant the service account the **Vertex AI User** role, which gives it permission to make predictions and call Google's models:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
```

You should see output confirming the IAM policy was updated:

```
Updated IAM policy for project [your-project-id].
bindings:
...
- members:
  - serviceAccount:lab2-cr-service@your-project-id.iam.gserviceaccount.com
  role: roles/aiplatform.user
...
```

---

## Verify Your File Structure

Before deploying, ensure your `zoo_guide_agent` directory has the correct structure:

```
zoo_guide_agent/
├── __init__.py        # Package identifier
├── agent.py           # Main agent code with root_agent
├── requirements.txt   # Python dependencies
└── .env               # Environment variables (MODEL, MCP_SERVER_URL)
```

You can verify with:

```bash
ls -la
```

---

## Understanding the IAM Roles

| Role | Service Account | Purpose |
|------|-----------------|---------|
| `roles/run.invoker` | `lab2-cr-service` | Allows the agent to call the MCP server on Cloud Run |
| `roles/aiplatform.user` | `lab2-cr-service` | Allows the agent to call Vertex AI / Gemini models |

Your application is now ready for deployment!