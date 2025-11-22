# Enable APIs

In the terminal, enable the APIs:

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```

If prompted to authorize, click **Authorize** to continue.

This command may take a few minutes to complete, but it should eventually produce a successful message similar to this one:

```
Operation "operations/acf.p2-73d90d00-47ee-447a-b600" finished successfully.
```

## What These APIs Do

| API | Purpose |
|-----|---------|
| `run.googleapis.com` | Cloud Run — for deploying and running your MCP server |
| `artifactregistry.googleapis.com` | Artifact Registry — for storing your container images |
| `cloudbuild.googleapis.com` | Cloud Build — for building your container images |