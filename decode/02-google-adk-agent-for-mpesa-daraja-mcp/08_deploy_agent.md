# Deploy the Agent Using the ADK CLI

With your local code ready and your Google Cloud project prepared, it's time to deploy the agent.

You will use the `adk deploy cloud_run` command, a convenient tool that automates the entire deployment workflow. This single command:

1. Packages your code
2. Builds a container image
3. Pushes it to Artifact Registry
4. Launches the service on Cloud Run

This makes your agent accessible on the web!

---

## Deploy

Run the following commands to deploy your agent. The `uvx` command allows you to run command line tools published as Python packages without requiring a global installation of those tools.

> **Note:** This deploy command will take a few minutes to finish running.

```bash
uvx --from google-adk \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=europe-west1 \
  --service_name=zoo-tour-guide \
  --with_ui \
  . \
  -- \
  --labels=dev-tutorial=codelab-adk \
  --service-account=$SERVICE_ACCOUNT
```

---

## Accept Prompts

### Artifact Registry Repository

You may be prompted with the following:

```
Deploying from source requires an Artifact Registry Docker repository to store built containers. A repository named [cloud-run-source-deploy] in region 
[europe-west1] will be created.

Do you want to continue (Y/n)?
```

Type `Y` and hit **ENTER**.

### Allow Unauthenticated Access

You may be prompted with the following:

```
Allow unauthenticated invocations to [zoo-tour-guide] (y/N)?
```

For this lab, we want to allow unauthenticated invocations for easy testing. Type `y` and hit **ENTER**.

> ⚠️ **Note:** Anyone with the URL will have access to this agent, so this is best for testing only.

---

## Deployment Progress

You'll see output similar to:

```
Installed 107 packages in 151ms
Start generating Cloud Run source files in /tmp/cloud_run_deploy_src/20251122_075927
Copying agent source code...
Copying agent source code completed.
Creating Dockerfile...
Creating Dockerfile complete: /tmp/cloud_run_deploy_src/20251122_075927/Dockerfile
Deploying to Cloud Run...
```

```
Building using Dockerfile and deploying container to Cloud Run service [zoo-tour-guide] in project [unstacked-labs-477314] region [europe-west1]
OK Building and deploying new service... Done.
  OK Validating Service...
  OK Uploading sources...
  OK Building Container...
  OK Creating Revision...
  OK Routing traffic...
  OK Setting IAM Policy...
Done.
Service [zoo-tour-guide] revision [zoo-tour-guide-00001-89p] has been deployed and is serving 100 percent of traffic.
Service URL: https://zoo-tour-guide-683099143523.europe-west1.run.app
```

---

## Get the Deployment Link

Upon successful execution, the command will provide the URL of the deployed Cloud Run service.

It will look something like:

```
https://zoo-tour-guide-XXXXXXXXXXXX.europe-west1.run.app
```

**Copy this URL for the next task!**

---

## What the `adk deploy` Command Does

| Flag | Purpose |
|------|---------|
| `--project=$PROJECT_ID` | Specifies your GCP project |
| `--region=europe-west1` | Deploys to the Europe West 1 region |
| `--service_name=zoo-tour-guide` | Names your Cloud Run service |
| `--with_ui` | Includes a web UI for testing the agent |
| `.` | Uses current directory as source |
| `--service-account=$SERVICE_ACCOUNT` | Uses your dedicated service account |
| `--labels=dev-tutorial=codelab-adk` | Adds a label for resource tracking |