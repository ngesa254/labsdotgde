# Source audit and change rationale

Audit date: **14 November 2026 (Africa/Nairobi)**. Implementation authority: the local `labsdotgde/decode/` checkout, read without executing its cloud/payment instructions.

## Provenance and scope

- Local branch: `release/devfest_2026`.
- Local commit: `576cd612fbaf111ca5bcbcbf947cd3b9cd6263b5`.
- Initial `git status --short` was empty before creating this destination. The later file-hash snapshot records `?? decode-codelabs/` because the empty destination/evidence scaffolding already existed; it excludes that destination from the baseline.
- No applicable `AGENTS.md` was found in the workspace ancestry, repository, source subtree or destination. Unrelated repositories' instructions were not applied.
- Read `Team/Gen AI/ENGINEERING_PERSONA_AND_CONSTRAINTS.md` for evidence, journey tracing and verification principles. Its unrelated infrastructure, credentials, live audits and commit instructions were not imported.
- Public reference: [DECODE release branch](https://github.com/ngesa254/labsdotgde/tree/release/devfest_2026/decode). The branch name matches the local branch name, but **remote commit equality could not be confirmed**: public GitHub API commit lookup returned HTTP 403; the browser retrieval returned a cache miss. No fetch, branch switch or claim of remote parity was made. Local source is the sole implementation baseline.
- `evidence/initial-state.json` contains SHA-256 hashes for all 12,943 pre-existing repository files outside this destination, plus branch/commit/status. `scripts/check_scope.py` compares that snapshot without modifying Git.

## Source inventory and lesson order

Read the overview `decode/README.md`, alternative `decode/README_.md`, both lab `readme.md` files, all lesson documents, the `decode/mpesa express` file (empty), embedded configuration/code, asset paths and cleanup sections. There are no standalone Python, Dockerfile, lock or dependency files under the original DECODE folder: runnable material is embedded in Markdown fences.

The intended order is the lab README order, **not lexical filename order**:

1. Lab 1: `01_intro`, `02_setup`, `03_cloudshell`, `04_enabling_apis`, `05_prep_project`, `06_create_mcp_server`, `07_deploy_on_cloudrun`, `08_addmcp_to_gemini_cli`, optional `09_verify_logs`, `10_add_mcp_prompt`, `11_gemini_flash_lite`, `11.5_cleanup`, then `12_conclusion` (all `.md`).
2. Lab 2: `01_intro`, `02_why_cloudrun`, `03_setup`, `04_enable_apis`, `05_create_project`, `06_create_agent_workflow`, `07_prepare_deployment`, `08_deploy_agent`, `09_test_agent`, `10_cleanup`, `11_congratulations` (all `.md`).

The source's objectives are remote FastMCP tool construction, IAM-protected Cloud Run deployment, Gemini CLI connection, merchant catalog/payment tooling, and an ADK workflow consuming that endpoint. Apigee is positioned for future governance; there is no proxy implementation. The source's two-lab narrative and author remain intact.

Machine-readable headings, line counts, links and missing targets are in `evidence/source-inventory.json`. Existing images were inventoried; the overview illustration depicts broader gateway features and the Lab 2 image still depicts a zoo tour/Wikipedia workflow. Neither is reused as evidence of this merchant implementation. Replacement diagrams are rendered SVGs with editable source in `scripts/diagrams.py`.

## Findings, corrections and evidence

| Source evidence | Discrepancy or missing context | New edition decision |
|---|---|---|
| Overview and alternate overview substantially duplicate each other | Multiple entry points and repeated setup/cleanup paths | One landing page and one authoritative Markdown source per lab |
| Lab 1 README says production-ready; no deployed tests supplied | Readiness claim unsupported by code or evidence | Describe a teaching sample; record precise local/cloud/payment verification levels |
| Lab 1 overview says catalog is a JSON file; embedded code uses a Python list | Storage description differs from implementation | Preserve static Python catalog and fixture prices; state no inventory/order persistence |
| Lab 1 `05` requires Python 3.13, overview says 3.11+; Lab 2 pins old SDK | Unclear reproducible common runtime | Use CPython 3.11; validated on 3.11.15; Docker base 3.11.14. Record both and Linux/container limits |
| Lab 1 `06`: `fastmcp==2.12.4`, `httpx==0.28.1` | Standalone FastMCP could be confused with MCP SDK's FastMCP | Keep distribution/import and direct versions; explicitly pin MCP 1.14.1/Pydantic 2.11.9 and resolved closures |
| Lab 2 `05`: ADK 1.14.0, dotenv 1.0.1, cloud logging 3.11.0 | Cross-lab authoring install with FastMCP fails: it requires dotenv >=1.1.0 | Separate participant environments; explicit dotenv 1.1.1 adjustment. Remove unused cloud-logging bootstrap/dependency; use platform logs |
| Lab 1 `06` quantity conversion uses `int()` | Silently accepts numeric strings, truncates floats, accepts bool | Pydantic strict integer bounds and explicit basket errors; tests cover invalid types and unknown IDs |
| Lab 1 `06` phone check uses prefix/length only | Letters can satisfy the old test; no subscriber validation | Full numeric syntax check, `2541`/`2547`; state syntax is not subscriber existence |
| `generate_access_token_request` returns a live bearer token | README implies request description; implementation exposes credentials to model | Remove public token tool. OAuth helper remains server-private in optional integration |
| Validation and initiation return full payload including derived Password | Credential-derived material and subscriber data become model-visible | Preparation uses illustrative placeholders; optional submission returns sanitized IDs/acceptance only |
| Initiation accepts shortcode, passkey, callback and amount from tool arguments | Model controls merchant/security configuration; no business consent/order binding | Server-owned environment configuration and fixed sandbox host; initiation disabled by default. Document remaining consent/idempotency/order-binding gaps |
| Sandbox key/passkey and shared webhook URL in source | Shared receiver is inappropriate for independent participants | Placeholder-only examples; no source credentials/shared webhook reused; optional operator-controlled receiver requirement |
| Lab 1 `08` asserts guaranteed prompt, no debit/reversal; production reversal notice | Those promises were not established by accessible primary evidence | Remove handset/money/reversal guarantees. Require portal-specific confirmation before any later sandbox operation |
| `parse_stk_callback` accepts arbitrary JSON | Parser is not a receiving endpoint, origin verification or reconciliation | Return `reported_success` separately from `payment_verified: false`; no deployed callback receiver claimed |
| STK timeout/error guidance suggests retries | A missing response does not establish no submission | One submission only; `outcome_unknown`, reconcile externally; no automatic retry or durable idempotency claim |
| Original error map includes numerical limits and provider-specific hints | Current portal data could not be fully retrieved without sign-in | Keep a small illustrative error map with explicit provider verification; remove unsupported limits/guarantees |
| Cloud Run `07` suggests dropping runtime SA on `actAs` failure | Workaround changes the security identity | Keep dedicated runtime; explain deployer/build/runtime roles and administrator recovery |
| Both labs grant project-wide invoker | Broad access unnecessary for one receiving service | Grant invoker on named MCP service and named agent service only |
| URL examples construct hostnames from project number | Does not establish actual deployed URL | Discover `status.url`; service origin and `/mcp` endpoint are distinct values |
| Gemini settings overwrite `~/.gemini/settings.json` with token | Destroys unrelated configuration and stores expiring token | Project-local demo settings with literal env references; quit/refresh/restart for expiry |
| ADK `06` obtains ID token when importing agent module | Long-running process retains expired header; local import reaches external systems | Factory with no network at import; new bounded turn obtains token, constructs toolset, runs and closes in same task |
| ADK `06` stores raw prompt in state/logs and greeter/planner/formatter chain | Extra model calls and handoff complexity obscure remote-tool objective | Single agent plus explicit tool allowlist; no raw prompt logging. Multi-agent composition deferred |
| ADK `08` floating `uvx` deploy and public UI | Pin can be bypassed and service exposed | Pinned Dockerfile + private FastAPI `/chat` API; no ADK development UI exposed |
| Source `gemini-2.0-flash-lite` and `gemini-2.5-flash` | Primary lifecycle lists retirement on 1 June and 20 October 2026 respectively | Remove obsolete CLI model switch; explicitly select `gemini-3.8-flash` for new runtime config, with required `MODEL`, an explicit supported `global` model location distinct from the Cloud Run region, and an unverified SDK/model integration gate |
| Lab 1 cleanup suggests removing server before Lab 2 | Breaks handoff | Retain Lab 1 until both labs finish; explicit non-secret variable handoff and restart file |
| Cleanup deletes shared Artifact Registry/project/global CLI config | May destroy unrelated resources | Target services/accounts/grants; inspect lab artifacts, leave shared repo/project/config intact |
| Missing `image-daraja-myapps.png`, `image-webhook-callback.png` | Participant sees broken assets | Do not reuse missing screenshots; diagrams and all required assets are local |
| Overview diagram draws Apigee on core path; no proxy files | Architecture aspiration shown as installed component | Separate Apigee extension diagram and acceptance requirements; direct IAM core path |

## Source-to-destination mapping

`L1` means `labs/01-mpesa-mcp-server/codelab.md`; `L2` means `labs/02-adk-payment-agent/codelab.md`. Each `##` is exactly one generated step. All paths below are relative to `decode/` in the original source.

| Destination step | Original lesson(s) or documented addition |
|---|---|
| L1 — From catalog to a trustworthy tool boundary | `README.md`; Lab 1 `readme.md`, `01_intro.md`; addition: explicit outcome/evidence contract |
| L1 — Choose your workspace and get an early result | Lab 1 `02_setup.md`, `03_cloudshell.md`, `05_prep_project.md`; additions: working copy, dependency lock, offline fixtures/tests, downloads |
| L1 — Trace catalog prices and reject invalid baskets | Lab 1 `06_create_mcp_server.md`; addition: strict domain validation and tests |
| L1 — Prepare an M-Pesa request without sending it | Lab 1 `06_create_mcp_server.md`; additions: placeholder payload, untrusted callback label, rendered payment flow |
| L1 — Expose the tools over Streamable HTTP | Lab 1 `06_create_mcp_server.md`; additions: no-initiation core and deterministic smoke client |
| L1 — Select a project and prepare the identities | Lab 1 `02_setup.md`–`04_enabling_apis.md`, `07_deploy_on_cloudrun.md`; addition: identity responsibility matrix |
| L1 — Build and deploy a protected MCP service | Lab 1 `07_deploy_on_cloudrun.md`; corrected container/identity/URL guidance |
| L1 — Authenticate a client and connect Gemini CLI | Lab 1 `08_addmcp_to_gemini_cli.md`; additions: read-only smoke checkpoint and project-local env-reference settings |
| L1 — Understand the optional sandbox integration | Lab 1 `06_create_mcp_server.md`, `07_deploy_on_cloudrun.md`; corrected authorization, secrets and evidence boundaries |
| L1 — Place Apigee and diagnose failures | Overview; Lab 1 `01_intro.md`, `09_verify_logs.md`; addition: extension trust-boundary diagram, per-boundary recovery |
| L1 — Hand off to Lab 2 and clean up at the right time | Lab 1 `11.5_cleanup.md`, `12_conclusion.md`; additions: restart file and scoped cleanup |
| L1 optional prompt/model content | `10_add_mcp_prompt.md` intentionally omitted: prompt directly called payment without code-enforced consent; `11_gemini_flash_lite.md` switch removed because retired model and no latency evidence |
| L2 — Let the model reason and the server enforce | Lab 2 `readme.md`, `01_intro.md`, `02_why_cloudrun.md`; addition: simpler agent and rendered sequence |
| L2 — Restore the Lab 1 handoff and check access | Lab 2 `03_setup.md`, `07_prepare_deployment.md`; addition: human/runtime checks separated |
| L2 — Prepare the agent environment | Lab 2 `05_create_project.md`; additions: complete sample files and non-networked lifecycle tests |
| L2 — Read the agent contract and transport lifecycle | Lab 2 `06_create_agent_workflow.md`; additions: factory, allowlist, bounded turn and same-task cleanup |
| L2 — Configure Vertex AI and the runtime identities | Lab 2 `04_enable_apis.md`, `07_prepare_deployment.md`; current primary model lifecycle and IAM documentation |
| L2 — Deploy the private agent API | Lab 2 `07_prepare_deployment.md`, `08_deploy_agent.md`; explicit private API/container alternative |
| L2 — Run four observable scenarios | Lab 2 `09_test_agent.md`; additions: invalid basket and false-payment-claim challenge |
| L2 — Recover and evaluate the implementation honestly | Lab 2 help content, `06_create_agent_workflow.md`; addition: evidence-level diagnosis and implementation gaps |
| L2 — Clean up only the resources you created | Lab 2 `10_cleanup.md`, `11_congratulations.md`; corrected scoped cleanup and completion contract |

Sample mapping: `domain.py`, `payments.py`, `server.py` split and correct Lab 1's embedded `server.py`. `agent.py` replaces the orchestration shape of Lab 2's embedded sample; `app.py`, both test modules, smoke client, locks, Dockerfiles, scripts and diagrams are documented additions. There is no other authoritative participant Markdown assembly input.

## Authoring reference audit

Read local Solace `README.md`, `markdown/codelab-4-codelab/codelab-4-codelab.md`, both relevant `package.json` files, `markdown/template/markdown.template`, and `init.sh`. Adopted focused lessons, prerequisites, explicit configuration context, visuals, checkpoints and two human review perspectives. Did not run `init.sh`, copy branding/assets, require Solace categories, create a fork or assign reviewers.

Their watch scripts use `lsof ... | xargs kill` / `kill-port` and floating Node dependencies. This edition uses a Python preview with port fallback and never terminates another process. The 2020 DEV article is historical context for Markdown/export/serve, not authority for installing Go/Node/Docker or using an old floating Docker image.

The official claat repository is archived (16 December 2025). The tested official `v2.2.6` macOS release binary reports embedded version `2.2.5-2023-06-15T18:32:06Z-872cbcf`; that mismatch is recorded, not silently relabeled. Blank metadata fields and one documented callout syntax did not behave as current prose suggested; build stages metadata and uses verified blockquote callouts. Visible author attribution is in the overview because this renderer does not surface `author` in its JSON/UI. Details: [TOOLCHAIN.md](TOOLCHAIN.md).

## Unresolved questions and release gates

1. Remote branch equality remains unknown because public retrieval failed.
2. No cloud build, Cloud Run IAM integration, runtime identity-token validation or actual model inference was authorized/performed. The current replacement model's compatibility with the older pinned SDK needs a deliberate cloud acceptance run before a facilitated event.
3. Actual local HTTP and ADK discovery pass, but MCP SDK 1.14.1 logs `ClosedResourceError` in its stateless message router when streams close. This is an observed upstream lifecycle diagnostic; root cause beyond the pinned transport path is not claimed. It has not been suppressed or called fixed. A reviewed SDK upgrade and rerun are recommended before live delivery.
4. Linux x86_64 wheel resolution dry-runs passed for both locks; container runtime/build has not been verified. The authoring host is macOS arm64; inspect platform-specific dependencies before promising Cloud Run reproducibility.
5. Daraja portal API details require sign-in and were only partially accessible. Current subscriber rules, limits, request fields and callback provenance must be verified by the operator before any optional sandbox exercise.
6. No callback receiver, trusted payment-status tool, durable idempotency/order/session store, customer-consent record or Apigee proxy exists. Those are intentional boundaries, not completed functionality.
7. The archived renderer remains a maintenance concern. Following the navigation failure, its runtime assets and fonts are vendored with hashes/licenses; reading/navigation is tested with external requests blocked. Cloud exercises and external references remain network-dependent.

This edition is authored, exported and locally checked. These release gates prevent describing it as cloud-verified, payment-verified or production-ready.

## Visual reference added during review

At the user's request, read `Decode 5.0/decode html - final 4.html` as a read-only color reference. Applied its forest green `#04140b`, dark green `#0a2214`, lime `#c8ff3d`, cream `#f1ede2`, yellow `#ffc233` and coral `#ff3b30` to the landing page only. Following the user's clarification, guided labs retain the original light claat theme, blue navigation controls and original diagram palette. A darker green is used for small landing-page text on cream to preserve contrast. No event dates, marketing claims, embedded imagery, scripts or placeholder event content were copied. The reference itself was not edited.

## Navigation follow-up

A fresh Chrome profile following the actual Start Lab link reached the lab URL but had no `#next-step` control while the remote runtime stalled. Earlier warm-browser/direct-URL checks did not establish this cold-start path reliably. The fix preserves claat HTML and native controls while serving scripts, styles and font assets from `site/vendor/claat/`, pinned by manifest checksums with upstream license notices. Internal handoff links now stay in the current tab. Browser checks follow the actual landing links, traverse all 20 steps and test the mobile menu while blocking external network requests. DECODE colors remain limited to the landing page.

## Branding and biography refinement

At the user's request, changed the biography to Electrical Engineer in the landing page, both authoritative codelabs and author/facilitator documentation. Reproduced the read-only reference page's typographic DE{C0}DE 5.0 wordmark (coral braces and lime version). Borrowed rounded navigation/buttons and direct section anchors for labs, prerequisites and trainer on the landing page. No event dates, claims or interactive event features were imported. Guided lesson colors/layout remain the original light theme.
