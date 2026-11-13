## 8. Optional Firestore vector search

Finish the base checks before proceeding. The extension uses a separate folder and service so you can compare both implementations during the workshop.

### 8.1 Copy source and create the named database

Run the copy commands when initializing the vector folder. Copying again replaces your vector edits.

```bash
mkdir -p "$WORK_DIR-vector"
cp "$WORK_DIR"/{agent.py,app.py,menu.json,requirements.txt} "$WORK_DIR-vector/"
cd "$WORK_DIR-vector"

gcloud services enable firestore.googleapis.com --project="$PROJECT_ID"
gcloud firestore databases create --project="$PROJECT_ID" \
  --database="$DB_ID" --location="$REGION" --type=firestore-native
```

For an existing database, inspect it before reusing it.

```bash
gcloud firestore databases describe --project="$PROJECT_ID" --database="$DB_ID"
```

Use these four pins in the vector folder. In the rehearsal the Firestore pins were accidentally added to the base folder, causing `No module named 'google.cloud'` when the vector seed ran.

```bash
printf '%s\n' 'google-adk==2.2.0' 'streamlit==1.56.0' \
  'google-cloud-firestore==2.27.0' 'google-genai==2.11.0' > requirements.txt

python3 -m venv "$WORK_DIR-vector-venv"
source "$WORK_DIR-vector-venv/bin/activate"
python -m pip install -r requirements.txt
python -m pip check
python -c 'from google import genai; from google.cloud import firestore; print("Imports OK")'

export EMBEDDING_LOCATION="us-central1"
export EMBEDDING_MODEL="text-embedding-005"
```

### 8.2 Create the shared embedding and retrieval code

This module uses the same project, database, embedding model, and vector length for seed writes and runtime queries. The menu item name and description are embedded. Structured tags remain available to the model as fields after retrieval.

```bash
cat > menu_store.py <<'PY'
import os

from google import genai
from google.cloud import firestore
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector

def menu_collection():
    project = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ["PROJECT_ID"]
    return firestore.Client(project=project, database=os.environ["DB_ID"]).collection("menu")

def embed(text: str) -> Vector:
    project = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ["PROJECT_ID"]
    client = genai.Client(
        vertexai=True, project=project, location=os.environ["EMBEDDING_LOCATION"]
    )
    response = client.models.embed_content(
        model=os.environ["EMBEDDING_MODEL"],
        contents=text,
        config={"output_dimensionality": 768},
    )
    values = response.embeddings[0].values
    if len(values) != 768:
        raise ValueError(f"Expected 768 embedding dimensions, received {len(values)}")
    return Vector(values)

def public_fields(snapshot):
    item = snapshot.to_dict()
    item.pop("embedding", None)
    return item

def list_menu():
    return [public_fields(doc) for doc in menu_collection().stream()]

def search_menu(query: str):
    matches = menu_collection().find_nearest(
        vector_field="embedding",
        query_vector=embed(query),
        distance_measure=DistanceMeasure.COSINE,
        limit=3,
    )
    return [public_fields(doc) for doc in matches.stream()]
PY

cat > seed.py <<'PY'
import argparse
import json
from pathlib import Path

from menu_store import embed, menu_collection

MATCHA = {
    "name": "Matcha Green Tea Latte",
    "description": "Creamy steamed oat milk infused with premium Japanese matcha powder.",
    "price": 5.50,
    "tags": ["sweet", "hot", "dairy-free"],
    "allergens": [],
}

parser = argparse.ArgumentParser()
parser.add_argument("--matcha", action="store_true", help="Insert only the Matcha demo item")
args = parser.parse_args()

if args.matcha:
    items = [MATCHA]
else:
    items = json.loads(Path(__file__).with_name("menu.json").read_text(encoding="utf-8"))

collection = menu_collection()
for item in items:
    doc_id = "matcha-latte" if args.matcha else item["name"].lower().replace(" ", "-")
    vector = embed(f"{item['name']}: {item['description']}")
    collection.document(doc_id).set({**item, "embedding": vector})
    print(f"Saved {doc_id}", flush=True)

print(f"Seed complete: {len(items)} documents written")
PY

export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
python seed.py
```

Expect eight writes. Document IDs are stable, so retries update the same records. The rehearsal initially hit `429 RESOURCE_EXHAUSTED` for `online_prediction_requests_per_base_model` with the base model name `textembedding-gecko`. A later run completed. If a brief retry fails again, inspect the project and region's Vertex AI quotas. You can test `export EMBEDDING_MODEL=gemini-embedding-001` with the same explicit 768 dimensions. If you switch, re-embed every document in the collection, including any existing Matcha demo document, before using the new model for queries. Equal dimensions alone do not make different models' vectors comparable.

[Google Cloud text embeddings](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings)

### 8.3 Build the index and verify search

```bash
gcloud firestore indexes composite create \
  --project="$PROJECT_ID" --database="$DB_ID" \
  --collection-group=menu --query-scope=COLLECTION \
  --field-config=field-path=embedding,vector-config='{"dimension":"768","flat":"{}"}'

gcloud firestore indexes composite list --project="$PROJECT_ID" --database="$DB_ID"
```

If the create command is waiting, the server is building the index. If it reports `ALREADY_EXISTS`, check the existing configuration. Run the query below when the index reaches `READY`.

```bash
python - <<'PY'
from menu_store import list_menu, search_menu

items = list_menu()
assert len(items) >= 8, items
results = search_menu("strong hot espresso")
assert results and len(results) <= 3, results
print("Menu count:", len(items))
print("Nearest:", [item["name"] for item in results])
PY
```

This tests Firestore and the embedding endpoint as your Cloud Shell identity. The deployed service has a separate identity and needs its own smoke test.

[Firestore vector search](https://docs.cloud.google.com/firestore/docs/vector-search)

### 8.4 Replace the two marked blocks

In the **vector folder's** `agent.py`, replace the entire `get_menu` block with the code below. Leave `tools=[get_menu]` and the chat model in place.

```python
# [START get_menu]
from menu_store import search_menu

def get_menu(query: str) -> str:
    """Search the current menu using a customer's request or preferences."""
    try:
        return json.dumps(search_menu(query))
    except Exception:
        logging.exception("Menu vector search failed")
        return json.dumps({"error": "Menu search is temporarily unavailable."})
# [END get_menu]
```

In the **vector folder's** `app.py`, replace the entire `load_menu` block.

```python
# [START load_menu]
from menu_store import list_menu

try:
    menu_items = list_menu()
except Exception:
    logging.exception("Could not load the Firestore sidebar menu")
    st.error("The menu is temporarily unavailable.")
    menu_items = []
# [END load_menu]
```

The app only reads the collection, so this guide grants the runtime `roles/datastore.viewer`. The account running `seed.py` needs write permissions. The original codelab uses the broader `roles/datastore.user` for the runtime.

```bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$BARISTA_SA" --role="roles/datastore.viewer"

python -m py_compile menu_store.py seed.py agent.py app.py
deploy_barista "$VECTOR_SERVICE" ",DB_ID=$DB_ID,EMBEDDING_LOCATION=$EMBEDDING_LOCATION,EMBEDDING_MODEL=$EMBEDDING_MODEL"
```

Use the vector service URL from the deploy output. The chat uses the `global` Gemini endpoint and the embedding client explicitly uses the regional endpoint.

### 8.5 Demonstrate a menu update without deploying again

1. Before inserting Matcha, open the vector app in a fresh session and ask **“Do you have any matcha drinks?”**. Expect the agent to say it could not find one among the menu results. If the item is already present from a prior rehearsal, use a clean live database for the before-and-after demo.
2. In the vector folder, with the same virtual environment and embedding variables, run `python seed.py --matcha`. Expect one write to `matcha-latte`.
3. Run `python -c 'from menu_store import search_menu; print([x["name"] for x in search_menu("matcha green tea")])'`. Check the result contains **Matcha Green Tea Latte**.
4. Refresh the vector app. Confirm the sidebar shows **Matcha Green Tea Latte · $5.50**. Ask again and check the chat recommends it with its listed price.
5. Ask specifically for a **matcha frappuccino**. A suitable answer explains that the returned menu contains a latte and offers it as an alternative. The base service's menu still contains the original eight items.

The sidebar checks a database list operation. The direct query checks vector ranking. The chat checks the ADK tool loop and response. Top-three retrieval can miss exact matches or return weak candidates. An exhaustive availability check calls for an exact lookup, and dietary constraints should be verified against structured fields.

---

[Lab overview](README.md) · [Previous](07_test_barista.md) · [Next](09_cleanup.md)
