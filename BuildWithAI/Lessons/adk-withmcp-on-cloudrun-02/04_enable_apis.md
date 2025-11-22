# Before You Begin

## Enable APIs and Set Environment Variables

Enable all necessary services for the ADK agent deployment:

```bash
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    aiplatform.googleapis.com \
    compute.googleapis.com
```

This command may take a few minutes to complete.

### Expected Output

```
Operation "operations/acat.p2-[GUID]" finished successfully.
```

## What These APIs Do

| API | Purpose |
|-----|---------|
| `run.googleapis.com` | Cloud Run — for deploying and running your ADK agent |
| `artifactregistry.googleapis.com` | Artifact Registry — for storing your container images |
| `cloudbuild.googleapis.com` | Cloud Build — for building your container images |
| `aiplatform.googleapis.com` | Vertex AI — for accessing Gemini models |
| `compute.googleapis.com` | Compute Engine — required for some AI Platform features |

> **Note:** If you completed Lab 1 in the same project, some of these APIs may already be enabled. The command will simply skip those that are already active.