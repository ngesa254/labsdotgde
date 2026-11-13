## 6. Deploy to Cloud Run

Your personal identity deploys, the build identity builds the image, and the runtime identity calls Gemini. The dedicated runtime identity receives the project-level `roles/aiplatform.user` role used by the codelab. It covers Vertex AI operations beyond model inference. Review each identity separately when troubleshooting IAM.

```bash
gcloud iam service-accounts create "$SA_ID" \
  --project="$PROJECT_ID" --display-name="Barista $TRACK Runtime"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$BARISTA_SA" --role="roles/aiplatform.user"
```

For `ALREADY_EXISTS`, confirm the existing service account is the intended one and run the role binding. Use the following function in the same terminal for both variants. Define it again after reopening Cloud Shell.

```bash
deploy_barista() {
  local service="$1"
  local extra_env="${2:-}"
  gcloud run deploy "$service" \
    --source . \
    --project="$PROJECT_ID" \
    --region="$REGION" \
    --allow-unauthenticated \
    --labels=dev-tutorial=codelab-streamlit-rag-adk \
    --command="/cnb/lifecycle/launcher" \
    --args='sh,-c,python3 -m streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false' \
    --service-account="$BARISTA_SA" \
    --set-env-vars="GOOGLE_GENAI_USE_ENTERPRISE=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=global${extra_env}"
}

cd "$WORK_DIR"
deploy_barista "$BASE_SERVICE"
```

The single quotes around `--args` preserve `$PORT` for the container's shell. The codelab's public access and Streamlit settings are for the mock-data demo. The service URL can be invoked by anyone and use project resources. For a restricted workshop, configure authenticated invocation and an authorized browser access path before sharing it.

Accept the prompt to create the Artifact Registry repository if the project and region match. Cloud Build detects Python, installs dependencies, and stores the resulting image in Artifact Registry. Cloud Run starts the image using the specified launcher and command. A Dockerfile gives control over the image build, and `--image` deploys an image produced by a separate build. The expected deploy output is **serving 100 percent of traffic** and a **Service URL**.

```bash
gcloud run services describe "$BASE_SERVICE" \
  --project="$PROJECT_ID" --region="$REGION" \
  --format='value(status.url)'
```

[Cloud Run source deploy](https://docs.cloud.google.com/run/docs/deploying-source-code) · [Build service account](https://docs.cloud.google.com/run/docs/configuring/services/build-service-account)

---

[Lab overview](README.md) · [Previous](05_build_agent_and_ui.md) · [Next](07_test_barista.md)
