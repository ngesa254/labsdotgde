## 9. Clean up after the rehearsal and live session

Keep the working rehearsal available through the live session if it is your fallback. This project also contains other work. Delete the individual Barista resources you created. **Skip project deletion, project-wide API disablement, and deletion of shared repositories or existing databases.**

### 9.1 Inventory and record images before deleting services

Run section 3 with the track you intend to clean up. Review the service and database lists. An optional service or database may be absent if you stopped after the base lab.

```bash
gcloud run services list --project="$PROJECT_ID" --region="$REGION"
gcloud firestore databases list --project="$PROJECT_ID"
gcloud iam service-accounts describe "$BARISTA_SA" --project="$PROJECT_ID"
```

For each existing Barista service, record the images referenced by its revisions. Run the same command with `"$VECTOR_SERVICE"` if that service exists.

```bash
gcloud run revisions list --service="$BASE_SERVICE" \
  --project="$PROJECT_ID" --region="$REGION" \
  --format='table(metadata.name,spec.containers[0].image)'
```

### 9.2 Remove the selected Cloud Run services

Run the commands individually for the services you created. The confirmation prompts are left enabled so you can review the target. Removing a service permanently removes its endpoint and revisions. It can take a short time to disappear from the list.

```bash
gcloud run services delete "$VECTOR_SERVICE" --project="$PROJECT_ID" --region="$REGION"
gcloud run services delete "$BASE_SERVICE" --project="$PROJECT_ID" --region="$REGION"
```

An absent service can be skipped. Recheck the service list before removing the runtime identity.

[Manage Cloud Run services](https://docs.cloud.google.com/run/docs/managing/services)

### 9.3 Remove the dedicated runtime identity

Only do this once all services using this identity are gone. Remove the role bindings you added. If you skipped vector search, skip the Firestore role removal. If you followed the original codelab and granted `roles/datastore.user`, use that role in the removal command instead.

```bash
gcloud projects remove-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$BARISTA_SA" --role="roles/aiplatform.user"

gcloud projects remove-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$BARISTA_SA" --role="roles/datastore.viewer"

gcloud iam service-accounts delete "$BARISTA_SA" --project="$PROJECT_ID"
```

### 9.4 Remove the optional Firestore database

Delete the named database only if you created it for this track and it contains workshop data you can discard. Database deletion removes its menu documents and indexes. If Firestore reports deletion protection, inspect the named database and its ownership before changing that setting. If you used an existing shared database, leave it in place and review only the documents and index you added.

```bash
gcloud firestore databases describe --project="$PROJECT_ID" --database="$DB_ID"
gcloud firestore databases delete --project="$PROJECT_ID" --database="$DB_ID"
```

[Manage Firestore databases](https://docs.cloud.google.com/firestore/docs/manage-databases)

### 9.5 Check Artifact Registry and remaining usage

Deleting Cloud Run services leaves their images in Artifact Registry. List image versions in the source-deploy repository, identify the images owned exclusively by the removed Barista services, and verify that other services or revisions do not use the same digest. Delete only confirmed workshop images through the console or by digest. Keep the shared repository itself.

```bash
gcloud artifacts docker images list \
  "$REGION-docker.pkg.dev/$PROJECT_ID/cloud-run-source-deploy" \
  --project="$PROJECT_ID" --include-tags
```

For a confirmed disposable image, substitute the full `LOCATION-docker.pkg.dev/PROJECT/REPOSITORY/IMAGE@sha256:DIGEST` reference below. `--delete-tags` also removes tags pointing to that version.

```bash
gcloud artifacts docker images delete "FULL_IMAGE_DIGEST_REFERENCE" \
  --project="$PROJECT_ID" --delete-tags
```

Source builds can also leave uploaded source archives. Review Cloud Build and Cloud Storage before removing any objects. Avoid deleting a shared build bucket. Check Billing Reports for the project after cleanup. Usage already incurred can appear later. Repeat section 9 for the other track once its demo is finished. Cloud Shell source files are useful for rerunning the lab and may be retained.

[Manage Artifact Registry images](https://docs.cloud.google.com/artifact-registry/docs/docker/manage-images)

---

[Lab overview](README.md) · [Previous](08_firestore_vector_search.md) · [Next](10_troubleshooting.md)
