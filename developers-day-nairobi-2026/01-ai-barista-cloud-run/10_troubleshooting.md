## 10. Troubleshooting by symptom

| Symptom | Diagnosis and next step |
|---|---|
| Project limit reached | Select an existing project you control. Use distinct service and database names for each track. |
| `(unset)` or project not found | Run `gcloud projects list` and use the project ID column. `labsdotgde` is the display name. |
| No active account selected | Authorize Cloud Shell, then use `gcloud auth list` and activate or sign in to the intended account. |
| Cloud console access blocked by MFA | Complete 2-Step Verification for the signed-in account and refresh. |
| Billing account missing or disabled | Run `gcloud billing projects describe "$PROJECT_ID"`. Confirm the intended active account is linked and the event credit is still usable. |
| Shell says `LS: command not found` | Use lowercase `ls`. |
| Shell says `--region: command not found` | Repaste the whole block. Keep each continuation backslash at the very end of its line. |
| `cloudshell edit` returns to the prompt | Look for the editor tab or open the editor manually. If it reports that it cannot send messages to the client, use `nano` and validate the saved file. |
| `Invalid JSON` or `Expecting value` | Check the filename, directory, and byte count. Remove copied Markdown, HTML entities, and trailing commas. |
| `requirements.txt` is empty | Write the package pins into the file and use `cat requirements.txt` before installing or deploying. |
| `No module named google.cloud` | Activate the vector environment and run `python -m pip install -r requirements.txt` from the vector folder. Use `python -m pip show google-cloud-firestore` to confirm the package is installed for the interpreter running the script. |
| Local SDK says default credentials are missing | Authorize Cloud Shell for API calls. Verify that local Python has Application Default Credentials for the intended account. The Cloud Run runtime uses its attached identity. |
| `iam.serviceaccounts.actAs` during deploy | Verify the deployer has permission to act as the exact runtime identity. Service Account User on that identity is the standard role. |
| Source build fails or cannot push an image | Open the linked Cloud Build log. For a builder permission error, check the build identity with `gcloud builds get-default-service-account --project="$PROJECT_ID"` and verify the permissions described in the Cloud Run source build documentation, including `roles/run.builder` where applicable. |
| Build reports `No matching distribution` or dependency resolution failure | Check the exact pins, Python version, and resolver output. Validate with the same requirements in a clean virtual environment before changing one version. |
| Cloud Run revision fails to listen on `PORT` | Inspect startup logs. Check the launcher command, preservation of literal `$PORT`, binding to `0.0.0.0`, and import errors. |
| Browser returns 403 before the UI loads | Check Cloud Run invocation access and any organization policy affecting public services. |
| UI loads, chat gives 403 | Check the runtime service account on that revision and its permission to call Gemini. For a Firestore 403, check the database project and runtime read permissions. |
| Chat or embeddings give 404 | Verify model ID and endpoint separately. Chat uses `global` here. Embedding code targets `us-central1`. For Firestore verify the exact database ID. |
| Embeddings give 429 | Retry after a short pause. If repeated, inspect quota for the exact project, region, and model. Change models only with a full reseed and matching query configuration. |
| Firestore says an index is required | Confirm the `menu` collection index exists in the selected named database and is `READY`. Check the field, scope, and vector dimensions. |
| Menu sidebar loads but vector chat fails | The sidebar is a list operation. Run the direct search smoke test, then check runtime logs for embedding and index errors. |
| Matcha never appears | Verify the inserted document, database ID, active service URL, and refreshed chat. Test direct search for the new item. |
| Follow-up forgets the earlier turn | Keep the same tab and session. Refresh starts a new chat in this lab. |

For an error **after deployment**, use runtime logs. For a **build error**, use the Cloud Build log from the deployment output.

```bash
gcloud run services logs read "$BASE_SERVICE" \
  --project="$PROJECT_ID" --region="$REGION" --limit=40
```

Substitute `"$VECTOR_SERVICE"` when debugging the Firestore version. Check logs locally and redact identifiers, tokens, and any sensitive prompts before sharing.

[Cloud Run troubleshooting](https://docs.cloud.google.com/run/docs/troubleshooting)

## Workshop completion checklist

- [ ] Verified project, billing, and API activation.
- [ ] Deployed the rehearsal and tested all three menu behaviors.
- [ ] Rebuilt and deployed the live lab to its own URL.
- [ ] If using Firestore, verified direct search and the Matcha before-and-after test.
- [ ] Removed the workshop services, dedicated identities, and disposable data and images after the session.

---

[Lab overview](README.md) · [Previous](09_cleanup.md)
