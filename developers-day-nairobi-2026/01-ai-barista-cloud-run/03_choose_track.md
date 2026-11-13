## 3. Choose a track and create the source folder

Run the rehearsal track first. When starting the live build, run the live setting and repeat sections 3–7. In a new terminal, re-export the project ID from section 2 and rerun this block.

```bash
export TRACK="test"   # Set to lab for the live build.
export REGION="us-central1"

if [ "$TRACK" = "test" ]; then
  export SA_ID="barista-test-sa"
  export DB_ID="coffee-menu-test"
else
  export SA_ID="barista-agent-sa"
  export DB_ID="coffee-menu"
fi

export WORK_DIR="$HOME/barista-$TRACK"
export BASE_SERVICE="coffee-barista-$TRACK"
export VECTOR_SERVICE="coffee-barista-$TRACK-vector"
export BARISTA_SA="${SA_ID}@${PROJECT_ID}.iam.gserviceaccount.com"

mkdir -p "$WORK_DIR"
cd "$WORK_DIR"
pwd
printf 'Project %s | Region %s | Service %s | Runtime %s\n' \
  "$PROJECT_ID" "$REGION" "$BASE_SERVICE" "$BARISTA_SA"
```

The folder should end in `barista-test` or `barista-lab`. `ls` lists Cloud Shell files. The project shown in the terminal prompt is the default cloud target, and changing it does not change the home directory. Existing home-directory files can appear in a new project session.

---

[Lab overview](README.md) · [Previous](02_project_setup.md) · [Next](04_create_menu.md)
