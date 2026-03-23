# Clean Up Environment

To avoid incurring charges on your Google Cloud account, clean up the resources created during this lab.

## Delete Cloud Run Service

Delete the Zoo Tour Guide service:

```bash
gcloud run services delete zoo-tour-guide --region=europe-west1 --quiet
```

## Delete Artifact Registry Repository

Delete the container repository that was created during deployment:

```bash
gcloud artifacts repositories delete cloud-run-source-deploy --location=europe-west1 --quiet
```

---

## (Optional) Additional Cleanup

### Delete the Service Account

If you no longer need the service account created for this lab:

```bash
gcloud iam service-accounts delete lab2-cr-service@$PROJECT_ID.iam.gserviceaccount.com --quiet
```

### Delete Local Files

Remove the project directory from Cloud Shell:

```bash
rm -rf ~/zoo_guide_agent
```

### Delete the MCP Server from Lab 1

If you're also done with Lab 1 resources:

```bash
gcloud run services delete zoo-mcp-server --region=europe-west1 --quiet
gcloud iam service-accounts delete mcp-server-sa@$PROJECT_ID.iam.gserviceaccount.com --quiet
```

### Delete the Entire Project

If you want to delete all resources at once:

```bash
gcloud projects delete $PROJECT_ID
```

> ⚠️ **Warning:** Deleting the project will remove ALL resources and cannot be undone.

---

## Congratulations! 🎉

You have successfully:

- ✅ Built a multi-agent system using Google ADK
- ✅ Connected an ADK agent to a remote MCP server
- ✅ Integrated Wikipedia as an external knowledge source
- ✅ Deployed the agent to Cloud Run with a web UI
- ✅ Tested the agent with real queries

**What's Next?**

Continue exploring the ADK with more advanced topics:

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Samples Repository](https://github.com/google/adk-samples)
- [Building Custom Tools](https://google.github.io/adk-docs/tools/)