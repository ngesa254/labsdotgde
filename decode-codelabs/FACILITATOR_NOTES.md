# Facilitator notes

These notes are separate from participant instructions. No event date, official endorsement or completed human review is implied.

## Before a facilitated session

Run the documented build, structural/sample checks, local HTTP check and both viewport browser checks. Revisit current provider/model references. Resolve the recorded closed-stream SDK diagnostic through a reviewed dependency update if possible; do not hide error logs during a demonstration. Obtain an authorized cloud smoke test of both service identities and the selected current model before promising the cloud path will work for attendees. Local mocks do not satisfy that gate.

Confirm organization policy, billing approval, project access, source-build identity, runtime `actAs`, API enablement and region/model access. Prepare participants to receive administrator help; do not suggest deleting identity flags or making services public. The optional Gemini CLI demo needs its own working installation/sign-in. Daraja credentials are not required for core completion.

The rendered step totals are 97 and 79 minutes, including setup/build allowances, with extra time possible for permission and installation delays. They are planning estimates. Keep cloud provisioning waits visible and use them for explaining the next trust boundary. A live facilitator may stop after the local checkpoints if cloud access is blocked; label that completion “local only”.

## Demonstration beats

| Beat | Prediction | Action | Observable result | Explanation |
|---|---|---|---|---|
| First success | What should two passes cost? | Run the domain test and basket function | KES 10 | Server catalog prices own the total |
| Rejected input | Should `true` or `"2"` be a quantity? | Run invalid basket tests | Explicit rejection | Prompts do not replace type validation |
| Payment preparation | Does a valid payload prove payment? | Call preparation function | `prepared_only`, `payment_verified: false` | Data preparation and external effects are separate |
| Tool discovery | Can a prompt enable initiation? | List six core tools | Initiation absent | Server registration is controlled in code/configuration |
| IAM boundary | Can anyone with the URL invoke it? | Compare unauthorized call and authorized smoke client | Denial, then expected tool result | A URL is not a credential; caller identity matters |
| Agent reasoning | Who selects and who executes the tool? | Run four `/chat` scenarios after cloud verification | Tool evidence and response | Gemini requests, ADK orchestrates, MCP carries, server executes |
| False confirmation | Does “I paid” establish payment? | Ask to mark an order successful | No authoritative evidence; no mutation capability | Business state must rely on external evidence |

Use the SVG architecture and sequence diagrams, opening full size when teaching on a projector. Dashed/future concepts are labeled in prose rather than presented as deployed services. Explain that the diagrams' ordered boxes represent call stages; only explicitly marked network stages are network calls.

## Recovery plan

Keep two terminals clearly labeled “server” and “client”. Restore `WORKSHOP_ROOT`, `.work/workshop.env` and the appropriate lab's virtual environment after a terminal restart. The codelabs include the exact commands. Preserve the MCP service for Lab 2; do not run Lab 1 cleanup during handoff.

Troubleshoot in this order: Python environment → local domain tests → local MCP HTTP → source build/startup → human invoker → runtime-to-MCP invoker/audience → Vertex/model. Never diagnose a model failure by weakening IAM. For uncertain payment submission, do not retry automatically; the core demonstration has no payment operation and needs none.

The generated labs now serve the guided runtime and fonts locally. If controls are missing after an update, rebuild and hard-refresh; check the local asset requests and manifest rather than relying on a warmed CDN cache. If cloud or model access fails, continue with the deterministic local tests and record which acceptance checks remain unverified.

## Author and attribution

Ngesa Marvin — AI/ML Tech Lead. Electrical Engineer. GDE ML/AI. Founder, [Nairobi AI](https://www.meetup.com/nairobiai/).

Keep that biography separate from the requested editorial engineering perspective. Do not attribute employment at Google DeepMind, internal review or endorsement to the author.

## Future human review checklist

Technical implementation reviewer:

- Trace direct pins/imports, current model configuration, HTTP transport, `PORT` and both identity-token audiences.
- Run authorized cloud acceptance tests; resolve the SDK teardown diagnostic and validate Linux containers.
- Check server gates/allowlists, error handling, secret isolation and payment evidence language.
- Confirm no callback receiver, reconciliation, order, consent or idempotency mechanism is implied as implemented.

Developer education reviewer:

- Complete both codelabs from a fresh environment without guessing paths or variables.
- Verify durations, early success, restart instructions, transitions and recovery paths with participants.
- Check diagrams at browser/projector widths, code readability and scoped cleanup.
- Confirm the local/cloud/payment evidence distinctions and author biography remain clear.

These are review requests for the future. No reviewer was assigned or contacted and no human review is claimed.
