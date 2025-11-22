# Project Setup

## Create a Google Cloud Account

1. If you don't already have a Google Account, you must [create a Google Account](https://accounts.google.com/signup).
   > **Note:** Use a personal account instead of a work or school account. Work and school accounts may have restrictions that prevent you from enabling the APIs needed for this lab.

2. Sign in to the [Google Cloud Console](https://console.cloud.google.com/).

3. [Enable billing](https://cloud.google.com/billing/docs/how-to/modify-project) in the Cloud Console.
   - Completing this lab should cost less than **$1 USD** in Cloud resources.
   - You can follow the steps at the end of this lab to delete resources to avoid further charges.
   - New users are eligible for the [**$300 USD Free Trial**](https://cloud.google.com/free).

4. [Create a new project](https://console.cloud.google.com/projectcreate) or choose to reuse an existing project.

---

## Activate Cloud Shell

Cloud Shell is a virtual machine that is loaded with development tools. It offers a persistent 5GB home directory and runs on Google Cloud. Cloud Shell provides command-line access to your Google Cloud resources.

1. In the Cloud Console, click **Activate Cloud Shell** (terminal icon) in the top right toolbar.

2. Click **Continue** when prompted.

3. Once connected, you are already authenticated and the project is set to your selected project.

---

## Verify Your Account and Project

Before proceeding, ensure you're using the correct Google account and project.

### Check Current Authenticated Accounts

```bash
gcloud auth list
```

You should see output similar to:

```
Credentialed Accounts

ACTIVE: *
ACCOUNT: your-email@gmail.com
```

### Check Current Project

```bash
gcloud config get-value project
```

### List Available Projects

```bash
gcloud projects list
```

---

## Switch Accounts (If Needed)

If you need to use a different Google account than what's currently active:

### 1. Login with the New Account

```bash
gcloud auth login your-email@gmail.com
```

A browser window will open — sign in with your account and allow access.

> **Note:** In Cloud Shell, you may see a message that you're already authenticated. Type `y` to proceed anyway if you need to add a different account.

### 2. Set the New Account as Active

```bash
gcloud config set account your-email@gmail.com
```

### 3. Confirm the Change

```bash
gcloud auth list
```

You should now see your desired account marked as active with an asterisk (`*`):

```
Credentialed Accounts

ACTIVE: *
ACCOUNT: your-email@gmail.com
```

---

## Set Your Project

If you need to switch to a different project:

```bash
gcloud config set project YOUR_PROJECT_ID
```

Replace `YOUR_PROJECT_ID` with your actual project ID from the `gcloud projects list` output.

Verify the change:

```bash
gcloud config get-value project
```

---

## Troubleshooting

### Cannot Revoke GCE-Provided Credentials

If you try to revoke the default Cloud Shell account and see this error:

```
ERROR: (gcloud.auth.revoke) Cannot revoke GCE-provided credentials.
```

This is expected behavior. You cannot revoke the default Cloud Shell credentials, but you can still add and switch to a different account using the steps above.

### Multiple Accounts Listed

If you have multiple accounts and want to ensure the correct one is active, use:

```bash
gcloud config set account your-preferred-email@gmail.com
```