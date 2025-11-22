# README: Google Cloud Cost & Billing Cleanup Guide

This document outlines the **complete step-by-step process** followed to identify and disable all services that could accrue costs across your Google Cloud projects. It includes checks, cleanup, billing unlinking, and verification.

---

## 🔍 Step 1: Check All Billing Accounts

List all billing accounts under your Google Cloud profile.

```bash
gcloud beta billing accounts list --format="table(ACCOUNT_ID, NAME, OPEN)"
```

* Note active (OPEN: True) billing accounts.

---

## 🧾 Step 2: Identify Projects Linked to Each Billing Account

List all projects linked to your billing accounts.

```bash
gcloud beta billing projects list --billing-account=<ACCOUNT_ID> --format="table(PROJECT_ID, BILLING_ENABLED)"
```

Example:

```bash
gcloud beta billing projects list --billing-account=01CBE3-C41864-245FAE --format="table(PROJECT_ID, BILLING_ENABLED)"
```

---

## 🧠 Step 3: Unlink Billing from a Project

To stop all charges immediately:

```bash
gcloud beta billing projects unlink <PROJECT_ID>
```

Verify:

```bash
gcloud beta billing projects describe <PROJECT_ID> --format="value(billingEnabled)"
# Should print: false
```

---

## 💻 Step 4: Check for Active Services and Instances

Run the following to check for anything running:

```bash
PROJECT=<PROJECT_ID>
ZONE=us-central1-a

gcloud compute instances list --project=$PROJECT
gcloud notebooks instances list --location=$ZONE --project=$PROJECT
gcloud run services list --platform=managed --project=$PROJECT
gcloud services list --enabled --project=$PROJECT
```

If these commands return **Listed 0 items**, no active services remain.

---

## 🧹 Step 5: Disable All Cost-Generating APIs

Disable compute, notebook, AI, and Cloud Run APIs:

```bash
gcloud services disable \
  notebooks.googleapis.com \
  aiplatform.googleapis.com \
  generativelanguage.googleapis.com \
  run.googleapis.com \
  compute.googleapis.com \
  --project=<PROJECT_ID> --force
```

Verify disabled status:

```bash
gcloud services list --enabled --project=<PROJECT_ID>
```

You should see only core APIs such as:

* cloudresourcemanager.googleapis.com
* serviceusage.googleapis.com
* logging.googleapis.com
* monitoring.googleapis.com

---

## ⚙️ Step 6: Remove Leftover Resources (Optional but Recommended)

Clean up remaining storage or repositories:

### Cloud Storage

```bash
gsutil ls -p <PROJECT_ID>
# Delete (be careful!)
gsutil -m rm -r gs://BUCKET_NAME
```

### Artifact Registry

```bash
gcloud artifacts repositories list --project=<PROJECT_ID> --format="table(NAME,FORMAT,LOCATION)"
# Delete
#gcloud artifacts repositories delete REPO_NAME --location=REGION --project=<PROJECT_ID>
```

### Secrets

```bash
gcloud secrets list --project=<PROJECT_ID>
#gcloud secrets delete SECRET_NAME --project=<PROJECT_ID>
```

### Service Accounts

```bash
gcloud iam service-accounts list --project=<PROJECT_ID>
#gcloud iam service-accounts delete SA_EMAIL --project=<PROJECT_ID>
```

---

## 🧾 Step 7: Confirm Final Billing Status

Ensure all projects are disconnected from billing:

```bash
gcloud beta billing projects describe <PROJECT_ID> --format="value(billingEnabled)"
```

Should return:

```
false
```

To double-check across all open billing accounts:

```bash
gcloud beta billing projects list --billing-account=<ACCOUNT_ID>
```

Each should list **0 items**.

---

## 🧭 Step 8: Final Verification Summary

| Project ID            | Billing Status | VM Instances | Notebooks | Cloud Run | Notes                 |
| --------------------- | -------------- | ------------ | --------- | --------- | --------------------- |
| unstacked-labs-477314 | Disabled       | None         | None      | None      | Cleaned & Billing Off |
| devfestdala           | Disabled       | None         | None      | None      | Cleaned & Billing Off |

---

## ✅ Summary

By completing these steps:

* All **billing-enabled services** have been unlinked.
* All **cost-accruing APIs** have been disabled.
* No **VMs, notebooks, or Cloud Run services** remain.
* Both `unstacked-labs-477314` and `devfestdala` are now **safe from any further billing**.

You can optionally delete these projects entirely from the GCP console if you wish to close them permanently:
👉 [https://console.cloud.google.com/cloud-resource-manager](https://console.cloud.google.com/cloud-resource-manager)

---

**Author:** Marvin Ngesa
**Date:** November 2025
**Purpose:** GCP Billing Cleanup & Cost Control Guide
