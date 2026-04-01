# Clean Up Environment

To avoid incurring charges on your Google Cloud account, clean up the resources created during this lab.

## Delete Cloud Run Service

```bash
gcloud run services delete adk-agent-safaricom-mcp-access --region=europe-west1 --quiet
```

## Delete Artifact Registry Repository

```bash
gcloud artifacts repositories delete cloud-run-source-deploy --location=europe-west1 --quiet
```

## Optional Additional Cleanup

```bash
gcloud iam service-accounts delete lab2-cr-service@$PROJECT_ID.iam.gserviceaccount.com --quiet
rm -rf ~/adk_agent_safaricom_mcp_access
gcloud run services delete safaricom-mpesa-mcp-server --region=europe-west1 --quiet
gcloud iam service-accounts delete mcp-server-sa@$PROJECT_ID.iam.gserviceaccount.com --quiet
```
