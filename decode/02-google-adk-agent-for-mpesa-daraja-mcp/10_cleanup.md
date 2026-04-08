# Clean Up Environment

To avoid incurring charges on your Google Cloud account, clean up the resources created during this lab.

> **Note:** If your Cloud Shell session has expired, re-set your project first:
>
> ```bash
> export PROJECT_ID=$(gcloud config get-value project)
> ```

## Delete Cloud Run Service

```bash
gcloud run services delete adk-agent-safaricom-mcp-access --region=europe-west1 --quiet
```

## Delete Artifact Registry Repository

```bash
gcloud artifacts repositories delete cloud-run-source-deploy --location=europe-west1 --quiet
```

## Delete Service Account

```bash
gcloud iam service-accounts delete lab2-cr-service@${PROJECT_ID}.iam.gserviceaccount.com --quiet
```

## Delete Local Project Files

```bash
rm -rf ~/adk_agent_safaricom_mcp_access
```

## Optional: Also Clean Up Lab 1 Resources

If you are done with both labs and want to remove everything:

```bash
gcloud run services delete safaricom-mpesa-mcp-server --region=europe-west1 --quiet
gcloud iam service-accounts delete mcp-server-sa@${PROJECT_ID}.iam.gserviceaccount.com --quiet
rm -rf ~/mpesa-mcp-server
```

> **Tip:** Alternatively, delete the entire project to remove all resources at once:
>
> ```bash
> gcloud projects delete $PROJECT_ID
> ```
