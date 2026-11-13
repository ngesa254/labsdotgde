## 2. Project, account, billing, and APIs

The workshop project is **labsdotgde**, project ID **`angelic-bee-193823`**. The existing project serves both tracks, so a project creation limit does not block this lab.

| Resource | Rehearsal | Live lab |
|---|---|---|
| Base source directory | `~/barista-test` | `~/barista-lab` |
| Base Cloud Run service | `coffee-barista-test` | `coffee-barista-lab` |
| Runtime service account ID | `barista-test-sa` | `barista-agent-sa` |
| Optional vector directory | `~/barista-test-vector` | `~/barista-lab-vector` |
| Optional vector service | `coffee-barista-test-vector` | `coffee-barista-lab-vector` |
| Optional Firestore database | `coffee-menu-test` | `coffee-menu` |
| Cloud Run region | `us-central1` | `us-central1` |
| Gemini chat location | `global` | `global` |
| Embedding location | `us-central1` | `us-central1` |

Participants using their own projects should substitute their actual project IDs throughout. To create a project, open the [project creation page](https://console.cloud.google.com/projectcreate), choose a display name and location, and copy the generated unique project ID after creation. If an authorized existing project is available, select it in the project picker.

### Link and verify billing

1. If using workshop credits, open the [Developers Day Nairobi credit page](https://g.dev/credits/devs-day-nairobi), sign in with the intended Google account, select **Claim Credit**, and open the event billing account once it appears. The event screen indicated a delay of up to five minutes. Check the expiry displayed after claiming.
2. In [Cloud Billing](https://console.cloud.google.com/billing), open **Your projects**, locate the project by ID, and use its action menu to link a billing account or change billing. Select **GDP Event Credit: Developers Day Nairobi** when using the event credit. Changing billing affects all workloads in the project.
3. Click the Cloud Shell terminal icon and authorize the session if prompted. If the console requires MFA, enable 2-Step Verification for the active account and refresh once it takes effect.

```bash
gcloud auth list
export PROJECT_ID="angelic-bee-193823"
gcloud config set project "$PROJECT_ID"
gcloud config get project
gcloud billing projects describe "$PROJECT_ID"
```

Check the account marked with an asterisk, the exact project ID, and `billingEnabled: true`. Compare the returned billing account with the event account in the console. A claimed credit by itself does not establish a project billing link. If `gcloud auth list` is empty, authorize Cloud Shell or run `gcloud auth login`. If your intended account is already listed, activate it using `gcloud config set account ACCOUNT_EMAIL` with your own email. Keep account identifiers and login tokens out of shared logs.

```bash
gcloud services enable run.googleapis.com aiplatform.googleapis.com \
  cloudbuild.googleapis.com --project="$PROJECT_ID"

gcloud services list --enabled --project="$PROJECT_ID" \
  --format='value(config.name)'
```

Check that all three names appear. If activation fails with `UREQ_PROJECT_BILLING_NOT_FOUND`, fix the billing link for this project and retry. If it fails with `PERMISSION_DENIED`, check the active identity and whether it has permission to enable services.

[Cloud Shell authorization](https://docs.cloud.google.com/shell/docs/auth) · [Billing changes](https://docs.cloud.google.com/billing/docs/how-to/modify-project) · [API enablement](https://docs.cloud.google.com/service-usage/docs/enable-disable)

---

[Lab overview](README.md) · [Previous](01_overview.md) · [Next](03_choose_track.md)
