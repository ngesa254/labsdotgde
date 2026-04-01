# Outro

Use this section if you want to clean up the lab resources and start the journey again from a fresh state in the same Google Cloud project.

## Reset the Lab Resources

Delete the deployed Cloud Run service:

```bash
gcloud run services delete safaricom-mpesa-mcp-server --region=europe-west1
```

Delete the service account created for the MCP server:

```bash
gcloud iam service-accounts delete mcp-server-sa@$(gcloud config get-value project).iam.gserviceaccount.com
```

Before deleting the local project folder, return to your home directory:

```bash
cd ~
pwd
```

Then delete the local project files:

```bash
rm -rf ~/mpesa-mcp-server
```

Delete the Artifact Registry repository created by source-based Cloud Run deploys:

```bash
gcloud artifacts repositories delete cloud-run-source-deploy --location=europe-west1
```

## Verify That the Reset Worked

Run the following commands:

```bash
gcloud run services list --region=europe-west1
gcloud iam service-accounts list --filter="email:mcp-server-sa@"
ls ~
```

You should see:

- no Cloud Run services listed for this lab
- no `mcp-server-sa` service account
- no `mpesa-mcp-server` folder in your home directory

## Start the Lab Again

To restart from a clean state, go back to:

1. [Project Setup](./02_setup.md)
2. [Open Cloud Shell Editor](./03_cloudshell.md)
3. [Enable APIs](./04_enabling_apis.md)

## Recommended Approach

If you want the cleanest possible rerun, create a brand new Google Cloud project and run the lab there instead of reusing the same project.

## Quick Redeploy (Without Full Reset)

If you only need to update `server.py` and push a new revision (e.g. after adding the MCP prompt in Step 10), you can redeploy without deleting anything:

1. Update your server code:

```bash
cloudshell edit ~/mpesa-mcp-server/server.py
```

2. Re-export credentials and deploy:

```bash
cd ~/mpesa-mcp-server
export MPESA_CONSUMER_KEY="7WS02XptTqkWBUl1mPWn4Vj0tMxjyWF1MwAneRRGxwl2d2lq"
export MPESA_CONSUMER_SECRET="2oNVkVPDebg0NiBteUUbjRlLEtnbHHkGKDyqLDbuAxHJ8Ax5M9K2NWrwzBH5zwDH"

gcloud run deploy safaricom-mpesa-mcp-server \
    --region=europe-west1 \
    --source=. \
    --set-env-vars="MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY},MPESA_CONSUMER_SECRET=${MPESA_CONSUMER_SECRET}" \
    --labels=dev-tutorial=codelab-mcp
```

3. Refresh your ID token (it expires every hour):

```bash
export ID_TOKEN=$(gcloud auth print-identity-token)
```

Then recreate `~/.gemini/settings.json` with the new token (see [Step 08](./08_addmcp_to_gemini_cli.md)).