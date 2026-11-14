# Validation evidence

Validation date: **14 November 2026**, Africa/Nairobi. Scope: authored, built with claat, structurally checked, locally exercised and browser inspected. **Not cloud verified or payment verified.** No provisioning, billing/IAM mutation, payment execution, commit, push or publication occurred.

## Actual results

| Check | Actual result | Evidence |
|---|---|---|
| claat export | Passed for both labs, 11 + 9 steps, 97 + 79 estimated minutes | Generated `site/codelabs/*/index.html` and `codelab.json`; `evidence/build.log` |
| Metadata/sequence | IDs, Draft status, ordered labels and durations matched authoritative sources | `evidence/structural-results.json` |
| Author handling | `author` not surfaced by this renderer; explicit visible attribution appears in both overviews | Generated HTML and desktop/mobile screenshots |
| Code/callouts | Language-tagged code emitted; actual styled callouts emitted; shell blocks pass `bash -n` without execution | `evidence/validation.log` |
| Local links/assets | All generated local image, full-size SVG, CSS, JS, download and handoff targets resolve; content links have no root-relative paths | Structural validator |
| Sample syntax/dependencies | Python AST checks, Docker CMD JSON parsing and `pip check` passed | `evidence/validation.log` |
| Unit behavior | **10 tests passed** (5 per lab), with no external calls | `evidence/validation.log` |
| MCP HTTP and ADK | Local actual Streamable HTTP returned six tools, KES 10 and an invalid-basket error; ADK discovered six tools, generated Gemini declarations and invoked the basket tool over HTTP | `evidence/integration-results.json`, `evidence/integration.log` |
| Transport limitation | Functional assertions passed, but pinned MCP SDK logged `ClosedResourceError` message-router errors on stream closure; deprecation/experimental warnings also emitted | Retained integration log; not suppressed or reported fixed |
| Linux dependencies | Both pinned locks resolved in pip Linux x86_64 CPython 3.11 binary-wheel dry-runs: 56 and 97 distributions | `evidence/linux-lab1.json`, `evidence/linux-lab2.json` and corresponding logs |
| Browser | Real installed Chrome via Playwright: upgraded custom elements, Back/Next, sidebar selection, exits, handoff links and loaded SVGs passed | `evidence/browser-subdirectory-results.json`, `evidence/browser-root-results.json` |
| Responsive check | 1440×1000 desktop and 390×844 narrow viewport; landing and both lab overviews inspected; no document-width overflow in checked narrow views | `evidence/*desktop.png`, `landing-mobile.png`, `lab1-mobile.png`, `lab2-mobile.png` |
| Subdirectory hosting | Passed at `/workshop/`; root preview checked separately | Browser result JSONs; local HTTP preview logs |
| Analytics configuration | Empty `codelab-gaid`, no default/personal tracking ID; generated analytics component and unused support script removed | `scripts/build.py`, structural assertions and generated output |
| Secret/data hygiene | Examples use placeholders and explicitly fictional phone fixtures; no key/private-key pattern found by checks; no secret store accessed | Validation checks and manual source/sample review |
| Preservation | All **12,943** pre-existing repository files hash-identical; no new file outside destination; branch/commit unchanged | `evidence/scope-results.json`, `evidence/scope.log` |
| Final file review | Reviewed all new editable sources, samples, scripts, generated HTML and resource/secret boundaries; no original source modified | `evidence/review-summary.json`; scope evidence |

Unit tests cover strict basket input, prices, unknown products, preparation/rejection, callback non-authority, disabled initiation without a client, mocked OAuth/STK acceptance and timeout with exactly one POST, private response shapes, agent filtering, origin validation, HTTP request validation, per-turn tokens and cleanup on success/failure. They do not call a model or Daraja. The local transport check is not an IAM test.

## Commands executed

Commands below are relative to `decode-codelabs/` unless an absolute path is shown. Installation/download steps required environment network approval; the sandbox's original proxy lookup failed, then the approved external-network retry succeeded.

```bash
# Tools and installation
python3.11 -m venv .venv
.tools/claat version
file .tools/claat
.venv/bin/python --version
.venv/bin/python -m pip freeze
.venv/bin/python scripts/lock_dependencies.py

# Build and non-networked checks
python3 scripts/build.py
.venv/bin/python scripts/validate.py

# Temporary local transport server; no external model/payment calls
.venv/bin/python scripts/integration_check.py

# Two retained previews during browser inspection
python3 scripts/preview.py --prefix /workshop/
python3 scripts/preview.py --port 8766
.venv/bin/python scripts/browser_check.py --url http://127.0.0.1:8765/workshop/
.venv/bin/python scripts/browser_check.py --url http://127.0.0.1:8766/

# Dependency-resolution checks, not installation into containers
.venv/bin/python -m pip install --dry-run --ignore-installed --only-binary=:all: \
  --platform manylinux_2_28_x86_64 --platform manylinux2014_x86_64 \
  --python-version 3.11 --target .cache/linux-check --cache-dir .cache/pip \
  -r labs/01-mpesa-mcp-server/sample-code/requirements.lock --report evidence/linux-lab1.json
.venv/bin/python -m pip install --dry-run --ignore-installed --only-binary=:all: \
  --platform manylinux_2_28_x86_64 --platform manylinux2014_x86_64 \
  --python-version 3.11 --target .cache/linux-check --cache-dir .cache/pip \
  -r labs/02-adk-payment-agent/sample-code/requirements.lock --report evidence/linux-lab2.json

# Scope and diff review
git -C .. status --short
git -C .. diff --stat
python3 scripts/check_scope.py
```

The initial install attempted source dotenv 1.0.1 alongside FastMCP and failed dependency resolution; it was replaced explicitly with 1.1.1. The final install used the direct pinned packages listed in the samples plus Playwright 1.56.0. `requirements-dev.lock` and `evidence/authoring-environment.txt` record the complete successful installed environment; `evidence/dependency-install.log` records the successful install.

Tool details: CPython **3.11.15** for validation, Python **3.14.3** for stdlib authoring scripts, pip **26.1**, Playwright **1.56.0**, existing Chrome (exact browser version recorded in browser results), Darwin arm64 host. claat downloaded as official `v2.2.6` asset, embedded version **`2.2.5-2023-06-15T18:32:06Z-872cbcf`**, SHA-256 **`3ba3eebec664076123626c2c77674f7779d5fc5647c53d180399183a3ba31695`**. No Go/Node/Docker authoring dependency was used.

## Failures and fixes

1. Network sandbox could not resolve its proxy for public downloads. Retried with required approval; used project-local tool/cache paths. Public GitHub API later returned 403 for remote-commit/tag queries; remote parity remains unknown.
2. FastMCP's dotenv constraint rejected source dotenv 1.0.1 in the shared validation environment. Explicitly adjusted to 1.1.1 and kept per-lab environments/locks.
3. claat rejected blank-separated metadata in direct input. Build now generates compact metadata in ignored staging while preserving authoritative requested source format.
4. A documented definition-style callout rendered as plain text. Changed to verified `> aside positive/negative` syntax.
5. The first browser assertion mistakenly expected 12 Lab 1 steps. The source/export both contain 11; corrected the test to the audited sequence. This was a test expectation error, not a missing lesson.
6. Browser inspection discovered renderer-created exit/Done links to `/`, which would escape a project mount. Added a small local navigation adaptation and verified the corrected relative paths.
7. Initial screenshots captured an in-flight step animation. Added a bounded settling wait and recaptured visible overviews; screenshots were then visually inspected.
8. The pinned transport emitted closed-stream errors despite successful tool results and awaited closures. No SDK mutation, log suppression or unsupported fix was made. This remains a release-review item.
9. Current primary model documentation showed source model retirement. Explicitly moved configuration to a listed `gemini-3.8-flash` replacement and a supported `global` model location, distinct from Cloud Run's region. No inference compatibility claim is made.
10. At the user's request, adapted the supplied DECODE HTML palette to the landing page only. Restored original light guided styling/blue controls and original diagram colors following clarification. Rechecked desktop/mobile rendering; preserved the reference file and did not import its event content.

## Limits and honest completion level

- **Authored:** two self-contained guided labs, full sample code, diagrams, audit, references, facilitator notes and future publication plan.
- **Built:** both labs exported using the pinned claat artifact; archives and assets generated successfully.
- **Locally verified:** structural checks, 10 unit tests, imports, dependency consistency, Linux wheel resolution, real local HTTP MCP/ADK tool execution, desktop/narrow browser behavior and source-preservation hashes.
- **Not cloud verified:** source/container builds, Cloud Run runtime, IAM denial/allow behavior, runtime metadata tokens, current model access and inference, cost/billing, model-specific SDK compatibility.
- **Not payment verified:** no Daraja request, callback ingestion, status reconciliation, real subscriber operation or monetary outcome was executed.
- No Apigee proxy, durable order/session store, callback receiver, idempotency ledger or server-side customer-consent flow exists. These are disclosed implementation boundaries.
- Runtime container base tags/package artifacts are not digest/hash locked. Linux wheel resolution is not Linux container execution. The codelab scripts/fonts are now vendored and checksum-verified. Locally served reading/navigation is tested with external requests blocked; cloud/package/reference operations remain network-dependent.
- The parser's author field is not supported visibly by this artifact; explicit overview attribution is the verified solution.
- Browser checks cover representative overviews, navigation, handoff and narrow layout. They are not a claim of exhaustive accessibility or every possible browser/device combination.

## Desk review perspectives

| Perspective | Review performed | Remaining gate |
|---|---|---|
| Participant | Checked initial working copy, environment choice, explicit commands, fixtures, expected results, fresh-terminal exports and handoff values | Fresh-user cloud/model walkthrough after administrator prerequisites |
| Facilitator | Checked early observable result, demonstrations, long operations and recovery boundaries | Resolve transport diagnostic; authorize and rehearse cloud path before an event |
| Technical reviewer | Traced tools, safe allowlists, credentials, audience, session ownership, code/diagram agreement, locks and cleanup scope | Current model/SDK inference, Linux container and provider-specific optional integration tests |

These are authoring-agent desk checks, not completed human reviews. Short future human reviewer checklists are in FACILITATOR_NOTES.md.

## Exact reproduction

```bash
cd "/Users/ngesamarvine/Documents/Terminal F/labsdotgde/decode-codelabs"
python3 scripts/install_claat.py
python3 scripts/build.py
.venv/bin/python scripts/validate.py
python3 scripts/preview.py --prefix /workshop/
```

For a clean validation environment, first create `.venv` using Python 3.11 and install `requirements-dev.lock` as documented in README.md. Open the printed local URL, normally **http://127.0.0.1:8765/workshop/**, and keep the preview command running. If the port is occupied, use the actual printed port. The inspection servers are temporary; starting this command reproduces them. No public URL was deployed.

## Follow-up: Start Lab and section navigation

After the user reported missing navigation, a fresh-profile click reached the lab page but `#next-step` was absent while the external frontend stalled. This exposed a gap in the earlier warmed-profile/direct-URL checks. The generated labs now load local runtime/styles/fonts, preserving the original light theme and blue controls. Assets and license notices are in `site/vendor/claat/`; build verifies SHA-256 against its manifest. Internal Lab 1/Lab 2 links stay in the same tab.

Reproduction checks now block external requests, click the real landing links, traverse every step, use Back/sidebar, test same-tab handoff and exercise mobile Next/menu/section selection. Results are recorded in the latest `evidence/browser-results.json` and `evidence/navigation-local-runtime.log`. The main preview remains running for the user; no unrelated process was stopped. The mobile test initially resumed a saved final step and correctly found Next hidden; resetting only the isolated test profile's saved progress allowed the intended first-step/mobile-menu scenario to be checked.

## Landing-page presentation update

At the user's request, changed the visible author-section label to TRAINER, removed the landing header's DRAFT wording and removed the independent/draft/tracking footer line. Replaced the NM placeholder with the user-selected local `ngesa.jpeg` photo. Codelab publication metadata remains Draft; no publication or cloud verification is implied by removing a visible landing-page badge. GitHub Pages compatibility is documented in PUBLISHING.md; no Pages files/settings were changed.

Landing browser verification passed: HTTP 200; section label TRAINER; original 1280×1280 photo loaded; no visible DRAFT text; footer contains only DECODE · From Code to Cash. Desktop and 390px layouts were visually inspected (`evidence/trainer-desktop.png`, `evidence/trainer-mobile.png`); the narrow viewport has no document overflow. Both claat exports passed again.

## Reference wordmark and landing navigation

The user corrected the biography to Electrical Engineer. Authoritative codelabs, landing page and author/facilitator documentation were updated and claat exports rebuilt. The landing header now uses the reference's typographic DE{C0}DE 5.0 mark with coral braces/lime version and locally served Bricolage Grotesque. Added rounded section navigation to Labs, Before you start and Trainer; pill buttons/chips and reduced-motion support are landing-only. Guided theme styles were not changed.

The updated landing page returned HTTP 200. Desktop (1440px) and mobile (390px) checks confirmed the exact DE{C0}DE 5.0 wordmark, loaded local typeface, Electrical Engineer biography and no horizontal overflow. Section hashes resolved correctly. Reduced-motion checks measured Labs/prerequisites at the configured offset, or at the document's scroll limit; Trainer remained visible above the footer. Screenshots include the decoded trainer photo. Results: `evidence/landing-wordmark-review.json`. The first strict scroll-position wait timed out during smooth scrolling; the reduced-motion inspection verified final positions without depending on animation timing.
