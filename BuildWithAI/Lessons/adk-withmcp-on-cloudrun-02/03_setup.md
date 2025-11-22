# Setup and Requirements

## Self-Paced Environment Setup

### 1. Create or Select a Project

Sign in to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project or reuse an existing one.

> **Important:** If you completed Lab 1, ensure you are using the **same project ID** so you can access the MCP server you deployed.

If you don't already have a Gmail or Google Workspace account, you must [create one](https://accounts.google.com/signup).

#### Understanding Project Identifiers

| Identifier | Description |
|------------|-------------|
| **Project Name** | Display name for this project's participants. Can be updated anytime. |
| **Project ID** | Unique across all Google Cloud projects. **Immutable** (cannot be changed after set). |
| **Project Number** | Numeric identifier used by some APIs. Auto-generated. |

> ⚠️ **Caution:** A Project ID is globally unique and can't be used by anyone else after you've selected it. Even if a project is deleted, the ID can't be used again.

> **Note:** If you use a Gmail account, you can leave the default location set to **No organization**. If you use a Google Workspace account, choose a location that makes sense for your organization.

### 2. Enable Billing

Next, you'll need to [enable billing](https://cloud.google.com/billing/docs/how-to/modify-project) in the Cloud Console to use Cloud resources/APIs.

- Running through this codelab won't cost much, if anything at all
- To shut down resources to avoid incurring billing beyond this tutorial, you can delete the resources you created or delete the project
- New Google Cloud users are eligible for the [**$300 USD Free Trial**](https://cloud.google.com/free) program

---

## Start Cloud Shell

### 3. Navigate to Cloud Shell Editor

Open the [Cloud Shell Editor](https://shell.cloud.google.com/?show=ide%2Cterminal).

If the terminal doesn't appear on the bottom of the screen, open it:

1. Click **Terminal**
2. Click **New Terminal**

### 4. Set Your Project

In the terminal, set your project with this command:

```bash
gcloud config set project [YOUR-PROJECT-ID]
```

> **Tip:** If you can't remember your project ID, you can list all your project IDs with:
> 
> ```bash
> gcloud projects list | awk '/PROJECT_ID/{print $2}'
> ```

### 5. Authorize if Prompted

If prompted to authorize, click **Authorize** to continue.

### 6. Verify Success

You should see this message:

```
Updated property [core/project].
```

> ⚠️ If you see a `WARNING` and are asked `Do you want to continue (Y/n)?`, then you have likely entered the project ID incorrectly. Press `n`, press `Enter`, and try to run the `gcloud config set project` command again.